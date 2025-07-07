"""
영상처리, 인공지능 비전 기술을 사용합니다.
이 모듈은 AI-Core 서버와 통신하여 동작합니다.
"""
import requests
import base64
import numpy as np
import cv2
import dlib
import json
import math
from PIL import Image, ImageDraw, ImageFont
import openpibo_models # For font file path
from .modules.pose.movenet import Movenet
from .modules.pose.utils import visualize_pose
import openpibo_detect_models
# =================================================================
# API 통신 헬퍼 함수
# =================================================================
def _api_call(endpoint: str, img_in: np.ndarray = None, params: dict = None):
    """
    AI-Core 서버와 통신을 전담하는 내부 헬퍼 함수입니다.

    :param str endpoint: 호출할 API의 엔드포인트 (예: "detect/detect_object")
    :param numpy.ndarray img_in: 서버로 전송할 이미지
    :param dict params: API에 전달할 추가 파라미터
    :return: 서버로부터 받은 데이터 (이미지 또는 JSON 데이터)
    """
    SERVER_URL = "http://127.0.0.1:50050"  # AI-Core 서버 주소

    payload = {"params": params or {}}
    if img_in is not None:
        # 이미지를 PNG로 압축 후 Base64로 인코딩하여 payload에 추가
        _, buffer = cv2.imencode('.png', img_in)
        img_b64 = base64.b64encode(buffer).decode('utf-8')
        payload["image"] = img_b64

    try:
        # API 서버에 POST 요청
        response = requests.post(f"{SERVER_URL}/{endpoint}", json=payload)
        response.raise_for_status()  # 200번대 응답이 아니면 에러 발생
        res_json = response.json()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"AI-Core 서버({SERVER_URL}) 연결에 실패했습니다: {e}")

    # 이미지 외의 데이터(JSON) 반환
    return res_json.get("data", res_json)

# =================================================================
# 로컬 Helper 함수
# =================================================================
def putTextPIL(img, text, points, size=30, colors=(255,255,255)):
    """
    이미지에 문자를 입력합니다. (한/영 가능 - pillow 이용) - 로컬 동작
    """
    if not isinstance(img, np.ndarray):
        raise Exception('"img" must be image data from opencv')
    if isinstance(colors, str):
        colors = (int(colors[5:7], 16), int(colors[3:5], 16), int(colors[1:3], 16))
    
    font = ImageFont.truetype(openpibo_models.filepath("KDL.ttf"), size)
    pil = Image.fromarray(img)
    ImageDraw.Draw(pil).text(points, text, font=font, fill=colors)
    img[:] = np.array(pil)
    return img

def vision_api(mode, image, params={}):
    """
    외부 인공지능 비전 API를 호출합니다. (기존 기능 유지)
    """
    if isinstance(image, np.ndarray):
        return requests.post(f"https://o-vapi.circul.us/{mode}", files={'uploadFile':cv2.imencode('.jpg', image)[1].tobytes()}, params=params).json()
    else:
        return requests.post(f"https://o-vapi.circul.us/{mode}", files={'uploadFile':open(image, 'rb')}, params=params).json()

