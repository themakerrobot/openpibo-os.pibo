import os
import sys
import asyncio
import shutil
import base64
import datetime
import subprocess
import json
import requests
from pathlib import Path
from typing import List

from fastapi import FastAPI, Request, UploadFile, File, Body
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager

# SSE broadcast: list of asyncio.Queue per connected client
sse_clients: list = []

async def broadcast(data: dict):
  for q in sse_clients:
    await q.put(data)

@asynccontextmanager
async def lifespan(app: FastAPI):
  asyncio.create_task(periodic_system_update())
  yield

try:
  app = FastAPI(lifespan=lifespan)
  templates = Jinja2Templates(directory="templates")
  app.mount("/static", StaticFiles(directory="static"), name="static")
  app.mount("/svg", StaticFiles(directory="svg"), name="svg")
  app.mount("/webfonts", StaticFiles(directory="webfonts"), name="webfonts")
except Exception as ex:
  print(f'Server error: {ex}')

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

codeExec = {
  'python': 'python3',
  'shell': 'sh',
}

protectList = [
  '/home/pi/openpibo-',
  '/home/pi/node_modules',
  '/home/pi/package.json',
  '/home/pi/package-lock.json',
  '/home/pi/config.json',
]

ENV_PATH = '/home/pi/.pyenv/bin'
record = ''
ps = None
PATH = '/home/pi/code'
codeText = ''
codePath = ''

mutex = asyncio.Lock()

def is_protect(p):
  for protected_path in protectList:
    if protected_path in p:
      return True
  return False

def read_directory(d):
  dlst = []
  flst = []
  try:
    for p in os.scandir(d):
      if p.is_dir(follow_symlinks=False) or p.is_symlink():
        dlst.append({
          'name': p.name,
          'type': 'folder',
          'protect': is_protect(f"{d}/{p.name}")
        })
      else:
        flst.append({
          'name': p.name,
          'type': 'file',
          'protect': is_protect(d) or is_protect(f"{d}/{p.name}")
        })
  except Exception as err:
    print(err)
    return False
  return sorted(dlst, key=lambda x: x['name']) + sorted(flst, key=lambda x: x['name'])


# ─── REST API endpoints ────────────────────────────────────────────────────────

@app.get('/', response_class=HTMLResponse)
async def read_root(request: Request):
  return templates.TemplateResponse("index.html", {"request": request})


@app.get('/api/init')
async def api_init():
  global codeText, codePath
  system_info = []
  try:
    system_info = subprocess.check_output(
      ['/home/pi/openpibo-os/system/system.sh']
    ).decode().strip().split(',')
  except Exception as err:
    print(err)
  try:
    with open(codePath, 'r') as f:
      codeText = f.read()
  except Exception:
    codeText = ''
  return JSONResponse(content={
    'codepath': codePath,
    'codetext': codeText,
    'path': PATH,
    'system': system_info,
  })


@app.get('/api/system_status')
async def api_system_status():
  result = {}
  try:
    system_info = subprocess.check_output(
      ['/home/pi/openpibo-os/system/system.sh']
    ).decode().strip().split(',')
    result['system'] = system_info
  except Exception:
    pass
  try:
    result['battery'] = requests.get(
      'http://127.0.0.1:8080/device/%2315%3A%21', timeout=2
    ).json().split(':')[1]
  except Exception:
    result['battery'] = '0%'
  try:
    result['dc'] = requests.get(
      'http://127.0.0.1:8080/device/%2314%3A%21', timeout=2
    ).json().split(':')[1]
  except Exception:
    result['dc'] = 'off'
  return JSONResponse(content=result)


