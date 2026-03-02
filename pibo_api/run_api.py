"""
pibo REST API Server
Exposes all openpibo package features as REST API endpoints.

Run: uvicorn run_api:app --host 0.0.0.0 --port 9000
  or: python run_api.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Request, UploadFile, File, Body
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Optional, List
from pydantic import BaseModel

import asyncio, base64, json, logging, time
import numpy as np
import cv2
import argparse


# ── Module singletons ──────────────────────────────────────────────────────────
_audio    = None
_device   = None
_motion   = None
_oled     = None
_speech   = None
_dialog   = None
_camera   = None
_detect   = None
_face     = None
_classify = None

def get_audio():
    global _audio
    if _audio is None:
        from openpibo.audio import Audio
        _audio = Audio()
    return _audio

def get_device():
    global _device
    if _device is None:
        from openpibo.device import Device
        _device = Device()
    return _device

def get_motion():
    global _motion
    if _motion is None:
        from openpibo.motion import Motion
        _motion = Motion()
    return _motion

def get_oled():
    global _oled
    if _oled is None:
        from openpibo.oled import Oled
        _oled = Oled()
    return _oled

def get_speech():
    global _speech
    if _speech is None:
        from openpibo.speech import Speech
        _speech = Speech()
    return _speech

def get_dialog():
    global _dialog
    if _dialog is None:
        from openpibo.speech import Dialog
        _dialog = Dialog()
    return _dialog

def get_camera():
    global _camera
    if _camera is None:
        from openpibo.vision_camera import Camera
        _camera = Camera()
    return _camera

def get_detect():
    global _detect
    if _detect is None:
        from openpibo.vision_detect import Detect
        _detect = Detect()
    return _detect

def get_face():
    global _face
    if _face is None:
        from openpibo.vision_face import Face
        _face = Face()
    return _face

def get_classify():
    global _classify
    if _classify is None:
        from openpibo.vision_classify import TeachableMachine
        _classify = TeachableMachine()
    return _classify


# ── Image helpers ──────────────────────────────────────────────────────────────
def b64_to_img(b64: str) -> np.ndarray:
    """Decode base64 string to numpy BGR image."""
    data = base64.b64decode(b64)
    arr  = np.frombuffer(data, np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)

def img_to_b64(img: np.ndarray, fmt: str = '.jpg') -> str:
    """Encode numpy BGR image to base64 string."""
    _, buf = cv2.imencode(fmt, img)
    return base64.b64encode(buf.tobytes()).decode()

def ok(data=None):
    body = {'result': 'ok'}
    if data is not None:
        body['data'] = data
    return JSONResponse(content=body)

def err(msg: str, status: int = 400):
    return JSONResponse(content={'result': 'error', 'message': str(msg)}, status_code=status)


# ── SSE camera stream ──────────────────────────────────────────────────────────
_camera_stream_active = False
_last_frame_b64: Optional[str] = None

def camera_loop():
    global _last_frame_b64, _camera_stream_active
    cam = get_camera()
    while _camera_stream_active:
        try:
            img = cam.read()
            if img is not None:
                _last_frame_b64 = img_to_b64(img)
        except Exception:
            pass
        time.sleep(0.1)


# ── App lifecycle ──────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(level=logging.ERROR,
                        format='%(asctime)s [%(levelname)s] %(message)s')
    yield

app = FastAPI(
    title='pibo REST API',
    description='REST API exposing all openpibo package features',
    version='1.0.0',
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'], allow_credentials=True,
    allow_methods=['*'], allow_headers=['*'],
)


# ══════════════════════════════════════════════════════════════════════════════
# AUDIO
# ══════════════════════════════════════════════════════════════════════════════

class AudioPlayBody(BaseModel):
    filename: str
    volume: int = 80
    background: bool = True
    volume2: float = 1.0

class AudioRecordBody(BaseModel):
    filename: str = '/tmp/record.wav'
    timeout: int = 5
    verbose: bool = True

@app.post('/api/audio/play', tags=['audio'], summary='Play audio file')
async def audio_play(body: AudioPlayBody):
    """Play an mp3 or wav file. volume: 0-100, background: run in background."""
    try:
        get_audio().play(body.filename, body.volume, body.background, body.volume2)
        return ok()
    except Exception as e:
        return err(e)

@app.post('/api/audio/stop', tags=['audio'], summary='Stop audio playback')
async def audio_stop():
    """Stop currently playing audio."""
    try:
        get_audio().stop()
        return ok()
    except Exception as e:
        return err(e)

@app.post('/api/audio/record', tags=['audio'], summary='Record from microphone')
async def audio_record(body: AudioRecordBody):
    """Record audio from microphone and save to file. timeout: seconds."""
    try:
        get_audio().record(body.filename, body.timeout, body.verbose)
        return ok({'filename': body.filename})
    except Exception as e:
        return err(e)


# ══════════════════════════════════════════════════════════════════════════════
# COLLECT
# ══════════════════════════════════════════════════════════════════════════════

class WikiBody(BaseModel):
    text: str
    simple: bool = False

class WeatherBody(BaseModel):
    region: str = '전국'
    simple: bool = False
    search_type: str = 'forecast'
    search_item: str = 'weather'

class NewsBody(BaseModel):
    topic: str = '뉴스랭킹'
    simple: bool = False
    search_type: str = 'title'

@app.post('/api/collect/wikipedia', tags=['collect'], summary='Search Wikipedia')
async def collect_wikipedia(body: WikiBody):
    """Search Wikipedia for text.
    simple=false returns chapter dict, simple=true returns list of strings."""
    try:
        from openpibo.collect import Wikipedia
        wiki = Wikipedia()
        if body.simple:
            result = wiki.search_s(body.text)
        else:
            result = wiki.search(body.text)
        return ok(result)
    except Exception as e:
        return err(e)

@app.post('/api/collect/weather', tags=['collect'], summary='Get weather info')
async def collect_weather(body: WeatherBody):
    """Get weather information for a Korean region.
    Regions: 전국, 서울, 인천, 경기, 부산, 울산, 경남, 대구, 경북, 광주, 전남, 전북, 대전, 세종, 충남, 충북, 강원, 제주
    simple=true: specify search_type (forecast/today/tomorrow/after_tomorrow) and search_item (weather/minimum_temp/highst_temp)"""
    try:
        from openpibo.collect import Weather
        w = Weather()
        if body.simple:
            result = w.search_s(body.region, body.search_type, body.search_item)
        else:
            result = w.search(body.region)
        return ok(result)
    except Exception as e:
        return err(e)

@app.post('/api/collect/news', tags=['collect'], summary='Get news articles')
async def collect_news(body: NewsBody):
    """Get news from JTBC RSS.
    Topics: 속보, 정치, 경제, 사회, 국제, 문화, 연예, 스포츠, 뉴스랭킹, 뉴스룸 ...
    simple=true: specify search_type (title/link/description)"""
    try:
        from openpibo.collect import News
        n = News()
        if body.simple:
            result = n.search_s(body.topic, body.search_type)
        else:
            result = n.search(body.topic)
        return ok(result)
    except Exception as e:
        return err(e)


# ══════════════════════════════════════════════════════════════════════════════
# DEVICE
# ══════════════════════════════════════════════════════════════════════════════

class EyeOnBody(BaseModel):
    colors: list         # [R,G,B] or [R,G,B,R,G,B] or ['#rrggbb','#rrggbb']
    hex: bool = False    # True if colors are hex strings
    intv: int = 0        # Fade interval

class DeviceCmdBody(BaseModel):
    code: str
    data: str = ''

@app.post('/api/device/cmd', tags=['device'], summary='Send raw device command')
async def device_cmd(body: DeviceCmdBody):
    """Send command to device board. code can be numeric (e.g. '20') or name."""
    try:
        result = get_device().send_cmd(body.code, body.data)
        return ok({'response': result})
    except Exception as e:
        return err(e)

@app.post('/api/device/eye/on', tags=['device'], summary='Turn on LED eyes')
async def device_eye_on(body: EyeOnBody):
    """Turn on LED eyes.
    colors: [R,G,B] for both eyes, [R,G,B,R,G,B] for separate.
    hex=true: colors is ['#rrggbb','#rrggbb'].
    intv: fade interval (0=instant)."""
    try:
        dev = get_device()
        if body.hex:
            result = dev.eye_on_s(body.colors, body.intv)
        else:
            result = dev.eye_on(*body.colors, intv=body.intv)
        return ok({'response': result})
    except Exception as e:
        return err(e)

@app.post('/api/device/eye/off', tags=['device'], summary='Turn off LED eyes')
async def device_eye_off():
    """Turn off LED eyes."""
    try:
        result = get_device().eye_off()
        return ok({'response': result})
    except Exception as e:
        return err(e)

@app.get('/api/device/battery', tags=['device'], summary='Get battery status')
async def device_battery(v: bool = False):
    """Get battery status. v=true returns only the value."""
    try:
        result = get_device().get_battery(v)
        return ok({'battery': result})
    except Exception as e:
        return err(e)

@app.get('/api/device/dc', tags=['device'], summary='Get DC connector status')
async def device_dc(v: bool = False):
    """Get DC connector status. v=true returns only the value."""
    try:
        result = get_device().get_dc(v)
        return ok({'dc': result})
    except Exception as e:
        return err(e)

@app.get('/api/device/system', tags=['device'], summary='Get system message')
async def device_system(v: bool = False):
    """Get system message from device. v=true returns only the value."""
    try:
        result = get_device().get_system(v)
        return ok({'system': result})
    except Exception as e:
        return err(e)

@app.get('/api/device/pir', tags=['device'], summary='Get PIR sensor value')
async def device_pir():
    """Get PIR (motion) sensor value."""
    try:
        result = get_device().get_pir()
        return ok({'pir': result})
    except Exception as e:
        return err(e)

@app.get('/api/device/touch', tags=['device'], summary='Get touch sensor value')
async def device_touch():
    """Get touch sensor value."""
    try:
        result = get_device().get_touch()
        return ok({'touch': result})
    except Exception as e:
        return err(e)

@app.get('/api/device/button', tags=['device'], summary='Get button value')
async def device_button():
    """Get button press value."""
    try:
        result = get_device().get_button()
        return ok({'button': result})
    except Exception as e:
        return err(e)


# ══════════════════════════════════════════════════════════════════════════════
# MOTION
# ══════════════════════════════════════════════════════════════════════════════

class MotorBody(BaseModel):
    n: int           # Motor index 0-9
    pos: int         # Position -80~80

class MotorsBody(BaseModel):
    positions: List[int]      # 10 positions
    movetime: Optional[int] = None  # milliseconds (in 50ms units)

class SpeedBody(BaseModel):
    n: int
    speed: int       # 0-255

class SpeedsBody(BaseModel):
    speeds: List[int]  # 10 speed values

class AccelBody(BaseModel):
    n: int
    accel: int       # 0-255

class AccelsBody(BaseModel):
    accels: List[int]  # 10 accel values

class MotionPlayBody(BaseModel):
    name: str
    cycle: int = 1
    path: Optional[str] = None

class MotionRawBody(BaseModel):
    exe: dict
    cycle: int = 1

@app.get('/api/motion/list', tags=['motion'], summary='Get motion list or data')
async def motion_list(name: Optional[str] = None, path: Optional[str] = None):
    """Get list of available motions (name=None) or specific motion data."""
    try:
        result = get_motion().get_motion(name, path)
        return ok(result)
    except Exception as e:
        return err(e)

@app.post('/api/motion/motor', tags=['motion'], summary='Move single motor')
async def motion_motor(body: MotorBody):
    """Move single motor (n: 0-9) to position (pos: -80~80)."""
    try:
        get_motion().set_motor(body.n, body.pos)
        return ok()
    except Exception as e:
        return err(e)

@app.post('/api/motion/motors', tags=['motion'], summary='Move all motors')
async def motion_motors(body: MotorsBody):
    """Move all 10 motors to specified positions. movetime in ms (50ms units)."""
    try:
        get_motion().set_motors(body.positions, body.movetime)
        return ok()
    except Exception as e:
        return err(e)

@app.post('/api/motion/speed', tags=['motion'], summary='Set motor speed')
async def motion_speed(body: SpeedBody):
    """Set speed of single motor (0=slowest, 255=fastest)."""
    try:
        get_motion().set_speed(body.n, body.speed)
        return ok()
    except Exception as e:
        return err(e)

@app.post('/api/motion/speeds', tags=['motion'], summary='Set all motor speeds')
async def motion_speeds(body: SpeedsBody):
    """Set speed for all 10 motors."""
    try:
        get_motion().set_speeds(body.speeds)
        return ok()
    except Exception as e:
        return err(e)

@app.post('/api/motion/acceleration', tags=['motion'], summary='Set motor acceleration')
async def motion_acceleration(body: AccelBody):
    """Set acceleration for single motor (0-255)."""
    try:
        get_motion().set_acceleration(body.n, body.accel)
        return ok()
    except Exception as e:
        return err(e)

@app.post('/api/motion/accelerations', tags=['motion'], summary='Set all motor accelerations')
async def motion_accelerations(body: AccelsBody):
    """Set acceleration for all 10 motors."""
    try:
        get_motion().set_accelerations(body.accels)
        return ok()
    except Exception as e:
        return err(e)

@app.post('/api/motion/play', tags=['motion'], summary='Play named motion')
async def motion_play(body: MotionPlayBody):
    """Execute a named motion from profile. cycle: repetition count."""
    try:
        get_motion().set_motion(body.name, body.cycle, body.path)
        return ok()
    except Exception as e:
        return err(e)

@app.post('/api/motion/play/raw', tags=['motion'], summary='Play raw motion data')
async def motion_play_raw(body: MotionRawBody):
    """Execute raw motion data dict. cycle: repetition count."""
    try:
        get_motion().set_motion_raw(body.exe, body.cycle)
        return ok()
    except Exception as e:
        return err(e)

@app.post('/api/motion/stop', tags=['motion'], summary='Stop motion')
async def motion_stop():
    """Stop currently executing motion."""
    try:
        get_motion().stop()
        return ok()
    except Exception as e:
        return err(e)


# ══════════════════════════════════════════════════════════════════════════════
# OLED
# ══════════════════════════════════════════════════════════════════════════════

class OledTextBody(BaseModel):
    x: int
    y: int
    text: str
    font: Optional[str] = None
    size: Optional[int] = None

class OledImageBody(BaseModel):
    filename: str

class OledDataBody(BaseModel):
    image_b64: str  # base64-encoded image

class OledRectBody(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int
    fill: Optional[bool] = None

class OledEllipseBody(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int
    fill: Optional[bool] = None

class OledLineBody(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int

class OledClearBody(BaseModel):
    image: bool = True
    fill: bool = True
    show: bool = True

@app.post('/api/oled/show', tags=['oled'], summary='Show OLED display')
async def oled_show():
    """Flush image buffer to OLED screen."""
    try:
        get_oled().show()
        return ok()
    except Exception as e:
        return err(e)

@app.post('/api/oled/clear', tags=['oled'], summary='Clear OLED display')
async def oled_clear(body: OledClearBody):
    """Clear OLED screen and/or buffer."""
    try:
        get_oled().clear(body.image, body.fill, body.show)
        return ok()
    except Exception as e:
        return err(e)

@app.post('/api/oled/text', tags=['oled'], summary='Draw text on OLED')
async def oled_text(body: OledTextBody):
    """Draw text at (x,y). Optionally set font and size before drawing."""
    try:
        oled = get_oled()
        if body.font or body.size:
            oled.set_font(body.font, body.size)
        oled.draw_text((body.x, body.y), body.text)
        oled.show()
        return ok()
    except Exception as e:
        return err(e)

@app.post('/api/oled/image', tags=['oled'], summary='Draw image file on OLED')
async def oled_image(body: OledImageBody):
    """Draw PNG image file on OLED (128x64 recommended)."""
    try:
        oled = get_oled()
        oled.draw_image(body.filename)
        oled.show()
        return ok()
    except Exception as e:
        return err(e)

@app.post('/api/oled/image/upload', tags=['oled'], summary='Upload and draw image on OLED')
async def oled_image_upload(file: UploadFile = File(...)):
    """Upload and display an image on OLED."""
    try:
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp.write(await file.read())
            tmppath = tmp.name
        oled = get_oled()
        oled.draw_image(tmppath)
        oled.show()
        os.unlink(tmppath)
        return ok()
    except Exception as e:
        return err(e)

@app.post('/api/oled/data', tags=['oled'], summary='Draw base64 image data on OLED')
async def oled_data(body: OledDataBody):
    """Draw base64-encoded image data on OLED."""
    try:
        img = b64_to_img(body.image_b64)
        get_oled().draw_data(img)
        get_oled().show()
        return ok()
    except Exception as e:
        return err(e)

@app.post('/api/oled/rectangle', tags=['oled'], summary='Draw rectangle on OLED')
async def oled_rectangle(body: OledRectBody):
    """Draw rectangle from (x1,y1) to (x2,y2). fill=true fills it."""
    try:
        get_oled().draw_rectangle((body.x1, body.y1, body.x2, body.y2), body.fill)
        get_oled().show()
        return ok()
    except Exception as e:
        return err(e)

@app.post('/api/oled/ellipse', tags=['oled'], summary='Draw ellipse on OLED')
async def oled_ellipse(body: OledEllipseBody):
    """Draw ellipse from (x1,y1) to (x2,y2). fill=true fills it."""
    try:
        get_oled().draw_ellipse((body.x1, body.y1, body.x2, body.y2), body.fill)
        get_oled().show()
        return ok()
    except Exception as e:
        return err(e)

@app.post('/api/oled/line', tags=['oled'], summary='Draw line on OLED')
async def oled_line(body: OledLineBody):
    """Draw line from (x1,y1) to (x2,y2)."""
    try:
        get_oled().draw_line((body.x1, body.y1, body.x2, body.y2))
        get_oled().show()
        return ok()
    except Exception as e:
        return err(e)

@app.post('/api/oled/invert', tags=['oled'], summary='Invert OLED colors')
async def oled_invert():
    """Invert OLED screen colors."""
    try:
        get_oled().invert()
        return ok()
    except Exception as e:
        return err(e)


# ══════════════════════════════════════════════════════════════════════════════
# SPEECH
# ══════════════════════════════════════════════════════════════════════════════

class TtsBody(BaseModel):
    text: str
    filename: str = '/tmp/tts.mp3'
    voice: str = 'main'
    lang: str = 'ko'
    play: bool = True  # auto-play after TTS

class SttBody(BaseModel):
    filename: str = '/tmp/stream.wav'
    timeout: int = 5
    verbose: bool = True

class DialogBody(BaseModel):
    question: str

class TranslateBody(BaseModel):
    text: str
    target: str = 'en'

class DialogLoadBody(BaseModel):
    filepath: str

class NlpBody(BaseModel):
    text: str
    mode: str  # summary, vector, sentiment, emotion, ner, wellness, hate

class LlmBody(BaseModel):
    prompt: Optional[str] = None
    system_prompt: Optional[str] = None
    temperature: float = 0.8
    max_tokens: int = 100

@app.post('/api/speech/tts', tags=['speech'], summary='Text-to-Speech')
async def speech_tts(body: TtsBody):
    """Convert text to speech and optionally play it.
    voices: espeak, gtts, e_gtts, main, boy, girl, man1, woman1
    lang: ko, en"""
    try:
        get_speech().tts(body.text, body.filename, body.voice, body.lang)
        if body.play:
            get_audio().play(body.filename)
        return ok({'filename': body.filename})
    except Exception as e:
        return err(e)

@app.post('/api/speech/stt', tags=['speech'], summary='Speech-to-Text')
async def speech_stt(body: SttBody):
    """Record audio and convert to text. timeout: seconds to record."""
    try:
        result = get_speech().stt(body.filename, body.timeout, body.verbose)
        return ok({'text': result})
    except Exception as e:
        return err(e)

@app.post('/api/speech/dialog', tags=['speech'], summary='Get dialog response')
async def speech_dialog(body: DialogBody):
    """Get a response for a question from the dialog database."""
    try:
        result = get_dialog().get_dialog(body.question)
        return ok({'answer': result})
    except Exception as e:
        return err(e)

@app.post('/api/speech/dialog/load', tags=['speech'], summary='Load dialog CSV file')
async def speech_dialog_load(body: DialogLoadBody):
    """Load dialog data from a CSV file (format: question,answer)."""
    try:
        get_dialog().load(body.filepath)
        return ok()
    except Exception as e:
        return err(e)

@app.post('/api/speech/dialog/reset', tags=['speech'], summary='Reset dialog to default')
async def speech_dialog_reset():
    """Reset dialog database to default data."""
    try:
        get_dialog().reset()
        return ok()
    except Exception as e:
        return err(e)

@app.post('/api/speech/translate', tags=['speech'], summary='Translate text')
async def speech_translate(body: TranslateBody):
    """Translate text to target language."""
    try:
        result = get_dialog().translate(body.text, body.target)
        return ok({'result': result})
    except Exception as e:
        return err(e)

@app.post('/api/speech/nlp', tags=['speech'], summary='NLP analysis')
async def speech_nlp(body: NlpBody):
    """Analyze text with deep learning.
    modes: summary, vector, sentiment, emotion, ner, wellness, hate"""
    try:
        result = get_dialog().nlp_dl(body.text, body.mode)
        return ok(result)
    except Exception as e:
        return err(e)

@app.post('/api/speech/llm', tags=['speech'], summary='Call LLM')
async def speech_llm(body: LlmBody):
    """Call LLM server with a prompt."""
    try:
        result = get_dialog().call_llm(
            body.prompt, body.system_prompt, body.temperature, body.max_tokens
        )
        return ok({'response': result})
    except Exception as e:
        return err(e)


# ══════════════════════════════════════════════════════════════════════════════
# CAMERA
# ══════════════════════════════════════════════════════════════════════════════

class CameraFilterBody(BaseModel):
    image_b64: Optional[str] = None  # input image; if None, capture from camera
    filter: str = 'none'             # none, stylization, detail, pencil, edge, flip
    flip_flags: int = 1              # for flip: 0=vertical,1=horizontal,-1=both
    degree: int = 10                 # for rotate
    scale: float = 0.9              # for rotate

@app.get('/api/camera/capture', tags=['camera'], summary='Capture single frame')
async def camera_capture(format: str = 'jpg'):
    """Capture a single frame from camera. Returns base64-encoded image."""
    try:
        img = get_camera().read()
        b64 = img_to_b64(img, f'.{format}')
        return ok({'image': b64, 'format': format})
    except Exception as e:
        return err(e)

@app.post('/api/camera/filter', tags=['camera'], summary='Apply image filter')
async def camera_filter(body: CameraFilterBody):
    """Apply a visual filter to camera capture or provided image.
    filters: stylization, detail, pencil, edge, flip, rotate"""
    try:
        cam = get_camera()
        if body.image_b64:
            img = b64_to_img(body.image_b64)
        else:
            img = cam.read()

        f = body.filter
        if f == 'stylization':
            out = cam.stylization(img)
        elif f == 'detail':
            out = cam.detailEnhance(img)
        elif f == 'pencil':
            _, out = cam.pencilSketch(img)
        elif f == 'edge':
            out = cam.edgePreservingFilter(img)
        elif f == 'flip':
            out = cam.flip(img, body.flip_flags)
        elif f == 'rotate':
            out = cam.rotate(img, body.degree, body.scale)
        else:
            out = img

        return ok({'image': img_to_b64(out)})
    except Exception as e:
        return err(e)

@app.get('/api/camera/stream', tags=['camera'], summary='MJPEG camera stream (SSE)')
async def camera_stream(request: Request):
    """Stream camera frames as SSE events with base64-encoded JPEG data."""
    global _camera_stream_active, _last_frame_b64
    import threading
    if not _camera_stream_active:
        _camera_stream_active = True
        t = threading.Thread(target=camera_loop, daemon=True)
        t.start()

    async def generate():
        global _camera_stream_active
        try:
            while True:
                if await request.is_disconnected():
                    break
                if _last_frame_b64:
                    data = json.dumps({'image': _last_frame_b64})
                    yield f'data: {data}\n\n'
                await asyncio.sleep(0.1)
        finally:
            pass

    return StreamingResponse(
        generate(),
        media_type='text/event-stream',
        headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'},
    )

@app.post('/api/camera/stream/stop', tags=['camera'], summary='Stop camera stream')
async def camera_stream_stop():
    """Stop the background camera capture loop."""
    global _camera_stream_active
    _camera_stream_active = False
    return ok()


# ══════════════════════════════════════════════════════════════════════════════
# VISION - DETECT
# ══════════════════════════════════════════════════════════════════════════════

class DetectBody(BaseModel):
    image_b64: Optional[str] = None   # base64 image; if None, capture from camera
    draw: bool = False                 # return annotated image

class TrackerInitBody(BaseModel):
    image_b64: Optional[str] = None
    x1: int
    y1: int
    x2: int
    y2: int

class MarkerBody(BaseModel):
    image_b64: Optional[str] = None
    marker_length: int = 2
    draw: bool = False

def _get_img(b64: Optional[str]) -> np.ndarray:
    if b64:
        return b64_to_img(b64)
    return get_camera().read()

@app.post('/api/vision/detect/object', tags=['vision-detect'], summary='Detect objects')
async def vision_detect_object(body: DetectBody):
    """Detect objects in image using YOLO model. Returns list of detections."""
    try:
        det = get_detect()
        img = _get_img(body.image_b64)
        items = det.detect_object(img)
        result: dict = {'items': items}
        if body.draw:
            out = det.detect_object_vis(img, items)
            result['image'] = img_to_b64(out)
        return ok(result)
    except Exception as e:
        return err(e)

@app.post('/api/vision/detect/qr', tags=['vision-detect'], summary='Detect QR/barcodes')
async def vision_detect_qr(body: DetectBody):
    """Detect QR codes and barcodes in image."""
    try:
        det = get_detect()
        img = _get_img(body.image_b64)
        items = det.detect_qr(img)
        result: dict = {'items': items}
        if body.draw:
            out = det.detect_qr_vis(img, items)
            result['image'] = img_to_b64(out)
        return ok(result)
    except Exception as e:
        return err(e)

@app.post('/api/vision/detect/pose', tags=['vision-detect'], summary='Detect body pose')
async def vision_detect_pose(body: DetectBody):
    """Detect body pose keypoints in image."""
    try:
        det = get_detect()
        img = _get_img(body.image_b64)
        items = det.detect_pose(img)
        result: dict = {'items': items}
        if items:
            result['analysis'] = det.analyze_pose(items)
        return ok(result)
    except Exception as e:
        return err(e)

@app.post('/api/vision/detect/marker', tags=['vision-detect'], summary='Detect ArUco markers')
async def vision_detect_marker(body: MarkerBody):
    """Detect ArUco markers in image. marker_length: physical size in cm."""
    try:
        det = get_detect()
        img = _get_img(body.image_b64)
        items = det.detect_marker(img, body.marker_length)
        result: dict = {'items': items}
        if body.draw:
            out = det.detect_marker_vis(img, items)
            result['image'] = img_to_b64(out)
        return ok(result)
    except Exception as e:
        return err(e)

@app.post('/api/vision/detect/gesture', tags=['vision-detect'], summary='Detect hand gestures')
async def vision_detect_gesture(body: DetectBody):
    """Detect hand gestures in image."""
    try:
        det = get_detect()
        img = _get_img(body.image_b64)
        items = det.recognize_hand_gesture(img)
        result: dict = {'items': items}
        if body.draw:
            out = det.recognize_hand_gesture_vis(img, items)
            result['image'] = img_to_b64(out)
        return ok(result)
    except Exception as e:
        return err(e)

@app.post('/api/vision/detect/tracker/init', tags=['vision-detect'], summary='Initialize object tracker')
async def vision_tracker_init(body: TrackerInitBody):
    """Initialize object tracker with bounding box (x1,y1,x2,y2)."""
    try:
        det = get_detect()
        img = _get_img(body.image_b64)
        det.object_tracker_init(img, (body.x1, body.y1, body.x2, body.y2))
        return ok()
    except Exception as e:
        return err(e)

@app.post('/api/vision/detect/tracker/update', tags=['vision-detect'], summary='Update object tracker')
async def vision_tracker_update(body: DetectBody):
    """Update object tracker with new frame. Returns current bounding box."""
    try:
        det = get_detect()
        img = _get_img(body.image_b64)
        bbox = det.track_object(img)
        result: dict = {'bbox': list(bbox) if bbox else None}
        if body.draw and bbox:
            out = det.track_object_vis(img, bbox)
            result['image'] = img_to_b64(out)
        return ok(result)
    except Exception as e:
        return err(e)


# ══════════════════════════════════════════════════════════════════════════════
# VISION - FACE
# ══════════════════════════════════════════════════════════════════════════════

class FaceTrainBody(BaseModel):
    image_b64: Optional[str] = None
    x1: int
    y1: int
    x2: int
    y2: int
    name: str

class FaceRecognizeBody(BaseModel):
    image_b64: Optional[str] = None
    x1: int
    y1: int
    x2: int
    y2: int

class FaceAnalyzeBody(BaseModel):
    image_b64: Optional[str] = None
    x1: int
    y1: int
    x2: int
    y2: int
    draw: bool = False

class FaceDbBody(BaseModel):
    filename: str

class FaceDeleteBody(BaseModel):
    name: str

@app.post('/api/vision/face/detect', tags=['vision-face'], summary='Detect faces')
async def vision_face_detect(body: DetectBody):
    """Detect faces in image. Returns list of (x1,y1,x2,y2) bounding boxes."""
    try:
        face = get_face()
        img = _get_img(body.image_b64)
        items = face.detect_face(img)
        result: dict = {'items': items}
        if body.draw:
            out = face.detect_face_vis(img, items)
            result['image'] = img_to_b64(out)
        return ok(result)
    except Exception as e:
        return err(e)

@app.post('/api/vision/face/analyze', tags=['vision-face'], summary='Analyze face')
async def vision_face_analyze(body: FaceAnalyzeBody):
    """Analyze face: returns age, gender, emotion."""
    try:
        face = get_face()
        img = _get_img(body.image_b64)
        item = (body.x1, body.y1, body.x2, body.y2)
        result_data = face.analyze_face(img, item)
        result: dict = {'analysis': result_data}
        if body.draw:
            out = face.analyze_face_vis(img, result_data)
            result['image'] = img_to_b64(out)
        return ok(result)
    except Exception as e:
        return err(e)

@app.post('/api/vision/face/train', tags=['vision-face'], summary='Register a face')
async def vision_face_train(body: FaceTrainBody):
    """Register/train a face with a name."""
    try:
        face = get_face()
        img = _get_img(body.image_b64)
        item = (body.x1, body.y1, body.x2, body.y2)
        result = face.train_face(img, item, body.name)
        return ok(result)
    except Exception as e:
        return err(e)

@app.post('/api/vision/face/recognize', tags=['vision-face'], summary='Recognize face')
async def vision_face_recognize(body: FaceRecognizeBody):
    """Recognize a registered face in image."""
    try:
        face = get_face()
        img = _get_img(body.image_b64)
        item = (body.x1, body.y1, body.x2, body.y2)
        result = face.recognize(img, item)
        return ok(result)
    except Exception as e:
        return err(e)

@app.post('/api/vision/face/delete', tags=['vision-face'], summary='Delete registered face')
async def vision_face_delete(body: FaceDeleteBody):
    """Delete a registered face from the database."""
    try:
        result = get_face().delete_face(body.name)
        return ok(result)
    except Exception as e:
        return err(e)

@app.get('/api/vision/face/db', tags=['vision-face'], summary='Get face database')
async def vision_face_db():
    """Get list of registered faces from database."""
    try:
        result = get_face().get_db()
        return ok({'db': result})
    except Exception as e:
        return err(e)

@app.post('/api/vision/face/db/init', tags=['vision-face'], summary='Initialize face database')
async def vision_face_db_init():
    """Initialize (clear) the face database."""
    try:
        result = get_face().init_db()
        return ok(result)
    except Exception as e:
        return err(e)

@app.post('/api/vision/face/db/save', tags=['vision-face'], summary='Save face database')
async def vision_face_db_save(body: FaceDbBody):
    """Save face database to file."""
    try:
        result = get_face().save_db(body.filename)
        return ok(result)
    except Exception as e:
        return err(e)

@app.post('/api/vision/face/db/load', tags=['vision-face'], summary='Load face database')
async def vision_face_db_load(body: FaceDbBody):
    """Load face database from file."""
    try:
        result = get_face().load_db(body.filename)
        return ok(result)
    except Exception as e:
        return err(e)

@app.post('/api/vision/face/mesh', tags=['vision-face'], summary='Detect face mesh')
async def vision_face_mesh(body: DetectBody):
    """Detect 3D face mesh landmarks."""
    try:
        face = get_face()
        img = _get_img(body.image_b64)
        items = face.detect_mesh(img)
        result: dict = {'items': items}
        if body.draw:
            out = face.detect_mesh_vis(img, items)
            result['image'] = img_to_b64(out)
        return ok(result)
    except Exception as e:
        return err(e)

@app.post('/api/vision/face/landmark', tags=['vision-face'], summary='Detect face landmarks')
async def vision_face_landmark(body: FaceAnalyzeBody):
    """Detect face landmarks (key points) for given face bbox."""
    try:
        face = get_face()
        img = _get_img(body.image_b64)
        item = (body.x1, body.y1, body.x2, body.y2)
        coords = face.landmark_face(img, item)
        result: dict = {'landmarks': coords}
        if body.draw:
            out = face.landmark_face_vis(img, coords)
            result['image'] = img_to_b64(out)
        return ok(result)
    except Exception as e:
        return err(e)


# ══════════════════════════════════════════════════════════════════════════════
# VISION - CLASSIFY
# ══════════════════════════════════════════════════════════════════════════════

class ClassifyLoadBody(BaseModel):
    model_path: str
    label_path: str

class ClassifyBody(BaseModel):
    image_b64: Optional[str] = None

@app.post('/api/vision/classify/load', tags=['vision-classify'], summary='Load classification model')
async def vision_classify_load(body: ClassifyLoadBody):
    """Load a TeachableMachine TFLite model on the AI-Core server."""
    try:
        get_classify().load(body.model_path, body.label_path)
        return ok()
    except Exception as e:
        return err(e)

@app.post('/api/vision/classify/predict', tags=['vision-classify'], summary='Classify image')
async def vision_classify_predict(body: ClassifyBody):
    """Classify image using loaded model. Returns class name and predictions."""
    try:
        img = _get_img(body.image_b64)
        class_name, predictions = get_classify().predict(img)
        return ok({'class': class_name, 'predictions': predictions})
    except Exception as e:
        return err(e)


# ══════════════════════════════════════════════════════════════════════════════
# HEALTH CHECK
# ══════════════════════════════════════════════════════════════════════════════

@app.get('/api/health', tags=['system'], summary='Health check')
async def health():
    """Check server is running."""
    return ok({'status': 'running'})

@app.get('/', tags=['system'], summary='API info')
async def root():
    return JSONResponse(content={
        'title': 'pibo REST API',
        'version': '1.0.0',
        'docs': '/docs',
        'redoc': '/redoc',
    })


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    import uvicorn
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=9000)
    args = parser.parse_args()
    uvicorn.run('run_api:app', host=args.host, port=args.port, reload=False)
