# 필리핀 배포판 차이점 (`ph` 브랜치 전용 문서)

이 파일은 **`ph` 브랜치에만 있다.** `main` 에는 없고, 합치지 않는다.

`ph` 는 `main` 을 merge 만 하는 브랜치다. 개발은 전부 `main` 에서 한다.
아래 항목이 `ph` 가 `main` 과 다른 **전부**이며, merge 후 반드시 유지되어야 한다.

검증:

```bash
git diff --name-status main ph
# 아래 표와 정확히 일치해야 한다. 모드 차이(0줄 항목)가 나오면 안 된다.
```

---

## 1. 기본 언어 영어 — `ko2en.js` 3종

| 파일 |
|---|
| `ide/static/ko2en.js` |
| `tools/static/ko2en.js` |
| `classifier/static/ko2en.js` |

**1·2행만** 다르다.

```js
// main (국내) — 브라우저 언어 자동 감지
const blang = (navigator.language || navigator.userLanguage).includes('ko')?'ko':'en';
let lang = localStorage.getItem("language")?localStorage.getItem("language"):blang;

// ph (필리핀) — 영어 고정
const blang = 'en';
let lang = localStorage.getItem("language") || blang;
```

**주의:** `blang` 은 브라우저 `localStorage` 에 `language` 값이 **없을 때만** 쓰인다.
각 앱이 페이지를 열 때 현재 언어를 즉시 `localStorage` 에 저장하므로, 한 번이라도
방문한 브라우저는 그 값이 고정된다. 검증용 태블릿에서 한국어로 열어본 적이 있으면
필리핀 기기에서도 한국어로 뜬다. 기기 문제가 아니다.

```js
localStorage.removeItem("language"); location.reload();
```

앱마다 포트가 달라(ide 80 / tools 50000 / classifier 50010) **origin 이 분리되어 있으므로
localStorage 도 각각이다.** 세 곳 모두 지워야 한다.

AP 모드 IP 는 `192.168.34.1` 고정이라(`system/hotspot.sh`) 기기가 달라도 origin 이 같다.
국내 기기와 필리핀 기기를 같은 태블릿으로 번갈아 쓰면 언어 설정이 서로 섞인다.

---

## 2. `system/ph_setup.sh` — 신규 파일 (100755)

이미지 생성 시 **1회 실행**하는 스크립트. 리포에 파일이 있다고 적용된 게 아니다.

```bash
sudo timedatectl set-timezone Asia/Manila
sudo raspi-config nonint do_wifi_country PH
sudo rm -f /etc/modprobe.d/brcmfmac.conf     # country=US 잔재 제거 (아래 참고)
sudo chmod +x /home/pi/openpibo-os/system/hotspot.sh
```

적용 여부 확인:

```bash
timedatectl | grep -i "time zone"            # Asia/Manila
sudo raspi-config nonint get_wifi_country    # PH
ls /etc/modprobe.d/brcmfmac.conf             # 없어야 한다
dmesg | grep -i "unknown parameter"          # 아무것도 안 나와야 한다
```

한국 값이 나오면 `sudo bash /home/pi/openpibo-os/system/ph_setup.sh && sudo reboot`.

### `brcmfmac.conf` 를 지우는 이유

베이스 이미지에 `options brcmfmac country=US` 가 들어있다. 현재 드라이버
(BCM4345/6 = CYW43455, 펌웨어 `7.45.265`)는 이 파라미터를 지원하지 않아
`brcmfmac: unknown parameter 'country' ignored` 로 무시하므로 **지금은 무해하다.**

문제는 드라이버·펌웨어를 올렸을 때다. 지원하는 버전이 되면 기기가 US 도메인이 된다.

| | 2.4GHz 최대 EIRP |
|---|---|
| PH | **20 dBm** |
| US | 30 dBm |

10 dB, 즉 **10배 초과 송신**이 된다. 조용히 규제 위반 상태가 되므로 미리 지운다.

### 규제 도메인이 실제로 설정되는 경로

`raspi-config nonint do_wifi_country PH` 는 `/boot/firmware/cmdline.txt` 에
`cfg80211.ieee80211_regdom=PH` 를 넣는다. 이게 `iw reg get` 의 `global` 을 PH 로 만든다.

