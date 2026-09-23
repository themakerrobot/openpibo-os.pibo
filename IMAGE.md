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
git describe --tags           # YYMMDDvN 또는 YYMMDDvN-ph
cat /home/pi/.OS_VERSION      # piBo_YYMMDDvN(-ph)
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

### TensorFlow · torch 걷어내기 (260924~, 이미지당 1회)

분류기·사물 인식이 TensorFlow·ultralytics·torch 를 안 쓴다. 코드가 import 하지 않으므로
**메모리는 태그만 올려도 줄어든다.** 아래는 SD 카드 용량과 이미지 크기를 줄이는 작업이다.

기기(260923 기준 pip 목록)에 이미 있는 것으로 충분하다. 새로 설치할 것은 없다.

| 쓰는 곳 | 패키지 (기기 버전) |
|---|---|
| 분류기 이미지 · movenet | `tflite-runtime` 2.14.0 |
| 분류기 손·얼굴·포즈 · 얼굴·손 인식 | `mediapipe` 0.10.18 (jax·jaxlib·matplotlib·sentencepiece·sounddevice 를 요구한다 — 남길 것) |
| 사물 인식 · TTS | `onnxruntime` 1.20.1 |
| 얼굴 분석(`vision_face.py`) | `openvino` 2024.5.0 — **남길 것** (`openvino-dev` 는 지워도 된다) |

컨테이너에서 위 버전 그대로(numpy 1.26.4) 분류기·사물 인식을 돌려 확인했다.

```bash
PY=/home/pi/.pyenv/bin/python3
SP=$($PY -c "import site; print(site.getsitepackages()[0])")

# 0) 새 태그에서 먼저 확인 — 둘 다 에러 없이 끝나야 한다
$PY -c "from openpibo.modules.teachlab import load_interpreter; print(load_interpreter())"
#   <class 'tflite_runtime.interpreter.Interpreter'>  (tensorflow 가 나오면 멈출 것)
$PY -c "import numpy as np; from openpibo.vision_detect import Detect; print(Detect().detect_object(np.zeros((480,640,3),'uint8')))"
#   []

# 1) 얼마나 줄어드는지
du -sh $SP/{tensorflow,tensorflow_estimator,tensorboard,keras,tf_keras,tensorflowjs,flax,optax,chex,orbax,torch,torchvision,torchaudio,ultralytics,openvino/tools} 2>/dev/null | sort -h

# 2) 1단계 — TensorFlow · torch · ultralytics 와 그것만 쓰던 것 (wheel 약 400MB)
sudo $PY -m pip uninstall -y \
  tensorflow tensorflow-cpu-aws tensorflow-estimator tensorflow-hub tensorflow-io-gcs-filesystem \
  tensorboard tensorboard-data-server keras tf-keras tensorflowjs \
  flax optax chex orbax-checkpoint \
  ultralytics ultralytics-thop torch torchvision torchaudio openvino-dev \
  onnx onnxslim py-cpuinfo libclang h5py gast astunparse google-pasta termcolor namex optree \
  etils toolz msgpack nest-asyncio grpcio werkzeug markdown

# 3) 2단계 — MeloTTS 시험 잔재 (wheel 약 360MB + 사전 파일)
#    MeloTTS requirements.txt 29개가 버전까지 그대로 깔려 있다(melotts 패키지 자체는 없다).
#    지금 TTS 는 Supertonic 3 이다(mtts.py = 원본 py/helper.py 그대로). onnxruntime·numpy·soundfile 만 쓴다.
#    Supertonic requirements 에 librosa 가 적혀 있지만 helper.py 는 import 하지 않는다
du -sh $SP/unidic $SP/unidic_lite $SP/mecab_ko_dic $SP/jieba $SP/gruut_lang_* 2>/dev/null   # 사전이 크다
sudo $PY -m pip uninstall -y \
  txtsplit cached-path transformers tokenizers huggingface-hub num2words docopt \
  unidic-lite unidic mecab-python3 pykakasi jaconv fugashi g2p-en distance anyascii jamo \
  gruut gruut-ipa gruut-lang-de gruut-lang-en gruut-lang-es gruut-lang-fr python-crfsuite jsonlines dateparser \
  g2pkk g2pk python-mecab-ko python-mecab-ko-dic konlpy jpype1 nltk \
  librosa audioread resampy numba llvmlite pooch pydub eng-to-ipa inflect unidecode \
  pypinyin cn2an proces jieba gradio gradio-client ffmpy safehttpx semantic-version tomlkit ruff orjson \
  langid loguru panphon munkres unicodecsv \
  boto3 botocore s3transfer jmespath google-cloud-storage google-cloud-core google-resumable-media \
  google-crc32c google-api-core googleapis-common-protos proto-plus google-auth google-auth-oauthlib \
  requests-oauthlib oauthlib cachetools rsa pyasn1 pyasn1-modules \
  tweepy twine readme-renderer nh3 rfc3986 requests-toolbelt id keyring \
  jaraco-classes jaraco-context jaraco-functools jeepney secretstorage backports-tarfile

# 4) 다시 확인
$PY -m pip check                       # 지운 것 때문에 깨진 의존이 없어야 한다
$PY -c "from openpibo.modules.teachlab import load_interpreter; print(load_interpreter())"
$PY -c "import numpy as np; from openpibo.vision_detect import Detect; print(Detect().detect_object(np.zeros((480,640,3),'uint8')))"
$PY -c "import openpibo.vision_face, openpibo.vision_classify, openpibo.speech, openpibo.collect; print('ok')"
$PY -c "from bs4 import BeautifulSoup; BeautifulSoup('<a/>', 'xml'); print('lxml ok')"   # 뉴스 블록
```

두 목록은 기기 pip 목록(310개, `test/requirements.txt`)을 버전별 PyPI 메타데이터로 의존 그래프를
만들어 계산했다. 131개를 지워도 남는 179개 중 **깨지는 의존은 0개**였다.

- **`lxml` 은 지우지 말 것.** `collect.py` 의 뉴스(`BeautifulSoup(..., 'xml')`)가 쓴다.
  기기에는 `konlpy` 의 의존으로 들어와 있어서 "고아 정리" 로 딸려 나가기 쉽다
- `tflite-runtime` 은 **지우지 말 것.** 없으면 `load_interpreter()` 가 TensorFlow 로 떨어지는데
  그것도 지웠으면 분류기와 movenet(포즈)이 못 뜬다
- `jax` `jaxlib` `matplotlib` `sentencepiece` `sounddevice` `ml-dtypes` `opt_einsum` `scipy` 는
  mediapipe·jax 가 요구한다. `sympy` 는 onnxruntime 이 요구한다. 남긴다
- `openvino` 는 `vision_face.py` 가 쓴다. 남긴다 (`openvino-dev` 만 지운다)
- **확인 전 보류**: `pandas` `seaborn` `scikit-learn`. 리포 코드는 안 쓰지만 수업 자료에서 쓸 수 있다
- 위 목록 밖의 작은 범용 라이브러리(`httpx` `rich` `typer` `aiofiles` `cryptography` 등)는
  지워도 얻는 게 적어서 그대로 뒀다

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
