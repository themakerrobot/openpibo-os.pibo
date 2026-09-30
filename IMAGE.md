# 마스터 이미지 만들기

기기 하나를 완성해 두고, 그 SD카드를 떠서 줄인 뒤 다른 카드에 굽는다.

`system/init` 이 부팅할 때 Pi 시리얼로 hostname 을 다시 잡고 재부팅하므로
(`hostname` → AP SSID `pibo-<시리얼8자리>` → `hotspot.sh` 채널 1/6/11),
같은 이미지를 여러 장에 구워도 기기끼리 구분된다. 이미지에 시리얼을 넣을 필요 없다.

---

## 1. 기준 기기 준비

배포 태그로 클론된 상태여야 한다. `git checkout main` 상태로 두지 말 것.

```bash
cd /home/pi/openpibo-os
git describe --tags           # YYMMDDvN 또는 YYMMDDvN-gl (예전 -ph)
cat /home/pi/.OS_VERSION      # piBo_YYMMDDvN(-gl)
```

### openpibo 를 리포 소스에서 임포트하도록 (이미지당 1회)

```bash
sudo bash /home/pi/openpibo-os/system/setup_openpibo_src.sh
```

`pip install` 한 `openpibo-python` 을 지우고 `site-packages` 에 `.pth` 로
`/home/pi/openpibo-os` 를 등록한다. 이걸 해야 **배포 태그 하나가 로봇 코드와
라이브러리를 함께 규정한다.** 안 하면 `git clone --branch <태그>` 로 받아도
`openpibo/` 만 옛 버전이 돌고, 겉보기엔 정상이라 알아채기 어렵다.

`.pth` 는 `site-packages` 에 있으므로 **리포가 아니라 이미지에 속한다.**
pyenv 를 새로 만들면 이 단계가 통째로 빠지니, 처음부터 이미지를 만들 때는
반드시 다시 실행할 것. 확인:

```bash
/home/pi/.pyenv/bin/python3 -c "import openpibo; print(openpibo.__version__, openpibo.__file__)"
# /home/pi/openpibo-os/openpibo/__init__.py 가 나와야 한다
```

의존성(`openpibo_models` 등)은 계속 pip 설치본을 쓴다. 지우지 말 것.

### 안 쓰는 패키지 걷어내기 — `system/venv_prune.py` (260930~, 이미지당 1회)

**새 태그에서 먼저 확인** — 둘 다 에러 없이 끝나야 한다(예전 TensorFlow·ultralytics 경로를 안 쓰는지):

```bash
PY=/home/pi/.pyenv/bin/python3
$PY -c "from openpibo.modules.teachlab import load_interpreter; print(load_interpreter())"
#   <class 'tflite_runtime.interpreter.Interpreter'>  (tensorflow 가 나오면 멈출 것)
$PY -c "import numpy as np; from openpibo.vision_detect import Detect; print(Detect().detect_object(np.zeros((480,640,3),'uint8')))"
#   []
```

※ 260924~260930 에는 여기에 지울 패키지 이름을 적어 두었다(260923 기기 목록 하나로 계산한 고정 목록). 기기마다 깔린 게 달라서
스크립트가 기기에서 직접 계산하게 바꿨다.

예전 OS 에서 올려 온 기기에는 지금 코드가 안 쓰는 패키지가 수 GB 남아 있다(260930 두 기기 모두 site-packages 5.5~5.6GB:
TensorFlow·torch·ultralytics, MeloTTS 시험 잔재(gruut·unidic·mecab·jieba·transformers·gradio …), 문서 도구(sphinx) 등).
**코드가 import 하지 않으므로 메모리는 태그만 올려도 줄어든다.** 이건 SD 카드 용량과 이미지 크기를 줄이는 작업이다.

`venv_prune.py` 는 '리포 코드가 import 하는 패키지(스크립트의 `ROOTS` + `requirements.txt`)와 그것들이 요구하는 것'만 남기고
나머지를 지울 목록으로 뽑는다. 기기에 **지금 깔린 것의 메타데이터로** 계산하므로 기기마다 목록이 달라도 된다.

