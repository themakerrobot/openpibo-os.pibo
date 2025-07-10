"""
영상처리, 인공지능 비전 기술을 사용합니다.
이 모듈은 AI-Core 서버와 통신하여 동작합니다.
"""
import requests
import base64
import numpy as np
import cv2
import json

# =================================================================
# API 통신 헬퍼 함수
# =================================================================
def _api_call(endpoint: str, img_in: np.ndarray = None, params: dict = None):
    """
    AI-Core 서버와 통신을 전담하는 내부 헬퍼 함수입니다.

    :param str endpoint: 호출할 API의 엔드포인트 (예: "tm/predict")
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

    # 이미지 외의 데이터(JSON) 반환
    return res_json.get("data", res_json)

# =================================================================
# TeachableMachine 클래스 (API 클라이언트 버전)
# =================================================================
class TeachableMachine:
  """
  Teachable Machine 모델을 사용하여 이미지를 분류합니다. (API-backed)
  이 클래스의 인스턴스는 내부적으로 AI-Core 서버와 통신하여 동작합니다.
  """
  def __init__(self):
    """
    TeachableMachine 클래스를 초기화합니다.
    실제 모델 로딩은 서버에서 이루어지므로, 이 메서드는 비어있습니다.
    """
    pass

  def load(self, model_path, label_path):
    """
    서버에 Tflite 모델을 로드하도록 요청합니다. (서버 API 호출)

    :param str model_path: 서버의 파일 시스템에 있는 모델 파일 경로
    :param str label_path: 서버의 파일 시스템에 있는 라벨 파일 경로
    """
    params = {"model_path": model_path, "label_path": label_path}
    result = _api_call("tm/load", params=params)
    if result.get("status") == "error":
        raise Exception(f"Failed to load Teachable Machine model on server: {result.get('message')}")

  def predict(self, img):
    """
    Tflite 모델로 추론합니다. (서버 API 호출)

    :param numpy.ndarray img: 분석할 이미지 객체
    :returns: (가장 높은 확률을 가진 클래스 명, 전체 클래스에 대한 확률 리스트)
    """
    result = _api_call("tm/predict", img_in=img)
    if "name" in result and "predictions" in result:
        # 서버는 dict를 반환하므로, 기존 규격에 맞게 튜플로 변환
        return result['name'], result['predictions']
    else:
        raise Exception(f"Failed to predict with Teachable Machine model: {result.get('message', 'Unknown error')}")

# =================================================================
# CustomClassifier 클래스 (API 클라이언트 버전)
# =================================================================
class CustomClassifier:
  """
  사용자 정의 Keras 모델을 사용하여 이미지를 분류합니다. (API-backed)
  이 클래스의 인스턴스는 내부적으로 AI-Core 서버와 통신하여 동작합니다.
  """
  def __init__(self):
    """
    CustomClassifier 클래스를 초기화합니다.
    실제 모델 로딩은 서버에서 이루어지므로, 이 메서드는 비어있습니다.
    """
    pass

  def load(self, model_path, label_path):
    """
    서버에 Keras 모델을 로드하도록 요청합니다. (서버 API 호출)

    :param str model_path: 서버의 파일 시스템에 있는 모델 파일 경로
    :param str label_path: 서버의 파일 시스템에 있는 라벨 파일 경로
    """
    params = {"model_path": model_path, "label_path": label_path}
    result = _api_call("cf/load", params=params)
    if result.get("status") == "error":
        raise Exception(f"Failed to load Custom Classifier model on server: {result.get('message')}")

  def predict(self, img):
    """
    Keras 모델로 추론합니다. (서버 API 호출)

    :param numpy.ndarray img: 분석할 이미지 객체
    :returns: (가장 높은 확률을 가진 클래스 명, 전체 클래스에 대한 확률 리스트)
    """
    result = _api_call("cf/predict", img_in=img)
    if "name" in result and "predictions" in result:
        # 서버는 dict를 반환하므로, 기존 규격에 맞게 튜플로 변환
        return result['name'], result['predictions']
    else:
        raise Exception(f"Failed to predict with Custom Classifier model: {result.get('message', 'Unknown error')}")

  def convert_tfjs_to_keras(self, model_path, label_path):
    """
    tfjs 모델을 Keras 모델로 변환합니다. (서버 API 호출)

    :param str model_path: 모델 파일 경로
    :param str label_path: 라벨 파일 경로
    """
    params = {"model_path": model_path, "label_path": label_path}
    result = _api_call("cf/convert_tfjs_to_keras", params=params)
    if result.get("status") == "error":
        raise Exception(f"Failed to convert Custom Classifier model on server: {result.get('message')}")
