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
import json,time,os,shutil,subprocess,asyncio
import wifi
import netwatch
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
nw = netwatch.NetWatch()   # 학교 WiFi ↔ AP 전환 판단(netwatch.py 에 규칙이 있다)

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
    elif pkt == "#14:!":
      return JSONResponse(content=device_control.system_data.get('dc', ''), status_code=200)
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

CONWIFI = '/home/pi/openpibo-os/system/conwifi.sh'

@app.post('/wifi')
async def f(data: dict = Body(...)):
  # 입력값은 셸을 거치지 않고 인자 목록으로 넘긴다(260929). 전엔 f"... '{ssid}' '{psk}'" 를 os.system 에 넘겨서
  # SSID·비밀번호에 ' 가 들어가면 따옴표가 닫히고 그 뒤가 root 명령으로 실행됐다(Kim's WiFi 같은 이름은 연결도 안 됐다).
  # 비밀번호는 로그에 남기지 않는다
  ssid = str(data.get('ssid', ''))
  psk = str(data.get('psk', ''))
  identity = str(data.get('identity', ''))
  print(f"[wifi] ssid={ssid!r} identity={identity!r} psk={'set' if psk else 'none'}")
  if ssid == "":
    return JSONResponse(content={'result':'fail', 'data':'ssid is empty.'}, status_code=200)   # 전엔 정의 안 된 ex 를 불러 500
  if psk == "":                 # open
    args = ['open', ssid]
  elif len(psk) < 8:
    return JSONResponse(content={'result':'fail', 'data':'psk must be at least 8 digits.'}, status_code=200)
  elif identity == "":          # wpa
    args = ['wpa-psk', ssid, psk]
  else:                         # wpa-e
    args = ['wpa-enterprise', ssid, identity, psk]
  try:
    await asyncio.to_thread(subprocess.run, ['sudo', CONWIFI, *args], timeout=90)
  except Exception as ex:
    print(f'[wifi] conwifi error: {ex}')
  os.system('shutdown -r now &')
  return JSONResponse(content="ok", status_code=200)

def wifi_update():
  global winfo, apmode
  try:
    tmp = os.popen('/home/pi/openpibo-os/system/system.sh').read().strip('\n').split(',')
    has_ip = (tmp[6] != '' and tmp[6][0:3] != '169') or (tmp[7] != '' and tmp[7][0:3] != '169')
    # 전엔 IP 가 한 번만 없어도 바로 AP 로 넘어갔다 → 판단은 netwatch 가 한다(저장된 SSID 가 보이면 90초 기다림 등)
    nw.step(has_ip)
    apmode = nw.apmode
    if winfo != tmp[6:12]:
      print(f'Network Change {winfo} -> {tmp[6:12]}')
      network_disp.run()
    winfo = tmp[6:12]
  except Exception as ex:
    print(f'[wifi_update] Error: {ex}')   # 예외가 나도 다음 점검은 이어간다(전엔 여기서 멈췄다)
  finally:
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