```bash
PY=/home/pi/.pyenv/bin/python3
sudo systemctl stop tools.service classify.service llama-server.service   # 도구가 떠 있으면 먼저 끈다

# 1) 목록만 본다 — 아무것도 안 바꾼다. 맨 위에 개수·용량, 아래에 큰 것부터
sudo $PY /home/pi/openpibo-os/system/venv_prune.py | head -40

# 2) 지운다. 지우기 전 목록을 /home/pi/venv_backup_<날짜>.txt 로 남기고, 지운 뒤 pip check 와 import 확인을 돌린다
sudo $PY /home/pi/openpibo-os/system/venv_prune.py --apply
#    import 확인 끝줄이 'N/N 모듈 import 됨 · 분류기 추론기: tflite_runtime.interpreter' 여야 한다

# 3) 서비스 다시 켜고 IDE·도구·분류기를 한 번씩 열어 본다
sudo systemctl restart ide.service booting.service
```

되돌리기(인터넷 필요): `sudo $PY -m pip install -r /home/pi/venv_backup_<날짜>.txt`

선택 항목 — 기본으로는 **남긴다**:

| 옵션 | 지우는 것 | 이유 |
|---|---|---|
| `--optional` | `pandas` `scikit-learn` `seaborn` (약 140MB) | 리포 코드는 안 쓰지만 수업 자료(파이썬 모드)에서 쓸 수 있다 |
| `--jax` | `jax` `jaxlib` `ml-dtypes` `opt-einsum` (약 265MB, `--optional` 과 같이 주면 scipy 약 130MB 도) | mediapipe 0.10.18 이 요구 목록에 적었지만 **불러오지 않는다.** jax·jaxlib·scipy 를 지우고 얼굴·손·포즈 랜드마커와 얼굴 메시(`FACEMESH_TESSELATION`)가 그대로 도는 것을 확인했다(컨테이너, mediapipe 0.10.18·numpy 1.26.4). 대신 `pip check` 가 `mediapipe requires jax` 를 알린다 — 알고 있는 것이다 |

알아 둘 것:
- **가상환경 밖은 건드리지 않는다.** `/home/pi/.pyenv` 는 시스템 패키지를 보는 가상환경이라 `gpiozero` `lgpio` `spidev` `python-apt` 등
  apt 패키지가 목록에 같이 보이지만(크기 0) 지울 대상에서 뺀다
- 남기는 것 중 눈여겨볼 것: `lxml`(뉴스 블록), `tflite-runtime`(분류기·movenet — 없으면 TensorFlow 를 찾는다), `openvino`(얼굴 분석),
  `av`(picamera2 가 요구), `matplotlib`(mediapipe 가 실제로 불러온다), `sympy`(onnxruntime 이 요구), `uvicorn[standard]`(uvloop·httptools·websockets —
  socket.io 웹소켓)
- `openpibo-face-models`(약 90MB)는 **지운다.** 얼굴 모델은 `/home/pi/.model/face` 에서 읽는다(`vision_face.py`). 이름은 예전 `setup.py` 에만 남아 있다
- `openpibo-detect-models`(약 80MB)는 `movenet_lightning.tflite` 하나 때문에 남는다. 그 파일을 `/home/pi/.model` 로 옮기면 뺄 수 있다(아직 안 함)
- 새 기능이 패키지를 쓰게 되면 스크립트의 `ROOTS` 와 `requirements.txt` 에 **둘 다** 넣을 것(파이보·PiBrain 같은 파일)

### 파이썬 패키지 · 모델 폴더 (260930~, 이미지당 1회)

```bash
PY=/home/pi/.pyenv/bin/python3
# 리포가 쓰는 패키지(requirements.txt). 새로 필요한 건 sherpa-onnx(STT) 둘뿐이다 — numpy·onnxruntime 을 끌고 오지 않는다
$PY -m pip install -r /home/pi/openpibo-os/requirements.txt
$PY -m pip check
```

`/home/pi/.model` 은 `leeyunjai/themaker`(HF)에서 받는다. **`git clone` 하지 말 것** — `.git/lfs` 에 모델이 한 벌 더 남는다.
`huggingface-cli download leeyunjai/themaker --local-dir ...` 로 받고, 아래를 맞춘다.

