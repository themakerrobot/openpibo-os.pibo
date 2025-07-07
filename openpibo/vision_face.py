"""
영상처리, 인공지능 비전 기술을 사용합니다.
이 모듈은 AI-Core 서버와 통신하여 동작합니다.
"""
import requests
import base64
import numpy as np
import cv2
import json
import os
import pickle
from PIL import Image, ImageDraw, ImageFont
import openpibo_models # For font file path

# =================================================================
# API 통신 헬퍼 함수
# =================================================================
def _api_call(endpoint: str, img_in: np.ndarray = None, params: dict = None):
    """
    AI-Core 서버와 통신을 전담하는 내부 헬퍼 함수입니다.

    :param str endpoint: 호출할 API의 엔드포인트 (예: "face/detect_face")
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

    # 서버 응답 처리
    if res_json.get("image"):
        # 응답에 'image' 키가 있으면 Base64 디코딩하여 이미지로 반환
        im_bytes = base64.b64decode(res_json["image"])
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
        return cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

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
# Face 클래스 (API 클라이언트 버전)
# =================================================================
class Face:
  """
  얼굴과 관련된 다양한 기능을 수행하는 클래스입니다. (API-backed)
  이 클래스의 인스턴스는 내부적으로 AI-Core 서버와 통신하여 동작합니다.
  """
  def __init__(self):
    """
    Face 클래스를 초기화합니다.
    실제 모델 로딩은 서버에서 이루어지므로, 클라이언트에서는 상태 변수만 초기화합니다.
    """
    self.facedb = [[],[]] # 로컬에서도 DB 상태를 가질 수 있으나, 최종 권위는 서버에 있음
    self.threshold = 0.4

  def detect_face(self, img):
    """
    얼굴을 탐색합니다. (서버 API 호출)
    """
    return _api_call("face/detect_face", img_in=img)

  def detect_face_vis(self, img, items):
    """
    탐색된 얼굴에 박스를 그립니다. (로컬 동작)
    """
    for item in items:
      x1, y1, x2, y2 = item
      cv2.rectangle(img, (x1,y1), (x2,y2), (50,255,50), 2)
    return img

  def landmark_face(self, img, item):
    """
    얼굴의 랜드마크를 탐색합니다. (서버 API 호출)
    """
    return _api_call("face/landmark_face", img_in=img, params={"item": item})

  def landmark_face_vis(self, img, coords):
    """
    탐색된 랜드마크를 이미지에 그립니다. (로컬 동작)
    """
    for i, coord in enumerate(coords):
      x, y = coord
      cv2.circle(img, (x, y), 2, (50, 200, 50), -1)
      putTextPIL(img, str(i+1), (x, y-15), 15, (255, 255, 255))
    return img

  def analyze_face(self, img, item):
    """
    얼굴의 나이, 성별, 감정을 추정합니다. (서버 API 호출)
    """
    return _api_call("face/analyze_face", img_in=img, params={"item": item})

  def analyze_face_vis(self, img, item):
    """
    얼굴 분석 결과를 이미지에 표시합니다. (로컬 동작)
    """
    x1, y1, x2, y2 = item['box']
    age, gender, emotion = item['age'], item['gender'], item['emotion']
    putTextPIL(img, f'{age}/{gender}/{emotion}', (x1, y1-30), 30, (255, 255, 255))
    return img

  def init_db(self):
    """
    서버의 얼굴 데이터베이스를 초기화합니다. (서버 API 호출)
    """
    self.facedb = [[], []] # 로컬 상태도 동기화
    return _api_call("face/init_db")

  def train_face(self, img, item, name):
    """
    얼굴을 학습하여 서버의 데이터베이스에 저장합니다. (서버 API 호출)
    """
    return _api_call("face/train_face", img_in=img, params={"item": item, "name": name})

  def delete_face(self, name):
    """
    서버의 데이터베이스에서 등록된 얼굴을 삭제합니다. (서버 API 호출)
    """
    return _api_call("face/delete_face", params={"name": name})

  def recognize(self, img, item):
    """
    등록된 얼굴을 인식합니다. (서버 API 호출)
    """
    return _api_call("face/recognize", img_in=img, params={"item": item})

  def get_db(self):
    """
    서버의 얼굴 데이터베이스를 가져옵니다. (서버 API 호출)
    """
    self.facedb = _api_call("face/get_db") # 로컬 상태 업데이트
    return self.facedb

  def save_db(self, filename):
    """
    서버의 얼굴 데이터베이스를 서버의 파일 시스템에 저장합니다. (서버 API 호출)
    """
    return _api_call("face/save_db", params={"filename": filename})

  def load_db(self, filename):
    """
    서버의 파일 시스템에서 얼굴 데이터베이스를 로드합니다. (서버 API 호출)
    """
    return _api_call("face/load_db", params={"filename": filename})

  def detect_mesh(self, image):
    """
    얼굴 메쉬를 탐색하고 거리, 방향을 추정합니다. (서버 API 호출)
    """
    return _api_call("face/detect_mesh", img_in=image)

  def detect_mesh_vis(self, image, items):
    """
    얼굴 메쉬 결과를 이미지에 그립니다. (로컬 동작)
    """
    # FACEMESH_TESSELATION은 서버에만 있으므로, 간단한 점만 그리는 방식으로 변경하거나
    # 해당 상수를 클라이언트에도 복사해와야 합니다. 여기서는 점만 그립니다.
    for item in items:
      landmarks = item['landmark']
      distance = item['distance']
      direction = item['direction']
      
      if landmarks:
        image_height, image_width, _ = image.shape
        points = []
        for lm in landmarks:
            x, y = int(lm['x'] * image_width), int(lm['y'] * image_height)
            points.append((x, y))
            cv2.circle(image, (x, y), 1, (200, 200, 200), -1)

        # 대표 위치에 텍스트 표시
        if len(points) > 103:
            x, y = points[103]
            putTextPIL(image, f'{distance}cm/{direction}', (x, y - 40), 30, (255, 255, 255))
            
    return image