# =================================================================
# Detect 클래스 (API 클라이언트 버전)
# =================================================================
class Detect:
  """
  인식과 관련된 다양한 기능을 사용할 수 있는 클래스입니다. (API-backed)
  이 클래스의 인스턴스는 내부적으로 AI-Core 서버와 통신하여 동작합니다.
  """
  def __init__(self):
    """
    Detect 클래스를 초기화합니다.
    실제 모델 로딩은 서버에서 이루어지므로, 이 메서드는 비어있습니다.
    """
    self.tracker = None # 로컬에서는 더 이상 트래커 객체를 유지하지 않습니다.
    self.pose_detector = Movenet(openpibo_detect_models.filepath("movenet_lightning.tflite"))

  def load_hand_gesture_model(self, modelpath='/home/pi/.model/hand/gesture_recognizer.task'):
    """
    서버에 손동작 인식 모델을 로드하도록 요청합니다. (서버 API 호출)
    """
    return _api_call("detect/load_hand_gesture_model", params={'modelpath': modelpath})

  def recognize_hand_gesture(self, image):
    """
    손동작을 인식합니다. (서버 API 호출)
    """
    return _api_call("detect/recognize_hand_gesture", img_in=image)

  def recognize_hand_gesture_vis(self, img, items):
    """
    손동작 인식 결과를 이미지에 표시합니다. (로컬 동작)
    """
    for item in items:
      hpoints = item["point"]
      name = item["name"]
      score = item["score"]
      for px, py in hpoints:
        cv2.circle(img, (px, py), 3, (255, 255, 255), -1)
      putTextPIL(img, f'{name}/{score}', (hpoints[0][0], hpoints[0][1] - 50), 30, (255, 0, 0))
    return img

  def load_object_model(self, modelpath='/home/pi/.model/object/yolo11s.onnx'):
    """
    서버에 사물 인식 모델을 로드하도록 요청합니다. (서버 API 호출)
    """
    return _api_call("detect/load_object_model", params={'modelpath': modelpath})

  def detect_object(self, img):
    """
    사물을 인식합니다. (서버 API 호출)
    """
    return _api_call("detect/detect_object", img_in=img)

  def detect_object_vis(self, img, items):
    """
    사물 인식 결과를 이미지에 표시합니다. (로컬 동작)
    """
    for item in items:
      x1,y1,x2,y2 = item['box']
      name = item['name']
      cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)
      putTextPIL(img, name, (x1, y1-30), 30, (0,255,0))
    return img

  def detect_qr(self, img):
    """
    이미지 안의 QR코드 및 바코드를 인식합니다. (서버 API 호출)
    """
    return _api_call("detect/detect_qr", img_in=img)

  def detect_qr_vis(self, img, items):
    """
    QR/바코드 결과를 이미지에 표시합니다. (로컬 동작)
    """
    for item in items:
      x1,y1,x2,y2 = item['box']
      data = str(item['data'])
      cv2.rectangle(img, (x1,y1), (x2,y2), (255,50,255), 2)
      putTextPIL(img, data, (x1, y1-30), 30, (255,50,255))
    return img

  def detect_pose(self, img):
    """
    이미지 안의 Pose를 인식합니다. (서버 API 호출)
    """
    if not type(img) is np.ndarray:
      raise Exception('"img" must be image data from opencv')

    list_persons = [self.pose_detector.detect(img)]
    return list_persons

  def detect_pose_vis(self, img, items):
    """
    포즈를 이미지에 표시합니다. (로컬 동작)
    이 함수는 서버에서 받은 dict 데이터를 기반으로 시각화합니다.
    """
    if not type(img) is np.ndarray:
      raise Exception('"img" must be image data from opencv')

    visualize_pose(img, items)

  def analyze_pose(self, data):
    """
    서버에 포즈 분석을 요청합니다. (서버 API 호출)
    """
    def distance(p1, p2):
      return math.sqrt((p1.x-p2.x)**2 + (p1.y-p2.y)**2)

    NOSE, LEFT_EYE, RIGHT_EYE, LEFT_EAR, RIGHT_EAR = 0,1,2,3,4
    LEFT_SHOULDER, RIGHT_SHOULDER, LEFT_ELBOW, RIGHT_ELBOW, LEFT_WRIST, RIGHT_WRIST = 5,6,7,8,9,10
    LEFT_HIP, RIGHT_HIP, LEFT_KNEE, RIGHT_KNEE, LEFT_ANKLE, RIGHT_ANKLE = 11,12,13,14,15,16

    res = []
    data = data[0].keypoints

    if data[LEFT_WRIST].coordinate.y < data[LEFT_ELBOW].coordinate.y:
      res.append("left_hand_up")
    if data[RIGHT_WRIST].coordinate.y < data[RIGHT_ELBOW].coordinate.y:
      res.append("right_hand_up")
    if distance(data[LEFT_WRIST].coordinate, data[RIGHT_WRIST].coordinate) <  75:
      res.append("clap")

    return res

  def object_tracker_init(self, img, p):
    """
    이미지 안의 사물 트래커를 설정합니다.

    example::

      img = camera.read()
      detect.object_tracker_init(img)

    :param numpy.ndarray img: 이미지 객체
    """

    if not type(img) is np.ndarray:
      raise Exception('"img" must be image data from opencv')

    self.tracker = dlib.correlation_tracker()
    x1,y1,x2,y2 = p
    self.tracker.start_track(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), dlib.rectangle(x1,y1,x2,y2))

  def track_object(self, img):
    """
    이미지 안의 사물 트래커를 갱신합니다.

    example::

      img = camera.read()
      detect.object_tracker_init(img, (10,10,100,100))
      position = detect.track_object(img)

    :param numpy.ndarray img: 이미지 객체

    :returns: x1,y1,x2,y2 업데이트 된 사물 위치
    """

    if not type(img) is np.ndarray:
      raise Exception('"img" must be image data from opencv')

    self.tracker.update(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    box = self.tracker.get_position()

    x1 = int(box.left())
    y1 = int(box.top())
    x2 = int(box.right())
    y2 = int(box.bottom())

    height, width = img.shape[:2]
    x1 = max(0, int(x1))
    y1 = max(0, int(y1))
    x2 = min(width - 1, int(x2))
    y2 = min(height - 1, int(y2))

    return (x1, y1, x2, y2)

  def track_object_vis(self, img, item):
    """
    마커 결과를 표시합니다.

    :param numpy.ndarray img: 이미지 객체
    :param array items: 마커 결과
    """

    if not type(img) is np.ndarray:
      raise Exception('"img" must be image data from opencv')

    x1,y1,x2,y2 = item
    cv2.rectangle(img, (x1,y1), (x2,y2), (255,50,255), 2)

  def detect_marker(self, img, marker_length=2):
    """
    이미지 안의 마커를 인식합니다. (서버 API 호출)
    """
    return _api_call("detect/detect_marker", img_in=img, params={'marker_length': marker_length})

  def detect_marker_vis(self, img, items):
    """
    마커 결과를 이미지에 표시합니다. (로컬 동작)
    """
    for item in items:
      cX, cY = item['center']
      topLeft, topRight, bottomRight, bottomLeft = item['box']
      markerID = item['id']
      distance = item['distance']

      cv2.line(img, tuple(topLeft), tuple(topRight), (255, 0, 0), 4)
      cv2.line(img, tuple(topRight), tuple(bottomRight), (255, 0, 0), 4)
      cv2.line(img, tuple(bottomRight), tuple(bottomLeft), (255, 0, 0), 4)
      cv2.line(img, tuple(bottomLeft), tuple(topLeft), (255, 0, 0), 4)
      cv2.circle(img, (cX, cY), 4, (0, 0, 255), -1)
      putTextPIL(img, f'{markerID}/{distance}cm', (topLeft[0], topLeft[1] - 15), 15, (0, 255, 0))
    return img