@app.get('/api/stream')
async def api_stream(request: Request):
  """SSE endpoint – clients subscribe here for real-time updates."""
  q: asyncio.Queue = asyncio.Queue()
  sse_clients.append(q)

  async def generate():
    try:
      while True:
        if await request.is_disconnected():
          break
        try:
          data = await asyncio.wait_for(q.get(), timeout=30)
          yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
        except asyncio.TimeoutError:
          yield "data: {\"ping\": true}\n\n"
    finally:
      if q in sse_clients:
        sse_clients.remove(q)

  return StreamingResponse(
    generate(),
    media_type='text/event-stream',
    headers={
      'Cache-Control': 'no-cache',
      'X-Accel-Buffering': 'no',
    }
  )


@app.get('/dir')
async def get_directory(folderName: str):
  files = []
  try:
    for p in os.scandir(folderName):
      if not p.is_dir() and not p.is_symlink() and not p.name.startswith('.'):
        files.append(p.name)
  except Exception:
    files = []
  return files


@app.get('/api/load_directory')
async def api_load_directory(p: str):
  global PATH
  res = read_directory(p)
  if res is not False:
    PATH = p
  else:
    res = read_directory(PATH)
  return JSONResponse(content={'data': res, 'path': PATH})


@app.get('/api/view')
async def api_view(p: str):
  try:
    with open(p, 'rb') as f:
      encoded = base64.b64encode(f.read()).decode('utf-8')
    return JSONResponse(content={'image': encoded, 'filepath': p})
  except Exception as err:
    return JSONResponse(content={'error': str(err)}, status_code=500)


@app.get('/api/play_file')
async def api_play_file(p: str):
  try:
    with open(p, 'rb') as f:
      encoded = base64.b64encode(f.read()).decode('utf-8')
    return JSONResponse(content={'audio': encoded, 'filepath': p})
  except Exception as err:
    return JSONResponse(content={'error': str(err)}, status_code=500)


@app.post('/api/load')
async def api_load(data: dict = Body(...)):
  global codeText, codePath
  p = data.get('path', '')
  if is_protect(p):
    return JSONResponse(content={'error': '파일 불러오기 오류: 보호 파일입니다.'}, status_code=403)
  try:
    with open(p, 'r') as f:
      codeText = f.read()
      codePath = p
    return JSONResponse(content={'code': codeText, 'filepath': codePath})
  except Exception as err:
    return JSONResponse(content={'error': str(err)}, status_code=500)


@app.post('/api/delete')
async def api_delete(data: dict = Body(...)):
  global codeText, codePath
  d = data.get('path', '')
  if is_protect(d):
    return JSONResponse(content={'error': '파일 삭제 오류: 보호 파일입니다.'}, status_code=403)
  if d == codePath:
    codePath = ''
    codeText = ''
  try:
    if os.path.isdir(d):
      shutil.rmtree(d)
    else:
      os.remove(d)
  except Exception as err:
    return JSONResponse(content={'error': '파일 삭제 오류: 파일명 파싱 에러입니다.'}, status_code=500)
  return JSONResponse(content={'data': read_directory(PATH)})


@app.post('/api/rename')
async def api_rename(data: dict = Body(...)):
  global codeText, codePath
  oldpath = data.get('oldpath', '')
  newpath = data.get('newpath', '')
  if is_protect(oldpath) or is_protect(newpath):
    return JSONResponse(content={'error': '파일 이름 변경 오류: 보호 파일입니다.'}, status_code=403)
  try:
    os.rename(oldpath, newpath)
  except Exception:
    return JSONResponse(content={'error': '파일 이름 변경 오류: 파일명 파싱 에러입니다.'}, status_code=500)
  result: dict = {'data': read_directory(PATH)}
  if oldpath == codePath:
    try:
      with open(newpath, 'r') as f:
        codeText = f.read()
        codePath = newpath
      result['code'] = codeText
      result['filepath'] = codePath
    except Exception as err:
      return JSONResponse(content={'error': str(err)}, status_code=500)
  return JSONResponse(content=result)


