# openpibo-os.pibo

Pibo 로봇 OS. Raspberry Pi(`pi` 유저, `/home/pi/openpibo-os`)에서 서비스가 작업본을 직접 실행한다.

주요 디렉토리: `ide/`(Blockly IDE, FastAPI + socket.io), `tools/`(모션·음성 도구),
`classifier/`(분류기 — 이미지·손·얼굴·포즈), `system/`(부팅·핫스팟 스크립트).

---

## 브랜치

| 브랜치 | 용도 | 규칙 |
|---|---|---|
| `main` | 국내 배포판 | **모든 개발은 여기서.** 기본 브랜치 |
| `ph` | 필리핀 배포판 | **개발 금지.** `main`을 merge만 한다 |
| `260624` | GitHub Pages 배포 운영 중 | **절대 건드리지 말 것.** push·force-push·merge 전부 금지 |

## 태그

- 국내 `YYMMDDv1`, 필리핀 `YYMMDDv1-ph` (예: `260909v1`, `260909v1-ph`)
- 같은 날 다시 릴리스하면 번호를 올린다 (`260909v2`, `260909v2-ph`)
- **태그는 이동하지 않는다.** 내용이 바뀌면 언제나 새 태그
- 삭제는 **같은 날 대체된 태그만** — `260909v2` 가 나왔으면 `260909v1` 은 지워도 된다.
  배포 이력 태그(`260624v1`, `250709v*` 등)는 남긴다
- 기기가 `git clone --branch <태그>` 로 배포본을 받으므로, 태그는 반드시 원격에 push되어 있어야 한다

### 태그 지우기 전 확인

`-ph` 태그의 커밋은 보통 **`ph` 브랜치에서만** 도달한다. 태그를 지운 뒤 `ph` 브랜치까지
지우면 그 커밋들이 unreachable 이 되어 GC 로 사라진다. **`ph` 브랜치는 남겨둘 것.**

```bash
for t in <지울 태그들>; do
  c=$(git rev-parse $t^{commit})
  git merge-base --is-ancestor $c origin/main && echo "$t: main"
  git merge-base --is-ancestor $c origin/ph   && echo "$t: ph"
done
git push origin :<태그> ...     # 원격 삭제
git tag -d <태그> ...           # 로컬 삭제
```

현장 기기가 옛 태그로 돌고 있으면 롤백 경로가 없어지니, 배포된 기기 상태를 먼저 확인할 것.

---

## PH 델타

**상세는 `ph` 브랜치의 `PH_DELTA.md`** 에 있다 (이유·검증·충돌 처리·배포 후 확인까지).
여기 표는 요약이고, 내용이 갈리면 `PH_DELTA.md` 가 기준이다.

`ph`가 `main`과 다른 부분은 **아래 16개 파일뿐**이다. merge 후 반드시 유지되어야 한다.

| 파일 | 내용 |
|---|---|
| `ide/static/ko2en.js`<br>`tools/static/ko2en.js`<br>`classifier/static/ko2en.js` | 1·2행이<br>`const blang = 'en';`<br>`let lang = localStorage.getItem("language") \|\| blang;` |
| `examples/*.json` (10개) | 텍스트 리터럴·변수명 영문 |
| `examples/collect.json` | **PH에는 없다.** `Weather.region_list` 가 한국 기상청 지역코드, `News` 가 JTBC RSS라 필리핀에선 동작 불가 |
| `ide/static/customblock_toolbox.js` | **Collect 카테고리 통째로**(wikipedia/weather/news) 미노출. 이것만 남았다 — circul.us·gtts 블록과 대화 블록 3개는 260914v6 에서 **main 에서도 제거**돼 더 이상 델타가 아니다 |
| `PH_DELTA.md` | **PH 전용 문서.** main 으로 가져오지 않는다 |

검증: `git diff --name-status <국내태그> <PH태그>` 결과가 위 16개 항목이고 **모드 차이 0줄**이어야 한다.

※ `system/ph_setup.sh` 는 260914v7 까지 17번째 델타였다. `main` 의
`system/setup_country.sh` 가 대신하면서 델타에서 빠졌다 (아래 '마스터 이미지' 참고).

