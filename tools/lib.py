import subprocess
import openpibo_models
# 카메라·얼굴·인식(vision_camera / vision_face / vision_detect)은 무거워서(dlib·OpenVINO·MediaPipe)
# 여기서 불러오지 않는다. 로봇 연결(모터·소리)을 먼저 알리고 vision_start 가 이어서 불러온다(260929)
from openpibo.audio import Audio
from openpibo.motion import Motion
import asyncio
import numpy as np
import time,datetime
import base64
import cv2,logging
import os,json,shutil,csv
from PIL import Image,ImageDraw,ImageFont,ImageOps
from queue import Queue
from threading import Thread, Timer, Lock

logging.basicConfig(level=logging.ERROR, format='%(asctime)s [%(levelname)s] %(message)s')

def to_base64(im):
  im = cv2.resize(im, (320, 240))
  _, buffer = cv2.imencode('.jpg', im, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
  return base64.b64encode(buffer).decode('utf-8')

class Pibo:
  def __init__(self, emit_func=None, logger=None):
    logging.info('Class INIT')
    self.emit = emit_func
    self.mymodel_path = "/home/pi/mymodel"
    self.trackX, self.trackY = 0, 0
    self.imgX, self.imgY = 0,0
    self.marker_length = 2
    self.motion_d = [0, 0, -80, 0, 0, 0, 0, 0, 80, 0] # current d value
    self.motion_p = [] # current pos list value
    self.motion_j = {} # current json value
    try:
      with open('/home/pi/mymotion.json', 'rb') as f:
        self.motion_j = json.load(f)
        #await self.emit('disp_code', self.motion_j)
    except Exception as ex:
      logging.error(f'[motion_start] Error: {ex}')
      pass
    self.vision_type = "camera"
    self.vision_sleep = True

    # 준비 순서(260929): 모터·소리 → [로봇 연결됨] → 카메라 → 사물·손 인식 → 얼굴 인식.
    # 전엔 얼굴(dlib 모델 약 120MB·OpenVINO 3개 컴파일·MediaPipe)까지 다 올린 뒤에야 연결됨이 떠서,
    # 동작 탭만 쓸 사람도 한참 기다렸다. 카메라 쪽은 vision_state 로 단계를 알린다(도구 [카메라] 탭에 표시)
    self.cam = None
    self.fac = None
    self.det = None
    self.frame = None
    self.res_img = None
    self.vision_state = {'step': 0, 'total': 3, 'key': 'vs_camera', 'camera': False, 'detect': False, 'face': False, 'error': ''}
    self.speech_od = None   # 온디바이스 TTS. 모델이 무거워 음성 탭을 열 때(voice_warm) 또는 처음 말할 때 올린다
    self.voice_state = 'idle'   # idle / loading / ready / error
    self._voice_lock = Lock()

    self.mot = Motion()
    self.aud = Audio()
    self.mot.set_motors(self.motion_d, movetime=1000)
    asyncio.run(self.emit('onoff', True, callback=None))
    Thread(name='vision_start', target=self.vision_start, args=(), daemon=True).start()

  def _vision_step(self, step, key, **done):
    self.vision_state.update(step=step, key=key, **done)
    asyncio.run(self.emit('vision_state', dict(self.vision_state), callback=None))

  def vision_start(self):
    """카메라 → 사물·손 인식 → 얼굴 인식 순으로 올린다. 카메라가 켜지면 바로 화면을 보내기 시작한다"""
    try:
      self._vision_step(1, 'vs_camera')
      from openpibo.vision_camera import Camera
      self.cam = Camera()
      Thread(name='vision_loop', target=self.vision_loop, args=(), daemon=True).start()
      self._vision_step(2, 'vs_detect', camera=True)
      from openpibo.vision_detect import Detect
      det = Detect()
      det.load_hand_gesture_model()
      self.det = det
      self._vision_step(3, 'vs_face', detect=True)
      from openpibo.vision_face import Face
      self.fac = Face()
      self._vision_step(3, 'vs_ready', face=True)
    except Exception as ex:
      logging.error(f'[vision_start] Error: {ex}')
      self.vision_state['error'] = str(ex)
      asyncio.run(self.emit('vision_state', dict(self.vision_state), callback=None))

  # 기능마다 필요한 모델. 아직 안 올라왔으면 카메라 화면만 보낸다
  NEEDS_FACE = ('face', 'face_landmark')
  NEEDS_DET = ('qr', 'object', 'hand', 'pose', 'track', 'marker')

  def vision_loop(self):
    while True:
      if self.vision_sleep == True:
        time.sleep(1)
        continue

      try:
        self.frame = self.cam.read()  # read the camera frame
        if (self.vision_type in self.NEEDS_FACE and self.fac is None) or (self.vision_type in self.NEEDS_DET and self.det is None):
          img, res = self.frame, ''
        elif self.vision_type == 'grayscale':
          img, res = cv2.cvtColor(self.frame.copy(), cv2.COLOR_BGR2GRAY), ''
        elif self.vision_type == 'canny':
          img, res = cv2.Canny(cv2.cvtColor(self.frame.copy(), cv2.COLOR_BGR2GRAY), 200, 200), ''
        elif self.vision_type == 'edgePreservingFilter':
          img, res = cv2.edgePreservingFilter(self.frame.copy()), ''
        elif self.vision_type == "cartoon":
          img, res = self.cam.stylization(self.frame.copy()), ''
        elif self.vision_type == "sketch_rgb":
          img, res = self.cam.pencilSketch(self.frame.copy())[1], ''
        elif self.vision_type == "detail":
          img, res = self.cam.detailEnhance(self.frame.copy()), ''
        elif self.vision_type == "qr":
          img, res = self.qr_detect()
        elif self.vision_type == "face":
          img, res = self.face_detect()
        elif self.vision_type == "face_landmark":
          img, res = self.face_landmark()
        elif self.vision_type == "object":
          img, res = self.object_detect()
        elif self.vision_type == "hand":
          img, res = self.hand_detect()
        elif self.vision_type == "pose":
          img, res = self.pose_detect()
        elif self.vision_type == "track":
          img, res = self.track_object()
        elif self.vision_type == "marker":
          img, res = self.detect_marker()
        else:
          img, res = self.frame, ""
      except Exception as ex:
        logging.error(f'[vision_loop] Error: {ex}')
        img, res = self.frame, str(ex)

      if img is None:   # 카메라가 첫 장을 못 읽었다. 스레드가 죽지 않게 다음 장을 기다린다
        time.sleep(0.5)
        continue
      self.res_img = img.copy()
      if self.cam:
        self.cam.putText(img, '+', (self.imgX-5,self.imgY), 0.6, (100,100,200), 3)
      asyncio.run(self.emit('stream', {'img':to_base64(img), 'data':res}, callback=None))
      time.sleep(0.5)

  def face_detect(self):
    im = self.frame.copy()
    items = self.fac.detect_face(im)
    res = ''

    if len(items) > 0:
      x1,y1,x2,y2 = items[0]
      face = self.fac.analyze_face(im, items[0])
      colors = (200,100,0) if face['gender'] == 'Male' else (100,200,0)
      self.cam.rectangle(im, (x1,y1), (x2, y2), colors, 3)
      self.cam.putText(im, f"{face['gender']}, {face['age']}, {face['emotion']}", (x1+10, y1+20),0.6,colors,2)
      res += f"{face['gender']}, {face['age']}, {face['emotion']} ({x1}, {y1})"
    return im, res

  def face_landmark(self):
    im = self.frame.copy()
    res = self.fac.detect_mesh(im)
    self.fac.detect_mesh_vis(im, res)

    return im, ",".join([f"{d['distance']} cm / {d['direction']}" for d in res])

  def object_detect(self):
    im = self.frame.copy()
    items = self.det.detect_object(im)
    res = ''

    for obj in items:
      x1,y1,x2,y2 = obj['box']
      colors = (100,100,200)
      self.cam.rectangle(im, (x1,y1), (x2, y2),colors,3)
      (text_width, text_height), baseline = cv2.getTextSize(f'{obj["name"]} {obj["score"]}', cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
      cv2.rectangle(im, (x1, y1 - text_height - baseline), (x1 + text_width, y1), colors, -1)
      self.cam.putText(im, f'{obj["name"]} {obj["score"]}', (x1, y1 - baseline), 0.5, (255,255,255),2)
      res += '[{}-({},{})] '.format(obj['name'], x1, y1)
    return im, res

  def hand_detect(self):
    im = self.frame.copy()
    res = self.det.recognize_hand_gesture(im)
    self.det.recognize_hand_gesture_vis(im, res)

    return im, ",".join([f"{d['name']} / {d['score']}" for d in res])

  def qr_detect(self):
    im = self.frame.copy()
    items = self.det.detect_qr(im)
    res = ''

    for item in items:
      if item['type'] != '':
        x1,y1,x2,y2 = item['box']
        colors = (100,0,200)
        self.cam.rectangle(im, (x1,y1), (x2, y2),colors,3)
        self.cam.putText(im, 'QR', (x1+10, y1+20),0.6,colors,2)
        res += '[{}-{} / ({},{})] '.format(item['data'], item['type'], x1, y1)

    return im, res

  def pose_detect(self):
    im = self.frame.copy()
    self.det.detect_pose_vis(im, self.det.detect_pose(im))
    return im, ''

  def object_tracker_init(self, d):
    if self.det is None or self.frame is None:
      return
    im = self.frame.copy()
    if self.det.tracker is not None:
      del self.det.tracker

    self.det.object_tracker_init(im, (d['x1'], d['y1'], d['x2'], d['y2']))
 
  def track_object(self):
    im = self.frame.copy()
    colors = (100,0,200)
    if self.det.tracker is not None:
      x1,y1,x2,y2 = self.det.track_object(im)
      self.cam.rectangle(im, (x1,y1), (x2,y2), colors,3)
    return im, ""

  def detect_marker(self):
    im = self.frame.copy()
    res = self.det.detect_marker(im, self.marker_length)
    cv2.imwrite("im.jpg", im)
    print('marker', im.shape, self.marker_length, res)
    self.det.detect_marker_vis(im, res)
    return im, " ".join([ f'({d["id"]})-{d["distance"]}cm' for d in res])

  def imwrite(self, name):
    if self.cam is None or self.res_img is None:
      return False
    self.cam.imwrite(name, self.res_img.copy())
    return True

  def mic(self, d):
    record_time = d['time']
    filename = "/home/pi/myaudio/mic.wav"
    self.aud.record(filename=filename, timeout=record_time)

  # 온디바이스 TTS(SpeechOnDevice) 목소리. PiBrain 도구와 같은 10가지(m1~m5 남성, f1~f5 여성)
  OD_VOICES = ("m1", "m2", "m3", "m4", "m5", "f1", "f2", "f3", "f4", "f5")

  def tts(self, d):
    """말하기. 성공하면 None, 실패하면 오류 문구를 돌려준다(도구 화면에 그대로 보인다)"""
    print("TTS", d)
    voice_type = d['voice_type']
    volume = d['volume']
    filename = "/home/pi/myaudio/tts.wav"

    try:
      if voice_type == "espeak":
        # 인자 목록으로 넘긴다. 전엔 os.system(f'espeak "{text}"') 이라 글자에 " 나 ; 가 들어가면
        # 셸 명령으로 실행됐다(서비스가 root 라 그대로 root 권한)
        subprocess.run(['espeak', str(d['text']), '-w', filename], check=True, timeout=30)
      elif voice_type in self.OD_VOICES:
        # ONNX 모델 로딩이 무거워 처음 호출될 때만 올린다.
        # lang='na' 는 자동 판별이라 한국어·영어 양쪽 배포판에서 그대로 쓸 수 있다.
        self.voice_warm()
        self.speech_od.tts(text=d['text'], filename=filename, voice=voice_type, lang='na')
      else:
        # 서버 TTS(oe-sapi)는 제거됐다
        logging.error(f'[tts] unsupported voice_type: {voice_type}')
        return f'unsupported voice: {voice_type}'
      self.aud.play(filename=filename, volume=volume)
    except Exception as ex:
      logging.error(f'[tts] Error: {ex}')
      return str(ex)
    return None

  def voice_warm(self):
    """온디바이스 목소리 모델을 올린다. 음성 탭을 열 때 미리 부르고, 말하기 전에도 부른다(한 번만 올라간다)"""
    with self._voice_lock:
      if self.speech_od is not None:
        return self.voice_state
      self.voice_state = 'loading'
      try:
        from openpibo.speech import SpeechOnDevice
        self.speech_od = SpeechOnDevice()
        self.voice_state = 'ready'
      except Exception as ex:
        logging.error(f'[voice_warm] Error: {ex}')
        self.voice_state = 'error'
        raise
      return self.voice_state

  def tts_stop(self):
    self.aud.stop()

  ## motion
  def make_raw(self):
    if len(self.motion_p) == 0:
      return {}
    return {'init_def':1, 'init':self.motion_p[0]['d'], 'pos':self.motion_p[1:]} if self.motion_p[0]['seq'] == 0 else {'init_def':0, 'pos':self.motion_p[:]}

  def get_motor_info(self):
    return self.motion_d, self.motion_p, self.motion_j

  def set_motor(self, idx, pos):
    self.motion_d[idx] = pos
    self.mot.set_speed(idx, 50)
    self.mot.set_acceleration(idx, 0)
    self.mot.set_motor(idx, pos)

  def set_motors(self, pos_lst, movetime=1000):
    self.motion_d = pos_lst
    self.mot.set_motors(pos_lst, movetime)

  def add_frame(self, seq):
    seq = int(round(float(seq)))   # 초×1000 이 16100.000000000002 처럼 올 수 있다(int 만 하면 32.3초가 32299 가 된다)
    _check = False
    for idx, pos in enumerate(self.motion_p):
      if pos['seq'] == seq:
        self.motion_p[idx] = {'d': self.motion_d[:], 'seq': int(seq)}
        _check = True
        break

    if _check == False:
      self.motion_p.append({'d': self.motion_d[:], 'seq': int(seq)})
      self.motion_p.sort(key=lambda x: x['seq'])
    return self.motion_p

  def delete_frame(self, seq):
    seq = int(round(float(seq)))
    for idx, pos in enumerate(self.motion_p):
      if pos['seq'] == seq:
        del self.motion_p[idx]
        break
    return self.motion_p

  def init_frame(self):
    self.motion_p = []
    return self.motion_p

  def play_frame(self, cycle):
    raw = self.make_raw()
    Thread(name='play_frame', target=self.mot.set_motion_raw, args=(raw, int(cycle)), daemon=True).start()

  def stop_frame(self):
    self.mot.stop()

  def add_motion(self, name):
    self.motion_j[name] = self.make_raw()
    with open('/home/pi/mymotion.json', 'w') as f:
      json.dump(self.motion_j, f)
    shutil.chown('/home/pi/mymotion.json', 'pi', 'pi')
    return self.motion_j

  def load_motion(self, name):
    if name in self.motion_j:
      a = self.motion_j[name]
    elif name in self.mot.get_motion():
      a = self.mot.get_motion(name)
    else:
      return self.motion_p

    self.motion_p = []
    if 'init_def' in a and 'init' in a:
      self.motion_p.append({'d':a['init'], 'seq':0})
    if 'pos' in a:
      for item in a['pos']:
        self.motion_p.append(item)

    return self.motion_p

  def delete_motion(self, name):
    if name in self.motion_j:
      del self.motion_j[name]
    with open('/home/pi/mymotion.json', 'w') as f:
      json.dump(self.motion_j, f)
    shutil.chown('/home/pi/mymotion.json', 'pi', 'pi')
    return self.motion_j

  def reset_motion(self):
    self.motion_j = {}
    with open('/home/pi/mymotion.json', 'w') as f:
      json.dump(self.motion_j, f)
    shutil.chown('/home/pi/mymotion.json', 'pi', 'pi')
    return self.motion_j
