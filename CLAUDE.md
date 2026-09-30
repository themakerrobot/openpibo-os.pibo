# openpibo-os.pibo

Pibo 로봇 OS. Raspberry Pi(`pi` 유저, `/home/pi/openpibo-os`)에서 서비스가 작업본을 직접 실행한다.

주요 디렉토리: `ide/`(Blockly IDE, FastAPI + socket.io), `tools/`(모션·음성 도구),
`classifier/`(분류기 — 이미지·손·얼굴·포즈), `system/`(부팅·핫스팟 스크립트).

---

## 브랜치

| 브랜치 | 용도 | 규칙 |
|---|---|---|
| `main` | 국내 배포판 | **모든 개발은 여기서.** 기본 브랜치 |
| `global` | 영문(해외) 배포판 — 필리핀·말레이시아 | **개발 금지.** `main`을 merge만 한다. 차이는 `GLOBAL_DELTA.md` |
| `260624` | GitHub Pages 배포 운영 중 | **절대 건드리지 말 것.** push·force-push·merge 전부 금지 |

`global` 은 **예전 `ph` 브랜치의 이름만 바꾼 것**이다(260930, PiBrain 과 맞춤). 히스토리는 그대로 이어져서 로그에
`Merge branch 'main' into ph` 같은 옛 제목이 남아 있다. `ph` 브랜치는 지운다(커밋은 전부 `global` 에 들어 있다. 웹 세션은 브랜치 삭제가 403 이라 사람이 지운다).
국가가 아니라 언어·배포 구분이라 나라 이름을 쓰지 않는다.

## 태그

- 국내 `YYMMDDv1`, 영문 `YYMMDDv1-gl` (예: `260930v7`, `260930v7-gl`)
  - 260930v6 까지 영문판 태그는 `-ph` 였다(`260915v1-ph` 등). **배포 이력이라 지우지 않는다.** 기기 버전 `piBo_…-ph` 도 소스 링크가 그대로 읽는다
- 같은 날 다시 릴리스하면 번호를 올린다 (`260909v2`, `260909v2-gl`)
- **파이보·파이브레인은 같은 번호로 찍는다(260930~).** 한쪽만 바뀌어도 둘 다 같은 `YYMMDDvN`(영문판은 `-gl`)으로 맞춘다.
  그래서 번호가 건너뛸 수 있다(PiBrain 은 260930v4 다음이 260930v7)
- **태그는 이동하지 않는다.** 내용이 바뀌면 언제나 새 태그
- 삭제는 **같은 날 대체된 태그만** — `260909v2` 가 나왔으면 `260909v1` 은 지워도 된다.
  배포 이력 태그(`260624v1`, `250709v*` 등)는 남긴다
- 기기가 `git clone --branch <태그>` 로 배포본을 받으므로, 태그는 반드시 원격에 push되어 있어야 한다

### 태그 지우기 전 확인

`-gl`·`-ph` 태그의 커밋은 보통 **`global` 브랜치에서만** 도달한다. 태그를 지운 뒤 `global` 브랜치까지
지우면 그 커밋들이 unreachable 이 되어 GC 로 사라진다. **`global` 브랜치는 남겨둘 것.**

```bash
for t in <지울 태그들>; do
  c=$(git rev-parse $t^{commit})
  git merge-base --is-ancestor $c origin/main && echo "$t: main"
  git merge-base --is-ancestor $c origin/global && echo "$t: global"
done
git push origin :<태그> ...     # 원격 삭제
git tag -d <태그> ...           # 로컬 삭제
```

현장 기기가 옛 태그로 돌고 있으면 롤백 경로가 없어지니, 배포된 기기 상태를 먼저 확인할 것.

---

## 영문판(global) 델타

**상세는 `global` 브랜치의 `GLOBAL_DELTA.md`** 에 있다 (이유·검증·충돌 처리·배포 후 확인까지. 260930 전 이름은 `PH_DELTA.md`).
여기 표는 요약이고, 내용이 갈리면 `GLOBAL_DELTA.md` 가 기준이다.

`global`이 `main`과 다른 부분은 **아래 16개 파일뿐**이다. merge 후 반드시 유지되어야 한다.

| 파일 | 내용 |
|---|---|
| `ide/static/ko2en.js`<br>`tools/static/ko2en.js`<br>`classifier/static/ko2en.js` | 1·2행이<br>`const blang = 'en';`<br>`let lang = localStorage.getItem("language") \|\| blang;` |
| `examples/*.json` (10개) | 텍스트 리터럴·변수명 영문 |
| `examples/collect.json` | **global 에는 없다.** `Weather.region_list` 가 한국 기상청 지역코드, `News` 가 JTBC RSS라 필리핀에선 동작 불가 |
| `ide/static/customblock_toolbox.js` | **Collect 카테고리 통째로**(wikipedia/weather/news) 미노출. 이것만 남았다 — circul.us·gtts 블록과 대화 블록 3개는 260914v6 에서 **main 에서도 제거**돼 더 이상 델타가 아니다 |
| `GLOBAL_DELTA.md` | **global 전용 문서.** main 으로 가져오지 않는다 |

검증: `git diff --name-status <국내태그> <영문태그>` 결과가 위 16개 항목이고 **모드 차이 0줄**이어야 한다.

※ `system/ph_setup.sh` 는 260914v7 까지 17번째 델타였다. `main` 의
`system/setup_country.sh` 가 대신하면서 델타에서 빠졌다 (아래 '마스터 이미지' 참고).

`ide/templates/index.html` 은 일부러 델타에 넣지 않았다. `?ver` 를 올릴 때마다 바뀌는 파일이라
델타로 두면 릴리스마다 충돌한다. 영문판 전용 파일의 `?ver` 도 `main` 에서 올린다.

### 예제 주의사항

- `examples/` 는 `restore`(공장초기화) 때만 `/home/pi/examples/` 로 복사된다
  (`ide/run_ide.py:369`). 리포만 고쳐서는 기존 기기에 반영되지 않는다 — 수동 복사하거나
  이미지를 다시 만들 것
- **TTS 블록은 `speech_otts_play`(온디바이스)와 `speech_etts_play`(espeak) 둘뿐이다.**
  전자는 `lang="na"`(자동 판별)라 한국어·영어 양쪽을 처리한다. 서버 TTS(`speech_tts*`)와
  gtts(`speech_gtts*`), 번역(`speech_translate`)은 260914v6 에서 제거됐다
- 텍스트 블록 기본값 `가나다` 는 `customblock.js`(수정 금지 파일)에 있다. 예제 안의 값을 바꿔도
  새로 끌어다 놓는 블록은 계속 `가나다` 로 뜬다

---

## 라이선스 (260930)