`iw reg get` 의 `phy#0` 는 `country 99: DFS-UNSET` 으로 남는데 정상이다.
`brcmfmac` 이 wiphy 에 자체 world 도메인을 씌우기 때문이고
(`self-managed` 는 아니다), 실제 국가는 펌웨어 `ccode` 에서 와야 하는데
`brcmf_c_process_txcap_blob: no txcap_blob available` 로 그 데이터가 없다.

**2.4GHz 에서는 실질 차이가 없다.** PH 와 `country 99` 둘 다 2402–2482 MHz,
최대 EIRP 20 dBm 이고, `hotspot.sh` 가 채널 1/6/11 만 쓰므로 어느 쪽으로 해석해도 안전하다.

**5GHz 를 쓰게 되면 반드시 다시 봐야 한다.** PH 는 5250–5330, 5490–5730 에 DFS 의무가
있는데 `country 99` 테이블에는 그 표기가 없다. 현재 `hotspot.sh` 가 `band bg`(2.4GHz 전용)라
해당 없다.

### `iw dev ap0 info` 의 txpower 는 믿지 말 것

`txpower 31.00 dBm` 으로 나오는데 **실측값도 규제값도 아니다.** 근거:

- `iw phy0 info` 에 txpower 항목이 아예 없다 — 드라이버가 조회를 지원하지 않는다
- `brcmf_c_process_txcap_blob: no txcap_blob available` — 국가별 출력 제한 테이블이 없다
- 규제 테이블은 PH·phy#0 양쪽 모두 2.4GHz **20 dBm** 상한이다

인증 서류에는 규제 한도(20 dBm EIRP)와 CYW43455 데이터시트 값을 쓸 것.
`(6, 20)` 의 `6 dBi` 도 규제 허용 상한이지 Pi 4B 내장 안테나의 실제 게인이 아니다.

---

## 3. `examples/*.json` — 예제 영문화 (10개)

`basic` `device` `gugudan` `motion` `speech_tts`
`vision_face1` `vision_face2` `vision_hand` `vision_marker` `vision_object`

Blockly 워크스페이스 JSON 의 **텍스트 리터럴과 변수명**을 영문으로 바꿨다.

| 한글 | 영문 |
|---|---|
| 가나다 | abc |
| 변수 | variable |
| 이미지 | image |
| 분석결과 / 분석결과_목록 | result / resultList |
| 얼굴 / 얼굴목록 | face / faceList |
| 사물결과 / 코드결과 / 포즈결과 | objectResult / codeResult / poseResult |
| 번역문장 | translatedText |

`speech_tts.json` 은 구조도 바꿨다:

- `speech_tts_play`(voice: main) 블록 **제거** — `lang` 인자를 안 넘겨
  `speech.py` 기본값 `lang="ko"` 로 떨어진다. 영어를 넣으면 한국어 발음으로 읽는다
- 그 뒤에 딸려 있던 `utils_sleep`(3초)도 제거
- `speech_translate` / `speech_gtts_play` 의 대상 언어를 `en` → **`es`** 로 변경.
  입력이 영어인데 대상도 영어면 번역 데모가 무의미해진다

### 예제는 리포만 고쳐서는 기기에 반영되지 않는다

`ide/run_ide.py` 의 `restore`(공장초기화) 핸들러에서만 `/home/pi/examples/` 로 복사된다.
배포할 때마다 수동 복사가 필요하다.

```bash
cp -rf /home/pi/openpibo-os/examples/* /home/pi/examples/
rm -f /home/pi/examples/collect.json     # cp 로는 안 지워진다
sudo chown -R pi:pi /home/pi/examples
```

---

## 4. `examples/collect.json` — 삭제

`main` 에는 있고 `ph` 에는 없다.

- `Weather.search()` 의 `region_list` 가 **한국 기상청 지역코드 전용**
  (`전국 서울 인천 경기 부산 …`). 필리핀 도시를 넣으면 KeyError
- `News` 는 **JTBC 뉴스 RSS** — 한국어 뉴스만 나온다

번역해도 못 쓰는 예제라 뺐다.

---

## 5. `ide/static/customblock_toolbox.js` — 한국 전용 블록 미노출

블록 **정의와 코드 생성기는 그대로 두고**(`customblock.js`,
`customblock_callback.js` 는 `main` 과 동일), 툴박스에서만 뺐다.
기존 워크스페이스에 그 블록이 들어있으면 여전히 열리고 실행된다.

### 뺀 것

**Collect 카테고리 통째로** — `wikipedia_search` `weather_forecast` `weather_search` `news_search`