| 폴더 | 들어갈 것 |
|---|---|
| `tts/assets/onnx` | Supertonic 3 **int8** 변환본(`leeyunjai/edge-lab` `tts-int8`, vocoder 만 fp32, 약 178MB) + `tts.json` `unicode_indexer.json` |
| `tts/assets` | `voice_styles/`(F1~F5·M1~M5) · `LICENSE` · `LICENSE-OpenRAIL-M.txt` · `MODIFICATIONS.md`(변환 고지 — 변형 모델이라 필요) |
| `stt` | `model.int8.onnx` `tokens.txt`(sherpa-onnx `sense-voice-zh-en-ja-ko-yue-int8-2024-07-17`) · `silero_vad.onnx` · `LICENSE-SenseVoice` |
| `llm` | `gemma-3-1b-it-Q4_K_M.gguf` + 링크 `llm-model.gguf` |
| `object` | `yolo11s.onnx`(Ultralytics YOLO11s, `imgsz=320` 고정 export) + **`NOTICE-yolo11s.txt`**(AGPL-3.0 고지, 리포 `system/` 에서 복사) |
| `hand` `face` | 그대로 |
| (지움) | `classifier/`(예전 TF 가중치), `tts/assets/{.git,audio_samples,img}`, fp32 `onnx` |

```bash
# yolo 가중치 고지(AGPL-3.0). 넣은 뒤 VERSION 의 sha256 목록을 다시 만든다
cp /home/pi/openpibo-os/system/NOTICE-yolo11s.txt /home/pi/.model/object/
$PY -c "import onnxruntime as o; m=o.InferenceSession('/home/pi/.model/object/yolo11s.onnx').get_modelmeta().custom_metadata_map; print(m['description'][:30], m['imgsz'], m['license'])"
#   Ultralytics YOLO11s model trai [320, 320] AGPL-3.0 License (https://ultralytics.com/license)
cd /home/pi/.model
grep -vE '^[0-9a-f]{64}  ' VERSION > VERSION.new
find . -type f ! -name VERSION ! -name VERSION.new -print0 | sort -z | xargs -0 sha256sum >> VERSION.new
mv VERSION.new VERSION

cd /home/pi/.model
du -sh */ | sort -h            # tts 약 181M, stt 약 230M, llm 769M
sed -n '/^## sha256/,$p' VERSION | tail -n +2 | sha256sum -c --quiet && echo "VERSION 과 같음"
$PY -c "from openpibo.speech import SpeechToText, SpeechOnDevice; SpeechOnDevice(); SpeechToText(); print('tts·stt ok')"
```

## 2. 뜨기 전 청소

이미지에 개인 정보와 기기별 상태가 딸려간다. 전원 끄기 전에 지운다.

```bash
# 기기별 상태
sudo rm -f  /etc/NetworkManager/system-connections/*.nmconnection*   # WiFi 비번
sudo rm -rf /home/pi/code/* /home/pi/myimage/* /home/pi/myaudio/* /home/pi/mymodel/* 2>/dev/null
sudo rm -f  /home/pi/mymotion.json /home/pi/custom_motion.json       # 검수 중 녹화한 모션
sudo rm -rf /home/pi/.npm /home/pi/openpibo-files/.git               # 용량 (수십~64MB)
sudo rm -f  /home/pi/.bash_history /root/.bash_history

# 로그
sudo journalctl --rotate && sudo journalctl --vacuum-time=1s

# 남아 있으면 안 되는 것들
ls -la /home/pi/.ssh/                 # 개인키가 있으면 지운다. known_hosts 도 사내 호스트가 남는다
ls -d  /home/pi/.git 2>/dev/null      # 있으면 지운다
grep -rIl "token\|password\|secret" /home/pi --exclude-dir=.openpibo-os.pibo 2>/dev/null | head

sudo shutdown -h now
```

**Raspberry Pi Imager 의 "OS 커스터마이즈" 를 쓴 카드는 기준 기기로 쓰지 말 것.**
`/boot/firmware/custom.toml`(구버전은 `firstrun.sh`)이 남아 있으면 첫 부팅에
`raspi-config nonint do_wifi_country` 를 다시 호출해서 `cmdline.txt` 의
`cfg80211.ieee80211_regdom` 값이 `PHPH` 처럼 덧붙는다.