@app.post('/api/add_file')
async def api_add_file(data: dict = Body(...)):
  global codeText, codePath
  p = data.get('path', '')
  if is_protect(PATH):
    return JSONResponse(content={'error': '파일 생성 오류: 보호 디렉토리입니다.'}, status_code=403)
  if not os.path.exists(p):
    try:
      os.makedirs(os.path.dirname(p), exist_ok=True)
      open(p, 'a').close()
      shutil.chown(os.path.dirname(p), user='pi', group='pi')
    except Exception as err:
      return JSONResponse(content={'error': str(err)}, status_code=500)
  codePath = p
  try:
    with open(p, 'r') as f:
      codeText = f.read()
    return JSONResponse(content={
      'code': codeText,
      'filepath': p,
      'data': read_directory(PATH),
    })
  except Exception as err:
    return JSONResponse(content={'error': str(err)}, status_code=500)


@app.post('/api/add_directory')
async def api_add_directory(data: dict = Body(...)):
  p = data.get('path', '')
  if is_protect(PATH):
    return JSONResponse(content={'error': '디렉토리 생성 오류: 보호 폴더입니다.'}, status_code=403)
  try:
    os.makedirs(p, exist_ok=True)
    shutil.chown(p, user='pi', group='pi')
    return JSONResponse(content={'data': read_directory(PATH)})
  except Exception as err:
    return JSONResponse(content={'error': str(err)}, status_code=500)


@app.post('/api/save')
async def api_save(data: dict = Body(...)):
  global codeText, codePath
  try:
    cp = data['codepath']
    if is_protect(cp) or is_protect(os.path.dirname(cp)):
      return JSONResponse(content={'error': '파일 저장 오류: 보호 파일입니다.'}, status_code=403)
    codeText = data['codetext']
    codePath = cp
    os.makedirs(os.path.dirname(codePath), exist_ok=True)
    with open(codePath, 'w') as f:
      f.write(codeText)
    shutil.chown(os.path.dirname(codePath), user='pi', group='pi')
    return JSONResponse(content={'ok': True})
  except Exception as err:
    return JSONResponse(content={'error': str(err)}, status_code=500)


async def run_execute(EXEC: str, codepath: str):
  global record, ps
  async with mutex:
    record = f'[{datetime.datetime.now()}]: \n\n'
    await broadcast({'record': record})
    if EXEC == 'python3':
      ps = await asyncio.create_subprocess_exec(
        f"{ENV_PATH}/{EXEC}", '-u', codepath,
        cwd=PATH,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.PIPE,
      )
    else:
      ps = await asyncio.create_subprocess_exec(
        EXEC, codepath,
        cwd=PATH,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.PIPE,
      )
    while True:
      line = await ps.stdout.readline()
      if not line:
        break
      record += line.decode()
      await broadcast({'record': record})
    err = await ps.stderr.read()
    if err:
      record += f'\n{err.decode()}'
      await broadcast({'record': record})
    await ps.wait()
    ps = None
    record += '\n종료됨.'
    await broadcast({'record': record, 'exit': True, 'file_manager': read_directory(PATH)})


@app.post('/api/execute')
async def api_execute(data: dict = Body(...)):
  global codeText, codePath, ps
  subprocess.Popen(['systemctl', 'stop', 'tools.service'])
  subprocess.Popen(['systemctl', 'stop', 'classify.service'])
  subprocess.Popen(['systemctl', 'stop', 'llama-server.service'])
  try:
    cp = data['codepath']
    if is_protect(cp) or is_protect(os.path.dirname(cp)):
      return JSONResponse(content={'error': '실행 오류: 보호 파일입니다.'}, status_code=403)
    codeText = data['codetext']
    codePath = cp
    if ps and ps.returncode is None:
      ps.kill()
      await ps.wait()
    os.makedirs(os.path.dirname(codePath), exist_ok=True)
    with open(codePath, 'w') as f:
      f.write(codeText)
    shutil.chown(os.path.dirname(codePath), user='pi', group='pi')
    asyncio.create_task(run_execute(codeExec[data['codetype']], codePath))
    return JSONResponse(content={'ok': True})
  except Exception as err:
    return JSONResponse(content={'error': str(err)}, status_code=500)