| 블록 | 이유 |
|---|---|
| `weather_forecast` / `weather_search` | 한국 기상청 지역코드 전용 |
| `news_search` | JTBC RSS, 한국어 |
| `wikipedia_search` | `openpibo/collect.py` 에 `ko.wikipedia.org` 하드코딩 |

**Speech 카테고리의 대화 블록 3개** — `speech_get_dialog` `speech_load_dialog` `speech_reset_dialog`

`Dialog.get_dialog` 는 한글 CSV 에 n-gram 유사도를 돌려 **한글 답변**을 낸다
(`openpibo/speech.py`). tools 의 Talk 섹션을 `main` 에서 아예 없앤 것과 같은 이유다.

### 안 뺀 것

`speech_translate`, `speech_start_llm`, `speech_call_llm`, `speech_stop_llm`,
`speech_stt`, `speech_tts*`, `speech_gtts*`, `speech_otts*`, `speech_etts*` 는 유지.

---

## `main` 과 같지만 필리핀에서 주의할 것

델타는 아니지만 알고 있어야 하는 제약이다.

- **`speech_tts` / `speech_tts_play` 블록** — `lang` 인자를 안 넘겨 한국어 엔진 고정.
  영어 문장을 넣으면 한글 발음으로 읽는다. PH 예제에서는 쓰지 않는다.
  `speech_otts*`(온디바이스)는 기본값이 `lang="na"`(자동)라 영어도 처리된다
- **`speech_gtts*`** — Google TTS. **네트워크가 필요하다.** 오프라인 기기에서는 못 쓴다
- **`speech_translate` 지원 언어** — `ko en es fr de zh-CN ja ru ar hi la ms`.
  **Tagalog(`tl`) 없음**
- **tools 음성 탭** — 목소리 5종(`espeak` / `m1` 남성 / `f1` 여성 / `gtts` / `e_gtts`).
  남성·여성은 온디바이스 TTS(`SpeechOnDevice`, `lang='na'`)라 영어를 읽는다.
  모델을 처음 쓸 때 올리므로 **첫 재생만 몇 초 걸린다**
- **텍스트 블록 기본값 `가나다`** — `customblock.js`(수정 금지 파일)에 있어서,
  예제 안의 값을 바꿔도 새로 끌어다 놓는 블록은 계속 `가나다` 로 뜬다

---

## merge 충돌 처리

`main` → `ph` merge 에서 충돌은 사실상 `ko2en.js` 1·2행뿐이다.

- **`classifier/static/ko2en.js` add/add 충돌** — 양쪽이 독립적으로 추가해서 난다.
  차이가 1·2행뿐이므로 `git checkout --ours classifier/static/ko2en.js`
- `ide/static/ko2en.js`, `tools/static/ko2en.js` 는 보통 자동 머지된다.
  그래도 merge 후 `head -n1` 3종을 **반드시 눈으로 확인**할 것
- `--theirs`(main) 를 잡으면 `blang` 이 자동감지로 돌아가 필리핀 요구사항이 깨진다

`ide/static/customblock_toolbox.js` 는 블록을 실제로 고칠 때만 충돌한다.
그때는 `main` 쪽 변경을 받아들이고 **위 5번의 제거를 다시 적용**하면 된다.

`ide/templates/index.html` 은 일부러 델타에 넣지 않았다. `?ver` 를 올릴 때마다
바뀌는 파일이라 델타로 두면 릴리스마다 충돌한다. 툴박스 `?ver` 는 `main` 에서 올린다.

---

## 배포 후 확인

브라우저는 **Ctrl+Shift+R** 로 강력 새로고침. `?ver` 를 올려도 페이지 자체가 캐시된다.

```bash
cd /home/pi/openpibo-os
git describe --tags                                            # YYMMDDvN-ph
head -n1 ide/static/ko2en.js                                   # const blang = 'en';
ls -l system/hotspot.sh system/ph_setup.sh system/booting.py   # 전부 -rwxr-xr-x
ls /home/pi/examples/                                          # 10개, collect.json 없음
timedatectl | grep -i "time zone"                              # Asia/Manila
sudo raspi-config nonint get_wifi_country                      # PH
```

브라우저:

1. IDE 툴박스에 **Collect 카테고리 없음**, Speech 에 **대화 블록 3개 없음**
2. IDE 예제 영문, `audio_record` 블록 활성
3. tools 음성 탭 2열, Talk 없음, 목소리 5종
4. tools 탭 닫고 → `systemctl is-active tools.service` → `inactive`
