from fastapi_socketio import SocketManager
from fastapi import FastAPI,Request,UploadFile,File,Body
from fastapi.responses import HTMLResponse,FileResponse,JSONResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager

import time,os,re,json,shutil,logging,asyncio,math
from urllib import parse
import argparse
from threading import Timer

pibo = None

# 글꼴은 IDE(80) 한 벌을 세 앱이 같이 쓴다(260929). 이 서버의 글꼴 주소는 IDE 주소로 영구 이동시킨다.
# 브라우저 캐시는 호스트가 같으면 포트가 달라도 같이 쓰므로, 한 번 받으면 IDE·도구·분류기가 다시 받지 않는다.
# 전엔 앱마다 사본이라 처음 열 때 앱마다 최대 1.3MB(Pretendard) + 아이콘 글꼴을 따로 받았다.
# IDE 는 CORS 를 모두 허용한다(글꼴은 CORS 로 받는다). PIBO_IDE_PORT 는 시험용(기본 80)
SHARED_FONT = re.compile(r'^/(static/fonts/Pretendard-[\w.-]+\.woff2|webfonts/fa-[\w.-]+\.(?:woff2|ttf))$')

class SharedFonts:
  def __init__(self, app):
    self.app = app

  async def __call__(self, scope, receive, send):
    m = SHARED_FONT.match(scope.get('path', '')) if scope['type'] == 'http' else None
    if m:
      port = int(os.environ.get('PIBO_IDE_PORT', 80))
      host = (dict(scope.get('headers') or []).get(b'host', b'').decode('latin-1').rsplit(':', 1)[0]) or '127.0.0.1'
      url = f"http://{host}{'' if port == 80 else f':{port}'}/{m.group(1)}"
      await RedirectResponse(url, status_code=301, headers={'Cache-Control': 'public, max-age=604800'})(scope, receive, send)
      return
    await self.app(scope, receive, send)

def init_pibo():
  global pibo
  from lib import Pibo
  pibo = Pibo(emit)
  os.system('/home/pi/.pyenv/bin/python3 /home/pi/openpibo-os/system/network_disp.py')

@asynccontextmanager
async def lifespan(app: FastAPI):
  logging.basicConfig(level=logging.ERROR, format='%(asctime)s [%(levelname)s] %(message)s')
  t = Timer(0, init_pibo)
  t.daemon = True
  t.start()
  yield

try:
  app = FastAPI(lifespan=lifespan)
  app.mount("/static", StaticFiles(directory="static"), name="static")
  app.mount("/webfonts", StaticFiles(directory="webfonts"), name="webfonts")
  app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
  # IDE·분류기처럼 gzip 으로 보낸다. 도구 첫 화면 JS·CSS 500KB → 133KB (수업에서 여러 대가 한 공유기로 받는다)
  app.add_middleware(GZipMiddleware, minimum_size=1000)
  app.add_middleware(SharedFonts)
  socketio = SocketManager(app=app, cors_allowed_origins=[], mount_location="/socket.io", socketio_path="")
except Exception as ex:
  logging.error(f'Server Error:{ex}')

# 화면(소켓·올린 파일)에서 오는 값은 그대로 믿지 않는다(261027). 숫자로 바꾸고 범위 안으로 자른다.
# 전엔 그대로 넘겨서 글자 하나로 녹음·모터 명령이 실패하거나 화면 스레드가 죽었다. 숫자가 아니면 None
def to_num(v, lo, hi, cast=int):
  if isinstance(v, bool):
    return None
  try:
    f = float(v)
  except (TypeError, ValueError):
    return None
  if not math.isfinite(f):
    return None
  f = min(max(f, lo), hi)
  return int(round(f)) if cast is int else f

MOTOR_KEEP = 999   # 동작 데이터에서 '이 모터는 그대로' 표시(openpibo motion_db)

def motor_pos(v):
  p = to_num(v, -MOTOR_KEEP, MOTOR_KEEP)
  if p is None or p == MOTOR_KEEP:
    return p
  return min(max(p, -80), 80)

def motor_list(v):
  if not isinstance(v, list) or len(v) != 10:
    return None
  lst = [motor_pos(p) for p in v]
  return None if None in lst else lst

