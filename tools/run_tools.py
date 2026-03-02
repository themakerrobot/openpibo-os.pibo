from fastapi import FastAPI, Request, UploadFile, File, Body
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

import time, os, json, shutil, logging, asyncio
import argparse

pibo = None

def init_pibo():
  global pibo
  from lib import Pibo
  pibo = Pibo()
  os.system('/home/pi/.pyenv/bin/python3 /home/pi/openpibo-os/system/network_disp.py')

@asynccontextmanager
async def lifespan(app: FastAPI):
  logging.basicConfig(level=logging.ERROR, format='%(asctime)s [%(levelname)s] %(message)s')
  loop = asyncio.get_event_loop()
  loop.run_in_executor(None, init_pibo)
  yield

try:
  app = FastAPI(lifespan=lifespan)
  app.mount("/static", StaticFiles(directory="static"), name="static")
  app.mount("/webfonts", StaticFiles(directory="webfonts"), name="webfonts")
  app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
  templates = Jinja2Templates(directory="templates")
except Exception as ex:
  logging.error(f'Server Error: {ex}')


# ── SSE broadcast ──────────────────────────────────────────────────────────────
sse_clients: list = []

async def broadcast(key: str, data):
  msg = json.dumps({key: data}, ensure_ascii=False)
  for q in sse_clients:
    await q.put(msg)

@app.get('/api/stream')
async def api_stream(request: Request):
  q: asyncio.Queue = asyncio.Queue()
  sse_clients.append(q)
  async def generate():
    try:
      while True:
        if await request.is_disconnected():
          break
        try:
          msg = await asyncio.wait_for(q.get(), timeout=30)
          yield f"data: {msg}\n\n"
        except asyncio.TimeoutError:
          yield "data: {\"ping\": true}\n\n"
    finally:
      if q in sse_clients:
        sse_clients.remove(q)
  return StreamingResponse(generate(), media_type='text/event-stream',
                           headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})


# ── Pages ──────────────────────────────────────────────────────────────────────
@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
  return templates.TemplateResponse("index.html", {"request": request})


# ── Status ─────────────────────────────────────────────────────────────────────
@app.get('/api/status')
async def api_status():
  return JSONResponse(content={'onoff': False if pibo is None else True})


# ── Vision ─────────────────────────────────────────────────────────────────────
@app.get('/api/vision/type')
async def api_vision_type_get():
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  return JSONResponse(content={'vision_type': pibo.vision_type})

@app.post('/api/vision/type')
async def api_vision_type_set(data: dict = Body(...)):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  pibo.vision_type = data.get('vision_type', 'camera')
  return JSONResponse(content={'ok': True})

@app.post('/api/vision/marker_length')
async def api_marker_length(data: dict = Body(...)):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  pibo.marker_length = data.get('marker_length', 2)
  return JSONResponse(content={'ok': True})

@app.post('/api/vision/tracker/init')
async def api_tracker_init(data: dict = Body(...)):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  if pibo.vision_type == "track":
    pibo.object_tracker_init(data)
  return JSONResponse(content={'ok': True})

@app.post('/api/vision/pointer')
async def api_pointer(data: dict = Body(...)):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  pibo.imgX, pibo.imgY = data.get('x', 0), data.get('y', 0)
  return JSONResponse(content={'ok': True})

@app.post('/api/vision/sleep')
async def api_vision_sleep(data: dict = Body(...)):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  pibo.vision_sleep = True if data.get('sleep', 'off') == 'on' else False
  return JSONResponse(content={'sleep': 'on' if pibo.vision_sleep else 'off'})

@app.get('/api/vision/stream')
async def api_vision_stream(request: Request):
  """MJPEG-style SSE camera stream."""
  async def generate():
    import base64
    while True:
      if await request.is_disconnected():
        break
      if pibo is None or pibo.vision_sleep:
        await asyncio.sleep(0.5)
        continue
      try:
        img_b64 = pibo.get_frame_b64()
        if img_b64:
          data = json.dumps({'img': img_b64, 'data': pibo.last_res or ''})
          yield f"data: {data}\n\n"
      except Exception as ex:
        logging.error(f'[vision_stream] {ex}')
      await asyncio.sleep(0.5)
  return StreamingResponse(generate(), media_type='text/event-stream',
                           headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})


# ── Device ─────────────────────────────────────────────────────────────────────
@app.get('/api/device/status')
async def api_device_status():
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  return JSONResponse(content={'system': pibo.system_value})

