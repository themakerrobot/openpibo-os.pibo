from fastapi_socketio import SocketManager
from fastapi import FastAPI,Request,UploadFile,File,Body
from fastapi.responses import HTMLResponse,FileResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

import time,os,json,shutil,logging,asyncio
from urllib import parse
import argparse
from threading import Timer

pibo = None

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
  socketio = SocketManager(app=app, cors_allowed_origins=[], mount_location="/socket.io", socketio_path="")
except Exception as ex:
  logging.error(f'Server Error:{ex}')

# REST API
@app.get('/', response_class=HTMLResponse)
async def f(request:Request):
  await emit('onoff', False if pibo is None else True)
  # 템플릿은 Jinja 문법을 안 쓴다. 파일을 그대로 보낸다(starlette 1.0 에서 옛 TemplateResponse 호출이 500)
  return FileResponse(os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html"), media_type="text/html",
                      headers={"Cache-Control": "no-cache"})

@app.post('/import_motion')
async def import_motion(data:UploadFile = File(...)):
  data.filename = "custom_motion.json"

  with open(f"/home/pi/{data.filename}", 'wb') as f:
    content = await data.read()
    f.write(content)

  try:
    with open(f'/home/pi/{data.filename}', 'rb') as f:
      content = json.load(f)
  except Exception as ex:
    logging.error(f'[import_motion] Error: {ex}')
    pass

  pibo.motion_j.update(content)
  with open('/home/pi/mymotion.json', 'w') as f:
    json.dump(pibo.motion_j, f)
  shutil.chown('/home/pi/mymotion.json', 'pi', 'pi')

  try:
    await emit('disp_motion', {'record':pibo.motion_j})
    return JSONResponse(content={"filename":data.filename}, status_code=200)
  except Exception as ex:
    return JSONResponse(content={'result':'파일에 문제가 있습니다.'}, status_code=500)

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
  pibo.vision_type=d

@app.sio.on('marker_length')
async def marker_length(sid, d=None):
  if pibo is None:
    return
  pibo.marker_length=d

@app.sio.on('object_tracker_init')
async def object_tracker_init(sid, d=None):
  if pibo is None:
    return
  if pibo.vision_type == "track":
    pibo.object_tracker_init(d)

@app.sio.on('update_img_pointer')
async def update_img_pointer(sid, d=None):
  if pibo is None:
    return
  pibo.imgX, pibo.imgY = d['x'], d['y']

@app.sio.on('mic')
async def mic(sid, d=None):
  if pibo is None:
    return
  pibo.mic(d)
  await emit('mic', '')
  pibo.aud.play("/home/pi/myaudio/mic.wav", d['volume'])

@app.sio.on('mic_replay')
async def mic_replay(sid, d=None):
  if pibo is None:
    return
  pibo.aud.play("/home/pi/myaudio/mic.wav", d['volume'])

@app.sio.on('tts')
async def tts(sid, d=None):
  if pibo is None:
    return
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
  pibo.set_motor(d['idx'], d['pos'])

@app.sio.on('set_motors')
async def set_motors(sid, d=None):
  if pibo is None:
    return
  pibo.set_motors(d['pos_lst'])

@app.sio.on('add_frame')
async def add_frame(sid, d=None):
  if pibo is None:
    return
  res = pibo.add_frame(d)
  await emit('disp_motion', {'table':res})

@app.sio.on('delete_frame')
async def delete_frame(sid, d=None):
  if pibo is None:
    return
  res = pibo.delete_frame(d)
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
  pibo.play_frame(d)

@app.sio.on('stop_frame')
async def stop_frame(sid, d=None):
  if pibo is None:
    return
  pibo.stop_frame()

@app.sio.on('add_motion')
async def add_motion(sid, d=None):
  if pibo is None:
    return
  res = pibo.add_motion(d)
  await emit('disp_motion', {'record':res})

@app.sio.on('load_motion')
async def load_motion(sid, d=None):
  if pibo is None:
    return
  res = pibo.load_motion(d)
  await emit('disp_motion', {'table':res})

@app.sio.on('delete_motion')
async def delete_motion(sid, d=None):
  if pibo is None:
    return
  res = pibo.delete_motion(d)
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
