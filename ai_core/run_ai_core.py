import base64
import argparse
import logging
import json
import uvicorn
import numpy as np
import cv2

from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import Optional, Dict, Any

# vision core 라이브러리 임포트
# from openpibo.vision_camera_core import Camera
from openpibo.vision_face_core import Face
from openpibo.vision_detect_core import Detect
from openpibo.vision_classify_core import TeachableMachine, CustomClassifier
from openpibo.speech_core import SpeechOnDevice

# --- 기본 설정 ---
logging.basicConfig(level=logging.INFO)

# --- 전역 AI 모델 인스턴스 ---
# 서버 시작 시 이 변수들에 모델이 로드됩니다.
# pibo_camera: Camera = None
pibo_face: Face = None
pibo_detect: Detect = None
pibo_tm: TeachableMachine = None
pibo_cf: CustomClassifier = None
pibo_tts: SpeechOnDevice = None

# --- 상태 유지가 필요한 객체를 위한 전역 변수 ---
# 참고: 이 방식은 동시에 단 하나의 트래커만 지원합니다.
# 멀티 유저/세션을 지원하려면 세션 ID별로 트래커를 관리해야 합니다.
object_tracker = None

# --- FastAPI 생명주기 관리 ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    서버 시작 시 AI 모델을 로드하고, 종료 시 자원을 해제합니다.
    """
    global pibo_face, pibo_detect, pibo_tm, pibo_cf, pibo_tts
    
    logging.info("AI-Core is loading... This may take a moment.")
    
    # pibo_camera = Camera()
    pibo_face = Face()
    pibo_detect = Detect()
    pibo_tm = TeachableMachine()
    pibo_cf = CustomClassifier()
    pibo_tts = SpeechOnDevice()
    
    logging.info("AI-Core has been successfully loaded. Ready for requests.")
    
    yield
    
    # 서버 종료 시 카메라 자원 해제
    # if pibo_camera and hasattr(pibo_camera, 'release'):
    #     pibo_camera.release()
    logging.info("AI-Core is shutting down.")

# --- FastAPI 앱 초기화 ---
app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# --- 요청/응답 모델 및 Helper 함수 ---
class AIRequest(BaseModel):
    """모든 API 요청을 위한 표준 모델"""
    image: Optional[str] = None  # Base64 인코딩된 이미지 문자열
    params: Optional[Dict[str, Any]] = {}

class NumpyEncoder(json.JSONEncoder):
    """Numpy 객체를 JSON으로 직렬화하기 위한 커스텀 인코더"""
    def default(self, obj):
        if isinstance(obj, np.integer): return int(obj)
        if isinstance(obj, np.floating): return float(obj)
        if isinstance(obj, np.ndarray): return obj.tolist()
        return super(NumpyEncoder, self).default(obj)

def create_json_response(content):
    """NumpyEncoder를 사용하여 JSON 응답 생성"""
    return JSONResponse(content=json.loads(json.dumps(content, cls=NumpyEncoder)))

def b64_to_mat(b64_string: str) -> np.ndarray:
    """Base64 문자열을 OpenCV Mat 이미지로 디코딩"""
    if not b64_string: return None
    im_bytes = base64.b64decode(b64_string)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
    return cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

def mat_to_b64(mat: np.ndarray) -> str:
    """OpenCV Mat 이미지를 Base64 문자열로 인코딩"""
    if mat is None: return None
    _, buffer = cv2.imencode('.png', mat)
    return base64.b64encode(buffer).decode('utf-8')

def parse_colors(colors_param):
    """문자열 또는 튜플/리스트 형태의 색상 값을 튜플로 변환"""
    if isinstance(colors_param, str) and colors_param.startswith('#'):
        return (int(colors_param[5:7], 16), int(colors_param[3:5], 16), int(colors_param[1:3], 16))
    return tuple(colors_param)

# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"message": "OpenPibo AI-Core is running."}

# # --- Camera Endpoints ---
# @app.post("/camera/read")
# def camera_read():
#     img = pibo_camera.read()
#     return {"image": mat_to_b64(img)}

# @app.post("/camera/create_matte")
# def camera_create_matte(req: AIRequest):
#     p = req.params
#     img = pibo_camera.create_matte(parse_colors(p['colors']))
#     return {"image": mat_to_b64(img)}

# @app.post("/camera/resize")
# def camera_resize(req: AIRequest):
#     img = b64_to_mat(req.image)
#     p = req.params
#     result_img = pibo_camera.resize(img, p['w'], p['h'])
#     return {"image": mat_to_b64(result_img)}

# @app.post("/camera/rotate")
# def camera_rotate(req: AIRequest):
#     img = b64_to_mat(req.image)
#     p = req.params
#     result_img = pibo_camera.rotate(img, p['degree'], p['ratio'])
#     return {"image": mat_to_b64(result_img)}

# @app.post("/camera/imwrite")
# def camera_imwrite(req: AIRequest):
#     img = b64_to_mat(req.image)
#     p = req.params
#     result = pibo_camera.imwrite(p['filename'], img)
#     return {"data": result}

# @app.post("/camera/draw_bitmap")
# def camera_draw_bitmap(req: AIRequest):
#     p = req.params
#     img = pibo_camera.draw_bitmap(p['w'], p['h'], p['val'], parse_colors(p['background']), parse_colors(p['pixel']))
#     return {"image": mat_to_b64(img)}

# @app.post("/camera/rectangle")
# def camera_rectangle(req: AIRequest):
#     img = b64_to_mat(req.image)
#     p = req.params
#     result_img = pibo_camera.rectangle(img, tuple(p['p1']), tuple(p['p2']), parse_colors(p['colors']), p['tickness'])
#     return {"image": mat_to_b64(result_img)}

# @app.post("/camera/circle")
# def camera_circle(req: AIRequest):
#     img = b64_to_mat(req.image)
#     p = req.params
#     result_img = pibo_camera.circle(img, tuple(p['p']), p['r'], parse_colors(p['colors']), p['tickness'])
#     return {"image": mat_to_b64(result_img)}

# @app.post("/camera/line")
# def camera_line(req: AIRequest):
#     img = b64_to_mat(req.image)
#     p = req.params
#     result_img = pibo_camera.line(img, tuple(p['p1']), tuple(p['p2']), parse_colors(p['colors']), p['tickness'])
#     return {"image": mat_to_b64(result_img)}

# @app.post("/camera/putTextPIL")
# def camera_putTextPIL(req: AIRequest):
#     img = b64_to_mat(req.image)
#     p = req.params
#     result_img = pibo_camera.putTextPIL(img, p['text'], tuple(p['points']), p['size'], parse_colors(p['colors']))
#     return {"image": mat_to_b64(result_img)}

# @app.post("/camera/putText")
# def camera_putText(req: AIRequest):
#     img = b64_to_mat(req.image)
#     p = req.params
#     result_img = pibo_camera.putText(img, p['text'], tuple(p['points']), p['size'], parse_colors(p['colors']), p['tickness'])
#     return {"image": mat_to_b64(result_img)}

# @app.post("/camera/stylization")
# def camera_stylization(req: AIRequest):
#     img = b64_to_mat(req.image)
#     p = req.params
#     result_img = pibo_camera.stylization(img, p['sigma_s'], p['sigma_r'])
#     return {"image": mat_to_b64(result_img)}

# @app.post("/camera/detailEnhance")
# def camera_detailEnhance(req: AIRequest):
#     img = b64_to_mat(req.image)
#     p = req.params
#     result_img = pibo_camera.detailEnhance(img, p['sigma_s'], p['sigma_r'])
#     return {"image": mat_to_b64(result_img)}

# @app.post("/camera/pencilSketch")
# def camera_pencilSketch(req: AIRequest):
#     img = b64_to_mat(req.image)
#     p = req.params
#     gray_img, color_img = pibo_camera.pencilSketch(img, p['sigma_s'], p['sigma_r'], p['shade_factor'])
#     return {"image_gray": mat_to_b64(gray_img), "image_color": mat_to_b64(color_img)}

# @app.post("/camera/edgePreservingFilter")
# def camera_edgePreservingFilter(req: AIRequest):
#     img = b64_to_mat(req.image)
#     p = req.params
#     result_img = pibo_camera.edgePreservingFilter(img, p['flags'], p['sigma_s'], p['sigma_r'])
#     return {"image": mat_to_b64(result_img)}

# @app.post("/camera/flip")
# def camera_flip(req: AIRequest):
#     img = b64_to_mat(req.image)
#     p = req.params
#     result_img = pibo_camera.flip(img, p['flags'])
#     return {"image": mat_to_b64(result_img)}

# --- Face Endpoints ---
@app.post("/face/detect_face")
def face_detect_face(req: AIRequest):
    img = b64_to_mat(req.image)
    result = pibo_face.detect_face(img)
    return create_json_response({"data": result})

@app.post("/face/landmark_face")
def face_landmark_face(req: AIRequest):
    img = b64_to_mat(req.image)
    result = pibo_face.landmark_face(img, req.params['item'])
    return create_json_response({"data": result})

@app.post("/face/analyze_face")
def face_analyze_face(req: AIRequest):
    img = b64_to_mat(req.image)
    result = pibo_face.analyze_face(img, req.params['item'])
    return create_json_response({"data": result})

@app.post("/face/init_db")
def face_init_db():
    pibo_face.init_db()
    return {"data": {"status": "success", "message": "Face DB initialized."}}

@app.post("/face/train_face")
def face_train_face(req: AIRequest):
    img = b64_to_mat(req.image)
    p = req.params
    pibo_face.train_face(img, p['item'], p['name'])
    return {"data": {"status": "success", "message": f"Face '{p['name']}' trained."}}

@app.post("/face/delete_face")
def face_delete_face(req: AIRequest):
    result = pibo_face.delete_face(req.params['name'])
    return {"data": result}

@app.post("/face/recognize")
def face_recognize(req: AIRequest):
    img = b64_to_mat(req.image)
    result = pibo_face.recognize(img, req.params['item'])
    return create_json_response({"data": result})

@app.get("/face/get_db")
def face_get_db():
    db = pibo_face.get_db()
    return create_json_response({"data": db})

@app.post("/face/save_db")
def face_save_db(req: AIRequest):
    pibo_face.save_db(req.params['filename'])
    return {"data": {"status": "success", "message": f"Face DB saved to {req.params['filename']}."}}

@app.post("/face/load_db")
def face_load_db(req: AIRequest):
    try:
        pibo_face.load_db(req.params['filename'])
        return {"data": {"status": "success", "message": f"Face DB loaded from {req.params['filename']}."}}
    except Exception as e:
        return create_json_response({"data": {"status": "error", "message": str(e)}})

@app.post("/face/detect_mesh")
def face_detect_mesh(req: AIRequest):
    img = b64_to_mat(req.image)
    mesh_data = pibo_face.detect_mesh(img)
    serializable_data = []
    for item in mesh_data:
        # landmark 객체는 직렬화가 어려우므로 필요한 정보만 추출
        serializable_data.append({
            "distance": item["distance"],
            "direction": item["direction"],
            "landmark": [{"x": lm.x, "y": lm.y, "z": lm.z} for lm in item["landmark"]]
        })
    return create_json_response({"data": serializable_data})

# --- Detect Endpoints ---
@app.post("/detect/load_hand_gesture_model")
def detect_load_hand_gesture_model(req: AIRequest):
    pibo_detect.load_hand_gesture_model(req.params.get('modelpath', '/home/pi/.model/hand/gesture_recognizer.task'))
    return {"data": {"status": "success"}}

@app.post("/detect/recognize_hand_gesture")
def detect_recognize_hand_gesture(req: AIRequest):
    img = b64_to_mat(req.image)
    result = pibo_detect.recognize_hand_gesture(img)
    return create_json_response({"data": result})

@app.post("/detect/load_object_model")
def detect_load_object_model(req: AIRequest):
    pibo_detect.load_object_model(req.params.get('modelpath', '/home/pi/.model/object/yolo11s.onnx'))
    return {"data": {"status": "success"}}

@app.post("/detect/detect_object")
def detect_detect_object(req: AIRequest):
    img = b64_to_mat(req.image)
    result = pibo_detect.detect_object(img)
    return create_json_response({"data": result})

@app.post("/detect/detect_qr")
def detect_detect_qr(req: AIRequest):
    img = b64_to_mat(req.image)
    result = pibo_detect.detect_qr(img)
    return create_json_response({"data": result})

# @app.post("/detect/detect_pose")
# def detect_detect_pose(req: AIRequest):
#     img = b64_to_mat(req.image)
#     persons = pibo_detect.detect_pose(img)
#     # Person 객체를 JSON 직렬화 가능한 dict로 변환
#     persons_data = [person.to_dict() for person in persons if person]
#     return create_json_response({"data": persons_data})

# @app.post("/detect/analyze_pose")
# def detect_analyze_pose(req: AIRequest):
#     from openpibo.modules.pose.utils import KeyPoint, Point, Person
#     persons_data = req.params.get("data", [])
#     persons = []
#     for p_data in persons_data:
#         keypoints = [KeyPoint(kp['body_part'], Point(kp['coordinate']['x'], kp['coordinate']['y']), kp['score']) for kp in p_data['keypoints']]
#         persons.append(Person(keypoints, p_data['score']))
#     result = pibo_detect.analyze_pose(persons)
#     return create_json_response({"data": result})

# @app.post("/detect/object_tracker_init")
# def detect_object_tracker_init(req: AIRequest):
#     global object_tracker
#     img = b64_to_mat(req.image)
#     pibo_detect.object_tracker_init(img, tuple(req.params['p']))
#     object_tracker = pibo_detect.tracker # 트래커를 전역 변수에 저장
#     return {"data": {"status": "success"}}

# @app.post("/detect/track_object")
# def detect_track_object(req: AIRequest):
#     global object_tracker
#     if object_tracker is None:
#         return create_json_response({"data": {"status": "error", "message": "Tracker not initialized."}})
#     pibo_detect.tracker = object_tracker # 전역 트래커를 인스턴스에 설정
#     img = b64_to_mat(req.image)
#     result = pibo_detect.track_object(img)
#     object_tracker = pibo_detect.tracker # 업데이트된 트래커를 다시 저장
#     return create_json_response({"data": result})

@app.post("/detect/detect_marker")
def detect_detect_marker(req: AIRequest):
    img = b64_to_mat(req.image)
    result = pibo_detect.detect_marker(img, req.params.get('marker_length', 2))
    return create_json_response({"data": result})

# --- Classifier Endpoints ---
@app.post("/tm/load")
def tm_load(req: AIRequest):
    p = req.params
    try:
        pibo_tm.load(p["model_path"], p["label_path"])
        return {"data": {"status": "success"}}
    except Exception as e:
        return create_json_response({"data": {"status": "error", "message": str(e)}})

@app.post("/tm/predict")
def tm_predict(req: AIRequest):
    img = b64_to_mat(req.image)
    try:
        name, preds = pibo_tm.predict(img)
        return create_json_response({"data": {"name": name, "predictions": preds}})
    except Exception as e:
        return create_json_response({"data": {"status": "error", "message": str(e)}})

@app.post("/cf/load")
def cf_load(req: AIRequest):
    p = req.params
    try:
        pibo_cf.load(p["model_path"], p["label_path"])
        return {"data": {"status": "success"}}
    except Exception as e:
        return create_json_response({"data": {"status": "error", "message": str(e)}})

@app.post("/cf/predict")
def cf_predict(req: AIRequest):
    img = b64_to_mat(req.image)
    try:
        name, preds = pibo_cf.predict(img)
        return create_json_response({"data": {"name": name, "predictions": preds}})
    except Exception as e:
        return create_json_response({"data": {"status": "error", "message": str(e)}})

@app.post("/cf/convert_tfjs_to_keras")
def cf_load(req: AIRequest):
    p = req.params
    try:
        pibo_cf.convert_tfjs_to_keras(p["model_path"], p["label_path"])
        return {"data": {"status": "success"}}
    except Exception as e:
        return create_json_response({"data": {"status": "error", "message": str(e)}})

@app.post("/speech/tts")
def speech_tts(req: AIRequest):
    p = req.params
    try:
        # 서버에 로드된 SpeechOnDevice 인스턴스의 tts 메서드를 호출
        pibo_tts.tts(
            text=p['text'],
            filename=p.get('filename', 'tts.mp3'),
            voice=p.get('voice', 2),
            lang=p.get('lang', 'ko')
        )
        return {"data": {"status": "success", "message": f"TTS file created at {p.get('filename', 'tts.mp3')}"}}
    except Exception as e:
        logging.error(f"TTS generation failed: {e}")
        return JSONResponse(status_code=500, content={"data": {"status": "error", "message": str(e)}})

# --- 서버 실행 ---
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, help='Set port number', default=50050)
    args = parser.parse_args()
    uvicorn.run('run_ai_core:app', host='0.0.0.0', port=args.port, access_log=False, reload=False)