**리포 전체가 AGPL-3.0 이다**(`LICENSE`, 사용자 결정). 이유는 사물 인식 가중치 `yolo11s.onnx` —
Ultralytics 배포물이고 AGPL-3.0 이다(파일 메타데이터에도 `license = AGPL-3.0` 이 박혀 있다). Ultralytics 는
가중치를 넣은 앱 전체를 파생물로 본다(Discussion #2127). 이 해석은 다툼이 있지만, 소스가 이미 공개돼 있으니
리포를 AGPL 로 내놓아 어느 해석으로도 맞게 했다.

- `LICENSE` — AGPL-3.0 전문(FSF 원문, sha256 `0d96a4ff…abcb0`). 고치지 말 것
- `THIRD_PARTY_NOTICES.md` — 리포 안 남의 코드(Blockly·CodeMirror·jQuery·Font Awesome·TF.js·MediaPipe 등)와
  `/home/pi/.model` 모델의 라이선스 표. **vendor 파일·모델을 넣거나 바꾸면 여기도 고칠 것.** 전부 AGPL 과 같이 쓸 수 있는 것만 넣는다
  (Apache-2.0 · MIT · OFL 은 된다. 비상업·연구 전용 라이선스는 안 된다)
- `system/NOTICE-yolo11s.txt` — 이미지 만들 때 `/home/pi/.model/object/` 에 복사(IMAGE.md)
- IDE [더보기] → **소스 코드 · 라이선스 (AGPL-3.0)**(`#source_bt`) — AGPL §13(네트워크로 쓰는 사람에게 소스 위치 안내).
  링크는 기기 버전(`piBo_260930v2` → 태그 `260930v2`)의 GitHub 트리. 버전 형식이 다르면 리포 첫 화면
- 사물 인식 모델을 Apache-2.0 인 것(D-FINE 등)으로 바꾸면 yolo 고지는 빼도 되지만 **리포 라이선스는 그대로 둔다**
- D-FINE(easydetect)은 보류(260930): 공개 가중치가 640 학습이라 320 에서 coco128 mAP50-95 가 dfine-n 0.147 · dfine-s 0.331
  (yolo11s 0.488). 320 으로 다시 학습해 보고 유의미하면 쓴다
- PiBrain 도 같은 LICENSE·고지·소스 링크를 넣었다(260930, 태그 형식 `YYMMDDvN` / `-gl`)

## 외부 의존

**자사 서버(circul.us)를 쓰는 기능은 260914v6 에서 전부 제거했다.** 서버를 순차적으로
내리는 중이므로 다시 넣지 말 것.

| 제거된 것 | 쓰던 서버 |
|---|---|
| `Speech.stt`, `vision_api`(vision_detect/vision_face) | `o-vapi.circul.us` |
| `Speech.tts` 의 서버 목소리(main/boy/girl/man1/woman1) | `oe-sapi.circul.us` |
| `Dialog.get_dialog_dl`, `nlp_dl`, `speech_api` | `oe-napi.circul.us` |
| `Dialog.translate` + `modules/speech/mtranslate.py` | Google translate_a |
| `Speech.tts` 의 gtts/e_gtts 분기 | Google translate_tts |

IDE 블록 8개(`speech_stt`※ `speech_tts` `speech_tts_play` `vision_call_ai_img(_ext)`
`speech_gtts` `speech_gtts_play` `speech_translate`)와 Tools 의 번역 패널·gtts 목소리도
같이 없앴다.

**남아 있는 외부 통신**

- `collect.py` — 위키백과 / 기상청 / JTBC RSS. 자사 서버가 아니고 **KR 전용**이다
  (PH 툴박스에는 Collect 카테고리가 없다)
- `Dialog.call_llm` — `localhost:50020` (llama-server). 외부 아님

※ `speech_stt` 와 `Speech.stt` 는 260930 에 **기기 안에서 도는 STT 로 되살렸다** — 아래 '음성 인식(STT)'.

음성은 `SpeechOnDevice`(ONNX, `lang='na'` 자동 판별)와 espeak 로 기기 안에서 처리한다.
`SpeechOnDevice` 는 **Supertonic 3**(supertone-inc/supertonic, 31개 언어)이다. `openpibo/modules/speech/mtts.py` 는
원본 `py/helper.py` 와 한 글자도 다르지 않다(2026-09 확인). 쓰는 패키지는 onnxruntime·numpy·soundfile 뿐이다.
원본 requirements 에 적힌 `librosa`·`PyYAML` 은 helper.py 가 import 하지 않는다.

**n-gram 챗봇도 같이 걷어냈다.** `Dialog` 의 `load` `reset` `ngram` `diff_ngram`
`get_dialog` 와 블록 3개(`speech_get_dialog` `speech_load_dialog` `speech_reset_dialog`).
서버를 쓰진 않았지만 데이터(`openpibo_models` 의 `dialog.csv`)가 한글 전용이라 영문
배포판에서 못 썼고, 국내에서도 LLM(`call_llm`)으로 대체된다. `Dialog` 에는 이제
`start_llm` `call_llm` `stop_llm` 만 있고, 생성자가 CSV 를 읽지 않아 기동이 조금 빨라졌다.

---

## 현장 네트워크

**쓸 수 있는 5GHz 채널은 `cfg80211.ieee80211_regdom` 값에 따라 다르다.**
국내·필리핀이 같지 않다.

| regdom | 36 / 40 / 44 / 48 | 52~144 (DFS) | 149 / 153 / 157 / 161 / 165 |
|---|---|---|---|
| `KR` | 20.0 dBm (48 은 17.0) | radar detection | **20.0 dBm — 사용 가능** |
| `MY` | — | — | **20.0 dBm — 사용 가능** |
| `US` | — | — | **20.0 dBm — 사용 가능** |
| `PH` | 17.0 dBm | no IR, radar detection | **disabled — 완전 차단** |
| `JP` | — | — | disabled (일본은 5.7GHz 를 WLAN 에 안 준다. 정상) |
| `00` (world) | — | — | 20.0 dBm, no IR |

**같은 기기 한 대**(Pi 4 · 커널 6.6.62 · 펌웨어 7.45.265 · regdb 2022.06.06)에서
`iw reg set` 으로 국가만 바꿔가며 몇 초 사이에 측정했다. 하드웨어·펌웨어·
`brcmfmac.conf` 는 전부 무관하다.

```bash
for c in KR PH MY US JP 00; do
  sudo iw reg set $c >/dev/null 2>&1; sleep 2
  printf "%-3s : %s\n" "$c" "$(sudo iw phy0 info | grep -E '5745|5785|5825' | tr -s ' ' | tr '\n' ' ')"
done
sudo iw reg set PH
```

**말레이시아는 제약이 없다.** 필리핀만 막힌다.

### ⚠ regdom 은 공유기가 덮어쓴다 (실측)

**붙은 AP 가 802.11d 로 방송하는 country IE 가 cmdline·`iw reg set` 을 이깁니다.**

```
접속 전:  country US          (iw reg set US)
접속 후:  country KR: DFS-JP  ← 한국 공유기가 방송한 값으로 바뀜
```

`iw reg set` 은 USER 힌트인데도 country IE 가 덮어썼다. 즉 `cfg80211.ieee80211_regdom`
에 뭘 박아도 **현장 공유기가 최종 결정권을 갖는다.**

그래서 아래 `--regdom=KR` 우회는 **필리핀에서 보장되지 않는다.** 현지 공유기가 `PH` 를
방송하면 기기가 PH 로 되돌아가고 149~165 가 disabled 가 된다. 붙어 있던 채널이 막히므로
연결이 끊기거나 재접속을 반복할 수 있다.

출처는 스캔으로 직접 확인했다. 붙어 있던 AP 가 `Country: KR` 을 쏘고 있었다:

```
BSS 58:86:94:65:14:46(on wlan0) -- associated
        SSID: pibo
        Country: KR     Environment: Indoor/Outdoor
```

**공유기마다 다르다.** 같은 자리에서 `KR` 을 쏘는 것(iptime·KT·U+), `US` 를 쏘는 것,
아예 안 쏘는 것이 섞여 있었다. 적용되는 건 **접속한 AP 하나**의 값이다.

**미검증:** 필리핀 현장 공유기가 실제로 `PH` 를 방송하는지. FCC 사양 장비는 `US` 를
쏘거나 IE 자체가 없는 경우도 많다. 확인 전에는 우회가 통한다고 가정하지 말 것.

#### 현장에서 확인하는 법

로봇이든 리눅스 노트북이든 한 줄이면 된다. 학교 공유기 SSID 아래 `Country:` 를 본다.

```bash
sudo iw dev wlan0 scan | grep -E "^BSS |SSID:|Country:"
```

| 방송값 | 판단 |
|---|---|
| `PH` | **우회 무효.** `--regdom` 쓰지 말 것. CLM blob 교체 말고 길이 없다 |
| `US` / 미방송 | 우회 유효. `--regdom=KR` 로 149~165 사용 가능 |

#### 결정: `--regdom=KR` 로 굽는다

현지 공유기 값을 출하 전에 확인할 수 없고, Pi 가 로봇 안에 들어가면 SD 를 빼기 어려워
재설정도 현실적이지 않다. 그래서 블라인드로 하나를 정해야 하고, 경우의 수로 보면
KR 이 지는 경우가 없다:

| 현지 공유기 | `PH` | `KR` |
|---|---|---|
| 36~48 | 됨 | 됨 |
| 149~165 + `US`/미방송 | **못 붙음** | **됨** |
| 149~165 + `PH` 방송 | 못 붙음 | 못 붙음 (끊김 반복) |

세 번째 줄은 둘 다 실패고 공유기 채널을 바꿔야만 풀린다. 실패 모양만 다르다.
두 번째 줄은 KR 만 된다. 현장 안내(36~48 고정)를 지키면 세 번째 줄은 생기지 않는다.

**PH 가 막히는 이유는 규제가 아니다.** 커널이 들고 있는 PH 규칙에는 그 대역이 있다:

```
country PH: DFS-FCC
        (5735 - 5835 @ 80), (N/A, 30), (N/A)    ← DFS 아님, 30 dBm 허용
```

규칙이 있는데 적용이 안 된다. `JP` 는 규제대로 정확히 막히므로 **메커니즘 자체는
정상 동작한다** — PH 만 예외다. **원인 미확인.** firmware CLM blob 에 PH 항목이 없어
드라이버가 제한적 기본값으로 떨어지는 것으로 의심하고 있지만 확인 전이다.
추측으로 단정하지 말 것. 그게 맞다면 regdb 를 올려도 안 풀린다.

> `regdom=KR` 을 필리핀 기기에 박으면 상위 채널이 바로 열리지만 **쓰지 말 것.**
> phy#0 world 도메인이 전 대역을 20 dBm 로 캡하므로(`(6, 20)`) 실제 출력은 PH 한도
> (2.4GHz 20 / 5.7GHz 30 dBm) 안에 들어오지만, 설정값 자체가 다른 나라 것이라
> 인증·감사에서 설명이 안 된다.

공유기 설정 규칙:

| 항목 | 값 | 이유 |
|---|---|---|
| 5GHz 채널 | **PH 배포판만 36~48 중 하나로 고정**<br>KR·MY 는 149~165 도 가능 | PH 만 상위 채널이 막혀 있다. `자동` 은 DFS·상위로 옮겨간다 |
| 채널 크기 | **80 이하** | 5GHz 에서 160MHz 블록은 5170~5330(ch50)·5490~5650(ch114) 둘뿐이고 **둘 다 DFS 를 포함한다.** 5735~5835 는 폭이 100MHz 라 160 자체가 불가능하다 |
| 모드 | **11ac** | CYW43455 는 11ax 미지원 |

**무선 확장(리피터)은 백홀 밴드가 서비스 채널을 결정한다. PH 현장에만 해당한다.**
5GHz 백홀이면 확장기 5GHz가 상위 채널에 묶인다 — **PH 기기는 상위가 157이면 전부 떨어진다.**
**백홀을 2.4GHz로 잡으면 확장기 5GHz 채널을 36으로 자유롭게 지정할 수 있다.**
수업 트래픽(태블릿↔로봇)은 확장기 안에서 스위칭되므로 백홀이 2.4GHz여도 병목이 아니다.
단 태블릿도 같은 확장기에 붙어야 한다.

> 5GHz가 막히면 로봇은 AP 모드로 떨어지고 **자력 복귀를 못 한다**(재부팅 필요).
> 공유기 펌웨어 업데이트·재부팅 후 채널이 유지됐는지 반드시 확인할 것.
> 30대가 한꺼번에 떨어지면 30대를 다 재부팅해야 한다.

**왜 복귀를 못 하나 (코드 확인, 260929)** — `system/booting.py` 는 부팅 때 IP 를 27초(3초×9)만 기다리고,
그 뒤 `wifi_update` 가 10초마다 보는데 **IP 가 한 번만 없어도** `hotspot.sh start` 를 부른다. `hotspot.sh` 는
AP 를 켜기 전에 `nmcli connection down pibo-wifi` 로 학교 WiFi 연결을 **직접 내린다** — 사용자가 내린 연결은
NetworkManager 가 다시 붙지 않는다. 그래서 수업에서 30대가 동시에 붙어 DHCP·접속이 수십 초 밀리면 일부가
AP 로 넘어가 그대로 남고, 그 로봇들이 2.4GHz AP 비콘을 쏴서 방이 더 붐빈다.
**적용함(260929, `system/netwatch.py` — 실기기 시험 전)**. **저장된 WiFi 는 늘 있다** — 납품할 때 현장 공유기를 `pibo` / `!pibo0314` 로
맞추고 로봇에도 그 값을 넣어서 준다. 사용자가 [인터넷 설정] 에서 다른 SSID 로 바꿀 수는 있다.
그래서 AP 로 넘어갈지는 '**지금 저장된** SSID(기본 `pibo` 든 바꾼 것이든)가 스캔에 보이는가' 하나로 가른다
(IP 가 없을 때만 스캔 — 붙어 있는 로봇은 건드리지 않는다):

| 상황 | 스캔 | 동작 |
|---|---|---|
| 저장된 SSID 의 공유기가 없음(꺼짐, 다른 장소로 가져감, 공유기 이름을 바꿈) | 안 보임 | **바로 AP** (지금과 같은 속도) |
| 교실에 그 공유기가 있는데 여러 대가 몰려 IP 가 늦음 | 보임 | **90초** 기다린 뒤 AP |
| 보이는데 비밀번호가 바뀜 등 | 보임 | 위와 같음(이 경우만 AP 가 90초 늦다) |

**90초인 이유:** NetworkManager 의 DHCP 대기 기본값이 45초라, 60초면 한 번 실패하고 다시 시도하는 도중에 AP 로 넘어간다.
90초면 두 번째 시도까지 기다린다. 공유기가 없으면 스캔에서 바로 가려지므로 길게 잡아도 손해가 적다.
구현은 기존 10초 점검(`wifi_update`)에서 'IP 없음 + SSID 보임' 이 9번 연속일 때 AP. 부팅 때의 27초(3초×9) 구간은
OLED 표시만 하고 AP 를 켜지 않으므로 그대로 둔다. 지금은 IP 가 없으면 서비스가 뜬 지 약 42초(5+27+10) 뒤 첫 점검에서 AP →
바꾸면 SSID 가 안 보일 때는 그대로 약 42초, 보일 때는 약 2분 10초 뒤 AP.
스캔은 **AP 로 넘어가기 전, IP 가 없을 때만** 본다: 10초 점검마다 `nmcli -t -f SSID dev wifi list --rescan auto`
(마지막 스캔이 30초보다 오래됐을 때만 새로 스캔 — 끊겨 있을 때 NM 이 스스로 하는 스캔을 재사용). IP 가 있을 때와 AP 모드에서는 안 본다
(AP 모드에서도 스캔은 된다 — [인터넷 설정] 의 WiFi 목록이 AP 로 붙어서 `/wifi_scan` → `nmcli dev wifi list` 로 뜬다.
AP 는 스스로 끄지 않으므로 스캔해서 판단할 게 없을 뿐이다).
**확인 필요:** 기기의 `nmcli -g ipv4.dhcp-timeout connection show pibo-wifi` (0 이면 기본값 45초)

**AP 모드는 스스로 끄지 않는다.** AP 로 계속 쓰는 수업도 있다. [인터넷 설정] 으로 학교 WiFi 를 잡아 IP 를 받거나
재부팅하면 나온다. (AP 에 아무도 안 붙어 있으면 2분마다 학교 WiFi 로 돌아가 보는 자력 복귀를 넣었다가 같은 이유로 뺐다 — 다시 넣지 말 것)
- 구조: 판단은 `netwatch.NetWatch.step(has_ip)` 한 곳, `booting.py` 의 `wifi_update` 는 10초마다 부르기만 한다.
  명령(nmcli·hotspot.sh)은 `ops` 로 바꿔 끼울 수 있어 기기 없이 시험했다(10개 경우: 바로 AP · 90초 · 중간에 IP ·
  AP 모드 1시간 유지 · AP 에서 IP 받으면 끔 · SSID 안 보임). `wifi_update` 는 예외가 나도 다음 점검을 이어간다(전엔 멈췄다)
- `hotspot.sh` 는 그대로다(AP 를 켤 때 학교 연결을 내리는 것도 그대로)
- **기기에서 볼 것:** ① 교실처럼 IP 가 늦을 때 90초 기다리는지 ② 공유기를 끄면 약 42초 뒤 AP
  ③ AP 모드가 계속 유지되고, [인터넷 설정] 으로 학교 WiFi 를 잡으면 AP 가 꺼지는지
  ④ `journalctl -u booting.service | grep netwatch` 로 판단 기록 확인. PiBrain(`openpibo-os.pibrain/system/booting.py`)도
  같은 구조(IP 한 번 없으면 AP)지만 아직 안 옮겼다
**확인 필요:** AP 를 켤 때 학교 연결을 내리는 게 CYW43455 의 AP+STA 같은 채널 제약 때문인지

WiFi 절전은 `system/init` 이 부팅 때 `iw wlan0 set power_save off` 로 끈다(260929 기기 확인: off).
**확인 필요:** NetworkManager 가 재접속할 때 다시 켜는지 — 켜지면 연결에 `802-11-wireless.powersave 2` 를 넣을 것

30명 규모 대역폭 (260929 개정): 카메라는 320×240 JPEG 를 **바이트 그대로**(base64 아님) 보낸다.
60장 중앙값 품질 80 은 17.8KB, 70 은 13.9KB.

| 무엇 | 평소 | 비고 |
|---|---|---|
| 분류기 카메라 (품질 80, 학습 입력) | 2 FPS · 대당 약 0.29 Mbps | [꾹 눌러 모으기] 동안만 약 6.7 FPS · 약 1 Mbps |
| 도구 [카메라] (품질 70) | 2 FPS · 대당 약 0.23 Mbps | 전엔 base64·품질 80 이라 0.39 Mbps |

- **탭이 가려지면 보내지 않는다.** 도구는 `visibilitychange` 에 `vision_sleep`, 분류기는 `camera_visible` 로 서버가
  보이는 화면이 하나라도 있을 때만 읽고 보낸다(카메라는 끄지 않는다 — Picamera2 는 다시 켜는 데 오래 걸린다).
  전엔 학생이 다른 탭·앱으로 가거나 태블릿 화면이 꺼져도 계속 보냈다
- 무선은 AP 를 거치며 airtime 을 2배 쓰므로 분류기 평소 30대면 약 18 Mbps, 전원이 동시에 모으면 약 60 Mbps.
  5GHz 80MHz 한 채널이면 여유가 있고, **2.4GHz 로는 안 된다**
- **처음 열 때 받는 양이 더 크다.** 분류기는 대당 약 9~10MB(MediaPipe wasm 11.2MB → gzip 3.3MB, 모델 3.6~5.6MB 는
  이미 압축돼 안 준다) → 30대면 약 300MB. 한 번 받으면 브라우저 캐시에 남으니 **수업 전에 태블릿마다 한 번 열어 둘 것**.
  강력 새로고침(Ctrl+Shift+R)은 캐시를 버리므로 업데이트 직후에만. IDE·도구·분류기 모두 gzip(도구는 260929 에 추가, JS·CSS 500 → 133KB)
- 글꼴은 IDE 한 벌을 세 앱이 같이 쓰고 두 굵기만 싣는다(260929) — 처음 한 번 최대 약 0.54MB + 아이콘 글꼴. '다듬기' 절 참고
- 공유기 한 대에 로봇 30 + 단말 30 = 60대는 동시접속 한계에 걸리니 유선 백홀로 AP 2대를 권한다. 30대를 한꺼번에 켜지 말고
  모둠별로 10~20초 간격으로 켜면 접속·DHCP 가 덜 몰린다

---

## 마스터 이미지

카드 뜨기·PiShrink·구운 뒤 검증은 **`IMAGE.md`** 에 있다.
Raspberry Pi Imager 의 "OS 커스터마이즈" 는 쓰지 말 것 — `custom.toml` 이 남아
첫 부팅에 `cmdline.txt` 를 다시 건드린다.

### 납품 국가

`sudo bash system/setup_country.sh <국가코드> [--regdom=XX]` 를 이미지 만들 때 한 번
돌린다. timezone · wifi country · `cmdline.txt` 의 `cfg80211.ieee80211_regdom` ·
`brcmfmac.conf` 잔재 · 실행비트를 한 번에 맞춘다. 멱등이라 재실행해도 안전하다.

| 국가 | 명령 | timezone | regdom | 브랜치·태그 |
|---|---|---|---|---|
| `KR` | `setup_country.sh KR` | `Asia/Seoul` | `KR` | `main` / `YYMMDDvN` |
| `PH` | **`setup_country.sh PH --regdom=KR`** | `Asia/Manila` | **`KR`** | `global` / `YYMMDDvN-gl` |
| `MY` | `setup_country.sh MY` | `Asia/Kuala_Lumpur` | `MY` | `global` / `YYMMDDvN-gl` |

**필리핀만 regdom 을 분리한다.** timezone 은 `Asia/Manila` 그대로다.

> **이 우회는 공유기가 `PH` 를 방송하면 풀린다** — country IE 가 regdom 을 덮어쓴다(실측).
> 그래도 KR 로 굽는 이유는 '현장 네트워크 → 결정' 참고. 그 경우는 `PH` 로 구워도 똑같이
> 못 붙는다. 현장 안내(36~48 고정)가 실제 방어선이다.

`PH` 로 두면
149~165 가 통째로 막히는데 그건 규제가 아니라 CLM blob 결함이라 ('현장 네트워크' 참고),
실제로 못 쓰는 채널을 현장 공유기 제약으로 떠넘기지 않으려는 것이다.

무선 관련 설정(wifi country, cmdline regdom)은 **전부 regdom 값으로 통일한다.**
timezone 만 국가를 따른다. 둘을 섞어두면 부팅 후 한쪽이 다른 쪽을 덮어써서
원인 추적이 불가능해진다.

`MY` 는 `PH` 와 달리 blob 에 상위 채널이 살아 있어 분리가 필요 없다.

**`global` 브랜치는 '영문 배포판'이다**(예전 이름 `ph` 는 필리핀만 가리키는 것처럼 보여서 바꿨다). 말레이시아도 UI·예제가
영문으로 같으므로 같은 태그를 쓰고, 국가 차이는 위 스크립트가 이미지에 넣는 값뿐이다.
**국가별 브랜치를 새로 만들지 말 것** — 델타가 배로 늘고 merge 대상이 늘어난다.
UI 를 현지어(말레이어 등)로 바꿔야 할 때만 별도 논의 대상이다
(`ko2en.js` 189개 키 + Blockly 로케일).

등록 안 된 국가코드는 스크립트가 usage 만 찍고 멈춘다. 추가할 때
**국가코드에서 timezone 을 추측하지 말 것** — `timedatectl list-timezones` 로 확인하고
`case` 에 넣는다.

---


### WiFi 저장(`booting.py` `POST /wifi`, 260929)

SSID·비밀번호·ID 는 `subprocess.run(['sudo', conwifi.sh, 종류, ssid, ...])` 인자 목록으로 넘긴다. 전엔
`os.system(f"... '{ssid}' '{psk}'")` 라 `'` 가 들어가면 따옴표가 닫히고 그 뒤가 **root 명령으로 실행**됐다
(8080 은 로그인 없이 받고 AP 모드에서도 열려 있다). `Kim's WiFi` 같은 이름은 연결도 안 됐다.
SSID 가 비면 실패 안내를 돌려준다(전엔 정의 안 된 `ex` 로 500). 비밀번호는 로그에 남기지 않는다.
**셸 문자열에 사용자 입력을 넣지 말 것** — `tools/lib.py` 의 espeak 도 같은 이유로 고쳤다

## 릴리스 절차

### 1. main

```bash
git checkout main && git pull
# 작업...
chmod +x <실행파일>          # git add 전에! (아래 '자주 나는 실수' 참고)
bash docs/build.sh [http://<IDE 주소>/]   # 태그 전에 도움말 다시 빌드 (아래 '도움말(docs)')
git add -A && git commit -m "..."
git push origin main
git tag -a YYMMDDv1 -m "KR release YYMMDDv1"
git push origin YYMMDDv1
```

### 도움말(docs) — 태그 전에 빌드 (260930)

IDE [도움말] 은 `booting.py`(8080) 가 리포의 `docs/build` 를 그대로 보여 준다. **빌드 결과가 리포에 커밋돼 있으므로
라이브러리·블록을 고치고 빌드하지 않으면 옛 문서가 배포된다**(260914v6 빌드가 260930 까지 그대로였다 — STT·분류기가 빠지고
없어진 번역·대화 블록이 남아 있었다).

- `bash docs/build.sh` — `make clean html` + 페이지마다 API 가 비지 않았는지 확인. 인자로 IDE 주소를 주면 블록 가이드
  (`docs/source/blocks/guide.md`)를 툴박스에서 다시 뽑는다(`docs/tools/gen_block_guide.py`, playwright 필요). 블록을 고쳤으면 주소를 줄 것
- **기기 밖(PC·컨테이너·웹 세션)에서 빌드한다.** `conf.py` 가 설치 안 된 하드웨어 패키지(picamera2·dlib·board 등)만 autodoc 용 가짜로
  바꾼다(기기에는 다 있어서 결과가 같다). numpy·opencv 가 있는 파이썬 + `docs/requirements.txt`. 파이썬은 `PY=` 로 고른다
- 테마는 **Furo**(MIT, 260930 — 예전 sphinx_rtd_theme). 밝게·어둡게는 브라우저를 따르고 외부 글꼴·CDN 이 없어 AP 모드에서도 된다.
  색은 `conf.py` `html_theme_options`, 덧칠은 `source/_static/mycss.css`
  글꼴은 IDE 와 같은 Pretendard 두 벌을 `source/_static/fonts/` 에 싣는다(8080 은 IDE 글꼴을 못 받는다 — 없으면 윈도에서 맑은 고딕으로 떨어져 촌스러웠다).
  첫 화면은 카드 4개(`index.rst` 의 raw html), API 페이지 제목은 `모듈 · 한국어 설명`
- 손으로 쓰는 페이지: `notes/piboMaker.md`(IDE·도구·분류기·대화 사용법, 캡처는 `notes/images/*`), `notes/software.md`, `notes/hardware.md`.
  화면을 크게 바꾸면 캡처도 다시 찍을 것
- `global` 에도 같은 `docs/build` 가 간다(문서는 한국어 한 벌. 델타 아님)

### 2. global

```bash
git checkout global && git pull
git merge main
# 충돌 처리 (아래 참고)
git push origin global
git tag -a YYMMDDv1-gl -m "Global release YYMMDDv1-gl"
git push origin YYMMDDv1-gl
```

### 3. 기기 검증

기기 작업본 구조:

- `/home/pi/openpibo-os` 는 심볼릭 링크(root 소유) → `/home/pi/.openpibo-os.pibo` (실제 클론, pi 소유)
- systemd 유닛(`ide.service`, `booting.service`)은 링크 경로를 쓴다. 링크는 건드리지 말 것
- 클론이 **shallow(`grafted`)** 다. `git fetch origin --tags` 로는 새 태그를 못 받으므로
  태그를 콕 집어 받아야 한다: `git fetch --depth=1 origin tag <태그>`
- 서비스가 작업본을 직접 실행한다. 기기를 `git checkout main` 상태로 두지 말 것

재클론이 가장 확실하다 (shallow fetch 꼬임 없음).

> **⚠️ AP 모드에서는 인터넷이 없다.** `booting.py` 는 유선·무선 IP가 없을 때만 AP를 켜므로,
> AP로 접속했다는 건 업링크가 끊겨 있다는 뜻이다. 이 상태에서 `git clone` 은 반드시 실패한다.
> **기존 작업본을 먼저 지우면 기기가 통째로 죽는다** — 링크가 깨져 `ide.service` ·
> `booting.service` 가 못 뜨고, AP를 올리는 게 `booting.py` 라 접속 수단까지 사라진다.
> (LED·인사 동작도 `booting.service` 라 "전원이 안 켜진 것"처럼 보인다. 리눅스는 살아있다.)
> 복구는 랜선을 꽂고 `ssh pi@<유선IP>` 로 들어가 다시 클론하는 것뿐이다.

**받아서 확인한 뒤에 교체한다. 지우는 건 마지막이다.**

```bash
# 0) 인터넷 확인 — 실패하면 여기서 멈춘다
ping -c2 -W3 github.com || echo "!! 인터넷 없음 (AP 모드?). WiFi/유선 연결 후 다시 시작"

# 1) 새 위치에 먼저 받는다. 실패해도 기존 작업본은 그대로다
cd /home/pi
git clone --depth 1 --branch YYMMDDv1-gl \
  https://github.com/themakerrobot/openpibo-os.pibo.git .openpibo-os.new

# 2) 받은 게 맞는지 확인. 여기서 이상하면 중단하고 .openpibo-os.new 만 지우면 된다
cd /home/pi/.openpibo-os.new
git describe --tags
head -n1 ide/static/ko2en.js
ls -l system/hotspot.sh system/setup_country.sh system/booting.py

# 3) 교체
sudo systemctl stop ide.service booting.service
cd /home/pi
sudo rm -rf /home/pi/.openpibo-os.old
sudo mv /home/pi/.openpibo-os.pibo /home/pi/.openpibo-os.old
mv /home/pi/.openpibo-os.new /home/pi/.openpibo-os.pibo
sudo chown -R pi:pi /home/pi/.openpibo-os.pibo

echo piBo_YYMMDDv1-gl > /home/pi/.OS_VERSION
sudo systemctl start ide.service booting.service
sleep 3
systemctl is-active ide.service booting.service

# 4) 정상 확인 후 백업 삭제
sudo rm -rf /home/pi/.openpibo-os.old
```

지우기 전에 `git status --short --ignored` 로 살릴 파일(녹음 `.wav`, 이미지 등)이 없는지 볼 것.
사용자 데이터는 보통 `/home/pi/openpibo-files` 라 별개다.

**`sudo` 없이는 삭제가 실패한다.** 디렉토리는 `pi` 소유지만, 서비스가 root로 실행되므로
`__pycache__` 가 root 소유로 생긴다. 클론 직후 `chown -R pi:pi` 를 해도 서비스가 뜨면 다시 생기니
매번 `sudo rm -rf` 가 필요하다. (유닛에 `Environment=PYTHONDONTWRITEBYTECODE=1` 를 주면
아예 안 생기지만, 유닛 파일은 리포 밖이라 이미지 작업이다.)

`cd` 를 `rm` 앞에 두지 말 것 — `cd` 가 실패한 상태에서 상대경로 `rm -rf` 가 돌면 엉뚱한 곳을 지운다.

검증:

```bash
cd /home/pi/openpibo-os
git describe --tags                                      # YYMMDDv1-gl
head -n1 ide/static/ko2en.js                             # const blang = 'en';
ls -l system/hotspot.sh system/setup_country.sh system/booting.py   # 전부 -rwxr-xr-x
curl -s http://localhost/static/ko2en.js | head -n1
```

브라우저는 **Ctrl+Shift+R** 로 강력 새로고침. `?ver` 를 올렸어도 페이지 자체가 캐시돼 있다.

---

## 도구 서비스 수명

`tools.service`(50000), `classify.service`(50010), `llama-server.service`(50020) 는
**셋 중 하나만** 돈다. 포트는 PiBrain 과 같다(260930 에 PiBrain 도구 50040 → 50000, 파이보 H/W 검수 8000 → 50050 으로 맞춤).
H/W 검수(`test/test.py`, 50050)는 유닛이 아니라 IDE 의 `/hwtest` 가 직접 띄우고, 켤 때 셋을 다 끈다. IDE가 하나를 켤 때 나머지를 stop 한다 (`ide/run_ide.py` 의
`/tools` `/classifier` `/llm` 핸들러). 부팅 시엔 안 뜬다.

**종료는 탭이 닫힐 때 브라우저가 알린다.** 각 페이지의 `beforeunload` 가
`/tools?enable=off` · `/classifier?enable=off` 를 부른다. 이 fetch에는
**`{ keepalive: true }` 가 반드시 있어야 한다.**

```js
fetch(`http://${location.hostname}/tools?enable=off`, { method: 'GET', keepalive: true })
```

`keepalive` 없이 그냥 `fetch(url)` 로 두면 브라우저가 언로드 도중 요청을 **취소**한다.
260624v1부터 260909v5까지 이 옵션이 없어서 tools·classifier는 탭을 닫아도 안 꺼졌다.
llama.cpp 웹 UI에는 `keepalive: true` 를 넣어 빌드했기 때문에 llm만 정상 동작했고,
그 차이가 원인을 특정하는 근거가 됐다.

이 밖의 정리 경로:

- IDE에서 **코드 실행** — `run_ide.py` 의 `execute` / `executeb` 가 3개 서비스를 전부 stop 한다
  (`subprocess.Popen(['systemctl','stop',...])` ×3). 수업 중에는 이게 계속 일어나므로,
  `enable=off` 가 죽어 있던 동안에도 실사용에서 티가 안 났다
- **다른 도구로 전환** — 켜는 쪽 핸들러가 나머지를 stop 한다
- 재부팅 / `sudo systemctl stop tools.service`

### 손대기 전에 알아야 할 것

`beforeunload` 는 탭 닫기·이동·새로고침에만 뜨고 **백그라운드 전환에는 안 뜬다.**
그래서 학생이 잠깐 자리를 비워도 서비스가 살아있다. 이게 이 방식의 핵심 장점이다.

시도했다 되돌린 방법 — 다시 하지 말 것:

1. **소켓 유휴 타임아웃** (`idle_watchdog`, 260909v5에 넣었다 260909v6에서 제거) —
   마지막 socket.io 접속이 끊기고 N초 뒤 SIGTERM. 태블릿 절전·앱 전환도 소켓을 끊으므로
   **자리 비움과 탭 닫기를 구분하지 못한다.** 돌아왔을 때 서비스가 죽어 있어 원래 버그보다 나쁘다
2. **`pagehide` 로 교체** — `beforeunload` 와 달리 백그라운드 전환에서도 뜬다.
   `e.persisted` 로 걸러야 하는데 소켓이 열린 페이지의 bfcache 적격 여부가 브라우저마다 달라
   신뢰할 수 없다

### 여는 방식 (260923)

IDE 의 [도구][대화][분류기] 는 누르는 **그 순간** 이름 붙인 새 탭
(`pibo_tools` / `pibo_llm` / `pibo_classifier`)을 `ide/static/launch.html` 로 연다.
그 대기 페이지가 `/<svc>?enable=on` 을 보내고, 실제로 응답할 때까지 기다린 뒤
스스로 서비스 주소로 이동한다(`location.replace`).

- 도구·분류기: 포트가 열렸는지를 `fetch(..., {mode:'no-cors'})` 로 본다(CORS 헤더 불필요)
- 대화: llama-server `/health` 가 모델 로딩 중 503, 준비되면 200. 포트만 보면 로딩 중에 들어가 버린다
- 켜기 요청을 5초마다 다시 보낸다. 같은 탭에서 떠나는 이전 도구 페이지의 `enable=off` 가
  늦게 도착해도 결국 켜진 상태로 끝나게 하려는 것이다
- 전에는 무조건 3초 뒤 `window.open` 했다 — 클릭에서 3초가 지나 팝업으로 막힐 수 있었고,
  대화 모델은 3초 안에 안 떠서 빈 화면이 먼저 떴고, 실패하면 스피너가 계속 돌았다
- 도구·분류기 헤더의 [IDE] 는 스크립트로 연 탭이면 `window.close()`, 아니면 IDE 로 이동.
  둘 다 `beforeunload` 가 서비스를 끈다. 대화(llama.cpp UI)에는 이 버튼을 넣을 수 없다
- 서비스가 꺼지면(다른 도구 켜기·코드 실행) 그 탭의 소켓이 끊기고 배너가 [다시 켜기] 를 준다

남은 문제: **탭 두 개 중 하나만 닫아도 서비스가 죽는다.** 이름 붙인 탭으로 IDE 버튼을 여러 번
눌러도 탭은 하나지만, 사용자가 탭을 직접 복제한 경우는 여전히 해당된다. 접속 수를 아는 건 tools/classifier
자신뿐이므로, 종료 판단을 그쪽으로 옮겨야 한다. IDE 셸(네비게이터) 작업과 함께 다룰 것.

참고: `@app.sio.on('connect')` / `('disconnect')` 는 `fastapi_socketio` 에서 정상 동작한다(검증함).
`ide/run_ide.py` 의 `@app.sio.on('connection')` 은 Node.js 이벤트 이름이라 **한 번도 안 불린다.**

---

## 분류기 (260924)

teach-lab 과 같은 기능(이미지·손·얼굴·포즈 가르치기)을 파이보 카메라로 한다.
**TensorFlow 를 쓰지 않는다.** 예전 분류기(TF.js MobileNetV2 → keras 변환 → TF 로 추론)를 통째로 바꿨다.

| 단계 | 어디서 | 무엇으로 |
|---|---|---|
| 카메라 | 파이보 → 태블릿 | socket.io `camera_image`, 320×240 JPEG |
| 특징 뽑기·학습 | 태블릿 브라우저 | MediaPipe wasm(`static/vendor/tasks-vision`) + TF.js 작은 MLP |
| 저장 | 파이보 | `POST /api/models` → `/home/pi/mymodel/<이름>/` |
| 추론 | 파이보 | `openpibo.vision_classify.CustomClassifier` — LiteRT(이미지) / MediaPipe(손·얼굴·포즈) + numpy |

모델 폴더 하나에 `project.json` `classifier.json` `classifier.bin` `labels.txt` `samples.json`
과 특징 모델 파일(`.tflite`/`.task`)이 들어간다. teach-lab 파이썬 내보내기와 같은 형식이라
`pip install teachlab` 으로 PC 에서도 돈다. `samples.json` 은 [이어서 배우기] 용이다.

블록: `[분류기 모델 … 불러오기]`(260929 전엔 '이미지 모델 설정하기')에 폴더 `mymodel`, 이름 칸에 모델 이름.
예전엔 이름 칸이 둘(모델·라벨)이었는데 라벨 칸을 뺐다(260930v9, 두 리포). 예전에 저장한 프로그램은 `customblock_callback.js` 끝의
불러오기 감싸개가 `labelpath` 입력을 걷어내고 연다(없는 입력이 있으면 Blockly 가 `MissingConnection` 으로 멈춘다 — 없는 필드는 경고만).
폴더 선택은 그대로 둔다(사용자). '폴더 선택'(빈 값)이면 `cf.load(''+'과일')` → `/home/pi/mymodel/과일`.
파이썬 `CustomClassifier.load(model_path)` 도 인자 하나다(260930v9 — 예전 블록에 맞춰 두었던 안 쓰는 `label_path` 를 뺐다).
예전 블록이 만든 파이썬을 `.py` 로 저장해 둔 경우 `load(a, b)` 는 TypeError 가 난다 — 두 번째 인자를 지우면 된다.
**예전 `model.keras` 는 못 읽는다** (불러오면 다시 학습하라는 오류). 의도한 호환 단절이다.

### 가져온 코드 — 두 곳을 함께 고칠 것

- `classifier/static/tl/` ← teach-lab `lib/` (74f421a). 바꾼 곳은 파일 첫 줄에 적었다(경로, `mirror:false`)
- `openpibo/modules/teachlab/` ← teach-lab `python/teachlab/`. 바꾼 곳은 `load_interpreter()` 하나
- 브라우저와 파이썬이 **같은 숫자**를 내야 한다. 정규화 식(`features.js` ↔ `landmarks.py`),
  자르기(`cropTo` ↔ `crop_to`)를 한쪽만 고치면 학습한 모델이 파이보에서 엉뚱한 답을 낸다
- 로봇 카메라는 거울이 아니다. 어느 소스도 좌우를 뒤집지 않는다
- 파이보는 추론 전에 카메라 그림을 짧은 변 240 으로 줄인다(`_as_stream_rgb`). 브라우저가 학습 때
  본 그림과 크기를 맞추려는 것이다. 스트림 크기를 바꾸면 여기도 바꿀 것
- **스트림(`run_classify.py` 의 `to_jpeg`)도 같은 식(짧은 변 240, 비율 유지)이다(260930).** 전엔 늘 320x240 으로 줄여서
  PiBrain 세로 카메라(480x640 — 카메라를 90° 돌려 달아 `read()` 가 돌려 준다)는 찌그러진 채 학습되고 추론은 안 찌그러져 답이 어긋났다.
  파이보(640x480)는 결과가 예전과 바이트까지 같다. 화면 칸 비율도 받은 그림을 따른다(`--ar-w/--ar-h`)

### 검증 (컨테이너, 가짜 카메라)

브라우저(headless Chromium)로 네 소스를 학습·저장하고 같은 사진을 `CustomClassifier` 로 돌렸다.
답은 6/6 일치. 특징 코사인: 손 0.99, 이미지 0.96~0.98(JPEG 차이), 얼굴 0.83~0.94.
얼굴이 낮은 건 브라우저 wasm 과 파이썬 MediaPipe 의 버전 차이다. 경계에 있는 그림은 한쪽만
잡기도 한다(손 사진 1장을 파이썬만 잡음). **파이보의 MediaPipe 버전으로는 미검증.**

### 막아 둔 것

MediaPipe wasm 이 1분마다 `odml.pa.googleapis.com/v1/log` 로 사용 기록을 보낸다. 끄는 옵션이
없어 `app.js` 맨 위에서 `fetch` 를 감싸 그 주소만 204 로 돌려준다(그러면 MediaPipe 가 전송을 멈춘다).
vendor 파일을 갈아 끼울 때 이 동작이 그대로인지 확인할 것.

### 기기 요구

기기(260923 pip 목록)에 이미 있는 것으로 돈다: `tflite-runtime` 2.14.0 · `mediapipe` 0.10.18 ·
`onnxruntime` 1.20.1 · numpy 1.26.4. **이 버전 그대로** 컨테이너에서 브라우저가 저장한 모델을 돌려
답 8/8 일치를 확인했다. `load_interpreter()` 는 `tflite_runtime` 을 고른다(LiteRT 설치 불필요).
TensorFlow·torch 걷어내기 순서와 지울 목록은 IMAGE.md. 파이보에서 실제 추론 속도·메모리는 아직 못 쟀다.
포즈는 한 화면에 여러 사람이 있으면 브라우저와 파이썬이 다른 사람을 잡을 수 있다(특징 코사인이 0.3 까지 떨어진 적 있음).

---

## 음성 인식 · TTS · 메모리 (260930)

### STT — `openpibo.speech.SpeechToText`, `Speech.stt`

- 모델: **SenseVoiceSmall int8**(한·영·중·일·광둥어, 언어 자동 판별) + **silero VAD**, 실행은 **sherpa-onnx 1.13.8**
  (자기 전용 onnxruntime 을 따로 싣는다 — 기기 onnxruntime 1.20.1·numpy 1.26 은 안 건드린다). 모델은 `/home/pi/.model/stt`
- `listen(timeout, filename, end_silence=0.8)`: `arecord -D plug:dmic_sv -c2 -r 16000 -f S32_LE -t raw`(Audio.record 와 같은 장치)를
  흘려받아 VAD 로 **말이 끝나면(0.8초 조용) 멈춘다.** `timeout` 은 최대 대기. 말이 없으면 빈 문자열. 소리가 작으면 최대 20배 키운다
- `transcribe(audio, sr)`: 25초 넘는 소리는 VAD 로 말 단위로 잘라 받아 적는다(통째로 넣으면 글자가 뒤섞였다)
- **`Speech.stt(filename, timeout, verbose)` 와 블록 `speech_stt` 는 예전(서버 STT) 이름·입력 그대로**다. 옛 프로그램이 그대로 열린다.
  블록 앞의 번개(인터넷 필요) 그림만 뺐다. 모델은 처음 부를 때 한 번 올린다(파이보에서 5~12초)
- sherpa-onnx 한국어 스트리밍 zipformer 는 쓰지 않는다(빈 결과 버그, k2-fsa/sherpa-onnx#2886). Moonshine 한국어 Tiny/Base 는
  비상업 라이선스라 뺐다. SenseVoice 모델 라이선스(FunASR)의 상업 조건은 **확인 필요**
- **파이보 마이크 소리에는 큰 DC 가 섞여 있다**(실측 약 -0.37, 몇 초에 걸쳐 조금씩 변함. 켤 때 0.5 로 튀기도 함).
  그대로 두면 silero VAD 가 말을 한 번도 못 잡아 `listen` 이 빈 글자를 돌려줬다(260930v1). 인식 모델은 DC 가 있어도 받아 적었다.
  그래서 `listen` 은 받는 대로 `_dc_block`(1차 고역 통과, 약 13Hz)으로 DC 를 걷고, VAD 에는 최근 최대 크기로 키워(최대 30배) 넣는다.
  `Audio.record` 는 sox 로 채널만 합치므로 녹음 파일에 DC 가 그대로 있다(STT 와 별개, 손대지 않음)
- 파이보 실측(260930v2): 말 두 번 모두 "안녕하세요 파이보입니다.", 말 없을 때 빈 글자, 모델 적재 4.9초.
  TTS 파일을 바로 넣으면 한·영 원문대로(영어 Pibo → Pebo). 컨테이너(가짜 마이크, DC·켤 때 튐 흉내) 13/13 + 기존 8/8.
  **서보가 움직일 때의 인식률·잘못 잡힘은 확인 필요**

### TTS 를 int8 로 (260930)

`/home/pi/.model/tts/assets/onnx` 를 Supertonic 3 int8 변환본(`leeyunjai/edge-lab` 의 `tts-int8`, vocoder 만 fp32 — story-play 와 같은 것)으로
바꿨다. 파일 이름이 같아 **코드는 그대로**다. 380MB → 178MB, 올린 메모리 약 606MB → 약 330MB, 합성 7.84초 → 6.05초(5.2초 문장).
음질은 들어 보고 괜찮다고 판단(사용자). 변형 모델이라 `MODIFICATIONS.md`·`LICENSE-OpenRAIL-M.txt` 를 같은 폴더에 둔다(OpenRAIL-M)

### 파이보 실측 (cd488e95, Pi 4 · RAM 1796MB · SD 스왑 2GB)

| 올린 것 | 메모리 |
|---|---|
| 기본(OS + IDE + booting) | 약 250MB 사용, 여유 약 1.5GB |
| llama-server (Gemma 3 1B Q4_K_M 806MB, `--ctx-size 2048`) | RSS 897MB (대부분 모델 파일 매핑) |
| TTS int8 + STT 를 올린 학생 프로그램 | 약 637~725MB |

- **셋(LLM·TTS·STT)을 동시에 올리면 여유가 거의 0 이다.** LLM 이 대답을 만들 때는 모델 806MB 가 전부 메모리에 있어야 해서
  `free` 의 '여유'를 믿으면 안 된다. 측정 중 SD 스왑이 29 → 170MB 로 늘었다. **fp32 TTS 로는 안 들어간다**
- 인식 5.2초 음성 1.33초, 합성 5.2초 문장 6.05초(int8). 대화 한 바퀴는 합성이 가장 느린 고리다 — 줄이려면 문장 단위로 쪼개 첫 문장부터 말하기
- 실제 대화 한 바퀴(녹음 → STT → LLM 생성 → TTS → 재생)에서의 시간·스왑은 **아직 안 쟀다**

### `/home/pi/.model` 과 `requirements.txt`

- `/home/pi/.model` 은 리포 밖(이미지)이다. 구성과 파일별 sha256 은 그 폴더의 `VERSION`. 코드가 읽는 것: `tts/assets/{onnx,voice_styles}`,
  `stt/`, `llm/llm-model.gguf`(링크), `object/yolo11s.onnx`, `hand/*.task`, `face/{detection,age-gender,emotion,landmark}`.
  `classifier/`(예전 TF 가중치)는 260930 에 지웠다(아무도 안 씀)
- 모델은 `leeyunjai/themaker`(HF)에서 손으로 받는다. **`git clone` 말고 `huggingface-cli download`** — clone 은 `.git/lfs` 에 한 벌을 더 남긴다(이번에 약 400MB)
- `requirements.txt`(리포 맨 위): 리포 코드가 직접 import 하는 패키지만, 기기 버전으로. `test/requirements.txt` 는 260923 전체 스냅숏(TF·torch 포함)
- **안 쓰는 패키지 걷어내기는 `system/venv_prune.py`(260930).** 기기에서 돌리면 `ROOTS`+`requirements.txt` 와 그 의존만 남기고 나머지를 목록으로 보여 주고,
  `--apply` 로 지운다(백업 목록·pip check·import 확인까지). 260930 두 기기 site-packages 5.5~5.6GB 의 대부분이 TF·torch·MeloTTS 잔재다.
  mediapipe 0.10.18 은 jax 를 불러오지 않는다(지우고 확인함, `--jax`). 패키지를 새로 쓰게 되면 `ROOTS` 와 `requirements.txt` 둘 다에 넣을 것. 자세한 건 IMAGE.md

## 사물 인식 (260924)

`openpibo.vision_detect.Detect.detect_object` 는 **ultralytics·torch 없이** onnxruntime 으로
YOLO ONNX 를 돌린다(`openpibo/modules/yolo_onnx.py`). 기본 모델은 그대로
`/home/pi/.model/object/yolo11s.onnx`.

- ultralytics `predict(conf=0.5, iou=0.4, imgsz=320)` 와 **같은 결과**다. coco128 128장에서
  `detect_object` 반환값이 예전 코드와 128/128 같았다(320 고정 · 동적 · 640 고정 모델 모두)
- 입력 크기: 모델에 고정돼 있으면 그 크기, 동적이면 320(`OBJECT_IMGSZ`). 동적 모델은 ultralytics 처럼
  32 배수까지만 채운다(640×480 → 320×256). 이걸 정사각형으로 채우면 결과가 달라진다
- 클래스 이름: ONNX 메타데이터 `names`(ultralytics export 가 넣는다) → 없으면 모델 옆 `labels.txt`.
  그래서 `load_object_model` 블록으로 올리던 사용자 YOLO 모델도 그대로 읽힌다
- 모델은 처음 `detect_object` 를 부를 때 올린다. `Detect()` 만 만들고 QR·마커만 쓰면 메모리를 안 쓴다
- mediapipe 도 `load_hand_gesture_model` 에서 처음 import 한다. 손 제스처를 안 쓰면 안 올라온다
  (기기 버전 0.10.18 기준 +87MB). 포즈는 MoveNet 그대로 — MediaPipe Pose Lite 보다 7배 빠르고 모델 메모리가 1/4
- 컨테이너 x86 4코어, 320: 예전(ultralytics) 최대 838MB · 53ms → 지금 194MB · 27ms.
  torch import 가 대부분이었다. **파이보 실측은 아직**

RT-DETR 은 쓰지 않는다. 320 에서 정확도가 크게 떨어졌다(coco128 mAP50-95 0.275 vs yolo11s 0.488).
공개 가중치가 640 으로 학습돼 있어서다. 쓸 일이 생기면 320 으로 학습·export 한다.

---

## 화면 v2 (260924) — 시안 B, **유일한 화면**

260924 부터 기본이었고, **260929 에 예전 화면(v1)을 지웠다**(이 절 끝 'v1 삭제'). 이름에 남은 'v2'
(`ide/static/v2/`, `body.pb-v2`, `--v2-*`)는 그대로 둔다 — 바꾸면 고칠 곳만 늘어난다.

**PiBrain(openpibo-os.pibrain)도 같은 화면·키트·분류기를 쓴다(260924).** 원본은 이 리포다.
`design/`·`ide/static/v2/`·`ide/templates/index.html`·`classifier/`·`openpibo/vision_classify.py`·`modules/teachlab/` 을
고치면 PiBrain 에도 옮길 것(키트는 `design/sync.sh ~/openpibo-os.pibrain`). PiBrain 에서 다른 점은
그쪽 CLAUDE.md '화면 v2' · '분류기' 표에 있다(배터리 칸 없음, 언어 키 `classifier_language` 등).
시안 A·B·C(Scratch식·MakeCode식·Arduino식) 중 **B(MakeCode식)** 로 정했다(260924).

- IDE: `run_ide.py` 의 `/` 는 늘 `templates/index.html`(`body.v2-app`). CSS·JS 는 `ide/static/v2/ide.css` · `ide.js`
- `index.js` 는 v1 시절부터 쓰던 한 벌이다. `index.js` 에서 id 를 바꾸거나 새 요소를 찾게 되면 `templates/index.html` 에도 넣을 것.
  v1 용 코드가 조금 남아 있다(편집기 cobalt/duotone-light 스위치 등 — `ide.js` 가 떼어 낸다)
- 도구·분류기: 마크업은 거의 그대로, `<body class="… pb-refresh pb-v2">` 두 층(`pibo-ui.css`)이 색·모양을 바꾼다.
  상단바 노랑, 주 동작 파랑. 도구 왼쪽 메뉴에만 라벨(`.pb-navlabel`)을 넣었다

### B 배치 (IDE)

- 상단바 48px(노랑): 패널 접기 · piBo 메이커 | 블록/파이썬 | 도구·대화·분류기·도움말·전체화면 · [더보기]
  - [더보기]: 화면 밝기 · 글자 크기 · 파이썬 편집기 테마 · 언어 · 초기화 · 전원 · 로고 (전체화면은 260930v3 에 상단바로 옮겼다)
- 왼쪽 패널(`#v2_side`, 폭 조절·접기 기억): `[파이보 | 파일]` 탭 + **실행·정지는 탭과 상관없이 맨 아래**
  - [파이보]: 화면 출력(`[IDE에 보기]` 블록) · 상태(WiFi→인터넷 설정, 온도, 배터리, 메모리, 켜진 시간, 버전, 시리얼→H/W 테스트) · 출력(실행 상태·지우기) · 입력
  - [파일]: 경로 + [추가](새 파일·새 폴더·올리기) · 목록 · 미리보기(사진·소리)
  - 실행을 시작하거나 화면 출력이 오면 [파이보] 탭으로 돌아가고, 접혀 있으면 편다
  - 760px 이하에선 편집기를 밀지 않고 위에 뜬다(z-index 80, Blockly 분류 70 위). 편집기를 누르면 닫힌다
- 편집기 줄: 파일 이름 · 미저장 표시 · [파이썬 코드] · [저장]
- 툴박스: **블록 찾기**(맨 위) + 색 타일 분류(아이콘을 분류 색 칸 안에). `ide.js` 가 Blockly 10 의
  `ToolboxCategory` 를 바꿔 끼운다
- 화면 출력은 경로 `/home/pi/.tmp.jpg` 로 구분한다(`ide.js` 의 `LIVE_PATH`). `run_ide.py` 의 `/show` 경로를 바꾸면 같이 바꿀 것

### 블록 찾기 — `@blockly/toolbox-search` 1.2.11

- `ide/static/v2/vendor/toolbox-search.js`(UMD, Apache-2.0, 라이선스 파일 옆에 있음). **Blockly 10 용 마지막 판**이다.
  Blockly 를 올리면 플러그인도 맞는 판으로 바꿀 것(2.x = Blockly 11, 3.x = 12)
- 플러그인 파일은 고치지 않고 `ide.js` 에서 등록된 클래스의 메서드만 바꿔 끼운다:
  - 색인: 원래 3글자(trigram) 단위라 '출력'·'소리' 같은 **두 글자 한국어가 하나도 안 걸렸다** → 블록 글자를 이어 붙여 부분 문자열로 찾는다
  - 입력: 원래 `keyup` 만 듣는다. 한글 입력기(특히 태블릿)는 조합 중 keyup 이 부실해서 `input` 에도 건다
  - 입력칸을 바로 눌러도 결과가 뜨게 검색 분류를 선택한다. 안내 문구·자리표시는 번역
- `index.js` 가 파일을 열 때마다 `setLanguage` → `updateToolbox(toolbox_dict[lang])` 로 툴박스를 다시 그린다.
  그래서 검색 분류는 `toolbox_dict` 원본 객체에 넣어 두고, 자리표시는 툴박스가 바뀔 때마다 다시 단다
- 블록 문구(`ko.js`/`en.js`)는 `setLanguage` 가 `<script>` 로 늦게 붙인다. 그 전에 툴박스를 그리면 검색 색인이
  블록을 만들다 실패하므로 문구가 온 뒤에 한다(`whenMsgReady`)

### 블록 색 (260924)

- 파이보 블록: `customblock.js` 첫 줄 `color_type` 의 **색 값만** 바꿨다(사용자 승인). 한글 문자열은 그대로다
- 기본 블록: `index.js` 테마 `blockStyles`. 전엔 `colorTertiary`(오타)라 테두리 색이 적용이 안 되고 있었다 → `colourTertiary`
- 분류 색: `customblock_toolbox.js` 의 기본 분류 8개 `"colour"`. **이 파일은 영문판 델타다** — global 에 merge 할 때
  색 줄은 Collect 분류와 떨어져 있어 보통 자동으로 합쳐지지만, 충돌하면 main 쪽 색을 받을 것
- customblock 3종은 셋 중 하나만 고쳐도 `?ver` 를 같이 올린다(지금 260929v1)

### 화면 밝기 (v2)

오래된 노트북 모니터에서 흰 바탕이 눈부셔 잘 안 보인다는 현장 의견으로 넣었다.
`html[data-theme]` = `light` / **`soft`(기본)** / `dark`, 쿠키 `pibo_theme` (포트 무관 → 세 앱이 같이 바뀐다).
고른 적 없으면 **늘 `soft`** 다(260929). 전엔 OS 가 어두운 모드면 `dark` 로 시작했는데, 학교 노트북이 어두운 모드인 경우가
있어 뺐다. 판정하는 곳 넷(`pibo-ui.js` 의 `getTheme`, IDE v2·도구·분류기 템플릿 인라인 스크립트)을 같이 고칠 것

- **색(시안 B, 260924 수정)** — 노랑 #fbc92d 는 상단바 한 곳, 상단바 글씨는 짙은 갈색 #3d2f12,
  선택된 탭([블록|파이썬]·분류기 [학습|시험|보관함])은 흰 알약. 주 동작(실행·저장·추가·꾹 눌러 모으기)과
  포커스·스위치는 **파랑 #2563eb**(흰 글씨 5.2:1), 정지·지울 것은 빨강. 어둡게에서는 상단바가 어두워지고 주 동작이 노랑이 된다
  - 처음엔 주 동작이 먹색 #1f2430 이었다. 노랑과 검정이 공사장 표지처럼 세다는 의견으로 바꿨다.
    비교한 안: 인디고 #4c59d6(탁함) · 연노랑 상단바+인디고(흐림) · 흰 상단바+노랑 버튼 · 보라 #6a4bd6
    (블록 분류 [수학]·[소리]·[음성]과 겹쳐 버튼이 블록처럼 보임) → 파랑
  - 토큰: IDE `--c-brand-ink` `--c-seg-on*` `--c-dark` `--c-accent`, 키트 `--v2-frame-ink` `--v2-seg-on*` `--v2-dark` `--v2-accent`.
    PiBrain 도구(`tools/static/index.css`)도 같은 값
- 비교용으로 두었던 예전 시안(먹빛 틀 · `?frame=teal` 청록 틀)은 260929 에 지웠다(CSS·쿠키 `pibo_frame`)
- soft: 순백(#fff) 대신 옅은 청회색(패널 #f5f6fa, 작업판 #eceef4). 처음엔 누런 회색
  (#f5f5f2)이었는데 칙칙하다는 의견으로 바꿨다. 글자 #1a1e29 대비 약 15:1, 보조 글자 7:1 이상
- dark: #1a1e27 계열. 순수 검정은 안 쓴다(흰 글자 번짐, 카드 경계가 안 보임)
- 파이썬 편집기(CodeMirror)는 v2 전용 테마 **`pibo-light` / `pibo-dark`**(`v2/ide.css`)를 쓰고 밝기를 따른다:
  어둡게 = `pibo-dark`, 기본·밝게 = `pibo-light`. [더보기] 의 편집기 테마 스위치(`#theme_check`)로 따로 바꿀 수 있고,
  밝기를 다시 고르면 거기에 맞춰진다. `index.js` 의 스위치 처리(cobalt/duotone-light)는 `ide.js` 가 떼어 낸다
  - 스위치로 고른 값은 localStorage `pibo_editor_theme` 에 남아 새로 고쳐도 유지되고, 밝기를 다시 고르면 지워진다(260929)
  - 화면 밝기와 편집기 테마가 다를 땐 편집기 바탕을 그 테마 색으로 고정한다(`ide.css` 끝). 전엔 둘 다 작업판 색
    (`--c-work`)을 써서 부드럽게·밝게에서 편집기만 어둡게 하면 밝은 바탕에 밝은 글자가 됐다
  - 키워드 인디고 · 함수 이름 파랑 · 내장 함수 보라 · 속성 청록 · 문자열 초록 · 숫자 주황 · 주석 회색 기울임.
    대비는 바탕 기준 전부 4.8:1 이상. 전엔 `duotone-light` 가 키워드·변수·숫자를 한 색으로 칠했고(주석 2.1:1),
    `cobalt` 는 바탕이 진한 파랑이라 화면과 따로 놀았다
  - 블록 분류 색을 코드에 입히는 안(반복=초록 등)도 봤지만 버렸다. 블록 팔레트에 비슷한 색 쌍이 있어
    (반복·시각 초록, 수학·음성 보라) 글자만으로는 오히려 헷갈리고, 키워드를 나누려면 overlay JS 가 필요하다
- 넓은 면적에는 앰버를 쓰지 않는다
- 첫 페인트 전에 정하려고 각 템플릿에 짧은 인라인 스크립트가 있다(IDE v2 는 `<head>`,
  도구·분류기는 `<body>` 바로 아래). 전역 변수를 만들지 않게 IIFE 로 감쌌다 —
  `tools/static/index.js` 의 최상위 `let` 과 이름이 겹치면 SyntaxError 가 난다
- IDE 색은 `ide/static/v2/ide.css` 의 `--c-*`, 도구·분류기는 `pibo-ui.css` 의 `--v2-*`. 값이 같다 — 같이 고칠 것

### 다듬기 (260924) — 글꼴·파랑 줄이기

"아직 촌스럽다"는 의견으로 색(노랑 상단바·파랑 주 동작)은 그대로 두고 아래만 바꿨다.

- **글꼴: Pretendard 를 싣는다.** 스택 맨 앞이 `"Pretendard"` 였는데 파일이 없어서 학교 윈도 노트북에서는
  맑은 고딕·Arial 로 떨어지고 있었다(촌티의 가장 큰 원인). `design/fonts/` 의 400~800 다섯 굵기를
  `sync.sh` 가 각 앱 `static/fonts/` 로 복사하고 `pibo-ui.css` 맨 위 `@font-face` 가 읽는다. 인터넷 불필요
  - **원본 배포판(pretendard 1.3.9 `dist/web/static/woff2-subset`)의 파일을 고치지 않고** 쓴다. 우리가 subset 을
    새로 만들면 SIL OFL 의 Reserved Font Name("Pretendard") 때문에 이름을 바꿔야 한다. KS X 1001 한글 2,780자 +
    라틴 등이 들어 있다. 여기 없는 글자(드문 옛 조합)는 기기 기본 글꼴로 그려진다
  - **두 굵기만 싣는다(260929)**: 보통 Regular(CSS 100~549) · 굵게 Bold(550~900). 파일당 약 270KB, 둘이 약 0.54MB.
    전엔 400~800 다섯 벌(1.35MB)이었다. 500 은 보통, 600·800 은 굵게로 그려진다(@font-face 범위 선언이라 가짜 굵기 없음)
  - **한 벌을 세 앱이 같이 쓴다(260929)**: 파일은 `ide/static/fonts/` 에만 있다(`sync.sh` 가 IDE 에만 복사).
    도구·분류기 서버는 `/static/fonts/Pretendard-*`·`/webfonts/fa-*` 요청을 IDE(80) 주소로 301 로 넘긴다(각 서버의
    `SharedFonts` — Pibo 도구·분류기, PiBrain 도구·분류기 네 곳에 같은 코드). IDE 는 CORS 를 모두 허용한다.
    브라우저 캐시는 호스트가 같으면 포트가 달라도 같이 쓰므로 한 번 받으면 세 앱이 다시 받지 않는다(브라우저로 확인).
    전엔 앱마다 사본이라 처음에 앱마다 최대 1.35MB + 아이콘 글꼴을 따로 받았다. IDE 가 죽어 있으면 도구·분류기는
    기기 기본 글꼴로 그려진다(아이콘도 빈칸) — `ide.service` 는 늘 떠 있으므로 받아들였다. 시험용 포트는 `PIBO_IDE_PORT`
  - **블록 글자도** Pretendard: `v2/ide.js` 10) 이 글꼴이 다 온 뒤 테마 `fontStyle` 을 바꿔 `setTheme` 으로 다시 잰다
    (Blockly 는 글자 폭으로 블록 크기를 정한다). 파일이 없으면 그대로 둔다
- **꽉 찬 파랑은 한 구역에 하나.** 분류기 [꾹 눌러 모으기]·보관함 [시험] 은 옅은 파랑(`--v2-tint*`). 꽉 찬 건
  [AI 가르치기]·[저장] 만. [AI 가르치기] 는 64 → 48px
- **수치는 파랑 한 가지.** 장수 칩·정확도 칩은 회색, 막대는 1등만 파랑(나머지 회색), 헷갈린 표 맞음은 파랑(틀림은 빨강),
  시험 답 칸은 옅은 파랑. 전엔 노랑·청록·베이지가 섞여 있었다
- **IDE 빈 화면 출력**은 점선 칸. 첫 그림이 오면 `ide.js` 가 `#v2_live[data-has]` 를 달고 그때부터 검은 사진 바탕
- 도구·분류기 상단바의 언어 select 는 판 없이(IDE 상단바 버튼처럼). 도구 [동작] 모터 이름 12.5px/600
- 규칙은 `pibo-ui.css` 끝 '다듬기' 절과 `v2/ide.css` 의 `.v2-live:not([data-has])`. 어둡게에서도 확인함
- **도구 [동작] (260928)**: 상단바 'off 1' → 상태 칩(`#onoff_val[data-state][data-label]`, `index.js` 의 `setRobotState`),
  모터 칸은 작은 카드 + 한글 이름(`motor_m0`~`m9`), 버튼 줄의 ⋮·`-` 는 `.pb-sep`(v2 에서 숨김),
  [등록하기] 가 유일한 꽉 찬 파랑, 지우는 버튼 둘은 판 없는 빨강이고 이름을 갈랐다(`clear_frames` 표 비우기 /
  `remove_all_motions` 동작 모두 지우기). 표는 내용만큼(최대 500px, 예전 고정 높이와 같다)이고 비면 `.motion-empty` 안내, 예제는 알약.
  새 키는 `tools/static/ko2en.js` **끝**에 붙였다(1·2행이 영문판 델타)
  - **로봇 칸은 늘 왼쪽에 고정**(그림을 보며 모터를 맞추는 화면이다). 오른쪽만 스크롤되게 `position: sticky`,
    화면 높이보다 크면 `index.js` 의 `fitRobot()` 이 `zoom` 으로 줄인다(모터 칸이 px 로 자리 잡혀 있어 통째로 줄여야
    모양이 유지된다. 1366×768 에서 0.87). 900px 이하(태블릿 세로)만 위아래로 쌓는다.
    한때 1200px 아래에서 표를 로봇 아래로 내렸는데 표를 보면 로봇이 화면 밖으로 나가서 되돌렸다
  - **사진 위 번호 점 + 옆 조작 패널 (260928)**: 사진에는 모터 번호와 현재 각도만(`.mdot`, 위치는 `index.js` 의 `MDOT`,
    `pibo_body.min.png` 기준 %), 누른 모터 하나를 옆 패널(`.mpanel`)에서 슬라이더·[−5 −1 +1 +5]·숫자로 조절한다.
    예전 모터 칸(`#mN_value`/`#mN_range`)은 v2 에서 숨기고 **값 저장소로 그대로** 쓴다 — 표 클릭·원래자세 등 기존 코드가
    `.val()` 로 바꾸면 300ms 마다 읽어 온다. 보내는 건 기존과 같은 `set_motor` 하나이고, [±] 를 빠르게 눌러도
    150ms 모아서 한 번만 보낸다(서보 명령 폭주 방지). 슬라이더는 놓을 때, 숫자는 Enter·포커스 이동 때 보낸다.
  - **줄 맞춤 (260928, 901px 이상)**: 두 카드를 화면 높이(`--motion-h`, `fitRobot` 이 잰다)에 맞추고 위·아래 끝과 윗줄(40px)을 맞춘다.
    왼쪽 `[원래자세 · 키 안내]` / `사진 + 조작 패널`, 오른쪽 `[반복 · 실행 · 정지 · (이 줄 지우기) · 표 비우기]` / `표`(여기만 스크롤) / `저장 칸`(140px).
    오른쪽 `.motion-record` 는 `display: contents` 로 풀어 버튼 줄·표가 격자 칸이 된다. 격자 열은 `minmax(0,1fr)` — 아니면 저장 칸이 카드 밖으로 나간다
    - 폭: 1300px 이상은 왼쪽:오른쪽 = 1.2:1(1:1 이면 세로로 긴 사진이 폭에 걸려 위아래가 빈다), 그 아래는 1:1(오른쪽 표·저장 칸이 넘친다)
    - **1299px 이하(태블릿 가로 1024~1280)** 는 조작 패널을 사진 아래로 내리고 두 칸(각도 | 시간·추가·수정)으로 편다.
      옆에 두면 사진이 가운데 줄의 절반만 찼다(1024)
    - 사진 폭은 `getMotions` 의 `fitStage` 가 남는 높이·폭에 맞춰 px 로 준다(ResizeObserver, 180~520px). 예전 `zoom` 방식은 걷어냈다
    - 901~1199 는 표 칸을 좁히고 [이 줄 지우기](⌫)·[표 비우기](휴지통)를 아이콘만, 1023 이하는 저장 칸 이름 칸을 한 줄로 따로.
      저장 칸 머리줄의 내보내기·가져오기·모두 지우기는 늘 아이콘만(영문에서 1200~1440 까지 넘쳤다)
    - 901~1920 × 높이 600/768/900 × 한/영에서 가로 넘침 0, 위·아래 끝 일치, 페이지 스크롤 0 을 쟀다
  - **시간·[추가·수정] (260928)** — '모션 하나 만드는 데 오래 걸린다'는 현장 의견으로. **조작 패널 맨 아래**(`.mpanel__add`):
    `시간 [ ]초` · `[추가·수정]` · `누를 때마다 시간 +0.5초`. 각도를 맞추고 바로 아래에서 누른다.
    버튼은 같은 시간이면 그 줄을 바꾸므로 [추가·수정](키 `add_or_edit`, 자세한 규칙은 title `add_or_edit_tip`)
    - 표가 바뀔 때마다(`disp_motion` 의 table → `window.afterMotionTable`) 시간 = 마지막 줄 + 0.5초(`STEP_MS`).
      전엔 시간을 매번 적어야 했고, 깜빡하면 0초 줄을 덮어썼다
    - 줄을 누르면(원래 동작: 그 자세·시간 불러오기) 그 줄이 표시되고 **표 버튼 줄에 [이 줄 지우기]** 가 나온다(표를 다루는 버튼이라 [표 비우기] 옆)
    - `#m_time_val`·`#add_frame_bt`·`#init_bt` 는 **요소를 옮긴 것**이라 예전 핸들러가 그대로 돈다
    - 키보드(노트북): ← → 모터, ↑ ↓ 1°(Shift 5°), Enter 추가·수정. 입력칸·select·팝업·다른 버튼에 포커스가 있으면 안 먹는다
    - **넣었다가 뺀 것 (다시 넣지 말 것)**: 왼쪽 아랫줄의 따로 된 '지금 자세를 표에 추가' 상자(140px) — 저장 칸과 높이를 맞추려고
      만들었는데 내용은 한 줄이라 상자만 컸다. 간격 고르기, [끝에 붙이기], 줄을 고르면 [이 장면 고치기] 로 바뀌는 버튼,
      [팔·손 좌우 같이](M2↔M8·M3↔M9 반대 부호) — '장면' 이라는 새 말과 모드가 늘어 '더 헷갈린다'는 의견(260928)
  - **저장 칸 (260928)**: 표 아래 `.mlib` 한 덩어리 — 머리줄(저장된 동작 · 파일 · 내보내기 · 가져오기 · 모두 지우기) ·
    이름 칸(자리표시, 이름표 숨김) + 등록·불러오기·삭제 · **저장된 이름 칩**(누르면 이름 칸에, 두 번 누르면 불러오기).
    예제는 머리줄 [예제 동작 N개] 를 누르면 저장 칸 위로 뜨는 목록(표를 밀지 않는다, 바깥을 누르면 닫힘). 파일 경로는 제목의 title.
    예전 textarea(`#motor_record`)는 숨기고 값만 받는다. 좁은 폭(≤1199)에선 머리줄 버튼이 아이콘만(title)
  - **시간(초)→ms 는 반올림한다.** `16.1*1000 = 16100.000000000002`, `32.3` 은 `32299.99…` 라 서버 `int()` 가 32299 로
    잘랐고 `delete_frame` 은 같은 값을 못 찾았다. 클라이언트 `Math.round`, `lib.py` 도 `int(round(float(seq)))`
  - `ko2en.js` 에 `confirm_motion_delete` 가 두 번 정의돼(장면·모션) 장면 지우기 확인창에 '모션을 삭제' 가 떴다.
    장면 쪽은 새 키 `confirm_frame_delete` 를 쓴다(뒤쪽 정의는 모션 삭제가 쓰므로 그대로 뒀다)
- **도구 준비 순서 (260929)** — "로봇 연결됨이 한참 뒤에 뜬다"는 의견으로. `tools/lib.py` 의 `Pibo`:
  1. 모터·소리(`Motion`·`Audio`) → **[로봇 연결됨]** (동작 탭은 이때부터 쓴다)
  2. `vision_start` 스레드: 카메라 → 사물·손 인식(`Detect` + 손 제스처 모델) → 얼굴 인식(`Face`: dlib 모델 약 120MB·OpenVINO 3개·
     MediaPipe 얼굴 메시, 가장 무겁다). 단계마다 `vision_state {step,total,key,camera,detect,face,error}` 를 보낸다.
     카메라가 켜지면 바로 화면을 보내기 시작하고, 모델이 아직 없는 기능은 결과 없이 화면만 보낸다
  - 전엔 얼굴 인식까지 다 올린 뒤에야 연결됨이 떴다. vision_camera·vision_face·vision_detect 는 `lib.py` 맨 위에서 불러오지 않는다.
    `lib.py` 가 쓰지도 않으면서 불러오던 `CustomClassifier`·`dlib` import 도 뺐다
  - 화면: 상단 칩 `로봇 준비 중 · N초`, [카메라] 탭 위에 `.v-boot` 줄(단계 이름 · n/3 · 경과 초 · 막대), 모델이 아직 없는 타일은
    '준비 중' 꼬리표(`data-wait`, 눌러 둘 수는 있다)
  - **[음성]**: 목소리 모델(`SpeechOnDevice`)은 음성 탭을 열 때 미리 올린다(`voice_warm`, 처음 한 번 몇 초). `voice_state`
    loading/ready 를 상태 줄에 보인다. 올리는 건 `Pibo.voice_warm()` 한 곳이고 잠금이 있어 두 번 누르거나 말하기와 겹쳐도 한 번만 올라간다
  - **접속하는 순간 상태를 준다**(`run_tools.py` 의 `connect`/`onoff` → `send_state`). 전엔 초기화가 끝날 때 한 번 방송하는 게 전부였고,
    화면이 5초마다 묻던 `onoff` 를 받는 곳이 없어서 그 뒤에 열거나 새로 고친 화면은 [로봇 연결됨] 이 끝내 안 뜰 수 있었다.
    화면의 '연결됨이 되면 원래자세로' 는 **안 됨 → 됨 으로 바뀔 때 한 번만** 돈다(`robotOn`). 서버가 답하게 되면서 5초마다 자세가 초기화될 뻔했다
  - 준비 전에 [카메라] 탭을 열면 그때 보낸 `vision_sleep` 이 버려지므로, 연결됨이 되면 지금 탭 기준으로 다시 보낸다
  - **[음성] 목소리 On/Off 는 없앴다(260929).** 번역·대화가 빠진 뒤로 [실행하기] 를 막는 것 말고 하는 일이 없었다
  - 검증: 무거운 모듈을 지연 있는 가짜로 바꿔 실제 `run_tools.py` + 브라우저로 돌렸다(연결됨 → 카메라 → 사물·손 → 얼굴 순서, 중간·다 된 뒤
    새로 고침, 원래자세 재전송 0, 목소리 준비·말하기). **파이보 실기기에서 단계별 시간은 아직 못 쟀다**
- **도구 [카메라]·[음성] (260928)**: 카메라는 4:3 화면 칸 + '기다리는 중' 안내(`.v-stage[data-has]`), 방향 슬라이더 정리.
  비전 기능은 select 대신 **타일**(`#v_tiles`, `index.js` 가 select 의 option 으로 만든다 — 누르면 select 값을 바꿔
  원래 `detect` 흐름 그대로). 마커 길이는 마커일 때만(`#article_vision[data-func]`). 음성은 이름표 폭을 맞춘 폼,
  꽉 찬 파랑은 [실행하기]·[녹음하기] 하나씩
  - **목소리 10가지 + espeak** (PiBrain 도구와 같은 `SpeechOnDevice` m1~m5 / f1~f5). [정지하기](`tts_stop` → `Audio.stop`),
    결과 한 줄(`tts_status`). 합성은 `asyncio.to_thread` 로 — 1~2초 동안 카메라 스트림 등이 멈추지 않게.
    espeak 는 인자 목록으로 부른다(전엔 `os.system(f'espeak "{text}"')` 라 글자가 셸 명령으로 실행될 수 있었다, root).
    **확인 필요:** 파이보 기기에 `voice_styles/M2~M5·F2~F5.json` 이 다 있는지(없으면 그 목소리만 오류 문구가 뜬다)
  - 키트의 일반 버튼 규칙(`body.pb-v2 button:not(...)…`)이 `:not()` 이 많아 우선순위가 높다. 도구 안의 버튼 모양을 바꿀 땐
    id 를 앞에 붙이고 배경은 `!important` 로 (`#v_tiles .v-tile`)

### 다듬기 (260930) — 화면 캡처로 찾은 것

1366×768(학교 노트북)·1024×768(태블릿 가로)로 IDE·도구·분류기를 찍어 보고 고쳤다. 파이보·PiBrain 같이.

- 상태 칸: 켜진 시간 `N hours` → `2시간 15분` / `2 h 15 min`(`v2_uptime`), 메모리 `메모리 15%`, 칸마다 툴팁(`v2_tip_*`)
- 툴박스: 화면 높이 820px 이하에선 분류 줄을 28px 로(`ide.css` 의 `@media (max-height: 820px)`). 전엔 768 에서 맨 아래 [도구] 가 잘렸다
- [화면 출력] 은 그림이 한 장도 안 왔으면 한 줄(40px)로 접힌다. 전엔 빈 4:3 칸이 약 240px 을 차지해 출력 칸이 좁았다
- 블록 문구(`ko.js`): 반복·논리·수학·글자·목록·변수·함수와 오른쪽 클릭 메뉴의 어색한 번역 약 110개를 고쳤다
  ("으로 계산 i 1 에서 1 을 이용하여 10 로" → "i 을(를) 1 부터 10 까지 1 씩 바꾸며 반복", '리스트' → '목록' 등).
  **Blockly 는 드롭다운 선택지들에 공통으로 있는 앞·뒤 낱말을 떼어 드롭다운 밖에 쓴다** — 선택지 문구를 바꿀 땐 화면으로 볼 것
  ("이 조건인 동안 반복" 이 "이 [조건인 동안] 반복" 으로 쪼개졌다). `%1`·`%2` 는 개수·번호를 그대로 둬야 한다
- 목소리 이름: IDE 말하기 블록의 `k0`~`k9` → `남성 1`~`여성 5`(`VOICE_M1`… `ko.js`·`en.js`). 값(`m1`…`f5`)은 그대로라 예전 프로그램이 열린다
- 빈 목록 블록이 톱니만 보였다 — 툴박스 `"itemCount": "0"`(문자열)을 Blockly 가 참으로 읽었다. 숫자 `0` 으로
- 분류기 블록 `[분류기 모델로 … 분류하기]` 는 손·얼굴·몸이 안 보이면 빈 글자(전엔 `None`)
- [인터넷 설정] 팝업의 영어 안내(Scanning… · Scan failed … · Connecting…)를 번역(`wifi_*`). 목록에 뒤늦게 붙는 글자라 `data-key` 로는 안 바뀐다 — `t()` 로
- 초기화 확인창: "초기화 후 종료합니다" → 무엇이 지워지는지(코드·사진·소리·분류기 모델·모션, WiFi 기본값, 전원 꺼짐)를 적었다
- 도구 [음성]: 말할 글자를 전체 폭 여러 줄 칸 + 글자 수(200), Enter 로 말하기·Shift+Enter 줄바꿈(한글 조합 중 Enter 는 넘김)
- 새 파일·새 폴더 띄어쓰기. 조사는 붙여 쓴다(WiFi를, LCD를)
- 확인(컨테이너): 블록 전체 검사 파이보 165·PiBrain 152 오류 0, 확인 40/40(한/영). **실기기·실제 태블릿으로는 아직 안 봤다**

### 전체화면 (260930) — 세 화면 같은 버튼, 탭을 바꾸면 한 번 눌러 복귀

**탭을 바꾸면 브라우저가 전체화면을 푼다. 막을 수 없다**(브라우저 규칙). 다시 켜는 것도 사용자 동작(누르기) 안에서만 된다.
그래서 IDE 에서 [도구] 를 누르면 IDE 의 전체화면이 풀리고, 새 탭은 보통 화면으로 뜬다. 한 번 누르면 돌아오게 했다(안 A).
끊김 없이 한 화면으로 쓰려면 도구·분류기를 IDE 안(iframe)에 넣어야 하는데(안 C), **하지 않기로 했다**(260930, 사용자 결정). 이유는 바로 아래 절.

- 코드는 키트 한 곳(`design/pibo-ui.js` '전체화면' 절). 각 앱의 예전 전체화면 코드(IDE `index.js` 맨 위, Pibo 도구 `index.js`, 분류기 `app.js`)는 지웠다
- 버튼: `#fullscreen_bt`(또는 `[data-pb-fs]`), 아이콘 칸 `#fullscreen_txt`(또는 `<i data-pb-fs-icon>`). 키트가 클릭·아이콘(`fa-maximize`/`fa-minimize`)을 맡는다.
  IDE 는 [더보기] 안에서 **상단바**로 옮겼다(도움말 옆, 1180px 이하는 아이콘만). PiBrain 도구에는 없던 버튼을 넣었다(`nav_fullscreen`)
- 켜면 쿠키 `pibo_fs=1`(포트와 상관없이 세 앱이 같이 본다). **사용자가 끄면**(버튼·Esc) 지운다.
  탭을 바꾸거나 [도구][대화][분류기] 를 눌러 풀린 건 끈 게 아니므로 남긴다(`openService` 가 `fsLeaving` 을 찍고, 풀린 뒤 400ms 에 화면이 가려져 있으면 남김)
- 쿠키가 있고 전체화면이 아니면: 화면이 보일 때 안내(`fs_tap` '화면을 한 번 누르면 전체화면으로 돌아가요'), **아무 곳이나 처음 누를 때**
  `pointerdown` 에서 다시 켠다(누른 동작은 그대로 된다). 전체화면 버튼을 누른 건 제외(켜자마자 꺼지므로)
- 대화(llama.cpp UI)에는 키트가 없어 이 동작이 없다
- 확인(컨테이너 Chromium): 세 화면 × Pibo·PiBrain 34/34 — 버튼·아이콘 전환·쿠키 기억/지움·안내·한 번 눌러 복귀·포트 간 쿠키 공유·pageerror 0,
  IDE 에서 [도구] 를 눌러 풀려도 쿠키 유지, IDE 상단바 820~1920 한/영 넘침 0. **실제 태블릿·학교 노트북 브라우저로는 아직 안 봤다**

### iframe 으로 합치기(안 C) — **하지 않는다** (260930 조사 후 사용자 결정)

다시 꺼내지 말 것. 아래는 그렇게 정한 근거다.


도구·분류기를 IDE 안 iframe 으로 띄우면 탭이 하나라 전체화면이 안 풀린다. 그 대신 아래가 걸린다.
**재 본 것**(컨테이너 Chromium, IDE 80 페이지에 도구 50000 을 iframe 으로):

| 확인한 것 | 결과 |
|---|---|
| iframe 주소를 도구 → 분류기로 바꿀 때 전체화면 | **유지된다** (안 C 로 얻을 수 있던 유일한 것) |
| 숨긴 iframe(`display:none`·화면 밖)의 `document.hidden` | **`false` 그대로**, `visibilitychange` 안 옴 |
| 숨긴 iframe 의 `requestAnimationFrame` / `setTimeout` | 60/s → **0/s** / 98/s 그대로 |
| iframe 을 **지울 때** `beforeunload`(→ `enable=off`) | **안 뜬다.** `src` 를 바꾸거나 위 탭을 닫으면 뜬다 |
| 위 창에서 iframe DOM 접근 | 안 된다(포트가 달라 교차 출처) → `postMessage` 로만 |
| iframe 안 `confirm()` | 뜬다 |

걸리는 것 (위 측정과 코드에서):

1. **카메라가 안 멈춘다.** 도구 `vision_sleep`·분류기 `camera_visible` 은 `document.hidden` 만 본다. IDE 화면으로 돌아가
   iframe 을 숨겨도 `false` 라 계속 보낸다(대당 0.23~0.29 Mbps × 30대 — '현장 네트워크' 대역폭 표). IDE 가 `postMessage` 로
   '가려짐/보임'을 알리고 두 앱이 그것도 봐야 한다
2. **분류기 학습이 멈춘다.** `tl/trainer.js` 가 에포크마다 `tf.nextFrame()` 을 기다리는데 tfjs 는 이걸 `requestAnimationFrame` 으로
   한다(`vendor/tfjs/tf.min.js` 확인). 숨긴 iframe 은 0/s 이므로 학습 중 IDE 로 넘어가면 멈췄다가 돌아오면 잇는다(추정 —
   실제 학습을 걸고 재 보진 않음). 학습 중에는 전환을 막거나 안내해야 한다
3. **서비스 끄기.** iframe 을 DOM 에서 지우면 `beforeunload` 가 안 떠서 서비스가 안 꺼진다. 끌 땐 `src='about:blank'` 로 바꾸거나
   IDE 가 직접 `enable=off` 를 보낼 것. 숨겨 두기만 하면 서비스는 계속 돈다(지금의 '백그라운드면 살려 둔다' 와 같다).
   코드 실행이 세 서비스를 끄는 건 그대로라, IDE 에서 실행하고 돌아오면 iframe 에 [다시 켜기] 배너가 떠 있다
4. **머리줄 두 겹, [IDE] 버튼.** 도구·분류기는 제 노랑 상단바가 있다. 그 [IDE](`backToIDE`)는 `window.close()` 가 iframe 에선
   안 되므로 IDE 주소로 이동한다 → **iframe 안에 IDE 가 한 번 더 뜬다.** 끼워 넣을 때용 모드(예: `?embed=1` — 상단바 숨김,
   [IDE] 는 `postMessage`)가 네 앱(파이보·PiBrain × 도구·분류기)에 필요하다
5. **설정이 실시간으로 안 넘어간다.** 밝기는 쿠키라 새로 열면 맞지만 이미 열린 iframe 에는 안 간다. 언어는 앱마다
   localStorage 키가 다르다(PiBrain `tools_language`·`classifier_language`). 넘기려면 `postMessage`
6. **한 탭에 다 올라간다.** 분류기(MediaPipe wasm 11.2MB·TF.js WebGL·모델)와 IDE(Blockly)가 한 탭이다. 오래된 태블릿에서
   메모리가 모자라 탭이 죽으면 **저장 안 한 IDE 코드도 같이 날아간다**(지금은 분류기 탭만 죽는다). 실제 태블릿 메모리는 **확인 필요**
7. **키보드.** 도구 [동작] 의 화살표·Enter 는 iframe 에 포커스가 있을 때만 먹는다(전환 뒤 한 번 눌러야 함). 반대로 iframe 안에선
   IDE 단축키가 안 먹는다
8. **새로 고침·주소.** 주소가 IDE 하나라 새로 고치면 도구도 처음부터(서비스 끔 → 켬, [로봇 준비 중] 다시). 주소에 `#tools` 처럼
   남겨야 제자리로 온다
9. **대화(llama.cpp UI)** 는 우리 코드를 못 넣는다. llama-server 가 `X-Frame-Options`·CSP 로 끼워 넣기를 막는지 **확인 필요**.
   막지 않아도 1~8 을 손댈 수 없으니 대화는 새 탭으로 두는 게 현실적이다
10. 다운로드(`a[download]`: 캡처·모션·모델 zip)·파일 올리기 — Chromium 은 iframe 안에서도 된다. iPad Safari 는 **확인 필요**

(참고로 했다면 필요했을 순서: ① 네 앱에 embed 모드 ② IDE 셸(전환 버튼, `postMessage` 약속: 가려짐·밝기·언어·IDE 로) ③ 카메라 가려짐 처리
④ 학습 중 전환 막기 ⑤ 끌 때 `about:blank` ⑥ 대화는 새 탭. '도구 서비스 수명' 의 남은 문제(탭 두 개 중 하나만 닫아도 서비스가 죽음)도
같이 다뤘어야 했다.) 측정 스크립트는 남기지 않았다 — 위 표의 방법대로 IDE 주소에 가짜 위 페이지를 띄워 재면 된다.

### 움직임 (260929)

"화려하게, 단 간단하게"로 넣었다. **그림 파일·라이브러리 없음, 브라우저를 타는 기능 없음**(View Transitions·`@property`·
`backdrop-filter` 안 씀), 축하 효과 없음. 움직이는 건 `transform`·`opacity`·작은 칸의 배경뿐이다(오래된 학교 노트북).
규칙은 `pibo-ui.css` 끝 '움직임' 절(도구·분류기·대기 페이지)과 `v2/ide.css` 끝(IDE). **움직임 줄이기(`prefers-reduced-motion`)면 전부 멈춘다** —
새 효과를 넣으면 각 파일 맨 아래 목록에도 넣을 것

| 무엇 | 어디 | 어떻게 |
|---|---|---|
| 숫자가 이전 값에서 올라감 | IDE 온도·메모리·배터리, 분류기 [시험] 결과 % | `PiboUI.countTo(el, 글자, ms)`(pibo-ui.js) — 글자 속 첫 숫자만 움직이고 앞뒤 글자는 그대로. 요소를 새로 만들면 0 부터 오르므로 배터리는 숫자 칸을 한 번만 만든다 |
| 결과 막대가 튕기듯 참 | 분류기 [시험] | `.bar-fill` 의 `transition` 곡선(살짝 넘쳤다 돌아옴) |
| 카메라 HUD | 도구 [카메라] `.v-stage`, 분류기 `#stage` | `::after` 에 모서리 꺾쇠 8개(그라데이션). 그림이 오기 전엔 `::before` 스캔선 |
| 모터 번호 점 각도 링 | 도구 [동작] `.mdot > b` | `index.js` 의 `gauge()` 가 `--g-a`(호)·`--g-s`(시작)를 단다. 한쪽 끝(범위 min/max)이면 한 바퀴, + 시계 방향·− 반대 |
| 연결 점 숨쉬기 | 도구 `#onoff_val[data-state=on]`, IDE `.v2-dot` | `pb-breathe` |
| 탭 전환 떠오르기 | IDE `.v2-side__page`, 분류기 `.only-*` | 숨김이 풀릴 때마다 `pb-tab-in` 이 다시 돈다. 도구 메뉴는 원래 jQuery 슬라이드 |
| 반짝이는 빈 카드·줄 | 분류기 보관함 첫 목록(`S.modelsLoaded`), IDE 파일 목록(템플릿의 `tr.v2-skel`) | `.pb-skel`. 목록이 오면 통째로 바뀐다 |
| 팝업·알림 튀며 등장 | 대화상자·와이파이·모달·알림 | `pb-rise`. IDE 는 키트의 `.pb .alert-popup-content` 보다 우선하게 `.v2-app` 을 붙였다 |
| 말하는 중 이퀄라이저 | 도구 [음성] 상태 줄 | `setTtsStatus(글, 'speak')` 가 `.pb-eq` 를 붙인다. 소리는 로봇에서 나므로 실제 크기가 아니라 '말하는 중' 표시. 녹음 막대는 원래 있었다 |
| 대기 페이지 | `launch.html` | 배경 빛 번짐(`body::before` transform), 아이콘 둘레 진행 링(`body[data-state]` busy/done/fail → 돎/초록/빨강). 밝기 쿠키를 따른다(전엔 늘 흰 바탕) |

확인(컨테이너): 효과 테스트 Pibo 36/36, PiBrain 25/25(도구 [동작]·[카메라]·[음성]은 Pibo 만 — PiBrain 도구는 마크업이 다르다),
움직임 줄이기에서 멈춤, 기존 테스트 회귀 없음. IX 22 의 '상태 카드: 온도' 는 숫자가 0.6초 동안 오르므로 0.4초 뒤에 읽으면 중간 값이다(테스트 대기를 늘림).
**실기기·학교 노트북에서 끊김은 아직 못 봤다**

### 검증 (컨테이너)

B: v2 전용 IX 22항목(패널 접기·탭·추가·미리보기·화면 출력·실행 시 탭 전환·블록 찾기·밝기·글자·언어·초기화·입력·WiFi),
기존 IX 27항목을 v2 주소로, 560~1960px 한/영 상단바 넘침 0, 도구 메뉴 3개 전환, 분류기 학습·저장 e2e, pageerror 0.
**실기기·실제 노트북 패널로는 아직 안 봤다.**

### v1 삭제 (260929)

지운 것: v1 템플릿(예전 `ide/templates/index.html`) → `index_v2.html` 을 `index.html` 로 이름 바꿈,
v1 전용 CSS(`index.css` `fontello.css` `cobalt.css` `duotone-light.css`), [새 화면으로](`#new_ui_bt`)·[예전 화면으로] 메뉴와
문구 키(`v1_new_design` `v2_old_design`), `?ui=` · 쿠키 `pibo_ui` 판정(`run_ide.py` `/`, `pibo-ui.js`, 도구·분류기 인라인 스크립트,
`launch.html`), 틀색 시안(`?frame=teal`, 쿠키 `pibo_frame`). 기기에 남은 `pibo_ui`·`pibo_frame` 쿠키는 이제 아무도 읽지 않는다.

일부러 남긴 것:
- **`body.pb-refresh` 층** — 도구·분류기는 이 층 위에 `pb-v2` 가 얹혀 있다. 빼면 v2 모양이 같이 틀어진다.
  두 층을 하나로 합치는 건 모양이 바뀌지 않는지 화면을 비교하며 따로 할 일이다
- 도구·분류기의 예전 요소(모터 칸 `#mN_value`, 비전 select 등) — v2 가 **값 저장소**로 쓴다
- `index.js` 의 v1 시절 코드 — 위 '화면 v2' 참고

확인(컨테이너): 바꾸기 전후 화면 캡처 비교(IDE·도구 3탭·분류기 × 부드럽게·어둡게, PiBrain IDE) — 차이는 매번 달라지는
애니메이션·카메라 대기 문구뿐(바뀐 뒤끼리 다시 찍어도 같은 크기로 다름). IX 22·27항목, 편집기 테마 16, [동작] 18·11,
준비 단계 14, 분류기 7, 스트림 7, 글꼴 공유 5 — PiBrain 도 같음. IX 27 의 '블록 바꾸면 미저장 표시(●)' 1건은 바꾸기 전 코드도 똑같이
실패한다: 도구·대화 탭을 연 뒤라 IDE 탭이 뒤로 가 있어 0.3초 안에 안 그려질 뿐, 1.5초 뒤에는 떠 있다(테스트 대기 시간 문제).
`global` 로 merge 하면 `-gl` 태그에서 영문 화면을 같이 볼 것

## IDE 서버·블록 메모 (260924)

- **첫 화면은 `FileResponse` 로 템플릿 파일을 그대로 보낸다** (`ide/run_ide.py` 의 `/`, `tools/run_tools.py` 의 `/`).
  템플릿에 Jinja 문법이 없어서다. 전에 쓰던 `TemplateResponse(이름, {"request": ...})` 는 starlette 1.0 부터
  받지 않아 첫 화면이 500 이 된다(컨테이너 starlette 1.7 에서 확인). 템플릿에 Jinja 를 쓰게 되면
  `TemplateResponse(request, 이름)` 새 순서로 쓸 것
- `restore` 의 `except` 는 `app.sio.emit(..., to=sid)`. 전엔 정의 안 된 `sio` 를 불러 오류 안내가 안 나갔다
- **`utils_dict_create` 는 값 블록이다(260924v3).** 전엔 위아래로 끼우는 모양인데 생성기가 값을 돌려줘서
  코드 생성이 실패했다(`[변수 = 빈 사전]` 을 만들 수 없었다). 예전 모양으로 저장된 파일은 불러오면
  중간에서 멈추므로 `customblock_callback.js` 끝에서 `Blockly.serialization.workspaces.load` 를 감싸
  문장 자리의 그 블록만 걷어낸다(하는 일이 없던 블록이라 프로그램은 같다). 그 IIFE 앞 `;` 는 지우지 말 것 —
  바로 위 `forBlock[...] = function(){...}` 에 세미콜론이 없어 괄호가 그 함수 호출로 붙는다
- 파일은 확장자와 상관없이 **지금 모드(블록/파이썬)로 열린다.** `.json` 을 파이썬 편집기로 열어 고치고 닫을 수
  있어서 일부러 그대로 둔다(권장 사용법은 아님)
- `static/socket.io.min.js`(vendor)는 보안 컨텍스트(`localhost`·https)에서 `navigator.userAgentData.toLowerCase`
  로 죽어 `io` 가 없어진다. 기기는 `http://<IP>` 라 해당 없음. **컨테이너 테스트는 `127.0.0.1` 말고 IP 주소로 열 것**

## merge 충돌 처리

`main` → `global` merge에서 나는 충돌은 사실상 `ko2en.js`의 1·2행뿐이다.

- **`classifier/static/ko2en.js` add/add 충돌** — 양쪽이 독립적으로 추가해서 발생. 차이는 1·2행뿐이므로
  `git checkout --ours classifier/static/ko2en.js` (= 영문판 유지)
- `ide/static/ko2en.js`, `tools/static/ko2en.js` — 보통 자동 머지되고 영문판의 1·2행이 유지된다.
  그래도 merge 후 `head -n1` 3종을 반드시 눈으로 확인할 것
- `--theirs`(main)를 잡으면 `blang`이 자동감지로 돌아가 **영문판 요구사항이 깨진다**

---

## 자주 나는 실수

1. **`git update-index --chmod=+x` 뒤에 `git add -A`** — `git add`가 워크트리 모드(644)를 다시 읽어
   chmod가 **취소된다**. 워크트리에 `chmod +x` 를 먼저 하고 `git add -A` 할 것
2. **tarball/zip으로 파일 덮어쓰기** — 압축물의 모드가 644면 리포의 755가 벗겨진다.
   덮어쓴 뒤 `git status`와 `git diff --cached --summary`로 `mode change` 확인
3. **실행비트가 필요한 파일** — `system/booting.py`, `system/hotspot.sh`, `system/setup_country.sh`,
   `system/setup_openpibo_src.sh`, `tools/static/index.js`. 전부 **100755**여야 한다

---

## 커밋 전 검증

```bash
python3 -m py_compile ide/run_ide.py
node --check ide/static/index.js ide/static/ko2en.js
node --check tools/static/index.js tools/static/ko2en.js classifier/static/ko2en.js
node --check --input-type=module < classifier/static/app.js
python3 -m py_compile classifier/run_classify.py openpibo/vision_classify.py
git diff --cached --summary          # 의도치 않은 mode change 없는지
git ls-tree -r HEAD system | grep -E "hotspot|booting|setup_country|setup_openpibo"   # 100755 확인
```

정적 파일(`*.js`)을 고쳤으면 `templates/index.html`의 `?ver=` 를 새 릴리스 번호로 올릴 것.
안 올리면 브라우저 캐시 때문에 기기에서 반영이 안 된다.

`ide/static/customblock.js`, `customblock_callback.js`, `customblock_toolbox.js` 는
셋 중 하나만 고쳐도 **세 개 모두** 같은 번호로 올린다.

---

## i18n

- UI 문자열은 `<앱>/static/ko2en.js` 의 `translations` 객체 + `t(key, ...args)` 헬퍼
- 서버(`ide/run_ide.py`)는 **한글 문장이 아니라 키**를 보낸다:
  `emit('update', {'dialog': 'err_save', 'detail': str(err)})`
  클라이언트가 `alert_popup(t(data.dialog, data.detail))` 로 번역
- `run_ide.py` 에 한글이 남아도 되는 곳은 **주석뿐**. `grep -n "[가-힣]" ide/run_ide.py` 로 확인
- `t()` 는 전역 함수다. 다른 스크립트에서 최상위 스코프에 `t` 를 선언하지 말 것
- **수정 금지**: `customblock.js`, `disable-top-blocks.js` 의 한글은 로케일 정의·주석·API 값이다
  (`customblock.js` 는 260929 에 `vision_resize` 의 툴팁 키 오타 하나만 고쳤다 — 없는 `VISION_FLIP_TOOLTIP` 를 가리키고 있었다)
- **블록 문구 `ko.js`·`en.js`**: 260929 에 정리했다(사용자 승인). 틀린 설명(대화하기·대화 끄기에 '시작합니다', 매트 만들기에
  '불러옵니다' 등), 분류기 블록 문구, en 오타·모터 블록 뜻, 없어진 블록(서버 TTS·STT·gtts·번역·n-gram 대화·서버 비전)의 키와
  주석 처리된 줄 57개를 지웠다. 두 파일은 PiBrain 과 **같은 파일**이다 — 같이 고칠 것.
  고치면 `index.js` 의 `langFileVersion` 을 올릴 것(두 파일은 `setLanguage` 가 그 번호로 붙인다)

### 번역을 안 타는 문자열

`record`(실행 로그)는 터미널에 **그대로** 찍힌다.
여기에 넣는 문자열은 양쪽 배포판에 같은 모습으로 보이므로 언어중립으로 쓸 것 (예: `[exit]`).

### 실행 로그 프로토콜 (260923v2)

- 시작할 때 `{'record': 전체}` 한 번 → 클라이언트가 터미널을 **갈아끼운다**
- 그 뒤로는 `{'record_add': 조각}` → **이어 붙인다**. 약 50ms(`LOG_FLUSH_SEC`) 단위로 묶어 보낸다
- 실행 중에 새로 붙은 화면(`init`)에는 그 소켓에만 `record` 를 한 번 보낸다
- 전에는 줄마다 전체를 다시 보냈다. 2000줄 출력(39KB)에 42MB·2000프레임이 나갔다 → 지금 43KB·5프레임
- 기기에 붙는 외부 도구(fleet 등)는 `record`·`record_add` 둘 다 처리해야 한다
- **학생 프로그램의 stderr 는 stdout 에 합친다(260928).** `execute` 가 `stderr=STDOUT` 으로 띄우고 4KB 조각으로 읽는다
  (점진 UTF-8 디코더). 전에는 stderr 를 프로그램이 끝난 뒤에 읽어서 ① 무한 반복 안의 에러가 [정지] 전까지 안 보였고
  ② stderr 가 약 1MB 쌓이면 프로그램이 멈췄다(실측: 20초 넘게 안 끝남 → 지금 0.2초). 줄 단위(`readline`)도 버렸다 —
  64KB 넘는 한 줄(`print('x'*100000)`)에서 예외로 실행이 끊겼고, 줄바꿈 없는 `input('이름? ')` 안내문이 안 보였다
- **학생 코드는 root 로 돈다 — 의도한 것이다.** GPIO 등 하드웨어 접근 때문. `pi` 권한으로 내리지 말 것

`periodic_system_update`(10초 주기)의 `system.sh`·`requests` 는 `run_blocking()` 으로
스레드에서 돈다. 코루틴 안에서 직접 부르면 그동안 IDE 전체(실행 출력·저장)가 멈춘다.
`/device/#14:!`(어댑터) 는 `mcu_control.py` 가 `#15` 와 같이 10초마다 캐시한다.

---

## Claude Code 웹 세션 제약

- `refs/tags/*` push가 403으로 막힌다. **태그는 사람이 직접 만들어야 한다**
  (로컬 CLI 또는 GitHub 웹 Releases). 태그 삭제도 같다
- **원격 브랜치 삭제**(`git push origin --delete …`)도 403 이다. 새 브랜치 push 는 된다
- 사내망 라우팅이 없어 기기 SSH 검증은 못 한다