def clean_motion(m):
  """동작 하나(make_raw 형식)를 검사해 숫자만 담은 새 dict 로 돌려준다. 틀리면 ValueError"""
  if not isinstance(m, dict):
    raise ValueError('motion must be an object')
  if not m:
    return {}
  out = {}
  if 'init_def' in m:
    init_def = to_num(m['init_def'], 0, 1)
    if init_def is None:
      raise ValueError('bad init_def')
    out['init_def'] = init_def
  if 'init' in m:
    init = motor_list(m['init'])
    if init is None:
      raise ValueError('bad init')
    out['init'] = init
  pos = m.get('pos', [])
  if not isinstance(pos, list):
    raise ValueError('bad pos')
  out['pos'] = []
  for item in pos:
    d = motor_list(item.get('d')) if isinstance(item, dict) else None
    seq = to_num(item.get('seq'), 0, 3600000) if isinstance(item, dict) else None
    if d is None or seq is None:
      raise ValueError('bad pos item')
    out['pos'].append({'d': d, 'seq': seq})
  return out

def clean_motions(j):
  if not isinstance(j, dict) or not j:
    raise ValueError('file must be an object of motions')
  return {str(name): clean_motion(m) for name, m in j.items()}

# REST API
@app.get('/', response_class=HTMLResponse)
async def f(request:Request):
  await emit('onoff', False if pibo is None else True)
  # 템플릿은 Jinja 문법을 안 쓴다. 파일을 그대로 보낸다(starlette 1.0 에서 옛 TemplateResponse 호출이 500)
  return FileResponse(os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html"), media_type="text/html",
                      headers={"Cache-Control": "no-cache"})

@app.post('/import_motion')
async def import_motion(data:UploadFile = File(...)):
  if pibo is None:
    return JSONResponse(content={'result':'not_ready'}, status_code=503)
  # 전엔 임시 파일(~/custom_motion.json)에 쓰고 읽었는데, 읽기에 실패해도 그대로 진행해 500 이 났다.
  # 메모리에서 바로 읽고 검사한다. 틀린 파일이면 400 + 문구 키(화면이 t() 로 번역)
  try:
    content = await data.read(2 * 1024 * 1024 + 1)
    if len(content) > 2 * 1024 * 1024:
      raise ValueError('file too large')
    content = clean_motions(json.loads(content))
  except Exception as ex:
    logging.error(f'[import_motion] Error: {ex}')
    return JSONResponse(content={'result':'motion_file_invalid'}, status_code=400)

  pibo.motion_j.update(content)
  with open('/home/pi/mymotion.json', 'w') as f:
    json.dump(pibo.motion_j, f)
  shutil.chown('/home/pi/mymotion.json', 'pi', 'pi')

  try:
    await emit('disp_motion', {'record':pibo.motion_j})
    return JSONResponse(content={"filename":"custom_motion.json"}, status_code=200)
  except Exception as ex:
    return JSONResponse(content={'result':'motion_file_invalid'}, status_code=500)

@app.get('/export_motion/{name}', response_class=FileResponse)
async def export_motion(name="all"):
  try:
    with open('/home/pi/mymotion.json', 'rb') as f:
      tmp = json.load(f)
  except Exception as ex:
    logging.error(f'[export_motion] Error: {ex}')
    return JSONResponse(content={'result':'저장된 모션이 없습니다.'}, status_code=500)

  if name == "all":
    j = tmp  
  elif name in tmp:
    j = dict()
    j[name] = tmp[name]
  else:
    return JSONResponse(content={'result':'선택한 모션이 없습니다.'}, status_code=500)

  with open('/home/pi/.motion.json', 'w') as f:
    json.dump(j, f)
  shutil.chown('/home/pi/.motion.json', 'pi', 'pi')
  return FileResponse(path="/home/pi/.motion.json", media_type="application/json", filename=f"{name}.json")

@app.get('/download_img', response_class=FileResponse)
async def download_img():
  if pibo is None or not pibo.imwrite('/home/pi/capture.jpg'):
    return JSONResponse(content={'result': 'camera not ready'}, status_code=503)
  return FileResponse(path="/home/pi/capture.jpg", media_type="image/jpeg", filename="capture.jpg")