@app.post('/api/executeb')
async def api_executeb(data: dict = Body(...)):
  global ps
  subprocess.Popen(['systemctl', 'stop', 'tools.service'])
  subprocess.Popen(['systemctl', 'stop', 'classify.service'])
  subprocess.Popen(['systemctl', 'stop', 'llama-server.service'])
  try:
    if ps and ps.returncode is None:
      ps.kill()
      await ps.wait()
    cp = data['codepath']
    os.makedirs(os.path.dirname(cp), exist_ok=True)
    with open(cp, 'w') as f:
      f.write(data['codetext'])
    shutil.chown(os.path.dirname(cp), user='pi', group='pi')
    asyncio.create_task(run_execute(codeExec[data['codetype']], cp))
    return JSONResponse(content={'ok': True})
  except Exception as err:
    return JSONResponse(content={'error': str(err)}, status_code=500)


@app.post('/api/stop')
async def api_stop():
  global ps
  subprocess.Popen(['pkill', 'play'])
  subprocess.Popen(['pkill', 'llama-server'])
  subprocess.Popen(['servo', 'init'])
  if ps and ps.returncode is None:
    ps.kill()
    await ps.wait()
  return JSONResponse(content={'ok': True})


@app.post('/api/prompt')
async def api_prompt(data: dict = Body(...)):
  global ps
  if ps and ps.stdin:
    ps.stdin.write((data.get('text', '') + '\n').encode())
    await ps.stdin.drain()
  return JSONResponse(content={'ok': True})


@app.post('/api/reset_log')
async def api_reset_log():
  global record
  record = f'[{datetime.datetime.now()}]: \n\n'
  subprocess.Popen([f'{ENV_PATH}/python3', '/home/pi/openpibo-os/system/network_disp.py'])
  subprocess.Popen(['servo', 'init'])
  return JSONResponse(content={'ok': True})


@app.post('/api/poweroff')
async def api_poweroff():
  os.system('echo "#11:!" > /dev/ttyS0')
  subprocess.Popen(['shutdown', '-h', 'now'])
  return JSONResponse(content={'ok': True})


@app.post('/api/restart')
async def api_restart():
  subprocess.Popen(['shutdown', '-r', 'now'])
  return JSONResponse(content={'ok': True})


@app.post('/api/restore')
async def api_restore():
  try:
    os.system('rm -rf /home/pi/code/*')
    os.system('rm -rf /home/pi/myimage/*')
    os.system('rm -rf /home/pi/mymodel/*')
    os.system('rm -rf /home/pi/myaudio/*')
    os.system('rm -rf /home/pi/examples/*')
    os.system('cp -rf /home/pi/openpibo-os/examples/* /home/pi/examples/')
    os.system("sudo /home/pi/openpibo-os/system/conwifi.sh wpa-psk 'pibo' '!pibo0314'")
    os.system('echo "#11:!" > /dev/ttyS0')
    subprocess.Popen(['shutdown', '-h', 'now'])
    return JSONResponse(content={'ok': True})
  except Exception as e:
    return JSONResponse(content={'error': str(e)}, status_code=500)


# ─── Original REST endpoints kept as-is ───────────────────────────────────────

@app.get('/download')
async def download_item(filename: str):
  full_path = os.path.join(PATH, filename)
  if is_protect(full_path):
    return JSONResponse(content={'error': '파일 다운로드 오류: 보호 디렉토리입니다.'}, status_code=403)
  if not os.path.exists(full_path):
    return JSONResponse(content={'error': '파일 또는 폴더를 찾을 수 없습니다.'}, status_code=404)
  if os.path.isfile(full_path):
    return FileResponse(full_path, filename=filename)
  elif os.path.isdir(full_path):
    zip_path = '/tmp/download.zip'
    if os.path.exists(zip_path):
      os.remove(zip_path)
    shutil.make_archive('/tmp/download', 'zip', root_dir=full_path)
    return FileResponse(zip_path, media_type='application/zip', filename='download.zip')
  return JSONResponse(content={'error': '올바른 파일 또는 폴더가 아닙니다.'}, status_code=403)


