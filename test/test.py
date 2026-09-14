import os
import sys
import time
import json
import signal
import asyncio
from contextlib import asynccontextmanager

# --- FastAPI and Web Server Imports ---
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

# --- OpenPibo Hardware Imports ---
from openpibo.oled import Oled
from openpibo.audio import Audio
from openpibo.motion import Motion
from openpibo.device import Device
from openpibo.vision_camera import Camera

# ==============================================================================
# 0. IDLE WATCHDOG
# ==============================================================================
# 이 서버는 검수용이라 절대 남아 있으면 안 된다. 하드웨어(시리얼·카메라·오디오)를
# 붙잡고 있어서 IDE 의 코드 실행이나 tools 가 오동작한다.
#
# 종료 경로는 셋이고, 앞의 것이 실패해도 뒤에서 잡는다.
#   1. 검수 탭을 닫으면 beforeunload 가 /api/shutdown 을 부른다 (즉시)
#   2. 같은 beforeunload 가 IDE 의 /hwtest?enable=off 도 불러 프로세스를 죽인다
#   3. 그래도 살아 있으면, 아래 워치독이 마지막 heartbeat 로부터
#      IDLE_TIMEOUT 초 뒤에 스스로 내려간다 (탭 강제종료·태블릿 절전·전원 차단 대비)
#
# tools/classifier 에는 이런 유휴 타임아웃을 넣으면 안 된다(260909v5 에서 넣었다
# v6 에서 제거). 거기서는 학생이 잠깐 자리를 비운 것과 탭을 닫은 것을 구분하지
# 못해 돌아왔을 때 서비스가 죽어 있는 게 더 나쁘다. 검수 도구는 요구가 정반대다.
# 2분. 페이지는 30초마다 heartbeat 를 보내는데, 백그라운드 탭은 브라우저가
# 약 1분에 한 번으로 throttle 하므로 실제 최대 간격은 60초다. 여유가 2배라
# 자리 비움에는 안 죽지만, 네트워크가 한 번 끊기면 종료될 수 있다.
# 남아 있는 것보다 다시 켜는 쪽이 낫다는 판단이다.
IDLE_TIMEOUT = 120          # 초. heartbeat 가 이만큼 끊기면 종료한다
HEARTBEAT_CHECK = 10        # 초. 워치독이 확인하는 주기

last_beat = time.time()


def touch():
    global last_beat
    last_beat = time.time()


async def idle_watchdog():
    while True:
        await asyncio.sleep(HEARTBEAT_CHECK)
        idle = time.time() - last_beat
        if idle > IDLE_TIMEOUT:
            print(f"[watchdog] no heartbeat for {idle:.0f}s, shutting down.")
            os.kill(os.getpid(), signal.SIGTERM)
            return


@asynccontextmanager
async def lifespan(app: FastAPI):
    touch()
    task = asyncio.create_task(idle_watchdog())
    yield
    task.cancel()


# ==============================================================================
# 1. INITIALIZE FASTAPI APP AND HARDWARE
# ==============================================================================

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Initialize Hardware Objects (globally, once) ---
try:
    oled_obj = Oled()
    audio_obj = Audio()
    motion_obj = Motion()
    device_obj = Device()
    camera_obj = Camera()
    os.system('sudo /home/pi/.pyenv/bin/python3 /home/pi/openpibo-os/system/network_disp.py')
except Exception as e:
    print(f"Error initializing hardware: {e}")
    oled_obj = audio_obj = motion_obj = device_obj = camera_obj = None

# ==============================================================================
# 2. HARDWARE CONTROL AND SYSTEM INFO FUNCTIONS
# ==============================================================================

# --- System Information Functions ---
def get_serial():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if line.startswith('Serial'):
                    return line.split(':')[1].strip()
    except Exception:
        return "N/A"

def get_fw():
    try:
        data = device_obj.send_raw("#10:!")
        return data.split(":")[1]
    except Exception:
        return "N/A"

def get_os():
    try:
        return os.popen('cat /home/pi/.OS_VERSION').read().strip()
    except Exception:
        return "N/A"

def get_memory():
    try:
        data = os.popen("vcgencmd get_config total_mem").read().strip()
        mem_gb = int(data.split("=")[1]) / 1024
        return f"{mem_gb:.1f} GB"
    except Exception:
        return "N/A"

def get_board():
    try:
        # /proc/device-tree/* 는 NUL 종료 문자열이라 strip() 으로는 안 지워진다.
        # 그대로 두면 보고서에 "Rev 1.4\x00" 이 네모 기호로 찍힌다.
        return os.popen('cat /proc/device-tree/model').read().replace('\x00', '').strip()
    except Exception:
        return "N/A"

# --- Hardware Test Functions ---
def oled_test():
    oled_obj.set_font(size=30)
    oled_obj.clear()
    oled_obj.draw_text((0, 0), "Oled")
    oled_obj.draw_text((0, 30), "Testing...")
    oled_obj.show()
    time.sleep(2)
    oled_obj.clear()
    oled_obj.show()
    os.system('sudo /home/pi/.pyenv/bin/python3 /home/pi/openpibo-os/system/network_disp.py')
    return {"status": "OLED test executed"}

def audio_test():
    audio_file = "/home/pi/openpibo-files/audio/effect/opening.mp3"
    if os.path.exists(audio_file):
        audio_obj.play(filename=audio_file, volume=80)
        time.sleep(5)
        audio_obj.stop()
        return {"status": "Audio test executed"}
    else:
        raise HTTPException(status_code=404, detail=f"Audio file not found: {audio_file}")