## socktio
# 준비 상태(260929): 화면이 붙는 순간 지금 상태를 그 화면에만 알려 준다.
# 전엔 초기화가 끝날 때 한 번 방송하는 게 전부라, 그 뒤에 열거나 새로 고친 화면은 [로봇 연결됨] 이 안 떴다
# (화면이 5초마다 'onoff' 를 묻지만 받는 곳이 없었다 → 아래 onoff 가 답한다)
async def send_state(sid):
  await app.sio.emit('onoff', pibo is not None, to=sid)
  if pibo is not None:
    await app.sio.emit('vision_state', dict(pibo.vision_state), to=sid)
    await app.sio.emit('voice_state', pibo.voice_state, to=sid)

@app.sio.on('connect')
async def on_connect(sid, *args):
  await send_state(sid)

@app.sio.on('onoff')
async def onoff(sid, d=None):
  await send_state(sid)

# 음성 탭을 열면 목소리 모델을 미리 올린다(처음 한 번 몇 초). 끝나면 모두에게 알린다
@app.sio.on('voice_warm')
async def voice_warm(sid, d=None):
  if pibo is None or pibo.voice_state in ('loading', 'ready'):
    return
  await emit('voice_state', 'loading')
  try:
    await asyncio.to_thread(pibo.voice_warm)
  except Exception as ex:
    logging.error(f'[voice_warm] Error: {ex}')
  await emit('voice_state', pibo.voice_state)

# vision
@app.sio.on('disp_vision')
async def disp_vision(sid, d=None):
  if pibo is None:
    return
  await emit('disp_vision', pibo.vision_type)

@app.sio.on('detect')
async def detect(sid, d=None):
  if pibo is None:
    return
  pibo.vision_type=str(d)

@app.sio.on('marker_length')
async def marker_length(sid, d=None):
  if pibo is None:
    return
  v = to_num(d, 0.1, 100, float)
  if v is not None:
    pibo.marker_length = v

@app.sio.on('object_tracker_init')
async def object_tracker_init(sid, d=None):
  if pibo is None:
    return
  if not isinstance(d, dict):
    return
  box = {k: to_num(d.get(k), 0, 4096) for k in ('x1', 'y1', 'x2', 'y2')}
  if None in box.values():
    return
  if pibo.vision_type == "track":
    pibo.object_tracker_init(box)

@app.sio.on('update_img_pointer')
async def update_img_pointer(sid, d=None):
  if pibo is None or not isinstance(d, dict):
    return
  x, y = to_num(d.get('x'), 0, 4096), to_num(d.get('y'), 0, 4096)
  if x is not None and y is not None:   # 정수가 아니면 화면 스레드의 putText 가 죽었다
    pibo.imgX, pibo.imgY = x, y

def volume_of(d):
  v = to_num(d.get('volume'), 0, 100) if isinstance(d, dict) else None
  return 80 if v is None else v

mic_lock = asyncio.Lock()

@app.sio.on('mic')
async def mic(sid, d=None):
  if pibo is None:
    return
  # 녹음 시간은 화면 입력칸과 같은 1~30초. 녹음은 스레드에서 — 전엔 녹음하는 동안 도구 서버 전체가 멈췄다
  if mic_lock.locked():   # 녹음 중에 또 누름
    return
  sec = to_num(d.get('time'), 1, 30) if isinstance(d, dict) else None
  if sec is None:
    await emit('mic', '')
    return
  async with mic_lock:
    try:
      await asyncio.to_thread(pibo.mic, {'time': sec})
    except Exception as ex:
      logging.error(f'[mic] Error: {ex}')
      await emit('mic', '')
      return
  await emit('mic', '')
  pibo.aud.play("/home/pi/myaudio/mic.wav", volume_of(d))

@app.sio.on('mic_replay')
async def mic_replay(sid, d=None):
  if pibo is None:
    return
  pibo.aud.play("/home/pi/myaudio/mic.wav", volume_of(d))