@app.post('/upload')
async def upload_file(files: List[UploadFile] = File(...)):
  if is_protect(PATH):
    return JSONResponse(content={'error': '파일 업로드 오류: 보호 디렉토리입니다.'}, status_code=403)
  for file in files:
    file_location = os.path.join(PATH, file.filename)
    with open(file_location, 'wb') as f:
      f.write(await file.read())
  directory_data = read_directory(PATH)
  try:
    shutil.chown(PATH, user='pi', group='pi')
  except Exception as err:
    print(err)
  return JSONResponse(content={'message': '파일 업로드 완료', 'data': directory_data}, status_code=200)


@app.post('/show')
async def show_file(data: UploadFile = File(...)):
  try:
    tmp_path = '/home/pi/.tmp.jpg'
    with open(tmp_path, 'wb') as f:
      f.write(await data.read())
    with open(tmp_path, 'rb') as f:
      encoded_image = base64.b64encode(f.read()).decode('utf-8')
    return JSONResponse(content={'image': encoded_image, 'filepath': tmp_path})
  except Exception as err:
    return JSONResponse(content={'error': str(err)}, status_code=500)


@app.get('/tools')
async def tools_service(enable: str):
  if enable == 'on':
    subprocess.Popen(['systemctl', 'stop', 'classify.service'])
    subprocess.Popen(['systemctl', 'stop', 'llama-server.service'])
    subprocess.Popen(['systemctl', 'start', 'tools.service'])
  elif enable == 'off':
    subprocess.Popen(['systemctl', 'stop', 'tools.service'])
  return HTMLResponse(content='', status_code=200)


@app.get('/classifier')
async def classifier_service(enable: str):
  if enable == 'on':
    subprocess.Popen(['systemctl', 'stop', 'tools.service'])
    subprocess.Popen(['systemctl', 'stop', 'llama-server.service'])
    subprocess.Popen(['systemctl', 'start', 'classify.service'])
  elif enable == 'off':
    subprocess.Popen(['systemctl', 'stop', 'classify.service'])
  return HTMLResponse(content='', status_code=200)


@app.get('/llm')
async def llm_service(enable: str):
  if enable == 'on':
    subprocess.Popen(['systemctl', 'stop', 'tools.service'])
    subprocess.Popen(['systemctl', 'stop', 'classify.service'])
    subprocess.Popen(['systemctl', 'start', 'llama-server.service'])
  elif enable == 'off':
    subprocess.Popen(['systemctl', 'stop', 'llama-server.service'])
  await asyncio.sleep(2)
  return HTMLResponse(content='', status_code=200)


# ─── Periodic system status broadcast ─────────────────────────────────────────

async def periodic_system_update():
  while True:
    try:
      system_info = subprocess.check_output(
        ['/home/pi/openpibo-os/system/system.sh']
      ).decode().strip().split(',')
      await broadcast({'system': system_info})
    except Exception:
      pass
    try:
      battery = requests.get(
        'http://127.0.0.1:8080/device/%2315%3A%21', timeout=2
      ).json().split(':')[1]
      await broadcast({'battery': battery})
    except Exception:
      await broadcast({'battery': '0%'})
    try:
      dc = requests.get(
        'http://127.0.0.1:8080/device/%2314%3A%21', timeout=2
      ).json().split(':')[1]
      await broadcast({'dc': dc})
    except Exception:
      await broadcast({'dc': 'off'})
    await asyncio.sleep(10)


if __name__ == '__main__':
  import argparse
  import uvicorn

  parser = argparse.ArgumentParser()
  parser.add_argument('--port', help='set port number', default=80)
  args = parser.parse_args()

  uvicorn.run('run_ide:app', host='0.0.0.0', port=int(args.port), access_log=False)