def motor_test():
    motion_obj.set_motors([0]*10)
    time.sleep(1)
    for i in range(10):
        motion_obj.set_speed(i, 30)
        motion_obj.set_acceleration(i, 0)
        motion_obj.set_motor(i, 10)
        time.sleep(0.3)
        motion_obj.set_motor(i, -10)
        time.sleep(0.3)
        motion_obj.set_motor(i, 0)
        time.sleep(0.5)
    return {"status": "Motor test executed"}

def mic_test():
    try:
        audio_obj.record(filename="stream.wav", timeout=5)
        audio_obj.play(filename="stream.wav", volume=100, background=False)
        return {"status": "Mic test executed"}
    finally:
        if os.path.exists("stream.wav"):
            os.remove("stream.wav")

def camera_test():
    img_path = "/tmp/pibo_capture.jpg"
    try:
        frame = camera_obj.read()
        camera_obj.imwrite(img_path, frame)
        return FileResponse(img_path, media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Camera capture failed: {e}")

def neopixel_test():
    device_obj.send_raw("#20:255,0,0!")
    time.sleep(0.3)
    device_obj.send_raw("#20:0,255,0!")
    time.sleep(0.3)
    device_obj.send_raw("#20:0,0,255!")
    time.sleep(0.3)
    device_obj.send_raw("#20:0,0,0!")
    return {"status": "Neopixel test executed"}

def battery_test():
    data = device_obj.send_cmd(Device.code_list['BATTERY']).split(":")[1]
    return {"battery_status": data}

async def system_stream_generator():
    """
    A generator that yields system status data in the SSE format.
    Format: "data: <json_string>\n\n"
    """
    device_obj.send_cmd(Device.code_list['PIR'], "on")
    for i in range(20):
        touch()   # 센서 스트림이 도는 동안에는 워치독이 끼어들지 않게 한다
        data = device_obj.send_cmd(Device.code_list['SYSTEM']).split(':')[1].split('-')

        # Safely get data from the split list
        pir = data[0] if len(data) > 0 and data[0] else "nobody"
        touch_v = data[1] if len(data) > 1 and data[1] else "No signal"
        dc = data[2] if len(data) > 2 and data[2] else "No signal"
        button = data[3] if len(data) > 3 and data[3] else "No signal"

        response_data = {
            "pir": pir,
            "touch": touch_v,
            "dc": dc,
            "button": button,
            "count": i + 1
        }
        # Manually format the data for SSE
        yield f"data: {json.dumps(response_data)}\n\n"
        await asyncio.sleep(1)
    device_obj.send_cmd(Device.code_list['PIR'], "off")


# ==============================================================================
# 3. API ENDPOINTS
# ==============================================================================

# Map test names to functions
TEST_FUNCTIONS = {
    "oled": oled_test,
    "audio": audio_test,
    "motor": motor_test,
    "mic": mic_test,
    "neopixel": neopixel_test,
    "battery": battery_test,
}

@app.get("/api/ping")
async def ping():
    """검수 페이지가 열려 있다는 신호. 끊기면 워치독이 서버를 내린다."""
    touch()
    return {"idle_timeout": IDLE_TIMEOUT}

@app.post("/api/shutdown")
async def shutdown():
    """검수 탭이 닫힐 때 호출된다. 서버만 종료하고 기기는 그대로 둔다."""
    async def _later():
        await asyncio.sleep(0.3)   # 응답을 보내고 나서 죽는다
        os.kill(os.getpid(), signal.SIGTERM)
    asyncio.create_task(_later())
    return {"message": "Inspection server is shutting down."}

@app.get("/api/system-info")
async def get_system_info():
    """Returns a JSON object with all system hardware/software details."""
    touch()
    return {
        "serial": get_serial(),
        "firmware": get_fw(),
        "os_version": get_os(),
        "board": get_board(),
        "memory": get_memory(),
    }

@app.post("/api/test/{test_name}")
async def run_test(test_name: str):
    """Runs a standard hardware test."""
    touch()
    if test_name not in TEST_FUNCTIONS:
        raise HTTPException(status_code=404, detail="Test not found")

    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, TEST_FUNCTIONS[test_name])
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        touch()   # 모터 검사처럼 오래 걸리는 항목 뒤에도 유휴로 오해하지 않게 한다

@app.get("/api/test/camera")
async def run_camera_test():
    """Handles the camera test specifically to return an image file."""
    touch()
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, camera_test)

@app.get("/api/test/system")
async def run_system_test_stream():
    """Streams system sensor data using FastAPI's native StreamingResponse."""
    touch()
    return StreamingResponse(system_stream_generator(), media_type="text/event-stream")

@app.post("/api/halt")
async def halt_system():
    """Shuts down the Raspberry Pi."""
    oled_obj.draw_text((10, 25), "Shutting down...")
    oled_obj.show()
    os.system('echo "#11:!" > /dev/ttyS0')
    os.system('sudo shutdown -h now &')
    return {"message": "System is shutting down."}

@app.get("/")
async def read_root():
    touch()
    return FileResponse(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html'))

# ==============================================================================
# 4. RUN THE SERVER
# ==============================================================================

if __name__ == "__main__":
    if any(obj is None for obj in [oled_obj, audio_obj, motion_obj, device_obj, camera_obj]):
        print("\nWARNING: One or more hardware components failed to initialize.")
        print("The API will run, but hardware-related endpoints may fail.")

    print("\nStarting OpenPibo Web Test Interface.")
    print("Access the frontend at http://<your-robot-ip>:8000/ in your browser.")
    print(f"Idle watchdog: shuts down after {IDLE_TIMEOUT}s without a heartbeat.")

    uvicorn.run(app, host="0.0.0.0", port=8000)