@app.post('/api/device/neopixel')
async def api_neopixel(data: dict = Body(...)):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  pibo.set_neopixel(data.get('value', [0,0,0,0,0,0]))
  return JSONResponse(content={'ok': True})

@app.post('/api/device/eye')
async def api_eye(data: dict = Body(...)):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  value = [0,0,0,0,0,0]
  raw = data.get('value', '')
  if raw:
    value = raw.split(',')
  pibo.set_neopixel(value)
  return JSONResponse(content={'ok': True})

@app.post('/api/device/oled/text')
async def api_oled_text(data: dict = Body(...)):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  pibo.set_oled(data)
  return JSONResponse(content={'ok': True})

@app.get('/api/device/oled/path')
async def api_oled_path(p: str):
  return JSONResponse(content={'files': os.listdir(p)})

@app.post('/api/device/oled/image')
async def api_oled_image(data: dict = Body(...)):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  pibo.set_oled_image(data.get('path', ''))
  return JSONResponse(content={'ok': True})

@app.post('/api/device/oled/clear')
async def api_oled_clear():
  os.system('/home/pi/.pyenv/bin/python3 /home/pi/openpibo-os/system/network_disp.py')
  return JSONResponse(content={'ok': True})


# ── Audio ──────────────────────────────────────────────────────────────────────
@app.post('/api/audio/mic')
async def api_mic(data: dict = Body(...)):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  await asyncio.to_thread(pibo.mic, data)
  pibo.aud.play("/home/pi/myaudio/mic.wav", data.get('volume', 50))
  return JSONResponse(content={'ok': True})

@app.post('/api/audio/mic/replay')
async def api_mic_replay(data: dict = Body(...)):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  pibo.aud.play("/home/pi/myaudio/mic.wav", data.get('volume', 50))
  return JSONResponse(content={'ok': True})

@app.post('/api/audio/tts')
async def api_tts(data: dict = Body(...)):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  await asyncio.to_thread(pibo.tts, data)
  return JSONResponse(content={'ok': True})

@app.post('/api/audio/play')
async def api_play_audio(data: dict = Body(...)):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  pibo.stop_audio()
  pibo.play_audio(data.get('filename', ''), data.get('volume', 50), True)
  return JSONResponse(content={'ok': True})

@app.post('/api/audio/stop')
async def api_stop_audio():
  if pibo is not None:
    pibo.stop_audio()
  return JSONResponse(content={'ok': True})

@app.get('/api/audio/path')
async def api_audio_path(p: str):
  return JSONResponse(content={'files': os.listdir(p)})


# ── Speech ─────────────────────────────────────────────────────────────────────
@app.post('/api/speech/question')
async def api_question(data: dict = Body(...)):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  res = await asyncio.to_thread(pibo.question, data)
  return JSONResponse(content={'answer': res, 'chat_list': list(reversed(pibo.chat_list))})

@app.post('/api/speech/translate')
async def api_translate(data: dict = Body(...)):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  res = await asyncio.to_thread(pibo.translate, data)
  return JSONResponse(content={'result': res})

@app.get('/api/speech/chat_list')
async def api_chat_list():
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  return JSONResponse(content={'chat_list': list(reversed(pibo.chat_list))})

@app.post('/api/speech/reset_csv')
async def api_reset_csv(data: dict = Body(...)):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  pibo.reset_csv(data)
  return JSONResponse(content={'ok': True})


# ── Motion ─────────────────────────────────────────────────────────────────────
@app.get('/api/motion/info')
async def api_motion_info():
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  pos, table, record = pibo.get_motor_info()
  return JSONResponse(content={'pos': pos, 'table': table, 'record': record})

@app.post('/api/motion/motor')
async def api_set_motor(data: dict = Body(...)):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  pibo.set_motor(data.get('idx', 0), data.get('pos', 0))
  return JSONResponse(content={'ok': True})

@app.post('/api/motion/motors')
async def api_set_motors(data: dict = Body(...)):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  pibo.set_motors(data.get('pos_lst', []))
  return JSONResponse(content={'ok': True})

@app.post('/api/motion/frame/add')
async def api_add_frame(data: dict = Body(...)):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  res = pibo.add_frame(data.get('seq', 0))
  return JSONResponse(content={'table': res})

@app.post('/api/motion/frame/delete')
async def api_delete_frame(data: dict = Body(...)):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  res = pibo.delete_frame(data.get('seq', 0))
  return JSONResponse(content={'table': res})

