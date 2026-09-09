from openpibo.oled import Oled
from openpibo.audio import Audio
from fastapi import FastAPI, Body, Request
from fastapi.responses import JSONResponse,HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from threading import Timer, Thread
from collections import Counter
import json,time,os,shutil
import wifi
import network_disp
import uart_ctrl
import argparse
from mcu_control import DeviceControl

@asynccontextmanager
async def lifespan(app: FastAPI):
  global winfo, ole, aud, device_control
  ole = Oled()
  aud = Audio()
  device_control = DeviceControl()
  device_control.send_raw("#20:150,150,150!")
  winfo = ['','','','','','']
  uart_ctrl.start()
  boot()
  device_control.send_raw("#20:0,0,0!")
  yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
apmode = False

templates = Jinja2Templates(directory="/home/pi/openpibo-os/docs")
app.mount("/build", StaticFiles(directory="/home/pi/openpibo-os/docs/build"), name="build")

@app.get('/', response_class=HTMLResponse)
async def read_root(request: Request):
  return templates.TemplateResponse("index.html", {"request": request})

@app.get("/device/{pkt}")
async def device_command(pkt: str):
  try:
    if pkt == "#15:!":
      return JSONResponse(content=device_control.system_data.get('battery', ''), status_code=200)
    elif pkt == "#40:!":
      return JSONResponse(content=device_control.system_data.get('system', ''), status_code=200)
    else:
      response = device_control.send_raw(pkt)
      return JSONResponse(content=response, status_code=200)
  except Exception as ex:
    return JSONResponse(content=f"Error: {str(ex)}", status_code=500)

@app.get('/wifi_scan')
async def f():
  return JSONResponse(content=wifi.wifi_scan(), status_code=200)

@app.get('/wifi')
async def f():
  return JSONResponse(content={'result':'ok', 'ssid':winfo[2], 'psk':winfo[3], 'ipaddress':winfo[0], 'eth1': winfo[1], 'identity':winfo[4], 'key-mgmt':winfo[5]}, status_code=200)

@app.post('/wifi')
async def f(data: dict = Body(...)):
  print(data)
  if data['ssid'] == "": # error
    return JSONResponse(content=f"Error: {str(ex)}", status_code=500)
  elif data['psk'] == "": # open
    os.system(f"sudo /home/pi/openpibo-os/system/conwifi.sh open '{data['ssid']}'")
  elif data['psk'] != "": # wpa or wpa-e
    if len(data['psk']) < 8:
      return JSONResponse(content={'result':'fail', 'data':'psk must be at least 8 digits.'}, status_code=200)
    elif data['identity'] == "": # wpa
      os.system(f"sudo /home/pi/openpibo-os/system/conwifi.sh wpa-psk '{data['ssid']}' '{data['psk']}'")
    else: #wpa-e
      os.system(f"sudo /home/pi/openpibo-os/system/conwifi.sh wpa-enterprise '{data['ssid']}' '{data['identity']}' '{data['psk']}'")
  else:
    return JSONResponse(content=f"Error: {str(ex)}", status_code=500)
  os.system('shutdown -r now &')
  return JSONResponse(content="ok", status_code=200)

def wifi_update():
  global winfo, apmode
  tmp = os.popen('/home/pi/openpibo-os/system/system.sh').read().strip('\n').split(',')
  if (tmp[6] != '' and tmp[6][0:3] != '169') or (tmp[7] != '' and tmp[7][0:3] != '169'):
    if apmode == True:
      #os.system("sudo ip link set ap0 down")
      os.system("/home/pi/openpibo-os/system/hotspot.sh stop")
      print(f'ap0 up->down')
    apmode = False
  else:
    if apmode == False:
      #os.system("sudo ip link set ap0 up")
      os.system("/home/pi/openpibo-os/system/hotspot.sh start")
      print(f'ap0 down->up')
    apmode = True
  if winfo != tmp[6:12]:
    print(f'Network Change {winfo} -> {tmp[6:12]}')
    network_disp.run()
  winfo = tmp[6:12]
  _ = Timer(10, wifi_update)
  _.daemon = True
  _.start()

## foot servo watchdog
# 발 서보(0, 6번) 과열 방지: 마지막 모터 명령 후 FOOT_HOLD_SEC 동안 새 명령이 없고
# 0/6번이 0이 아니면 FOOT_STEP씩 FOOT_STEP_MS 간격으로 0까지 되돌린다.
# .motor_pos 및 servo write 단위: 각도 x10 (-800 ~ 800)
FOOT_POS_FILE = "/home/pi/.motor_pos"
FOOT_CH = (0, 6)
FOOT_HOLD_SEC = 10.0
FOOT_STEP = 50
FOOT_STEP_MS = 100
FOOT_POLL = 0.5

def foot_read_pos():
  try:
    with open(FOOT_POS_FILE) as f:
      v = [int(x) for x in f.read().strip().split(",")]
    return v if len(v) == 10 else None
  except Exception:
    return None

def foot_mtime():
  try:
    return os.stat(FOOT_POS_FILE).st_mtime
  except Exception:
    return 0

def foot_ramp_to_zero(n, cur):
  step = -FOOT_STEP if cur > 0 else FOOT_STEP
  p = cur
  while p != 0:
    p = 0 if abs(p) <= FOOT_STEP else p + step
    os.system(f"servo write {n} {p}")
    time.sleep(FOOT_STEP_MS / 1000)
    now = foot_read_pos()
    if now is None or now[n] != p:   # 외부 명령 개입 시 중단
      return
  print(f'foot {n}: {cur} -> 0')

def foot_watchdog():
  last_seen = foot_mtime()
  while True:
    time.sleep(FOOT_POLL)
    m = foot_mtime()
    pos = foot_read_pos()
    if pos is None:
      continue
    if m != last_seen:
      last_seen = m
      continue
    if time.time() - m < FOOT_HOLD_SEC:
      continue
    for n in FOOT_CH:
      if pos[n] != 0:
        foot_ramp_to_zero(n, pos[n])
    last_seen = foot_mtime()

## boot
def boot():
  try:
    with open('/home/pi/.OS_VERSION', 'r') as f:
      os_version = str(f.readlines()[0].split('\n')[0])
  except Exception as ex:
    os_version = "OS (None)"
    pass

  try:
    with open('/home/pi/config.json', 'r') as f:
      tmp = json.load(f)
  except Exception as ex:
    pass

  aud.play("/home/pi/openpibo-os/system/opening.mp3", 70)
  ole.clear()
  ole.draw_image("/home/pi/openpibo-os/system/pibo.jpg")
  ole.draw_text((5,0), os_version)
  ole.show()
  time.sleep(5)
  for i in range(1,10):
    tmp = os.popen('/home/pi/openpibo-os/system/system.sh').read().strip('\n').split(',')
    if (tmp[6] != '' and tmp[6][0:3] != '169') or (tmp[7] != '' and tmp[7][0:3] != '169'):
      #os.system("/home/pi/openpibo-os/system/hotspot.sh stop")
      break
    ole.draw_text((5,5), "˚".join(["" for _ in range(i+1)]))
    ole.show()
    time.sleep(3)
  network_disp.run()
  _ = Timer(10, wifi_update)
  _.daemon = True
  _.start()
  Thread(target=foot_watchdog, daemon=True).start()

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--port', help='set port number', default=8080)
  args = parser.parse_args()

  import uvicorn
  uvicorn.run('booting:app', host='0.0.0.0', port=args.port, access_log=False)