`ide/templates/index.html` 은 일부러 델타에 넣지 않았다. `?ver` 를 올릴 때마다 바뀌는 파일이라
델타로 두면 릴리스마다 충돌한다. PH 전용 파일의 `?ver` 도 `main` 에서 올린다.

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

IDE 블록 8개(`speech_stt` `speech_tts` `speech_tts_play` `vision_call_ai_img(_ext)`
`speech_gtts` `speech_gtts_play` `speech_translate`)와 Tools 의 번역 패널·gtts 목소리도
같이 없앴다.

**남아 있는 외부 통신**

- `collect.py` — 위키백과 / 기상청 / JTBC RSS. 자사 서버가 아니고 **KR 전용**이다
  (PH 툴박스에는 Collect 카테고리가 없다)
- `Dialog.call_llm` — `localhost:50020` (llama-server). 외부 아님

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

30명 규모 대역폭: 분류기 카메라는 320×240 JPEG(품질 80), 평소 2 FPS 로 대당 약 0.4 Mbps,
[꾹 눌러 모으기] 를 누르는 동안만 약 6.7 FPS·1.3 Mbps 다(`classifier/run_classify.py` 의
`FRAME_SLOW`/`FRAME_FAST`, 복잡한 장면 기준 실측). 무선은 AP를 거치며 airtime 을 2배 쓰므로
평소 30대면 약 24 Mbps, 전원이 동시에 모으면 약 80 Mbps. 5GHz 80MHz 한 채널이면 여유가 있고, **2.4GHz 로는 안 된다.**
공유기 한 대에 로봇 30 + 단말 30 = 60대는 동시접속 한계에 걸리니 유선 백홀로 AP 2대를 권한다.

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
| `PH` | **`setup_country.sh PH --regdom=KR`** | `Asia/Manila` | **`KR`** | `ph` / `YYMMDDvN-ph` |
| `MY` | `setup_country.sh MY` | `Asia/Kuala_Lumpur` | `MY` | `ph` / `YYMMDDvN-ph` |

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

**`ph` 브랜치는 '필리핀'이 아니라 '영문 배포판'이다.** 말레이시아도 UI·예제가
영문으로 같으므로 같은 태그를 쓰고, 국가 차이는 위 스크립트가 이미지에 넣는 값뿐이다.
**국가별 브랜치를 새로 만들지 말 것** — 델타가 배로 늘고 merge 대상이 늘어난다.
UI 를 현지어(말레이어 등)로 바꿔야 할 때만 별도 논의 대상이다
(`ko2en.js` 189개 키 + Blockly 로케일).

등록 안 된 국가코드는 스크립트가 usage 만 찍고 멈춘다. 추가할 때
**국가코드에서 timezone 을 추측하지 말 것** — `timedatectl list-timezones` 로 확인하고
`case` 에 넣는다.

---

## 릴리스 절차

### 1. main

```bash
git checkout main && git pull
# 작업...
chmod +x <실행파일>          # git add 전에! (아래 '자주 나는 실수' 참고)
git add -A && git commit -m "..."
git push origin main
git tag -a YYMMDDv1 -m "KR release YYMMDDv1"
git push origin YYMMDDv1
```

### 2. ph

```bash
git checkout ph && git pull
git merge main
# 충돌 처리 (아래 참고)
git push origin ph
git tag -a YYMMDDv1-ph -m "PH release YYMMDDv1-ph"
git push origin YYMMDDv1-ph
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
git clone --depth 1 --branch YYMMDDv1-ph \
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

echo piBo_YYMMDDv1-ph > /home/pi/.OS_VERSION
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
git describe --tags                                      # YYMMDDv1-ph
head -n1 ide/static/ko2en.js                             # const blang = 'en';
ls -l system/hotspot.sh system/setup_country.sh system/booting.py   # 전부 -rwxr-xr-x
curl -s http://localhost/static/ko2en.js | head -n1
```

브라우저는 **Ctrl+Shift+R** 로 강력 새로고침. `?ver` 를 올렸어도 페이지 자체가 캐시돼 있다.

---

## 도구 서비스 수명