@app.post('/api/motion/frame/init')
async def api_init_frame():
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  res = pibo.init_frame()
  return JSONResponse(content={'table': res})

@app.post('/api/motion/frame/play')
async def api_play_frame(data: dict = Body(...)):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  pibo.play_frame(data.get('cycle', 1))
  return JSONResponse(content={'ok': True})

@app.post('/api/motion/frame/stop')
async def api_stop_frame():
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  pibo.stop_frame()
  return JSONResponse(content={'ok': True})

@app.post('/api/motion/add')
async def api_add_motion(data: dict = Body(...)):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  res = pibo.add_motion(data.get('name', ''))
  return JSONResponse(content={'record': res})

@app.post('/api/motion/load')
async def api_load_motion(data: dict = Body(...)):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  res = pibo.load_motion(data.get('name', ''))
  return JSONResponse(content={'table': res})

@app.post('/api/motion/delete')
async def api_delete_motion(data: dict = Body(...)):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  res = pibo.delete_motion(data.get('name', ''))
  return JSONResponse(content={'record': res})

@app.post('/api/motion/reset')
async def api_reset_motion():
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  res = pibo.reset_motion()
  return JSONResponse(content={'record': res})


# ── Simulation ─────────────────────────────────────────────────────────────────
@app.post('/api/simulate/play')
async def api_sim_play(data: dict = Body(...)):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  key = data.get('key', '')
  content = data.get('content', '')
  if key == 'eye':
    pibo.set_neopixel(content)
    return JSONResponse(content={'result': {'eye': 'stop'}})
  elif key == 'motion':
    if data.get('type') == 'default':
      pibo.async_sim_motion(content, data.get('cycle', 1))
    elif data.get('type') == 'mymotion':
      pibo.async_sim_motion(content, data.get('cycle', 1), "/home/pi/mymotion.json")
  elif key == 'audio':
    pibo.async_sim_audio(data.get("type", "") + content, data.get("volume", 50))
  elif key == 'oled':
    if data.get('type') == 'text':
      pibo.set_oled({'x': data.get('x', 0), 'y': data.get('y', 0), 'size': data.get('size', 20), 'text': content})
    else:
      pibo.set_oled_image(content)
    return JSONResponse(content={'result': {'oled': 'stop'}})
  elif key == 'tts':
    pibo.tts({'text': content, 'voice_type': data.get('type', 'gtts'), 'volume': data.get('volume', 50)})
    return JSONResponse(content={'result': {'tts': 'stop'}})
  return JSONResponse(content={'ok': True})

@app.post('/api/simulate/stop')
async def api_sim_stop(data: dict = Body(...)):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  d = data.get('key', '')
  if d == 'eye':
    pibo.set_neopixel([0,0,0,0,0,0])
  elif d == 'motion':
    pibo.stop_frame()
    pibo.set_motors([0, 0, -80, 0, 0, 0, 0, 0, 80, 0])
  elif d == 'audio':
    pibo.stop_audio()
  elif d == 'oled':
    os.system('/home/pi/.pyenv/bin/python3 /home/pi/openpibo-os/system/network_disp.py')
  elif d == 'tts':
    pibo.stop_audio()
  return JSONResponse(content={'ok': True})

@app.get('/api/simulate/audio')
async def api_sim_audio_list(p: str):
  return JSONResponse(content={'files': os.listdir(p)})

@app.get('/api/simulate/oled')
async def api_sim_oled_list(p: str):
  return JSONResponse(content={'files': os.listdir(p)})

@app.get('/api/simulate/motion')
async def api_sim_motion_list(type: str = 'default'):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  motions = pibo.mot.get_motion() if type == 'default' else pibo.mot.get_motion(path="/home/pi/mymotion.json")
  return JSONResponse(content={'motions': motions})

@app.post('/api/simulate/items/play')
async def api_sim_play_items(data: dict = Body(...)):
  if pibo is not None:
    pibo.start_simulate(data.get('items', []))
  return JSONResponse(content={'ok': True})

@app.post('/api/simulate/items/stop')
async def api_sim_stop_items():
  if pibo is not None:
    pibo.stop_simulate()
  return JSONResponse(content={'ok': True})

@app.post('/api/simulate/items')
async def api_sim_add_item(data: dict = Body(...)):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  res = {}
  try:
    with open('/home/pi/mysim.json', 'rb') as f:
      res = json.load(f)
  except Exception:
    pass
  res[data['name']] = data['data']
  with open('/home/pi/mysim.json', 'w') as f:
    json.dump(res, f)
  return JSONResponse(content={'ok': True})