@app.sio.on('tts')
async def tts(sid, d=None):
  if pibo is None:
    return
  if not isinstance(d, dict):
    return
  d = {'voice_type': str(d.get('voice_type', '')), 'text': str(d.get('text', '')), 'volume': volume_of(d)}
  # 온디바이스 합성이 1~2초 걸린다. 스레드로 돌려야 그동안 다른 화면(카메라 스트림 등)이 안 멈춘다
  cold = pibo.voice_state != 'ready' and d and d.get('voice_type') in pibo.OD_VOICES
  if cold:
    await emit('voice_state', 'loading')
  err = await asyncio.to_thread(pibo.tts, d)
  if cold:
    await emit('voice_state', pibo.voice_state)
  await emit('tts_status', {'ok': err is None, 'error': err or ''})

@app.sio.on('tts_stop')
async def tts_stop(sid, d=None):
  if pibo is None:
    return
  await asyncio.to_thread(pibo.tts_stop)
  await emit('tts_status', {'ok': True, 'stopped': True, 'error': ''})

# speech
# motion
@app.sio.on('disp_motion')
async def disp_motion(sid, d=None):
  if pibo is None:
    return
  res = pibo.get_motor_info()
  await emit('disp_motion', {'pos':res[0], 'table':res[1], 'record':res[2]})

@app.sio.on('set_motor')
async def set_motor(sid, d=None):
  if pibo is None:
    return
  if not isinstance(d, dict):
    return
  idx, pos = to_num(d.get('idx'), -1, 10), to_num(d.get('pos'), -80, 80)
  if idx is None or not 0 <= idx <= 9 or pos is None:
    return
  pibo.set_motor(idx, pos)

@app.sio.on('set_motors')
async def set_motors(sid, d=None):
  if pibo is None:
    return
  lst = motor_list(d.get('pos_lst')) if isinstance(d, dict) else None
  if lst is None:
    return
  pibo.set_motors(lst)

@app.sio.on('add_frame')
async def add_frame(sid, d=None):
  if pibo is None:
    return
  seq = to_num(d, 0, 3600000)
  if seq is None:
    return
  res = pibo.add_frame(seq)
  await emit('disp_motion', {'table':res})

@app.sio.on('delete_frame')
async def delete_frame(sid, d=None):
  if pibo is None:
    return
  seq = to_num(d, 0, 3600000)
  if seq is None:
    return
  res = pibo.delete_frame(seq)
  await emit('disp_motion', {'table':res})

@app.sio.on('init_frame')
async def init_frame(sid, d=None):
  if pibo is None:
    return
  res = pibo.init_frame()
  await emit('disp_motion',{'table':res})

@app.sio.on('play_frame')
async def play_frame(sid, d=None):
  if pibo is None:
    return
  cycle = to_num(d, 1, 100)
  if cycle is None:
    return
  pibo.play_frame(cycle)

@app.sio.on('stop_frame')
async def stop_frame(sid, d=None):
  if pibo is None:
    return
  pibo.stop_frame()

@app.sio.on('add_motion')
async def add_motion(sid, d=None):
  if pibo is None:
    return
  if not isinstance(d, str) or d.strip() == '':
    return
  res = pibo.add_motion(d)
  await emit('disp_motion', {'record':res})

@app.sio.on('load_motion')
async def load_motion(sid, d=None):
  if pibo is None:
    return
  res = pibo.load_motion(str(d))
  await emit('disp_motion', {'table':res})

@app.sio.on('delete_motion')
async def delete_motion(sid, d=None):
  if pibo is None:
    return
  res = pibo.delete_motion(str(d))
  await emit('disp_motion', {'record':res})

@app.sio.on('reset_motion')
async def reset_motion(sid, d=None):
  if pibo is None:
    return
  res = pibo.reset_motion()
  await emit('disp_motion', {'record':res})

@app.sio.on('vision_sleep')
async def vision_sleep(sid, d='off'):
  if pibo is None:
    return
  pibo.vision_sleep = True if d == 'on' else False
  return await emit('vision_sleep', 'on' if pibo.vision_sleep else 'off')

async def emit(key, data, callback=None):
  try:
    logging.debug(f'{key}')
    await app.sio.emit(key, data, callback=callback)
  except Exception as ex:
    logging.error(f'[emit] Error: {ex}')

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--port', help='set port number', type=int, default=50000)
  args = parser.parse_args()

  import uvicorn
  uvicorn.run('run_tools:app', host='0.0.0.0', port=args.port, access_log=False)