`tools.service`(50000), `classify.service`(50010), `llama-server.service`(50020) 는
**셋 중 하나만** 돈다. IDE가 하나를 켤 때 나머지를 stop 한다 (`ide/run_ide.py` 의
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

블록: `[이미지 모델 설정하기]` 에 폴더 `mymodel`, 이름 칸에 모델 이름. 두 번째 칸(라벨)은 안 쓴다.
`ide/static/ko.js` 의 문구는 여전히 "이미지 모델" 이지만 수정 금지 파일이라 그대로 뒀다.
**예전 `model.keras` 는 못 읽는다** (불러오면 다시 학습하라는 오류). 의도한 호환 단절이다.

### 가져온 코드 — 두 곳을 함께 고칠 것

- `classifier/static/tl/` ← teach-lab `lib/` (74f421a). 바꾼 곳은 파일 첫 줄에 적었다(경로, `mirror:false`)
- `openpibo/modules/teachlab/` ← teach-lab `python/teachlab/`. 바꾼 곳은 `load_interpreter()` 하나
- 브라우저와 파이썬이 **같은 숫자**를 내야 한다. 정규화 식(`features.js` ↔ `landmarks.py`),
  자르기(`cropTo` ↔ `crop_to`)를 한쪽만 고치면 학습한 모델이 파이보에서 엉뚱한 답을 낸다
- 로봇 카메라는 거울이 아니다. 어느 소스도 좌우를 뒤집지 않는다
- 파이보는 추론 전에 카메라 그림을 짧은 변 240 으로 줄인다(`_as_stream_rgb`). 브라우저가 학습 때
  본 그림과 크기를 맞추려는 것이다. 스트림 크기를 바꾸면 여기도 바꿀 것

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

## 화면 v2 (260924) — 시안 B, **기본 화면**

**v2 가 기본이다(260924 부터).** 예전 화면(v1, `index.html`)은 주소 끝 `?ui=v1` 로 가고 `?ui=v2` 로 돌아온다.
v1 에는 [새 화면으로](`#new_ui_bt`) 버튼, v2 에는 [더보기] → [예전 화면으로] 가 있다.
v1 은 되돌아갈 길로만 남겨 둔 것이다. 실기기 확인 후 지운다(이 절 끝 '정리할 것').
시안 A·B·C(Scratch식·MakeCode식·Arduino식) 중 **B(MakeCode식)** 로 정했다(260924).

- 고른 값은 쿠키 `pibo_ui` 에 남는다(`design/pibo-ui.js`). **`v1` 일 때만 쿠키를 심고**, `?ui=v2` 는 쿠키를 지운다.
  쿠키는 포트를 안 가려서 IDE(80)에서 고르면 도구(50000)·분류기(50010)도 따라간다
- 판정하는 곳이 넷이다 — 같이 고칠 것: `run_ide.py` 의 `/`, `pibo-ui.js` 의 `UI`,
  도구·분류기 템플릿 `<body>` 바로 아래 인라인 스크립트, `launch.html`(`?ui=` 를 넘겨받는다)
- IDE: `run_ide.py` 의 `/` 가 쿼리 → 쿠키 순으로 보고 `v1` 이 아니면 `templates/index_v2.html` 을 준다.
  CSS·JS 는 `ide/static/v2/ide.css` · `ide.js`. **`index.css` 는 싣지 않는다**
- **요소 id 는 v1 과 전부 같다.** `index.js` 는 한 벌이다. `index.js` 에서 id 를 바꾸거나
  새 요소를 찾게 되면 `index_v2.html` 에도 넣을 것
- 도구·분류기: 마크업은 거의 그대로, `body.pb-v2` 층(`pibo-ui.css` 맨 아래)이 색·모양을 바꾼다.
  상단바 노랑, 주 동작 먹색. 도구 왼쪽 메뉴에만 라벨(`.pb-navlabel`)을 넣었다(v1 에서는 숨김)

### B 배치 (IDE)

- 상단바 48px(노랑): 패널 접기 · piBo 메이커 | 블록/파이썬 | 도구·대화·분류기·도움말 · [더보기]
  - [더보기]: 화면 밝기 · 글자 크기 · 파이썬 편집기 테마 · 전체화면 · 언어 · 예전 화면 · 초기화 · 전원 · 로고
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

### 블록 색 (260924, v1·v2 공통)

- 파이보 블록: `customblock.js` 첫 줄 `color_type` 의 **색 값만** 바꿨다(사용자 승인). 한글 문자열은 그대로다
- 기본 블록: `index.js` 테마 `blockStyles`. 전엔 `colorTertiary`(오타)라 테두리 색이 적용이 안 되고 있었다 → `colourTertiary`
- 분류 색: `customblock_toolbox.js` 의 기본 분류 8개 `"colour"`. **이 파일은 PH 델타다** — ph 에 merge 할 때
  색 줄은 Collect 분류와 떨어져 있어 보통 자동으로 합쳐지지만, 충돌하면 main 쪽 색을 받을 것
- customblock 3종은 셋 중 하나만 고쳐도 `?ver` 를 같이 올린다(지금 260924v2)

### 화면 밝기 (v2)

오래된 노트북 모니터에서 흰 바탕이 눈부셔 잘 안 보인다는 현장 의견으로 넣었다.
`html[data-theme]` = `light` / **`soft`(기본)** / `dark`, 쿠키 `pibo_theme` (포트 무관 → 세 앱이 같이 바뀐다).
OS 가 어두운 모드면 `dark` 로 시작한다.

- **색(시안 B)** — 노랑 #fbc92d 는 상단바 한 곳, 주 동작(실행·저장·추가·AI 가르치기)은 먹색 #1f2430,
  포커스·스위치는 인디고 #4c59d6, 정지·지울 것은 빨강. 어둡게에서는 상단바가 어두워지고 주 동작이 노랑이 된다
- 예전 시안(먹빛 틀 · `?frame=teal` 청록 틀)의 CSS 가 `pibo-ui.css` 에 조금 남아 있다. B 로 채택하면 지울 것
  흰 면적이 줄고 노랑 [실행]·브랜드 마크가 또렷해진다. 틀까지 밝게 두면 전부 비슷한 회색이라 칙칙했다
- soft: 순백(#fff) 대신 옅은 청회색(패널 #f5f6fa, 작업판 #eceef4). 처음엔 누런 회색
  (#f5f5f2)이었는데 칙칙하다는 의견으로 바꿨다. 글자 #1a1e29 대비 약 15:1, 보조 글자 7:1 이상
- dark: #1a1e27 계열. 순수 검정은 안 쓴다(흰 글자 번짐, 카드 경계가 안 보임)
- 파이썬 편집기(CodeMirror)는 v2 전용 테마 **`pibo-light` / `pibo-dark`**(`v2/ide.css`)를 쓰고 밝기를 따른다:
  어둡게 = `pibo-dark`, 기본·밝게 = `pibo-light`. [더보기] 의 편집기 테마 스위치(`#theme_check`)로 따로 바꿀 수 있고,
  밝기를 다시 고르면 거기에 맞춰진다. `index.js` 의 스위치 처리(cobalt/duotone-light)는 `ide.js` 가 떼어 낸다
  - 키워드 인디고 · 함수 이름 파랑 · 내장 함수 보라 · 속성 청록 · 문자열 초록 · 숫자 주황 · 주석 회색 기울임.
    대비는 바탕 기준 전부 4.8:1 이상. 전엔 `duotone-light` 가 키워드·변수·숫자를 한 색으로 칠했고(주석 2.1:1),
    `cobalt` 는 바탕이 진한 파랑이라 화면과 따로 놀았다
  - 블록 분류 색을 코드에 입히는 안(반복=초록 등)도 봤지만 버렸다. 블록 팔레트에 비슷한 색 쌍이 있어
    (반복·시각 초록, 수학·음성 보라) 글자만으로는 오히려 헷갈리고, 키워드를 나누려면 overlay JS 가 필요하다
  - v1 은 예전대로 `cobalt` 시작
- 넓은 면적에는 앰버를 쓰지 않는다
- 첫 페인트 전에 정하려고 각 템플릿에 짧은 인라인 스크립트가 있다(IDE v2 는 `<head>`,
  도구·분류기는 `<body>` 바로 아래). 전역 변수를 만들지 않게 IIFE 로 감쌌다 —
  `tools/static/index.js` 의 최상위 `let` 과 이름이 겹치면 SyntaxError 가 난다
- IDE 색은 `ide/static/v2/ide.css` 의 `--c-*`, 도구·분류기는 `pibo-ui.css` 의 `--v2-*`. 값이 같다 — 같이 고칠 것

### 검증 (컨테이너)

B: v2 전용 IX 22항목(패널 접기·탭·추가·미리보기·화면 출력·실행 시 탭 전환·블록 찾기·밝기·글자·언어·초기화·입력·WiFi),
기존 IX 27항목을 v2 주소로, 560~1960px 한/영 상단바 넘침 0, 도구 메뉴 3개 전환, 분류기 학습·저장 e2e, pageerror 0.
**실기기·실제 노트북 패널로는 아직 안 봤다.**

**테스트할 때:** v1 을 볼 땐 쿠키 `pibo_ui=v1` 을 넣을 것. 쿠키 없이 `templates/index.html` 을 바로 열면
`pibo-ui.js` 가 v2 로 판정해 v1 화면에 `pb-v2` 층이 얹힌다(실제 기기에서는 생기지 않는 조합).

### 정리할 것 (v1 을 지울 때)

실기기에서 수업 흐름(블록 실행·파이썬·입력·화면 출력·도구·분류기 전환)을 확인한 뒤:
`index_v2.html` → `index.html` 로 이름을 바꾸고 v1 템플릿·`index.css`·`#new_ui_bt`·`body.pb-refresh`,
`pb-v2` 조건(층은 기본 스타일로 흡수), 예전 틀색(`?frame=teal`·먹빛) CSS, `v2_old_design` 메뉴를 걷어낸다.
`ph` 로도 넘어가니 PH 태그에서 영문 화면을 같이 볼 것

## merge 충돌 처리

`main` → `ph` merge에서 나는 충돌은 사실상 `ko2en.js`의 1·2행뿐이다.

- **`classifier/static/ko2en.js` add/add 충돌** — 양쪽이 독립적으로 추가해서 발생. 차이는 1·2행뿐이므로
  `git checkout --ours classifier/static/ko2en.js` (= PH 버전 유지)
- `ide/static/ko2en.js`, `tools/static/ko2en.js` — 보통 자동 머지되고 PH의 1·2행이 유지된다.
  그래도 merge 후 `head -n1` 3종을 반드시 눈으로 확인할 것
- `--theirs`(main)를 잡으면 `blang`이 자동감지로 돌아가 **PH 요구사항이 깨진다**

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
- **수정 금지**: `ide/static/ko.js`, `customblock.js`, `disable-top-blocks.js` 의 한글은
  로케일 정의·주석·API 값이다

### 번역을 안 타는 문자열

`record`(실행 로그)는 터미널에 **그대로** 찍힌다.
여기에 넣는 문자열은 양쪽 배포판에 같은 모습으로 보이므로 언어중립으로 쓸 것 (예: `[exit]`).

### 실행 로그 프로토콜 (260923v2)

- 시작할 때 `{'record': 전체}` 한 번 → 클라이언트가 터미널을 **갈아끼운다**
- 그 뒤로는 `{'record_add': 조각}` → **이어 붙인다**. 약 50ms(`LOG_FLUSH_SEC`) 단위로 묶어 보낸다
- 실행 중에 새로 붙은 화면(`init`)에는 그 소켓에만 `record` 를 한 번 보낸다
- 전에는 줄마다 전체를 다시 보냈다. 2000줄 출력(39KB)에 42MB·2000프레임이 나갔다 → 지금 43KB·5프레임
- 기기에 붙는 외부 도구(fleet 등)는 `record`·`record_add` 둘 다 처리해야 한다

`periodic_system_update`(10초 주기)의 `system.sh`·`requests` 는 `run_blocking()` 으로
스레드에서 돈다. 코루틴 안에서 직접 부르면 그동안 IDE 전체(실행 출력·저장)가 멈춘다.
`/device/#14:!`(어댑터) 는 `mcu_control.py` 가 `#15` 와 같이 10초마다 캐시한다.

---

## Claude Code 웹 세션 제약

- `refs/tags/*` push가 403으로 막힌다. **태그는 사람이 직접 만들어야 한다**
  (로컬 CLI 또는 GitHub 웹 Releases). 브랜치 push는 정상
- 사내망 라우팅이 없어 기기 SSH 검증은 못 한다