@app.delete('/api/simulate/items')
async def api_sim_remove_item(name: str = None):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  res = {}
  try:
    with open('/home/pi/mysim.json', 'rb') as f:
      res = json.load(f)
  except Exception:
    pass
  if name and name in res:
    del res[name]
  with open('/home/pi/mysim.json', 'w') as f:
    json.dump(res, f)
  shutil.chown('/home/pi/mysim.json', 'pi', 'pi')
  return JSONResponse(content={'ok': True})

@app.get('/api/simulate/items')
async def api_sim_list_items():
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  res = {}
  try:
    with open('/home/pi/mysim.json', 'rb') as f:
      res = json.load(f)
  except Exception:
    pass
  return JSONResponse(content={'items': list(res.keys())})

@app.get('/api/simulate/item')
async def api_sim_get_item(name: str):
  if pibo is None:
    return JSONResponse(content={'error': 'pibo not ready'}, status_code=503)
  res = {}
  try:
    with open('/home/pi/mysim.json', 'rb') as f:
      res = json.load(f)
  except Exception:
    pass
  return JSONResponse(content={'item': res.get(name, {})})


# ── Original REST endpoints ────────────────────────────────────────────────────
@app.post('/import_motion')
async def import_motion(data: UploadFile = File(...)):
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
    return JSONResponse(content={"filename": data.filename, "record": pibo.motion_j}, status_code=200)
  except Exception as ex:
    return JSONResponse(content={'result': '파일에 문제가 있습니다.'}, status_code=500)

@app.get('/export_motion/{name}', response_class=FileResponse)
async def export_motion(name="all"):
  try:
    with open('/home/pi/mymotion.json', 'rb') as f:
      tmp = json.load(f)
  except Exception as ex:
    logging.error(f'[export_motion] Error: {ex}')
    return JSONResponse(content={'result': '저장된 모션이 없습니다.'}, status_code=500)
  if name == "all":
    j = tmp
  elif name in tmp:
    j = {name: tmp[name]}
  else:
    return JSONResponse(content={'result': '선택한 모션이 없습니다.'}, status_code=500)
  with open('/home/pi/.motion.json', 'w') as f:
    json.dump(j, f)
  shutil.chown('/home/pi/.motion.json', 'pi', 'pi')
  return FileResponse(path="/home/pi/.motion.json", media_type="application/json", filename=f"{name}.json")

@app.get('/download_img', response_class=FileResponse)
async def download_img():
  pibo.imwrite('/home/pi/capture.jpg')
  return FileResponse(path="/home/pi/capture.jpg", media_type="image/jpeg", filename="capture.jpg")

@app.post('/upload_oled')
async def upload_oled(data: UploadFile = File(...)):
  if pibo is None or pibo.onoff == False:
    return JSONResponse(content={'result': 'OFF 상태입니다.'}, status_code=500)
  data.filename = "tmp.jpg"
  filepath = f"/home/pi/{data.filename}"
  with open(filepath, 'wb') as f:
    f.write(await data.read())
  pibo.set_oled_image(filepath)
  os.remove(filepath)
  return JSONResponse(content={"filename": data.filename}, status_code=200)

@app.post('/upload_file/{directory}')
async def upload_file(directory="myaudio", data: UploadFile = File(...)):
  if directory not in ["myaudio", "myimage"]:
    return JSONResponse(content={'result': 'myaudio, myimage로 업로드만 가능합니다.'}, status_code=500)
  os.system(f"mkdir -p '/home/pi/{directory}'")
  filepath = f"/home/pi/{directory}/{data.filename}"
  with open(filepath, 'wb') as f:
    f.write(await data.read())
  return JSONResponse(content={"filename": data.filename}, status_code=200)

@app.post('/upload_csv')
async def upload_csv(data: UploadFile = File(...)):
  data.filename = "mychat.csv"
  filepath = f"/home/pi/{data.filename}"
  with open(filepath, 'wb') as f:
    f.write(await data.read())
  res = pibo.load_csv(filepath)
  os.remove(filepath)
  if res:
    return JSONResponse(content={}, status_code=200)
  else:
    return JSONResponse(content={'result': 'csv 파일 에러'}, status_code=500)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--port', help='set port number', default=50000)
  args = parser.parse_args()

  import uvicorn
  uvicorn.run('run_tools:app', host='0.0.0.0', port=args.port, access_log=False)