```bash
ls -l /boot/firmware/custom.toml /boot/firmware/firstrun.sh   # 둘 다 없어야 한다
```

## 3. 카드 이미지로 뜨기 (Windows)

Win32DiskImager 나 Raspberry Pi Imager 의 읽기 기능으로 `C:\img\pibo.img` 에 저장한다.
카드 전체 용량만큼 나온다(32GB 카드면 약 30GB).

## 4. PiShrink 로 줄이기 (WSL2)

1. 이미지 파일을 `C:\img\pibo.img` 에 둔다 (경로는 예시)
2. WSL2 Ubuntu 가 없으면 관리자 PowerShell 에서 `wsl --install` 후 재부팅.
   이미 있으면 Ubuntu 실행
3. Ubuntu 터미널에 그대로 붙여넣는다

```bash
sudo apt update && sudo apt install -y parted e2fsprogs wget
cd /mnt/c/img
wget https://raw.githubusercontent.com/Drewsif/PiShrink/master/pishrink.sh
chmod +x pishrink.sh
sudo ./pishrink.sh pibo.img pibo_small.img
```

4. 몇 분 뒤 `C:\img\pibo_small.img` 가 생긴다. 실제 사용량 크기(예: 6~8GB)다
5. Raspberry Pi Imager → **Use custom** → `pibo_small.img` → 새 카드에 굽기.
   **"OS 커스터마이즈" 는 "설정 없음" 으로 둘 것** (2번 항목 참고)
6. 파이에서 첫 부팅 시 카드 전체 용량으로 자동 확장된다

PiShrink 는 `/etc/rc.local` 에 확장 스크립트를 심었다가 첫 부팅 후 원래대로 되돌린다.
구운 카드로 부팅한 뒤 원복됐는지 확인한다.

## 5. 구운 카드 검증

```bash
echo "===== 배포본 ====="
cd /home/pi/openpibo-os
git describe --tags
cat /home/pi/.OS_VERSION
head -n1 ide/static/ko2en.js                                   # PH 는 const blang = 'en';
/home/pi/.pyenv/bin/python3 -c "import openpibo; print(openpibo.__version__, openpibo.__file__)"
                                                               # 경로가 /home/pi/openpibo-os/openpibo/ 여야 한다
ls -l system/hotspot.sh system/setup_country.sh system/booting.py tools/static/index.js
ls /home/pi/examples/                                          # PH 는 10개, collect.json 없음

echo "===== 서비스 ====="
systemctl is-active ide booting                                # active active
systemctl is-active tools classify llama-server                # 전부 inactive 가 정상
curl -s -o /dev/null -w "ide:%{http_code}\n" http://localhost/
curl -s http://localhost:8080/wifi_scan | head -c 200; echo

echo "===== 시스템 ====="
hostname                                                       # 시리얼 8자리
df -h / | tail -1                                              # 카드 용량으로 확장됐는지
timedatectl | grep -i "time zone"                              # PH 는 Asia/Manila
head -13 /etc/rc.local | tail -1                               # system/init 호출 (PiShrink 원복 확인)
ls -l /boot/firmware/custom.toml /boot/firmware/firstrun.sh 2>&1   # 둘 다 없어야 한다

echo "===== 장치 ====="
ls -l /dev/ttyS0 /dev/ttyGS0 /dev/video0
dmesg | grep -iE "error|fail" | grep -vi txcap_blob | tail
```

`/dev/ttyS0` 는 MCU, `/dev/ttyGS0` 는 USB gadget serial 이다.
`mcu_control.py` 는 포트 열기에 실패해도 조용히 `self.ser = None` 으로 넘어가므로,
파일 존재만으로는 부족하고 LED·모터가 실제로 움직이는지 봐야 한다.

`brcmfmac: brcmf_c_process_txcap_blob: no txcap_blob available` 은 정상이다.
이 칩에 국가별 송신 테이블이 없다는 뜻이고, 그래서 `iw reg get` 의 `phy#0` 가
`country 99` (전 대역 20 dBm)로 고정된다.
