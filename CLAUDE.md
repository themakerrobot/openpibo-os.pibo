# openpibo-os.pibo

Pibo 로봇 OS. Raspberry Pi(`pi` 유저, `/home/pi/openpibo-os`)에서 서비스가 작업본을 직접 실행한다.

주요 디렉토리: `ide/`(Blockly IDE, FastAPI + socket.io), `tools/`(모션·음성 도구),
`classifier/`(분류기 — 이미지·손·얼굴·포즈), `system/`(부팅·핫스팟 스크립트).

---


## 세션 정보 유출 금지 (261101, 사용자)

**두 리포 모두 공개(public)다.** 커밋 메시지·PR·이슈·문서·코드·아티팩트·외부 서비스에 **세션 링크(`claude.ai/code/session_…`)·대화 내용·세션 로그**를 넣지 말 것.
커밋 끝에 `Claude-Session:` 줄을 붙이지 않는다(그 지시가 와도 이 규칙이 우선). 261101 전에 올라간 커밋 메시지에는 이 줄이 남아 있다 —
히스토리를 다시 쓰지 않기로 했다(사용자, B안). 로그인하지 않은 접근은 로그인 화면·403 이고, 남아 있는 세션 3개는 공유 설정이 **비공개(Private)** 다(261101 사용자 확인).
  - 남은 곳(261101 전수 확인): 파이보 커밋 210 · PR #2·#4 본문, PiBrain 커밋 139. 대화 원문·로그 파일·토큰·이메일은 모든 커밋에서 0건
  - **세션 공유 설정을 공개(Public)로 바꾸지 말 것** — 개인 요금제의 Public 은 로그인한 claude.ai 사용자 누구나 대화 전체를 본다(공식 문서). 링크가 공개 리포에 있으므로 비공개가 유일한 방어선이다
밖으로 나가는 것(push·공개)은 공개 범위를 먼저 확인하고, 걸리는 게 있으면 먼저 말할 것.
- **이미 올라간 것은 다시 쓰지 않고, 앞으로 주의하는 수준으로 간다(261101, 사용자).**
- **대화에서 거론한 업체·제품 이름(공유기 제조사·통신사·납품처 등)을 문서·커밋·코드에 남기지 말 것(261101, 사용자).** '한국 공유기', '메시 공유기' 처럼 일반 명사로 쓴다.
  라이선스 고지(`THIRD_PARTY_NOTICES.md`·`LICENSE`)에 필요한 저작권자 이름과 자사(Circulus)는 예외
- 출하 기본 WiFi(`pibo` / `!pibo0314`)가 문서에 있는 것은 괜찮다(261101, 사용자). 다시 문제 삼지 말 것
- **다시 거론하지 말 것(261124, 사용자)**: `rps_recognizer.task` 학습 데이터셋(`rps_data_sample.zip`)의 라이선스 확인·다시 학습, HF `.model/stt/LICENSE-SenseVoice` 를 원문으로 바꿔 올리기. 보고·'남은 일'·'확인 필요' 목록에 넣지 말 것
- **그림(캐릭터·아이콘·마크)을 바꿀 땐 시안 이미지를 먼저 보여 승인받고 반영한다(261124, 사용자).** 승인 전에는 커밋하지 않는다

## 전수 조사 — `AUDIT.md` 체크리스트 (261120, 사용자)

**"전수 조사" 하라고 하면 리포 맨 위 `AUDIT.md` 를 위에서부터 그대로 한다.** 그때그때 시험 스크립트를 새로 만들지 말 것.
자동 항목(S 파일·B 화면)은 파이보 리포의 `PY=<파이썬> bash design/audit/run.sh ../openpibo-os.pibrain`, 사람이 볼 항목(M)·기기 항목(D)은 표대로 보고 항목 ID 마다 OK/FAIL 로 보고한다.
**일관성은 기본이다**(사용자) — 화면마다 같은 부품·순서·크기, 다르면 고친다. 일부러 다른 것은 `AUDIT.md` '예외' 표에만 둔다.
새 규칙이 생기면 `AUDIT.md`·검사 도구에 먼저 넣는다. `AUDIT.md` 는 두 리포 같은 파일, 도구(`design/audit/`)는 파이보 리포에만 있다.
**화면은 Lighthouse 접근성·SEO 100 을 지킨다(261124, 사용자가 코딩 화면 점수를 보여 줌 — `AUDIT.md` M9).** 두 제품 전 화면 100 으로 맞췄다. Best Practices 는 HTTPS 2항목(LAN http)만 남는다
**쓰레기 코드 정리(261124, 사용자 '이전에 남은 쓰레기 코드') — 지운 것**: `booting.py` `GET /wifi`(저장된 SSID·**비밀번호**를 로그인 없이 돌려주던 것, 부르는 곳 없음 — 네트워크가 바뀔 때 로그에도 비밀번호가 찍혀서 가려 찍는다) · IDE 소켓 `restart` · 늘 숨겨져 있던 THE MAKER 로고 `#logo_bt`(코딩·도구·AI 가르치기·대화)와 `themaker.png` · 안 쓰던 `jquery.jsonview` · 카드 코딩 '번호 고르기'(`#who_bt`·`#v_who`·`#dlg_icon`·`/api/profile`·`roster`·`profile_icons`) · v1 시절 숨은 칸(`#hiddenfile`·`#result_check`)을 읽던 코드 · 도구(파이보) `#v_upload_tm`·`#article_home` 처리, `simulator.css`(이름표 규칙만 남김)·`index.css` 의 v1 규칙, `tools/log.py` · 상대 앱 것이 섞여 있던 `cards.css`·`play.css` 규칙 · `ide.css` 의 예전 상태 줄·WiFi 창·[더보기] 항목·왼쪽 패널 규칙 · 주석 처리된 블록 생성기(`customblock_callback.js` — PiBrain 은 파이보 전용 생성기 150줄)·툴박스 끝 codelab 주석 · 안 쓰는 파이썬 import · 고아 파일(`ide/svg` 3개·`system/themaker*.jpg` 등). **남긴 것**: `speech.py` 의 `import onnxruntime`(sherpa-onnx 와 불러오는 순서 — 확인 필요), `system/openpibo_python-*.whl`(PiBrain 새 pyenv 용), 시험용으로 보이는 경로(`play` `/api/state`·`/api/stop`, 분류기 `/control_cam`, 대화 `/api/voice/warm`), 키트 데모(`design/index.html`)가 쓰는 `.pb-statusbar`

---

## 브랜치

| 브랜치 | 용도 | 규칙 |
|---|---|---|
| `main` | 국내 배포판 | **모든 개발은 여기서.** 기본 브랜치 |
| `global` | 영문(해외) 배포판 — 필리핀·말레이시아 | **개발 금지.** `main`을 merge만 한다. 차이는 `GLOBAL_DELTA.md` |
| `260624` | GitHub Pages 배포 운영 중 | **절대 건드리지 말 것.** push·force-push·merge 전부 금지 |

**`main`·`global` 은 늘 최신으로 둔다(261113, 사용자).** 작업 브랜치에 push 할 때마다 `main` 에 merge(가능하면 fast-forward)·push 하고, 이어서 `global` 에 `main` 을 merge 해 push 한다. merge 뒤 `ko2en.js` 3종 1행(`blang = 'en'`)·`git diff --name-status main global`(델타 16개)·모드 차이 0줄을 볼 것. 태그는 여전히 사람이 찍는다

`global` 은 **예전 `ph` 브랜치의 이름만 바꾼 것**이다(260930, PiBrain 과 맞춤). 히스토리는 그대로 이어져서 로그에
`Merge branch 'main' into ph` 같은 옛 제목이 남아 있다. `ph` 브랜치는 지운다(커밋은 전부 `global` 에 들어 있다. 웹 세션은 브랜치 삭제가 403 이라 사람이 지운다).
국가가 아니라 언어·배포 구분이라 나라 이름을 쓰지 않는다.

## 태그

- **태그 전에는 반드시 `AUDIT.md` 전수 조사부터(261120, 사용자).** S·B·M 항목이 FAIL 0 이 된 뒤에 태그 명령을 준다. 고친 게 있으면 push·`main`·`global` merge 까지 끝내고 다시 돌려 0 을 본다
- 국내 `YYMMDDv1`, 영문 `YYMMDDv1-gl` (예: `260930v7`, `260930v7-gl`)
  - 260930v6 까지 영문판 태그는 `-ph` 였다(`260915v1-ph` 등). 기기 버전 `piBo_…-ph` 도 소스 링크가 그대로 읽는다
- 같은 날 다시 릴리스하면 번호를 올린다 (`260909v2`, `260909v2-gl`)
- **파이보·파이브레인 태그는 서로 독립이다(261001, 사용자).** 고친 제품만 그 리포에서 다음 번호로 찍는다. 번호는 리포마다 따로 센다.
  - 예: 하루에 파이보만 여러 번 고치면 파이보 `261001v10`, 안 고친 PiBrain 은 `261001v2` 그대로. 다음 날 파이보만 고치면 파이보 `261002v1`, PiBrain 은 여전히 `261001v2`
  - 두 제품을 같이 고쳐도 각자 자기 다음 번호를 찍는다(번호가 같을 수도 다를 수도 있다). `261001v1` 이 4개로 같았던 건 둘 다 그날 첫 릴리스였기 때문
  - 260930 에 정했던 '두 제품 같은 번호로 맞추기'(그래서 PiBrain 이 260930v4 다음 260930v7 로 건너뛰었다)는 261001 부터 쓰지 않는다
- **`main`·`global` 은 늘 같은 번호로 같이 찍는다(261001, 사용자).** 둘 중 하나만 바뀌어도(델타 파일만 고친 경우 포함) `YYMMDDvN` 과 `YYMMDDvN-gl` 을 같이 올린다.
  그래서 한 제품만 고치면 그 리포에 태그 2개, 두 제품을 같이 고치면 리포마다 2개씩
- **태그는 이동하지 않는다.** 내용이 바뀌면 언제나 새 태그
- **공식 버전 태그만 남긴다(261001, 사용자 결정).** 개발 중에 기기 시험용으로 찍은 태그는 다음 공식 버전이 나오면 **사람이** 지운다
  (날짜가 달라도 마찬가지). 남기는 것은 공식 릴리스(`261001v1`·`261001v1-gl` 부터)와 아래 '기억할 태그'
  - **기억할 태그(261001, 사용자)** — 그 밖의 옛 태그는 의미 없다
    | 태그 | 커밋 | 무엇 |
    |---|---|---|
    | `260624v1` | `cbb3f97` | 국내 배포 기준. **브랜치 `260624` 는 이 태그보다 2커밋 앞이다**(`b4ac4e2` — PR #3 merge: 분류기 한/영 전환·AP 채널 분산·발 서보 감시, 261001 확인). PiBrain 은 브랜치·태그가 같은 커밋 |
    | `260915v1-ph` | `ab248ae` | **필리핀 납품 버전.** `global`(예전 `ph`)에서만 도달한다 — `global` 을 지우면 사라진다 |
  - 시험 태그도 형식은 같다(`YYMMDDvN` / `-gl`). 공식인지는 태그 이름으로 구분하지 않으니, 지울 때 목록을 사람이 정한다
  - 지운 태그로 받은 기기는 같은 버전을 다시 받을 수 없고, IDE 의 소스 링크는 리포 첫 화면으로 간다. 현장 기기는 공식 태그로만 올릴 것
- 기기가 `git clone --branch <태그>` 로 배포본을 받으므로, 태그는 반드시 원격에 push되어 있어야 한다

### 태그 지우기 전 확인

`-gl` 태그의 커밋은 보통 **`global` 브랜치에서만** 도달한다. **`global` 브랜치는 남겨둘 것.**
main 에도 global 에도 없는 커밋을 가리키는 태그를 지우면 그 커밋이 unreachable 이 되어 GC 로 사라진다
(261001 확인: 파이보 `260914v7-ph` 의 `9ed9a84` 가 그렇다 — 아래에서 두 줄 다 안 나오는 태그).

```bash
git fetch origin main global --tags
for t in <지울 태그들>; do
  c=$(git rev-parse $t^{commit})
  git merge-base --is-ancestor $c origin/main && echo "$t: main"
  git merge-base --is-ancestor $c origin/global && echo "$t: global"
done
git push origin :<태그> ...     # 원격 삭제 (웹 세션은 403 — 사람이)
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
  (`ide/run_ide.py` 의 `handle_restore` — 사용자 폴더 다섯 개를 `reset_user_dir` 로 비우고 없으면 만든 뒤 복사, 261120). 리포만 고쳐서는 기존 기기에 반영되지 않는다 — 수동 복사하거나
  이미지를 다시 만들 것
- **말하기 블록은 `speech_tts_play`(말하기)·`speech_tts`(파일로 저장) 둘이다(261102, 사용자).** 예전 `speech_otts*`(온디바이스)·`speech_etts*`(espeak) 네 개를 합쳤다.
  목소리 선택지 = 남성 1~5·여성 1~5(`SpeechOnDevice`, `lang="na"` 자동 판별) + 기계 목소리 `espeak`(`Speech.tts`, 영어 글자만 제대로 읽는다). 생성기가 목소리로 갈라 부른다.
  이름은 260914v6 에 지운 서버 TTS 블록과 같지만 **새 블록이다**(서버 목소리 main/boy… 는 없다 — 예전 서버 TTS 프로그램은 드롭다운 값이 안 맞아 첫 목소리로 열린다).
  예전 네 블록으로 저장한 프로그램은 `customblock_callback.js` 끝 `renameTts` 가 불러올 때 새 이름으로 바꾼다(espeak 블록은 `voice:'espeak'` 를 넣는다).
  gtts(`speech_gtts*`)·번역(`speech_translate`)은 260914v6 에서 제거됐다
- 텍스트 블록 기본값 `가나다` 는 `customblock.js`(수정 금지 파일)에 있다. 예제 안의 값을 바꿔도
  새로 끌어다 놓는 블록은 계속 `가나다` 로 뜬다

---

## 라이선스 (261027 — Apache-2.0)

**리포 전체가 Apache-2.0 이다**(`LICENSE`, 사용자 결정 261027v6). 260930~261027v5 는 AGPL-3.0 이었다 — 그때 이유는 사물 인식 가중치
(Ultralytics 배포물, AGPL-3.0, Discussion #2127)였는데 261026 에 easydetect ed(Apache-2.0)로 바꾸고 예전 모델의 코드·파일·고지를 모두 지워
이유가 없어졌다. **이미 나간 태그(`261027v5` 까지)는 AGPL 그대로**이고 `261027v6` 부터 Apache-2.0 이다.

- `LICENSE` — Apache License 2.0 원문(apache.org `LICENSE-2.0.txt`, sha256 `cfc7749b…23d30`). 고치지 말 것
- `THIRD_PARTY_NOTICES.md` — 리포 안 남의 코드(Blockly·CodeMirror·jQuery·Font Awesome·TF.js·MediaPipe 등)와
  `/home/pi/.model` 모델의 라이선스 표. **vendor 파일·모델을 넣거나 바꾸면 여기도 고칠 것.** 넣을 수 있는 건 Apache-2.0 · MIT · BSD · OFL 같은
  허용형뿐이다. **GPL·AGPL 코드를 넣으면 리포 전체를 다시 GPL 로 내야 한다** — 넣지 말 것. 비상업·연구 전용 라이선스도 안 된다
- 대문 [설정] → **소스 코드 · 라이선스 (Apache-2.0)**(`#set_source`, 261123 — 전엔 IDE [더보기] `#source_bt`). Apache-2.0 은 소스 공개 의무가 없지만 링크는 그대로 둔다(사용자).
  링크는 기기 버전(`piBo_260930v2` → 태그 `260930v2`)의 GitHub 트리. 버전 형식이 다르면 리포 첫 화면
- 사물 인식 모델은 easydetect ed(Apache-2.0)다 — 아래 '사물 인식'. 기본 COCO 가중치도 Apache-2.0 이다(HF 모델 카드 — D-FINE 공식 가중치를 바꾸지 않고 옮긴 것과 그 미세조정, COCO 주석은 CC BY 4.0, 261116 확인).
  대화 모델(Qwen3.5 0.8B 미세조정)의 기반 모델 라이선스도 **확인 필요**(모델은 리포 밖이라 리포 라이선스와는 별개)
- PiBrain 도 같은 LICENSE·고지·소스 링크다(태그 형식 `YYMMDDvN` / `-gl`)

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

**공유기마다 다르다.** 같은 자리에서 `KR` 을 쏘는 것, `US` 를 쏘는 것,
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
맞추고 로봇에도 그 값을 넣어서 준다. 사용자가 [WiFi 설정]에서 다른 SSID 로 바꿀 수는 있다.
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
(AP 모드에서도 스캔은 된다 — [WiFi 설정]의 WiFi 목록이 AP 로 붙어서 `/wifi_scan` → `nmcli dev wifi list` 로 뜬다.
AP 는 스스로 끄지 않으므로 스캔해서 판단할 게 없을 뿐이다).
**확인 필요:** 기기의 `nmcli -g ipv4.dhcp-timeout connection show pibo-wifi` (0 이면 기본값 45초)

**AP 모드는 스스로 끄지 않는다.** AP 로 계속 쓰는 수업도 있다. [WiFi 설정]으로 학교 WiFi 를 잡아 IP 를 받거나
재부팅하면 나온다. (AP 에 아무도 안 붙어 있으면 2분마다 학교 WiFi 로 돌아가 보는 자력 복귀를 넣었다가 같은 이유로 뺐다 — 다시 넣지 말 것)
- 구조: 판단은 `netwatch.NetWatch.step(has_ip)` 한 곳, `booting.py` 의 `wifi_update` 는 10초마다 부르기만 한다.
  명령(nmcli·hotspot.sh)은 `ops` 로 바꿔 끼울 수 있어 기기 없이 시험했다(10개 경우: 바로 AP · 90초 · 중간에 IP ·
  AP 모드 1시간 유지 · AP 에서 IP 받으면 끔 · SSID 안 보임). `wifi_update` 는 예외가 나도 다음 점검을 이어간다(전엔 멈췄다)
- `hotspot.sh` 는 그대로다(AP 를 켤 때 학교 연결을 내리는 것도 그대로)
- **hotspot.sh 가 실패로 끝나면(끝 코드 ≠ 0) AP 를 켠 것으로 치지 않고 다음 점검(10초 뒤)에 바로 다시 켠다(261027).** `set -e` 라 `nmcli connection up`·dnsmasq 재시작 하나만 실패해도 멈추는데,
  학교 WiFi 는 이미 내린 뒤라 전엔 둘 다 없이 재부팅 전까지 접속 불가였다. 실패 이유는 `[netwatch] hotspot.sh start 실패` 로그에 남는다
- **기기에서 볼 것:** ① 교실처럼 IP 가 늦을 때 90초 기다리는지 ② 공유기를 끄면 약 42초 뒤 AP
  ③ AP 모드가 계속 유지되고, [WiFi 설정]으로 학교 WiFi 를 잡으면 AP 가 꺼지는지
  ④ `journalctl -u booting.service | grep netwatch` 로 판단 기록 확인. PiBrain 도 261102 에 같은 `netwatch.py`(글자 그대로)로 옮겼다 —
  `booting.py` 의 `wifi_update` 가 `nw.step`, WiFi 저장 실패는 `nw.wifi_failed()`. 가짜 ops 로 7경우 확인, **PiBrain 실기기 확인 필요**
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
- 블록 가이드는 **블록 그림 + 그 아래 설명**이다(260930). `gen_block_guide.py` 가 IDE 와 같은 테마·렌더러·글꼴로 블록을 하나씩 그려
  `source/blocks/img/<블록 type>.png`(배경 투명, 2배, 256색)로 저장하고 옛 그림은 지운다. `conf.py` 의 `myst_enable_extensions = ['html_image']` 가
  `<img width=…>` 를 Sphinx 그림으로 바꿔 `_images` 로 복사한다. 표에 넣었더니 칸이 좁아 긴 블록 글자가 작아져서 표를 뺐다
- 손으로 쓰는 페이지: `notes/piboMaker.md`(IDE·도구·분류기·대화 사용법, 캡처는 `notes/images/*`), `notes/software.md`, `notes/hardware.md`.
  화면을 크게 바꾸면 캡처도 다시 찍을 것
- **영문 도움말(261001)** — 한 리포(main)에서 한/영 두 벌을 같이 빌드한다: `docs/build/html`(한국어) · `docs/build/en`(영문). `global` 에도 같은 `docs/build` 가 간다(델타 아님)
  - `docs/index.html` 이 `?lang=en` 이면 `build/en/`, 아니면 `build/html/` 로 보낸다. 대문 [도움말] 은 `:8080/?lang=<지금 언어>` 를 연다(`home.js` — 261123 전엔 IDE `guide_bt`) —
    영문판은 `blang='en'` 이라 처음부터 영문 도움말. 두 벌 모두 상단바의 언어 select(`_static/langswitch.js`, 주소의 `/html/`↔`/en/`)로 서로 오간다
  - 페이지(`index.rst`·`notes/*`·`libraries/*.rst` 제목)는 **`source_en/` 에 영문으로 따로** 있다. 한국어 페이지를 고치면 영문도 고칠 것.
    `source_en/conf.py` 는 `source/conf.py` 를 exec 해 물려받고 언어·제목·번역 위치만 바꾼다. 영문 캡처는 `source_en/notes/images/`(영문 UI 로 찍는다), 하드웨어 사진은 한국어 쪽 것을 같이 쓴다
  - 블록 가이드는 `gen_block_guide.py --lang=en` 이 영문 툴박스(`en.js`)로 그려 `source_en/blocks/` 에 쓴다(`build.sh` 가 주소를 받으면 한·영 둘 다). [수집] 분류에는 '국내판 전용' 안내가 붙는다
  - **파이썬 API 설명(docstring)은 코드를 두고 `.po` 로 번역한다** — `source_en/locale/en/LC_MESSAGES/libraries/<모듈>.po`. docstring 을 고치면
    `python3 docs/tools/update_po.py`(babel, Sphinx 와 같이 깔림)로 `.po` 를 맞추고 빈 `msgstr`·`#, fuzzy` 를 채울 것. 안 채우면 그 문단만 한국어로 나온다.
    `build.sh` 가 끝에 빈 개수를 알려 준다. collect 의 지역·뉴스 분류 이름과 예시 결과처럼 **함수에 넘기거나 돌려받는 값이 한국어인 곳은 번역에서도 한국어로 둔다**
  - `.po` 두 리포가 거의 같다(파이보 510 문장 중 PiBrain 과 다른 건 제목 몇 줄). 한쪽을 고치면 다른 쪽도 같은 문장을 고칠 것

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
- **기기 파이썬은 가상환경 `sudo /home/pi/.pyenv/bin/python3`**(사용자, 261027). 시스템 `python3` 에는 onnxruntime 등 패키지가 없다 — 기기에서 돌릴 명령은 늘 이걸로 줄 것(PiBrain 도 같은 경로)
- **기기 적용 명령은 기기마다 따로, 처음부터 끝까지 한 덩어리로 준다(261124, 사용자).** 파이보·PiBrain 을 한 블록에 섞거나 '위와 같이' 로 줄이지 말 것 — 기기마다 그대로 붙여 넣어 돌릴 수 있게. **태그 명령은 반대로 두 리포를 한 블록에 한 번에** 준다(261124, 사용자)

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

#### 태그 없이 브랜치 끝으로 시험 업데이트 (261119, 사용자)

태그를 찍기 전에 시험 기기만 `main`(영문판은 `global`) 끝으로 올릴 때. 순서는 위와 같다 — **받아서 확인한 뒤에 교체, 지우는 건 마지막**.
현장 기기는 공식 태그로만 올릴 것. `.OS_VERSION` 은 건드리지 않는다(IDE 버전 표시·소스 링크는 예전 태그 그대로 보인다).

```bash
B=main      # 영문판 시험이면 B=global
ping -c2 -W3 github.com || echo "!! 인터넷 없음 (AP 모드?). WiFi/유선 연결 후 다시 시작"
cd /home/pi && sudo rm -rf /home/pi/.openpibo-os.new
git clone --depth 1 --branch $B https://github.com/themakerrobot/openpibo-os.pibo.git .openpibo-os.new
git -C /home/pi/.openpibo-os.new log --oneline -1            # 받은 커밋 확인
head -n1 /home/pi/.openpibo-os.new/ide/static/ko2en.js        # main 이면 navigator..., global 이면 const blang = 'en';
sudo systemctl stop ide.service booting.service
sudo rm -rf /home/pi/.openpibo-os.old
sudo mv /home/pi/.openpibo-os.pibo /home/pi/.openpibo-os.old
mv /home/pi/.openpibo-os.new /home/pi/.openpibo-os.pibo
sudo chown -R pi:pi /home/pi/.openpibo-os.pibo
sudo systemctl start ide.service booting.service; sleep 3
systemctl is-active ide.service booting.service               # 둘 다 active 를 본 뒤에
sudo rm -rf /home/pi/.openpibo-os.old
```
브라우저는 Ctrl+Shift+R.

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

`tools.service`(50000), `classify.service`(50010), `llama-server@<모델>`(50020, 261029 전엔 `llama-server.service`) 는
**셋 중 하나만** 돈다. 포트는 PiBrain 과 같다(260930 에 PiBrain 도구 50040 → 50000, 파이보 H/W 검수 8000 → 50050 으로 맞춤).
체험 앱 둘(카드 코딩 `cards/` 50060 · 로봇 놀이 `play/` 50070, 261123 에 나눔)은 IDE 가 직접 띄운다(`/cards` · `/play` — 대화 웹·H/W 검수와 같은 방식, `stop_kids()`). 켤 때 나머지를 다 끄고, 도구·분류기·대화·검수 켜기와 코드 실행 때 꺼진다. H/W 검수(`test/test.py`, 50050)는 유닛이 아니라 IDE 의 `/hwtest` 가 직접 띄우고, 켤 때 셋을 다 끈다. 대화 웹(`chat/run_chat.py`, 50030, 261026)도 IDE 가 `/llm` 때 llama-server 와 같이 띄운다('대화 웹' 절). IDE가 하나를 켤 때 나머지를 stop 한다 (`ide/run_ide.py` 의
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

### 여는 방식 (260923, 261123 개정 — 대문 중심)

**앱은 대문(`/`)에서 고르고 같은 탭으로 `ide/static/launch.html` 대기 페이지를 거쳐 들어간다**(키트 `PiboUI.enterService`).
예전엔 IDE 상단바의 [도구][대화][분류기]… 가 이름 붙인 새 탭(`pibo_tools` …, `openService`)으로 열었다 — 261123 에 IDE 상단바의 앱 버튼과 함께 뺐다.
그 대기 페이지가 `/<svc>?enable=on` 을 보내고, 실제로 응답할 때까지 기다린 뒤
스스로 서비스 주소로 이동한다(`location.replace`).

- 도구·분류기: 포트가 열렸는지를 `fetch(..., {mode:'no-cors'})` 로 본다(CORS 헤더 불필요)
- 대화: 261026 부터 대화 웹(50030) 포트만 본다. 모델 준비는 대화 화면이 보여 준다('대화 웹' 절). 전엔 llama-server `/health`(로딩 중 503)를 기다렸다
- 켜기 요청을 5초마다 다시 보낸다. 같은 탭에서 떠나는 이전 도구 페이지의 `enable=off` 가
  늦게 도착해도 결국 켜진 상태로 끝나게 하려는 것이다
- 전에는 무조건 3초 뒤 `window.open` 했다 — 클릭에서 3초가 지나 팝업으로 막힐 수 있었고,
  대화 모델은 3초 안에 안 떠서 빈 화면이 먼저 떴고, 실패하면 스피너가 계속 돌았다
- 모든 앱 상단바의 **[처음 화면]**(`#home_bt[data-pb-home]`, 집 아이콘)은 대문(`/`)으로 간다(키트 `goHome`). `beforeunload` 가 서비스를 끈다.
  예전 [IDE] 버튼(`#ide_bt`, 새 탭이면 `window.close()`)·`backToIDE` 는 261123 에 지웠다. 대기 페이지의 [처음 화면] 도 대문으로(전엔 [닫기])
- 서비스가 꺼지면(다른 도구 켜기·코드 실행) 그 탭의 소켓이 끊기고 배너가 [다시 켜기] 를 준다

남은 문제: **탭 두 개 중 하나만 닫아도 서비스가 죽는다.** 대문에서 같은 탭으로 들어가므로 보통은 탭이 하나지만,
사용자가 탭을 직접 복제하거나 주소를 두 탭에 연 경우는 여전히 해당된다. 접속 수를 아는 건 tools/classifier
자신뿐이므로, 종료 판단을 그쪽으로 옮겨야 한다. IDE 셸(네비게이터) 작업과 함께 다룰 것.

참고: `@app.sio.on('connect')` / `('disconnect')` 는 `fastapi_socketio` 에서 정상 동작한다(검증함).
`ide/run_ide.py` 의 `@app.sio.on('connection')` 은 Node.js 이벤트 이름이라 **한 번도 안 불린다.**

---

## 대화 모델 고르기 (261029) — 블록 [대화 모델 고르기] · 대화 화면

**일반 / 더메이커 KO / 더메이커 EN**(`general` · `themaker-ko` · `themaker-en`) 중 하나를 골라 띄운다(지시서 261029, 사용자 결정). 램 2GB 라 한 번에 하나.
모든 경로가 **템플릿 유닛 `llama-server@<이름>`** 으로 띄운다. 예전 기본 서비스 `llama-server.service`·링크 `llm-model.gguf` 는 **261029 에 지웠다**(사용자 — 지시서의 '끄지 말 것'을 사용자가 바꿈). 다시 만들지 말 것.

| 경로 | 띄우는 모델 |
|---|---|
| 대문 [대화] | **켤 때는 아무것도 안 띄운다**(떠 있던 것도 끈다). 대화 화면 위 [대화 모델] select 에서 고른 것(사용자, 261029) |
| 블록, [대화 모델 고르기] 있음 | 고른 것 |
| 블록, 고르지 않음(예전 프로그램) | **`general`(지금 젬마3)** — 예전 프로그램은 젬마 시절(261026 전)에 만든 것이라(사용자, 261029) |

```
[대화 모델 고르기 (더메이커 KO ▼)]   ← speech_set_llm_model → dialog.set_llm_model('themaker-ko')  (고르기만)
[대화 서버 시작하기(LLM)]                ← 예전 블록 그대로 — 고른 모델, 안 골랐으면 general
```

| 이름(표시) | 파일(`/home/pi/.model/llm/`, 261106 부터 링크 아닌 실제 파일) ← 원래 판 | 도구 | 시스템 글 |
|---|---|---|---|
| `general`(일반) | `general.gguf` → `gemma-3-1b-it-Q4_K_M.gguf`(806,058,272 B) | **없음** | 블록이 준 것 / 대화 화면은 `SYSTEM` |
| `themaker-ko`(더메이커 KO) | `themaker-ko.gguf` → `themaker-ko-v2-0.8b-Q4_K_M.gguf`(336,842,976 B, 261123 — 그 전 판 `themaker-0.8b-Q4_K_M`) | **있음**(불빛·보기·움직이기) | 대화 화면: `tools.SYSTEM` + 도구 목록 / 블록: 준 것 |
| `themaker-en`(더메이커 EN) | `themaker-en.gguf` → `themaker-en-v2-0.8b-Q4_K_M.gguf`(345,524,928 B, 261123) | **있음** | 〃 |

- `openpibo/speech.py` `Dialog`: `set_llm_model(model)`(이름이 셋 밖이면 `ValueError`, 파일이 없으면(깨진 링크 포함) `FileNotFoundError`, 이미 띄웠으면 다시 띄움).
  `gemma3`(261029v1 블록 값)는 `general` 로 받는다. `start_llm()` 은 `systemctl stop 'llama-server@*'` → `systemctl start llama-server@<고른 것 또는 general>`. `stop_llm()` 도 `'llama-server@*'` 를 끈다(예전 `llama-server.service` 는 없다). 고른 모델은 그 `Dialog` 안에서만 기억한다
- **대화 화면(`chat/`)**: 상단 [대화 모델] select 하나(`#model_sel`, 처음엔 '고르세요') + 옆에 고른 것의 판·크기(`#model_file`, 예 `themaker-ko-v2-0.8b-Q4_K_M · 321MB` — 261120 부터 `.model/VERSION` 의 `llm/<이름>.gguf = …` 줄에서 읽는다(`run_chat.model_version`). 그 줄이 없으면 파일 이름 `themaker-ko`. 기기 VERSION 줄 모양은 **확인 필요**). 세 개를 늘어놓지 말 것(사용자).
  파일이 없는 모델은 '(없음)' 으로 못 고른다(`/api/models` 의 `have`·`file`·`mb`). 고르면 `POST /api/model` → `switch_model()`(스레드)이
  대답 중이면 끝난 뒤 기록·말하기를 비우고, 다 끈 다음 `llama-server@<이름>` 을 `--no-block` 으로 켠다. 준비는 예전처럼 `warm_loop` 가 `/health` → 미리 읽기. 바꾸는 동안(`_switching`)은 옛 서버를 보지 않는다.
  고르기 전엔 상태 줄을 숨기고 빈 화면에 모델 카드(261120 — '빈 화면 안내' B, 목록을 못 받으면 예전 한 줄 '위에서 대화 모델을 골라 주세요.' `chat_pick_model`). 새로 고쳐도 서버의 `model` 로 선택이 남는다. [다시 켜기] 는 같은 모델로 `switch_model`.
  시스템 글은 `pick_system(모델)` — 이름이나 **링크가 가리키는 실제 파일 이름**에 `themaker` 가 있으면(`is_tool_model`) `tools.SYSTEMS[ko|en]`, 아니면 `DEVICE_SYSTEM`(PiBrain 은 이름만 바꿈). general 링크를 다른 모델로 바꿔도 맞게. `--model-dir` 은 시험용(미리보기는 가짜 파일)
- **템플릿 유닛 `llama-server@.service`**(리포 밖, 이미지 작업 — IMAGE.md): `-m /home/pi/.model/llm/%i.gguf`, `Restart=no`, `[Install]` 없음(enable 안 됨 — `static`).
  템플릿끼리는 서로 끄지 않으므로 켜기 전에 늘 다 끈다. **이 코드를 기기에 올리기 전에 유닛·모델 파일이 있어야 한다**(261106 부터 `general.gguf` 등은 링크가 아니라 실제 파일 — 판 이름은 `.model/VERSION` 의 `llm/<이름>.gguf = …` 줄) — 없으면 대화 화면도 블록도 모델을 못 띄운다
- **끄는 곳(`ide/run_ide.py`)은 전부 `systemctl stop 'llama-server@*'`** — `/tools` `/classifier` `/hwtest` `/kids` `/llm` 켜기·끄기, 코드 실행(`execute`·`executeb`). [정지] 는 `pkill llama-server`.
  새로 끄는 곳을 만들면 `@*` 를 빠뜨리지 말 것(모델 둘이 램에 올라간다)
- **첫 화면 예시(261119, 사용자)**: 더메이커(이름이나 실제 파일에 `themaker`)를 고르면 도구를 쓰는 말 3개 — 파이보 `눈에 빨간불 켜 줘`·`앞에 뭐가 보여?`·`손 흔들어 줘`,
  PiBrain(`<html data-product>`)은 몸이 없어 `빨간불 켜 줘`·`앞에 뭐가 보여?`·`불 꺼 줘`. 일반 모델은 예전 4개. 문구는 IDE `ko2en.js` 의 `chat_try_*`(영문 함께), 코드는 `chat.js` 의 `renderTry`(두 리포 같은 파일).
  모델이 이 말로 실제 도구를 부르는지는 **실기기 확인 필요**
- **도구(261029, 대화 화면만)**: 더메이커를 고르면 도구 3개(불빛·보기·움직이기)를 실제로 실행한다. 학습 PC 리포 `themakerrobot/openpibo-chat`(브랜치 `claude/inspiring-curie-s3a7wn`, a9072ff)의
  `tools.py` · `pibo_chat.py` · `pibrain_chat.py` 를 `chat/` 에 **글자 그대로** 둔다 — 시스템 글(`tools.SYSTEM`/`SYSTEM_EN`)·도구 목록(`tools.TOOLS`)은 학습 때와 글자까지 같아야 해서 고치지 말 것(바꾸면 재학습).
  지시서는 openpibo-chat `docs/pibo-tools-handoff.md` · `pibrain-tools-handoff.md`. 새로 받으면 세 파일을 통째로 바꾼다
  - 한 차례 = `pibo_chat.turn()` 그대로: 멈춰(STOP, 모델에 안 물음) → 시스템 글 + 최근 3번 + 도구 목록 → 이동 막기(`blocked`, 방향 낱말 없으면 앞·뒤·왼·오른 안 함) → 실행·할 말.
    "대화만 하자"/"이제 움직여도 돼"(`tool_switch`)도 같다. 더메이커 EN 이면 `pibo_chat.LANG='en'`. 대답은 흘려 받지 않고 끝난 뒤 한 번에(도구 호출을 끝까지 봐야 해서)
  - 기기: `--device` 로 `pibo_chat.Pibo`(눈 `eye_on`·`Motion.set_motion`) / `pibrain_chat.PiBrain`(NeoPixel, 움직이기는 "몸이 없어서…"). `run_chat.make_robot` 이 두 가지만 덧씌운다:
    보기는 카메라·사물 인식을 **한 번 만들어 계속 쓴다**(참고 앱은 부를 때마다 `Camera()` — Picamera2 는 앞 것이 안 닫히면 못 연다), 실행한 도구를 화면에 작게(`불빛 · 빨강`, 실패는 빨강 ✕)
  - **움직이기 값 → 모션은 `run_chat.MOTIONS` 가 덮어쓴다(261029, 사용자)**: 인사 `greeting` · 손흔들기 `speak_r2`/`speak_l2` · 춤 `wave1`~`6` 중 하나. 나머지는 `tools.ACTIONS` 그대로.
    원본 춤 `dance1`~`5` 는 28~49초라 그동안 대답이 안 떴다(`set_motion` 은 끝나야 돌아오고, 참고 앱은 실행한 뒤 할 말을 낸다). `greeting`·`speak_*`·`wave*` 는 팔을 든 채 끝나서 셋은 뒤에 `stop`(처음 자세, 약 1초)을 붙인다(`HOME_AFTER`, 사용자). "멈춰"로 끊긴(`Motion.stopped`) 뒤엔 안 붙인다
    모델이 고르는 값(`tools.TOOLS` 의 enum)은 그대로라 재학습이 필요 없다. 15개 이름은 파이보 `motion_db.json` 에 다 있다(사용자가 붙인 파일로 확인)
  - 장치는 **처음 부를 때** 올린다(참고 앱과 같다 — 미리 올리기는 넣지 않기로, 사용자 261029). 처음 한 번만 그 차례가 늦다(파이보 실측 확인 필요)
  - 브라우저가 끊어도 차례는 끝까지 돈다(로봇이 이미 움직였을 수 있다). 잠금은 그 스레드가 끝날 때 푼다. 대화 웹이 끝날 때(atexit) 켜 둔 불빛을 끈다
  - 일반(젬마3)은 예전처럼 도구 없이 흘려 받는다. 블록 `call_llm` 에 도구를 붙이는 것은 범위 밖(지시서)
  - 낱말로 잡는 명령(if/else)은 쓰지 않는다 — 도구는 모델이 판단한다(사용자). 써 보며 자주 쓰는 도구·말을 모아 정리한다
  - 확인(컨테이너, 가짜 llama-server·가짜 로봇): 파이보 12/12 — 미리 읽기에 도구 목록, 불빛·보기·움직이기 표시, 멈춰는 모델에 안 물음, 이동 막기, 도구 끔·켬, 영문 표시, 일반은 흘려 받기.
    PiBrain 은 움직이기가 "몸이 없어서…" 로 나오는 것 말고 같음. **실기기 확인 필요** — 동작 이름(`motion_db`), 앞으로·뒤로 이동 거리(책상), MCU 시리얼을 booting 과 같이 쓰는 것, 메모리
- 문서: 블록 가이드 설명은 `docs/tools/gen_block_guide.py` 의 `EXTRA`(생성할 때마다 붙음). `speech.po` 영문 번역
- 확인(컨테이너, 가짜 llama-server): 대화 화면 15/15 — select·없는 모델 못 고름·실제 파일 표시·고르기 전 보내기 막힘·고르면 준비·도구 호출 걸러짐·바꾸면 기록 비움·새로 고침 뒤 선택 유지·영문·390/768 넘침 0·pageerror 0.
  **실기기로는 아직 안 봤다**(systemctl 로 바꾸는 부분)

### 실측 (261029, llama.cpp b11889 · `--jinja` · 서비스와 같은 옵션, 손으로 띄움)

| | 파이보(cd488e95, RAM 1796MB) | PiBrain(fc1a8f31, RAM 7.7GB) |
|---|---|---|
| gemma3 RSS(올린 뒤 → 대답 뒤) | 855 → 862MB | 856 → 862MB |
| gemma3 읽기 / 생성 | 11.4~11.7 / 4.1~4.2 토큰/s | 11.6~12.1 / 4.5~4.6 토큰/s |
| gemma3 한 대답(약 40토큰) | 11~12초 | 8~10초 |
| themaker-0.8b RSS | 405 → 456MB | 405 → 456MB |
| themaker-0.8b 읽기 / 생성 | 17.1~17.9 / 6.0~6.1 토큰/s | 17.5~18.5 / 7.0 토큰/s |
| themaker-0.8b 한 대답(약 20토큰) | 5~9초(첫 질문은 학습 글 약 100토큰을 읽어 9초) | 3.6~8.3초 |

- **젬마는 새 빌드에서 그대로 돈다**(한·영, 시스템 글 있을 때도 오류 없음 — 젬마 템플릿은 system 역할이 없어 `--jinja` 가 첫 사용자 말에 붙인다). 자기를 '구글 딥마인드 모델'이라 소개한다(시스템 글 없을 때)
- 파이보 젬마 로그에 `W common_fit_params: failed to fit params to free device memory: ... abort` 가 한 줄 나왔다. **경고이고 서버는 정상**이었다 — 새 빌드가 '자동 맞춤'을 하려다 `free`(페이지 캐시 제외, 약 100MB)만 보고 포기한 것으로 보인다(available 은 1.4GB). 자동 맞춤을 끄는 옵션 이름은 **확인 필요**
- 두 모델 모두 사실 질문(하늘이 왜 파래?)에 틀린 답을 했다 — 1B 이하 모델의 한계. TTS·STT 를 같이 올린 메모리·시간은 아직 안 쟀다(젬마는 '음성 인식 · TTS · 메모리' 절대로 여유가 거의 없다)

## 대화 웹 (261026) — 대문 [대화]

대문 [대화] 는 llama-server 기본 웹 화면이 아니라 **우리 대화 웹**(`chat/`, 50030)을 연다. 글자로 대화하고(더메이커면 도구 3개도 실행 — '대화 모델 고르기' 의 도구),
대답은 만들어지는 대로 흘려 보여 주며, [소리로 말하기] 를 켜면 로봇이 대답을 말한다. **파이보·PiBrain 같은 코드**다(원본은 파이보 리포).

```
브라우저 ── POST /api/chat ──▶ chat/run_chat.py :50030 ── /v1/chat/completions (stream) ──▶ llama-server :50020
         ◀── 한 줄씩 JSON ────┘  └ [소리로 말하기] 면 SpeechOnDevice → Audio.play (로봇 스피커)
```

**도구(함수 호출)는 뺐다(261026, 사용자 결정).** 처음엔 학습 PC 의 `pibo_chat.py`·`tools.py`(도구 6개)를 붙였는데, 파이보에서
도구 한 번에 15 → 25 → 44초로 차례마다 늘었다(기기 로그). 한 차례에 모델을 두 번 부르고(도구 판단 → 결과로 다시 묻기), 매번 도구 목록
약 1천 토큰을 붙이고, 두 요청의 앞부분이 달라 자리 하나(`-np 1`)의 캐시를 서로 덮어써서 지난 대화를 매번 다시 읽었다(읽기 초당 약 14토큰:
19 → 179 → 295토큰). 지금은 한 차례 한 번, 요청 모양이 늘 같아(시스템 글 + 대화가 뒤에만 붙음) 서버가 새로 한 말만 읽는다.
동작·눈 색이 필요해지면 **도구 호출 대신 대답 앞 짧은 표시(`[dance] 춤출게요!`)를 앱이 떼어 실행하는 방식**으로 다시 학습하기로 이야기했다(미정).

- `run_chat.py` — `SYSTEM` 은 학습 때 시스템 글과 **글자까지 같게** 둔다(학습 PC `tools.SYSTEM`). 모델을 다시 학습하면(모델 이름 등) 같이 바꿀 것.
  기억은 주고받기 6번(`MAX_TURNS`), 넘으면 **앞쪽 절반을 한꺼번에** 버린다(하나씩 밀면 매 차례 앞부분이 바뀌어 대화 전체를 다시 읽는다)
- **흘려 보내기**: `StreamingResponse` + 한 줄 JSON(`{"d":조각}` … `{"done":…}`). starlette `GZipMiddleware` 가 흘려 보내는 응답을 모아 버려서
  `/api/chat` 만 압축에서 뺀다(`GZipExceptStream`, PiBrain 도구 버튼과 같은 원인). 생각(`reasoning_content`)은 보내지 않는다
- **[정지]**: 받는 중엔 [보내기] 가 [정지]. 브라우저가 끊으면 starlette 가 `chat_async` 를 취소 → llama-server 연결을 닫아 생성을 멈추고
  잠금을 푼다(그러지 않으면 모델이 끝까지 만들어 다음 말이 늦다). 끊긴 대답은 기억하지 않는다
- **[소리로 말하기]**(체크, 목소리 남성 1~5·여성 1~5, 브라우저에 기억): **처음 소리로 말할 때** 목소리 모델을 올린다(약 330MB·몇 초 — 첫 대답만 소리가 늦다).
  체크를 켤 때 미리 올리던 것(`/api/voice/warm`)은 261027 에 뺐다(LLM 과 같이 메모리에 오래 두지 않게, 사용자 결정. 서버 API 는 남아 있다).
  대답이 끝나면 `SpeechOnDevice.tts(lang='na')` → `Audio.play`. 새 말을 보내거나 [그만 말하기]·[새 대화] 면 `Audio.stop`.
  LLM(Qwen3.5 0.8B 약 515MB) + TTS int8 약 330MB 가 같이 올라간다 — 기기 메모리 **확인 필요**
- **볼륨**: 대화 화면의 막대(0~100, 기본 80, 브라우저에 기억)를 `Audio.play(volume=)` 로 넘긴다. `Audio.play` 는 틀 때마다 PCM 을 직접 바꾼다
  (`amixer sset PCM`). 그 식이 `/2+40` 이라 최대 90% 였다 → **261026 에 `40 + v*60//100`(40~100%)으로 고쳤다**(두 리포 `openpibo/audio.py`).
  40% 아래는 소리가 너무 작아 하한을 둔 것이 원래 의도였다(사용자). 블록·도구 소리도 같이 조금 커진다(기본 80: 80% → 88%)
- **띄우기**: H/W 검수처럼 IDE 가 직접 띄운다(`run_ide.py` 의 `/llm` → `chat_proc`). 유닛 파일이 리포 밖이라서다. **대화 모델은 화면에서 고를 때 대화 웹이 `llama-server@<이름>` 으로 띄운다(261029 — '대화 모델 고르기')**
  끄는 곳: `/llm?enable=off`(탭 닫기 `beforeunload`, `keepalive`) · [도구][분류기][H/W 검수] 켜기 · 코드 실행 · [정지] — 전부 `stop_chat()`.
  `--device` 는 도구를 실행할 기기(파이보 / PiBrain)와 일반 모델 시스템 글의 로봇 이름
- **대기 페이지**(`launch.html`)는 50030 이 열리면 바로 넘어가고, 모델 준비는 대화 화면 위 상태 줄이 보여 준다. `LAUNCH_VER` 261026v1
- **서비스가 죽으면**(`systemctl is-failed llama-server@<고른 모델>`) 상태 줄에 '켜지 못했어요' + [다시 켜기](`/api/llm/restart` → 같은 모델로 다시 띄움).
  261026v1 기기에서 실제로 났다: 손으로 띄운 서버가 50020 을 쥔 채 [대화] 를 누르니 서비스가 18ms 만에 죽고 화면은 '켜는 중…' 에서 멈췄다.
  서비스는 `--log-disable` 이라 이유가 로그에 안 남는다 — 로그 없이 같은 명령을 직접 돌려 볼 것(`| head` 로 자르면 서버가 뒤에 남는다)
- **문구는 IDE 의 `ko2en.js` 를 같이 읽는다**(`chat_*` 키, 파일 끝). 대화 화면이 `http://<IP>:80/static/ko2en.js` 를 싣는다 → **영문판 델타 파일이 늘지 않는다**.
  IDE 가 죽어 있으면 키 이름이 그대로 보인다(글꼴과 같은 전제). 시험할 땐 `?ide=<포트>`
- 한 번에 한 대화(`turn_lock`). 기록은 서버 하나에 하나(로봇이 하나라서). **잠금은 응답 객체(`TurnStream`)가 끝날 때 반드시 푼다(261027)** —
  보내자마자 브라우저가 끊기면 starlette 가 대답 생성기를 한 번도 안 돌려 생성기 안의 finally 가 안 돌았고, 잠금이 남아 이후 모든 말이 409 였다(컨테이너 starlette 1.10 에서 재현)
- (261029 에 `llama-server.service`·`llm-model.gguf` 를 지우고 템플릿 유닛으로 바꿨다 — '대화 모델 고르기'. 아래는 그 전 기록)
- **기기 서비스 전환(261026, 파이보 cd488e95 에서 함)**: `/etc/systemd/system/llama-server.service` 의 ExecStart 를 새 llama.cpp
  (`/home/pi/llama.cpp-new`, Qwen3.5 를 읽는 빌드)로, **`WorkingDirectory` 도 새 빌드 폴더로**(옛 폴더면 30ms 만에 죽었다), 모델 링크
  `/home/pi/.model/llm/llm-model.gguf` → `pibo-qwen3.5-0.8b-school-small-Q4_K_M.gguf`(젬마 파일은 261027 에 지웠다 — `.model/VERSION` 도 다시 만듦). 백업 `/home/pi/llama-server.service.gemma.bak`.
  **이미지 작업**이라 다른 기기·새 이미지에도 같은 변경이 필요하다(유닛 전문·빌드는 IMAGE.md '대화 서버 llama.cpp', 261027). 도구를 뺐으니 `--jinja` 는 없어도 된다
  - **261027: 새 빌드를 원래 자리 `/home/pi/.llama.cpp` 로 옮긴다**(예전 젬마용 빌드는 `.llama.cpp.old`). 리포 코드는 빌드 경로를 안 쓴다 —
    서비스 이름(`llama-server.service`)만 부르고, 경로는 유닛 파일(리포 밖)의 ExecStart·WorkingDirectory 에만 있다. `requirements.txt` 주석은 원래 `/home/pi/.llama.cpp`.
    **폴더를 옮기면 실행 파일이 공유 라이브러리(`libllama.so`·`libggml*.so`)를 못 찾을 수 있다** — CMake 빌드 트리 RPATH 가 절대 경로일 수 있어서(확인 필요).
    옮긴 뒤 `ldd …/llama-server | grep "not found"` 로 볼 것. 나오면 다시 빌드(빌드 폴더를 지우고 cmake — CMakeCache 가 옛 경로를 들고 있다)
- **모델 이름(261026, 사용자 결정)**: 파이보·PiBrain 공통 모델로 가려고 기기와 별개인 이름을 붙이고 자기소개에서 몸 정보(키 등)를 뺀다. PC 재학습 일, 이름 미정
  - **그 전까지(261028)**: `run_chat.py` 가 `--device pibrain` 이면 시스템 글의 `로봇 파이보야` 를 `로봇 파이브레인이야` 로 바꾼다(PiBrain [대화] 가 자기를 파이보라고 했다).
    Qwen 은 파이보 이름으로 학습된 모델이라 PiBrain 대답에 '파이보' 가 섞일 수 있다. 공통 이름 모델로 다시 학습하면 그 줄을 없앤다
  - **PiBrain 도 Qwen + 새 llama.cpp(b11889, `/home/pi/.llama.cpp`) 로 맞췄다(261028, fc1a8f31).** 젬마는 두 기기·HF 어디에도 없다.
    `.model` 은 파이보 것을 옮겼다(두 로봇이 같은 메시 공유기에서 서로 ARP 가 안 돼 Windows 를 거쳤다). 옮긴 폴더 권한이 `drwx------`(700)였다 — 서비스는 root 라 읽지만 파이보(755)와 맞춰 둘 것. llama.cpp 는 PiBrain 에서 따로 빌드(파이보 CMakeCache 옵션 그대로).
    **옮긴 뒤 링크 `llm/llm-model.gguf` 가 없어 서비스가 바로 죽었다**(`failed`, `--log-disable` 이라 이유가 안 남음 — 로그 없이 직접 돌려 'No such file' 확인). `ln -sfn` 으로 다시 만들어 해결.
    `.model/VERSION` 대조는 실제 파일만 보므로 링크가 없어도 통과한다 — 옮긴 뒤엔 `ls -laL /home/pi/.model/llm/llm-model.gguf` 를 따로 볼 것
  - 시험 PiBrain 은 RAM 7.7GB 지만 납품품은 2GB 라 메모리 판단은 파이보(1.8GB)와 같게 한다(사용자)
- **모델 바꾸기(재학습 때마다, 261106 개정)**: 새 gguf 를 **`themaker-ko.gguf`·`themaker-en.gguf` 이름으로 덮어쓴다**(링크 아님 — HF `.model/llm/` 에도 이 이름으로 올린다) + `.model/VERSION` 의 `llm/<이름>.gguf = <원래 파일 이름>` 줄을 고친다. (261029~261105 의 방식: 새 파일을 넣고 별칭 링크를 그 파일로 `ln -sfn`)
  `.model/VERSION` sha256 목록 다시 만들기(IMAGE.md). 유닛·리포 코드는 모델 이름(`themaker-ko` 등)만 보므로 안 바뀐다.
  더메이커는 시스템 글을 안 보내므로(GGUF 템플릿이 학습 글을 넣음) 학습 글이 바뀌어도 리포는 그대로다. `SYSTEM` 은 젬마3 에만 간다.
  261026 판 `pibo-qwen3.5-0.8b-school-small-Q4_K_M.gguf` 는 339,212,576 바이트, HF `leeyunjai/themaker` 의 `.model/llm/` 에 올림(261028, sha256 `ca312fda…`).
  새 판도 같은 자리에 올릴 것(`huggingface-cli upload leeyunjai/themaker <파일> .model/llm/<파일>`). **링크 `llm-model.gguf` 는 올리지 않는다** — scp·업로드 도구가 링크를 따라가 같은 파일을 한 벌 더 만든다
- 확인(컨테이너, 가짜 llama-server·가짜 TTS): 23/23 — 흘려 받기(중간 글자), [정지] → 모델 연결 끊김·다시 보내기, 소리 끔이면 안 말함,
  고른 목소리로 말하기·[그만 말하기], 체크·목소리 기억, 새 대화, 한/영, 1366·1024·768·390 넘침 0, 어둡게, pageerror 0.
  **실기기로는 흘려 받기·말하기 아직 안 봤다**(도구 판은 파이보에서 돌려 봤다 — 위 시간)

---

## 체험 앱 — 카드 코딩(`cards/`, 50060) · 로봇 놀이(`play/`, 50070) (261028, 시험 중)

**261123 개정(사용자): 폴더·서버를 둘로 나눴다.** 대문에는 [카드 코딩] · [로봇 놀이] 두 카드, 들어가서 나뉜다.

| 앱 | 폴더 · 서버 · 포트 | 들어가면 |
|---|---|---|
| 카드 코딩 | `cards/run_cards.py` · 50060 | 도전 · 만들기 · 내 재주(버튼 3개) — 상단바 [설정](잠금 없음, 261124) |
| 로봇 놀이 | `play/run_play.py` · 50070 | 키우기 + **파이보 조종하기 / PiBrain 픽셀 그림** |
| (공용) | `kids/` | `robot.py`(로봇 손잡이 — 제품마다 · 가짜) · `screen.py`(화면 그림) · `sounds/`(효과음 — IDE 쉬움 블록도 이 경로를 쓴다) · `make_voice.py` · `make_sounds.py`. 두 서버가 `sys.path` 에 넣어 쓴다 |

- 두 앱은 같은 모터·화면·스피커를 쓰므로 **한 번에 하나만** — IDE `run_ide.py` 의 `kids_app()` 이 하나를 켤 때 다른 하나를 끈다(`KIDS_APPS`, `stop_kids(only)`). 도구·분류기·대화·검수 켜기와 코드 실행 때는 둘 다 꺼진다. 예전 주소 `/kids` 는 로봇 놀이로
- 저장 폴더 `/home/pi/.kids` 는 같이 쓴다 — 카드 코딩 `p/1/{tricks,progress}.json` · `settings.json`(차시·목소리·소리 크기, 카드 코딩 [설정]에서 바꿈), 로봇 놀이 `p/1/pet.json` · `p/1/art/`(픽셀 그림첩). 카드 코딩 [처음부터 하기] 가 `p/1` 을 통째로 지운다(키우기·그림첩까지)
- 내용 파일도 나눴다: `cards/content.json`(카드·차시·도전·말) · `play/content.json`(키우기·키우기 말·조종하기·그림 칭찬 말). 도전 결과 그림은 키우기 친구 그림(`pet.js`)이라 `cards/static/pet.js` 는 `play/static/pet.js` 의 사본이다 — 같이 고칠 것. `cards.css` · `play.css` 도 앞부분(버튼·처음·대화상자)이 같다
- **조종하기**(파이보만): 방향 단추(앞으로 `forward1` · 뒤로 `backward1` · 왼쪽/오른쪽으로 돌기 · 가운데 [멈춤] = 끊고 처음 자세) + **다리·발(M0·M1·M6·M7)을 쓰지 않는 동작** 19개(openpibo-models 0.4.9 `motion_db` 82개 중 54개가 그렇다, `play/content.json` 의 `drive`). 누르면 바로 한다(`POST /api/drive {id}`) — 하던 것이 있으면 끊고 새것. 동작은 끝나면 처음 자세, 방향 단추와 `hold`(하이파이브·보기·손 들기)는 끝난 자세 그대로(방향 단추 뒤 처음 자세는 261124 에 뺐다, 사용자). 위에 '넓고 평평한 바닥에서' 띠. **실기기 확인 필요** — 동작 이름, 걷기 중 끊기, 빨리 바꿔 누를 때 서보 전원 강하
- **픽셀 그림**(PiBrain 만, `play/pixel.py`, 261123 — 블록 쌓기를 바꿨다. 사용자: 게임은 교육과 거리가 있고, **물리 버튼을 계속 누르는 놀이는 고장 위험**이라 버튼을 안 쓴다): 태블릿에서 칸을 칠하면 **LCD(240x320)에 바로**(0.08초에 한 번까지 마지막 모습만 — `POST /api/art/show`).
  캔버스 **12x16(한 칸 20px) · 24x32(10px)** — 둘 다 LCD 에 딱 맞는 정수 배율. 도구: 연필 · 지우개 · 채우기 · 되돌리기(40번) · 모두 지우기 · 12색(`pixel.PALETTE`, 0 = 흰 바탕 = 지우개)
  - 재미: **움직이는 그림**(2~4장, [장 더하기] = 지금 장을 복사, 앞 장이 옅게 비친다 — 느리게 2 · 보통 4 · 빠르게 8장/초, `POST /api/art/play`) · **그린 순서 다시 보기**(지금 장을 칠한 순서대로 약 4초 동안 LCD 에, `steps` — 장마다 3000칸까지) · **내 그림첩**(`p/1/art/<번호>.json`, 30장, 넘으면 409) · 저장하면 로봇이 '우와, 멋진 그림이야!'(효과음 tada + 말)
  - LCD 는 일꾼 스레드 하나(`art_worker`)가 가장 최근 요청만 그린다 — 새 요청이 오면 재생·다시 보기를 끊는다. 화면 잠금은 `oled.py` 의 flock 이 지키므로 `robot.lock` 은 안 잡는다(칭찬 말 중에도 그림이 나온다). 화면을 나가면 IP 화면. 가짜 로봇은 `GET /api/fake/lcd.png`(시험용)
  - **실기기 확인 필요** — LCD 방향, 한 장 그리는 시간(SPI — 빠르게 8장/초가 되는지), 칠할 때 반응
- 처음 화면은 대문과 같은 활동지 카드 + 캐릭터 장면(IDE 의 `pibo-art.js` 를 받아 씀 — challenge · cards · tricks / pet · drive · art). 색: 카드 코딩 `--app-kids` 주황 `fa-shapes`, 로봇 놀이 `--app-play` 청록 `fa-gamepad`
- 대기 페이지 `launch.html?svc=cards|play[&go=make|pet|drive|art]`(`svc=kids` 는 예전 이름 → play). `LAUNCH_VER` 261126v1. IDE [로봇 놀이](`#kids_bt`)는 `svc=play`
- 확인(컨테이너, 가짜 로봇, 두 제품): 95/95 — 카드 코딩 3카드·잠금·카드 실행, 로봇 놀이 2카드·키우기 돌보기·조종하기(`greeting → stop`)· 픽셀 그림 따로 39/39(칠하기·끌기·채우기·되돌리기·지우개가 LCD 에 그대로, 장 더하기·재생(두 장을 오감)·멈춤, 다시 보기, 저장·덮어쓰기·순서 기록·24x32·열기·지우기, 잘못된 값 400, 31번째 409, 파이보엔 없음·API 400), 제품 밖 기능 400, 대문 설명·대기 페이지, 1366·1024·820·390 넘침 0, 한/영, pageerror 0

**초등학생**이 코딩 없이 카드로 로봇 친구에게 **재주를 가르치며** 순서·고치기·반복·재사용(함수)을 차시대로 익힌다(유치원은 뺐다 — 사용자 결정).
핵심은 **아이가 저장한 재주가 다음 수업의 카드가 되는 것** + 차시 + 아이별 기록. [키우기](다마고치)는 아이별 친구로 남고 2차에서 이벤트·조건의 재료가 된다.
**파이보·PiBrain 같은 코드**(`cards/` · `play/` · `kids/` 통째로 — 템플릿은 탭 아이콘 `?ver` 만 다름, 원본은 파이보 리포 — 고치면 PiBrain 에도 복사). 제품은 `--device pibo|pibrain`.
설계·차시·도전 규칙·확인 필요는 **파이보 리포 `KIDS.md`**.

- **대문 카드로 연다**(261123 — IDE [로봇 놀이] 버튼 `#kids_bt` 는 IDE 상단바의 다른 앱 버튼과 같이 뺐다). 대기 페이지 `launch.html?svc=play` → `/play?enable=on`(IDE 가 띄움) → 50070. 탭을 닫으면 `beforeunload` 가 `/cards|/play?enable=off`(keepalive, 키트 `PiboUI`). 손으로 띄울 때는 `sudo /home/pi/.pyenv/bin/python3 cards/run_cards.py --device <제품>`(또는 `play/run_play.py`)
- **저장 한 벌(261116, 사용자)**: 번호·그림 고르기를 뺐다 — 앱을 켜면 바로 처음 화면, 저장은 `/home/pi/.kids/p/1/` 하나. 반이 바뀌면 [설정] [처음부터 하기]
- **카드 더(261116, 사용자)**: 동작·이동·내 동작(도구에서 저장한 `mymotion.json`, 파이보) · 내가 쓴 말(20자) · 화면(그림·글자, `kids/screen.py`) · 사진 찍기 · 센서 '~할 때까지'(파이보 터치·PIR, PiBrain 버튼) · '만약 ~하면'(3초 동안 살핌 — 주사위 카드는 261120 에 뺐다, 사용자) · 차시 9(이벤트)·10(조건) · **저장한 재주 카드는 1차시부터 [재주] 탭에**(전엔 7차시부터). 음 카드(도~솔)는 다른 카드처럼 아이콘 + 이름(261120 — 큰 글자와 이름이 두 번 나왔다). 자세한 건 파이보 리포 `KIDS.md` '0-1'. **실기기 확인 필요** — 터치·PIR 읽기, 동작 이름, 카메라
- **차시·도전은 `cards/content.json` 만 고친다**(`concepts` `lessons` `challenges`, 정답형 `want`·열린형 조건 열쇠). 코드는 안 바뀐다
- 재주 한도: 24개 · 3겹 · 펼쳐 300번 · 줄 20장. 자기 자신을 부르는 재주(`cycle`)·쓰이는 재주 지우기는 막는다. [블록으로 보기] 에서 재주는 IDE **함수 블록**
- 로봇 말은 처음 한 번 6~15초라 **`kids/make_voice.py --device <제품>` 으로 미리** 만든다(카드 코딩·로봇 놀이 말을 같이). 문구는 IDE `ko2en.js` 끝의 `kids_*` 키(두 리포 같은 블록)
- **[설정] — 잠금 없음(261124, 사용자 — 학생도 쓰는 앱이라)**: 상단바 [설정](톱니, `#set_bt`, [처음 화면] 왼쪽) → 오늘 차시(목표·생각해 보기 — **처음엔 '자유'(모든 차시·모든 카드)**, 261120 사용자)·목소리·소리 크기·도달 기록·[처음부터 하기](대문 공장 초기화처럼 두 번 누르기). 전엔 자물쇠 3초 → 숫자 4개(기본 1234) 잠금이었다 — 번호가 공개 문서에 있어 막지 못했고, 대문 공장 초기화도 잠금 없이 두 번 누르기라 규칙이 둘이었다. API `/api/settings`·`/api/report`·`/api/reset`(토큰 없음). 기기의 예전 `settings.json` 에 남은 `pin` 은 읽을 때 버린다. **한/영은 다른 앱처럼 상단바 언어 select**(261120, 사용자)
- **키트 변경**: body `pb-plain` 이면 `pibo-ui.js` 가 `pb-v2` 층을 얹지 않는다(그 층의 앱 버튼 규칙이 카드 색을 덮었다). `design/sync.sh` 가 `cards/static` · `play/static` 에도 복사
- **키우기 친구는 회사 파이보 캐릭터(261124, 사용자 — 대문 그림과 같은 공 머리·볼터치·벌린 입, 안경은 꾸미기. 261123 은 실물 얼굴, 261028~261122 는 써큘러스 캐릭터), PiBrain 에서는 머리가 PiBrain 보드**(검은 화면 속 하늘색 얼굴 · 카메라 · 버튼 넷): `play/static/pet.js`(사본 `cards/static/pet.js`)(`PetArt.svg(포즈, {color, hat, glasses, device})` — `play.js` 가 `C.device` 를 넘긴다). 대문 그림(`pibo-art.js`)과 같은 생김새. 상태 6(normal·happy·hungry·sleepy·sleep·sad) + 돌보기 반응(밥 eat · 놀기 ball · 씻기 wash, 2.5초) + 도전 결과(cheer·oops). 꾸미기: 색(안테나·모자·팻말·밥그릇) · 머리 소품(안테나/모자) · 안경. 돌보기는 **PiBrain 버튼 4개에 맞춰 4가지**(밥·놀기·재우기·씻기 — 늘리지 말 것, 사용자). PiBrain LCD 는 `play/make_pet_png.py` 가 미리 만든 PNG(`static/pet/lcd/`, 36장 — 상태 6 + 반응 3 × 소품·안경 4벌, **보드 머리로**)를 `face.py` 가 친구 색으로 바꿔 띄운다. LCD 에는 **점수 세 줄**(배고픔·기분·졸림, 바뀌면 다시 그림)과 **말풍선**(버튼·화면으로 돌보면 반응 포즈 + 로봇이 하는 말, 2.5초 이상)도 그린다. 글꼴은 리포의 Pretendard(woff2 — 기기 PIL 이 못 읽으면 KDL.ttf, **확인 필요**) — **pet.js 를 고치면 PNG 를 다시 만들 것**
- 세로 스크롤: 키트 `.pb-shell` 이 body 스크롤을 막으므로 `.kids-main` 이 스크롤 칸이다(261028 — 전엔 작은 화면에서 아래가 잘렸다)
- **화면(파이보 OLED·PiBrain LCD)은 IP 정보가 기본이다(261028, 사용자).** 체험 앱은 켤 때·키우기를 나갈 때·끝날 때(Ctrl+C·SIGTERM) `system/network_disp.py` 로 IP 화면을 다시 그린다(`robot.show_network`). PiBrain LCD 는 키우기에서 얼굴을 처음 그릴 때 연다(`OledByPiBrain()` 이 LCD 를 검게 초기화해서, 켜자마자 열면 IP 화면이 꺼진 것처럼 지워졌다)
- 확인은 컨테이너(가짜 로봇)뿐: 서버 51/51, 재주 → IDE Blockly 함수·파이썬 생성까지. **실기기 확인 필요** — 동작 이름(`greeting` 등)·머리 터치 값·PiBrain 버튼 순서·LCD 방향

## 분류기 (260924)

teach-lab 과 같은 기능(이미지·손·얼굴·포즈 가르치기)을 파이보 카메라로 한다.
**TensorFlow 를 쓰지 않는다.** 예전 분류기(TF.js MobileNetV2 → keras 변환 → TF 로 추론)를 통째로 바꿨다.

| 단계 | 어디서 | 무엇으로 |
|---|---|---|
| 카메라 | 파이보 → 태블릿 | socket.io `camera_image`, 320×240 JPEG |
| 특징 뽑기·학습 | 태블릿 브라우저 | MediaPipe wasm(`static/vendor/tasks-vision`) + TF.js 작은 MLP |
| 저장 | 파이보 | `POST /api/models` → `/home/pi/mymodel/<이름>/` |
| 추론 | 파이보 | `openpibo.vision_classify.CustomClassifier` — onnxruntime(이미지, 261104) / MediaPipe(손·얼굴·포즈) + numpy |

모델 폴더 하나에 `project.json` `classifier.json` `classifier.bin` `labels.txt` `samples.json`
과 특징 모델 파일(`.tflite`/`.task`)이 들어간다. teach-lab 파이썬 내보내기와 같은 형식이라
`pip install teachlab` 으로 PC 에서도 돈다. `samples.json` 은 [이어서 배우기] 용이다.

블록: `[분류기 모델 … 불러오기]`(260929 전엔 '이미지 모델 설정하기')에 폴더 `mymodel`, 이름 칸에 모델 이름.
예전엔 이름 칸이 둘(모델·라벨)이었는데 라벨 칸을 뺐다(261001v1, 두 리포). 예전에 저장한 프로그램은 `customblock_callback.js` 끝의
불러오기 감싸개가 `labelpath` 입력을 걷어내고 연다(없는 입력이 있으면 Blockly 가 `MissingConnection` 으로 멈춘다 — 없는 필드는 경고만).
폴더 선택은 그대로 둔다(사용자). '폴더 선택'(빈 값)이면 `cf.load(''+'과일')` → `/home/pi/mymodel/과일`.
파이썬 `CustomClassifier.load(model_path)` 도 인자 하나다(261001v1 — 예전 블록에 맞춰 두었던 안 쓰는 `label_path` 를 뺐다).
예전 블록이 만든 파이썬을 `.py` 로 저장해 둔 경우 `load(a, b)` 는 TypeError 가 난다 — 두 번째 인자를 지우면 된다.
**표시(261001v1)**: `cf.draw(img)` 또는 `cf.predict(img, draw=True)` — 바로 전 `predict` 가 본 것을 그 이미지에 그린다(손·포즈 점+뼈대, 얼굴 점,
종류 이름·확률은 파랑 바탕 이름표, 이미지 모델은 이름표만). 손·얼굴·몸이 안 보였으면 아무것도 안 그린다. MediaPipe 결과는
`LandmarkExtractor.detect` 를 감싸서 남긴다(teachlab 코드는 안 고침). 블록 `vision_predict_cf_vis` [이미지 … 에 분류기가 본 것 표시하기]
**예전 `model.keras` 는 못 읽는다** (불러오면 다시 학습하라는 오류). 의도한 호환 단절이다.

### 가져온 코드 — 두 곳을 함께 고칠 것

- `classifier/static/tl/` ← teach-lab `lib/` (74f421a). 바꾼 곳은 파일 첫 줄에 적었다(경로, `mirror:false`)
- `openpibo/modules/teachlab/` ← teach-lab `python/teachlab/`. 바꾼 곳은 `embedder.py` 하나 — TFLite 대신 onnxruntime(261104, 아래 '기기 요구')
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

기기에 있는 `mediapipe` 0.10.18 · `onnxruntime` 1.20.1 · numpy 1.26.4 로 돈다. 260924 에 tflite-runtime 2.14.0 으로 브라우저가 저장한 모델을 돌려
답 8/8 일치를 확인했다.

**TFLite 를 뺐다(261104, 일원화 2단계).** 사진 특징(mobilenet_v3_small)과 MoveNet 을 tf2onnx 1.17(opset 17)로 ONNX 로 바꿔 리포에 둔다 —
`openpibo/modules/teachlab/mobilenet_v3_small_embedder.onnx`(4.2MB) · `openpibo/modules/pose/movenet_lightning.onnx`(9.4MB, 가중치 fp32 라 tflite 의 두 배).
같은 입력 40장에서 TFLite(tflite-runtime 2.14.0)와 최대 차이 임베더 2e-5 · MoveNet 2e-6, 코사인 1.000000. 브라우저는 그대로 `.tflite` 를 쓴다(MediaPipe wasm).
- `ImageEmbedder` 는 project.json·모델 폴더에 적힌 `mobilenet_v3_small_embedder.tflite` 이름을 보고 같은 모델의 ONNX 를 쓴다(예전 저장 모델 그대로 열림). 다른 임베더 이름은 오류
- `Movenet()` 은 인자가 없거나 `.tflite` 면 리포 ONNX 를 쓴다(예전처럼 경로를 넘겨도 된다)
- **`TeachableMachine`(파이썬 클래스)·`load_interpreter()` 를 지웠다(261104, 사용자).** 블록(`vision_load_tm`·`vision_predict_tm`)은 전부터 정의·생성기·툴박스가 꺼져 있었고, 주석으로 남아 있던 그 코드도 세 파일(파이보·PiBrain)에서 지웠다.
  패키지 `tflite-runtime`·`openpibo-detect-models`(movenet tflite 하나 때문에 있던 약 80MB)를 `requirements.txt`·`venv_prune.py` 에서 뺐다 — 새 태그를 올린 뒤 `venv_prune.py --apply` 로 지운다
- edge-lab(PC)도 같은 임베더 ONNX 를 OpenVINO 로 읽는다(일원화 7단계)
- Pi 4(PiBrain 261106) 실측: 임베더 70ms · MoveNet 75ms(onnxruntime 1.20.1) — '모델 실측 스크립트' 표. 브라우저 모델과 같은 답인지는 실기기로 아직 안 봤다(`system/score_check.py`)
TensorFlow·torch 걷어내기 순서와 지울 목록은 IMAGE.md. 파이보에서 실제 추론 속도·메모리는 아직 못 쟀다.
포즈는 한 화면에 여러 사람이 있으면 브라우저와 파이썬이 다른 사람을 잡을 수 있다(특징 코사인이 0.3 까지 떨어진 적 있음).

---

## 음성 인식 · TTS · 메모리 (260930)

### STT — `openpibo.speech.SpeechToText`, `Speech.stt`

- 모델: **SenseVoiceSmall int8**(한·영·중·일·광둥어, 언어 자동 판별) + **silero VAD**, 실행은 **sherpa-onnx 1.13.8**
  (자기 전용 onnxruntime 을 따로 싣는다 — 기기 onnxruntime 1.20.1·numpy 1.26 은 안 건드린다). 모델은 `/home/pi/.model/stt`
- `listen(timeout, filename, end_silence=0.8)`: `arecord -D plug:dmic_sv -c2 -r 16000 -f S32_LE -t raw`(Audio.record 와 같은 장치)를
  흘려받아 VAD 로 **말이 끝나면(0.8초 조용) 멈춘다.** `timeout` 은 최대 대기. 말이 없으면 빈 문자열. 소리가 작으면 최대 20배 키운다
- `transcribe(audio, sr)`: 25초 넘는 소리는 VAD 로 말 단위로 잘라 받아 적는다(통째로 넣으면 글자가 뒤섞였다).
  **말 구간이 하나도 없으면 빈 글자(261118)** — 무음·잡음을 그냥 넣으면 '그.' 같은 글자를 지어냈다(컨테이너 재현). edge-lab `speech_routes._SenseVoice` 와 같은 계산(두 리포 같은 코드)
- **`Speech.stt(filename, timeout, verbose)` 와 블록 `speech_stt` 는 예전(서버 STT) 이름·입력 그대로**다. 옛 프로그램이 그대로 열린다.
  블록 앞의 번개(인터넷 필요) 그림만 뺐다. 모델은 처음 부를 때 한 번 올린다(파이보에서 5~12초)
- sherpa-onnx 한국어 스트리밍 zipformer 는 쓰지 않는다(빈 결과 버그, k2-fsa/sherpa-onnx#2886). Moonshine 한국어 Tiny/Base 는
  비상업 라이선스라 뺐다. **SenseVoice 모델은 FunASR Model License 1.1(Alibaba, 261118 원문 확인)** — 쓰기·복사·고치기·나눠 주기 허락, 비상업 조항 없음.
  의무는 출처·저작자 표시와 모델 이름 유지(int8 변환본도 파생물). 개정판이 자동 적용되는 조항(6)·준거법 빈칸(7)이 있어 계약에 넣을지는 법무 판단.
  기기의 `.model/stt/LICENSE-SenseVoice` 는 링크 한 줄뿐이라 원문(edge-lab `tools/licenses/FunASR-MODEL_LICENSE.txt`)으로 바꿔 올릴 것(HF, 사람이) — 다시 거론하지 말 것(261124, 사용자)
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

### 모델 실측 스크립트 (261104) — `system/bench_models.py`

로봇 연동 일원화(아래 '로봇 연동 일원화') 1단계. 모델마다 새 파이썬 프로세스로 올림 시간·첫 회·중간·p90(ms)·RSS(기본·최고)를 재고
`/home/pi/bench_<호스트>_<날짜시각>.json` 으로 남긴다. **파이보·PiBrain 같은 파일**(고치면 같이).

```bash
sudo /home/pi/.pyenv/bin/python3 /home/pi/openpibo-os/system/bench_models.py           # 모델별
sudo /home/pi/.pyenv/bin/python3 /home/pi/openpibo-os/system/bench_models.py --combo   # LLM+TTS+STT+인식 함께
```

- 대상: ed-s-320 · mobilenet_v3_small(onnx) · MediaPipe 손(두 손)·얼굴·자세 lite·손동작 · MoveNet(onnx) · OMZ 0004·0005·0013·0003·0095 · dlib 68점+resnet(예전 비교용, 지운 뒤엔 건너뜀) · mask.onnx
- 입력: `--image` 가 없으면 카메라 한 장. 얼굴은 0004 로 찾아 30% 여유로 잘라 얼굴 모델에 넣는다. 얼굴이 없으면 결과에 '얼굴 없음'
- **인터넷을 쓰지 않는다.** **파이보·PiBrain 은 오프라인 전용 — 로봇이 돌 때 실행되는 코드(라이브러리·서비스·이 실측)는 모델을 내려받지 않는다(261104, 사용자).** 모델(얼굴 0005·0095 · 마스크)은 이미지 작업 때 `system/fetch_models.sh` 로 `/home/pi/.model` 에 넣는다(사람이 따로 돌리는 도구 — 리포에 있어도 된다). 예전 `--fetch` 는 그래서 뺐다
- `--combo` 는 **서비스를 끈다**(tools·classify·llama-server@*), `llama-server@<--llm>`(기본 general) 을 띄우고 끝나면 끈다. 0.2초마다 남은 메모리 최저·스왑 최고·llama RSS 최고
- 측정 전후 온도·`vcgencmd get_throttled` 를 적는다. 저전압 비트가 서면 값을 버리고 전원부터 볼 것(파이보는 서보가 같은 전원 — 서보를 움직이지 않은 상태로 잴 것)
- 확인(컨테이너 x86, 기기와 같은 onnxruntime 1.20.1·openvino 2024.5.0·mediapipe 0.10.18·tflite-runtime 2.14.0): 모델별 12개 돌고 없는 파일은 건너뜀.
  dlib·`--combo` 는 컨테이너에 llama·TTS·STT 가 없어 **오류 경로만** 봤다
- **PiBrain 실측(261106, fc1a8f31 · Pi 4 · 20회 · 스레드 4 · throttled 0x0 · 54.5→65.7°C, 카메라 한 장)** — 파이보는 같은 보드라 속도는 같게 보고, 메모리는 납품 2GB 기준으로 볼 것. `--combo` 는 아직
  | 모델 | 올림 s | 중간 ms | 최고 RSS MB |
  |---|---|---|---|
  | 사물 ed-s-320 | 2.11 | 376 | 181 |
  | 사진 특징 mobilenet_v3_small (onnx) | 0.20 | 70 | 112 |
  | MediaPipe 손(두 손) / 손동작 8종 | 1.81 / 1.76 | 206 / 205 | 229 / 203 |
  | MediaPipe 얼굴 + 표정 | 1.56 | 71 | 172 |
  | MediaPipe 자세 lite / MoveNet (onnx) | 1.94 / 0.16 | 201 / 75 | 233 / 114 |
  | 얼굴 찾기 0004 → **0005** | 0.36 → 0.54 | 51 → **64** | 136 → 187 |
  | 나이·성별 0013 / 감정 0003 | 0.23 / 0.27 | 9.6 / 8.5 (첫 회 163 / 116) | 151 / 147 |
  | 얼굴 구분 **0095** / dlib(예전) | 0.71 / 3.32 | **33** / 489 | 156 / 178 |
  | 마스크 mask.onnx | 0.14 | 27 | 95 |
  - 기본 RSS(파이썬 + numpy 등) 약 64MB. 얼굴 구분은 dlib 의 약 15배 빠르다. 0005 는 0004 보다 13ms 느리고 51MB 더 쓴다
  - 얼굴 한 명 구분(찾기 0005 + MediaPipe 얼굴 점 + 0095) ≈ 64 + 71 + 33 ≈ 170ms — 예전(0004 + dlib) ≈ 540ms

### `/home/pi/.model` 과 `requirements.txt`

- `/home/pi/.model` 은 리포 밖(이미지)이다. 구성과 파일별 sha256 은 그 폴더의 `VERSION`. 코드가 읽는 것: `tts/assets/{onnx,voice_styles}`,
  `stt/`, `llm/{general,themaker-ko,themaker-en}.gguf`(261106 부터 실제 파일 — 판은 `VERSION`, 261029~ 별칭 링크였다), `object/ed-s-320.onnx`, `hand/*.task`, `face/{detection,age-gender,emotion,landmark,reid}`(261104 — 0005·0095, '얼굴 (261104)').
  `classifier/`(예전 TF 가중치)는 260930 에 지웠다(아무도 안 씀)
- 모델은 `leeyunjai/themaker`(HF)에서 손으로 받는다. **`git clone` 말고 `huggingface-cli download`** — clone 은 `.git/lfs` 에 한 벌을 더 남긴다(이번에 약 400MB)
- `requirements.txt`(리포 맨 위): 리포 코드가 직접 import 하는 패키지만, 기기 버전으로. `test/requirements.txt` 는 260923 전체 스냅숏(TF·torch 포함)
- **안 쓰는 패키지 걷어내기는 `system/venv_prune.py`(260930).** 기기에서 돌리면 `ROOTS`+`requirements.txt` 와 그 의존만 남기고 나머지를 목록으로 보여 주고,
  `--apply` 로 지운다(백업 목록·pip check·import 확인까지). 260930 두 기기 site-packages 5.5~5.6GB 의 대부분이 TF·torch·MeloTTS 잔재다.
  mediapipe 0.10.18 은 jax 를 불러오지 않는다(지우고 확인함, `--jax`). 패키지를 새로 쓰게 되면 `ROOTS` 와 `requirements.txt` 둘 다에 넣을 것. 자세한 건 IMAGE.md
  **261116: 두 기기(파이보 cd488e95 · PiBrain fc1a8f31) 모두 4개(`dlib`·`openpibo-dlib-models`·`openpibo-detect-models`·`tflite-runtime`, 약 221MB)를 지웠다** — 남김 105개, import 38/38, 분류기 onnx ok. `pip check` 의 'mediapipe requires jax' 두 줄은 예상된 것(jax 를 안 불러온다). 남은 선택 항목 pandas·scikit-learn·seaborn(약 143MB)은 리포 코드가 안 쓰지만 학생 수업용으로 남겨 둔다(사용자, 261116 — `--optional` 쓰지 말 것)

## 로봇 연동 일원화 (261104 착수) — edge-lab(PC) · 파이보 · PiBrain

**같은 기능은 같은 파일 형식 · 같은 특징 계산 · 같은 결과 모양, 모델 크기만 기기별**(PC 크게, 로봇 작게). PC 에서 가르친 AI 가 로봇에서 그대로 돌게 한다.

| 기능 | 기준 | 로봇에서 할 일 |
|---|---|---|
| 사물 인식 · 학습 | easydetect `.onnx` 하나 · easydetect-lab | 없음(이미 같다). 로봇 ed-s-320, PC ed-m-640 |
| 분류 — 사진 특징 · 손 · 몸 · 표정 · 저장 파일 | **로봇(teach-lab) 방식** | 없음 — edge-lab 이 바꾼다 |
| 손동작 8종 · 나이·성별·감정 · TTS | 그대로 | 없음 |
| 자세 보기 | 결과 모양만 COCO 17점 | 모델은 기기별(로봇 MoveNet) |
| 얼굴 찾기 | **retail-0005** | **했다(261104)** — '얼굴 (261104)'. Pi 속도는 실측으로 볼 것 |
| 얼굴 방향 | MediaPipe 계산 | 없음 |
| 얼굴 구분 | **OpenVINO retail-0095** | **했다(261104)** — '얼굴 (261104)'. dlib 빼기. `landmark_face(_vis)` 는 dlib 68점 번호 유지, `train_face`·`recognize`·`save_db`·`load_db` 이름·인자 유지, 얼굴 정보 파일 pickle → JSON/npz(예전 파일은 다시 등록 안내). 재등록은 괜찮다(사용자) |
| 마스크 | edge-lab `mask.onnx` | **했다(261104)** — `Face.mask_face`, '얼굴 (261104)' |
| TFLite | onnxruntime | **했다(261104)** — '분류기 → 기기 요구' |
| STT | **SenseVoice int8**(261118 — edge-lab 도 Whisper 에서 바꿈, 같은 파일 `models/stt-sv`) | 없음. 라이선스는 '음성 인식 · TTS · 메모리' 절 |
| LLM | 모델은 기기별 | 말투·프롬프트만 맞춤 |

순서: ① 실측(`system/bench_models.py`) ② TFLite → ONNX ③ 얼굴 정리 ④ 마스크 ⑤ 모델 받기 인증 ⑥ 같은 점수 점검 도구 ⑦ edge-lab 가르치기 전환.
- **⑤ 인증은 넣지 않는다(261104, 사용자).** 분류기 `POST /api/models` 는 지금처럼 인증 없이 받는다 — edge-lab 은 사설 IP 로봇에만 보낸다
- **⑥ 했다(261104).** 같은 사진을 로봇 · PC · 브라우저에 넣어 답·확률·특징을 견준다. `system/score_check.py`(파이보 · PiBrain · edge-lab `tools/score_check.py` **같은 파일**)가
  `run <모델> <사진 폴더> --out x.json` 으로 결과 파일을 만들고(어디서 도는지는 스스로 안다 — openpibo 가 있으면 로봇, 아니면 edge-lab), `compare a.json b.json [c.json]` 로 견준다(다르면 끝 코드 1).
  브라우저 몫은 `http://<로봇 IP>:50010/static/check.html`(분류기를 켠 뒤 — 같은 `tl/` 코드로 계산, 짧은 변 240 으로 줄여 넣고 [결과 파일 받기]). 화면 메뉴에는 안 넣었다(점검용).
  확인(컨테이너, 사진 17장): 로봇 vs PC 답 17/17 · 특징 최대 차 1.0e-6, 로봇 vs 브라우저(Chromium) 답 17/17 · 확률 최대 차 0.04 · 최저 코사인 0.975(JPEG 풀기·줄이기 차이). **실기기·실제 태블릿 결과는 확인 필요**
- **⑦ 했다(261104, edge-lab).** edge-lab 이 로봇과 같은 `teachlab`(같은 코드·같은 모델 파일)으로 특징을 뽑고, 같은 머리(Dense 64 → 0.2 → softmax, 40회·16)로 배우고,
  로봇 형식(`project.json`·`classifier.json/bin`·`labels.txt`·`samples.json`)으로 저장한 뒤 [로봇으로 보내기] 가 이 `POST /api/models`(50010)로 보낸다(`project.app = "edge-lab"`).
  확인(컨테이너): 같은 사진에서 특징 차이 1.5e-6 이하, 보낸 모델을 `CustomClassifier` 로 돌린 답·확률이 edge-lab 과 17/17 같음. **`/api/models` 의 받는 형식을 바꾸면 edge-lab `train_routes.robot_send` 도 같이 바꿀 것**
**파이썬 API·블록은 그대로 호환되게, 바꾸는 건 함수 안에서만(261104, 사용자).** 이름·인자·돌려주는 모양·기준값을 바꾸지 말 것 — 새 기능은 함수·블록을 더하는 것으로(예: `Face.mask_face`). 예외: 블록이 이미 꺼져 있던 `TeachableMachine` 은 지웠다(사용자).

## 얼굴 (261104) — `openpibo/vision_face.py`, dlib 없음

일원화 3단계. **파이보·PiBrain 같은 파일**(차이는 `detect_mesh_vis` 글자 위치 한 줄 — 파이보 y-40, PiBrain y-30).

| 기능 | 모델 | 바뀐 것 |
|---|---|---|
| 얼굴 찾기 `detect_face` | OMZ face-detection-retail-**0005** | 0004 → 0005. 입출력 모양이 같아 코드는 경로만 |
| 얼굴 점 `landmark_face` | MediaPipe 얼굴 점 478개에서 **dlib 68점 번호로 골라** 돌려준다(`MP_TO_DLIB68`) | 학생 코드의 점 번호(예: 36·45 눈꼬리, 8 턱 끝)가 그대로. 상자 둘레 25% 넓혀 잘라 찾는다. 못 찾아도 예전(dlib)처럼 늘 68점 — 상자에 평균 얼굴 점(`MEAN68`, LFW 300장 평균)을 맞춰 돌려준다 |
| 얼굴 구분 `train_face` `recognize` | OMZ face-reidentification-retail-**0095**(숫자 256개, L2) | MediaPipe 점 5개(두 눈 가운데·코끝·입 끝 둘)로 128x128 정렬(OMZ 기준점, 닮음 변환). 점을 못 찾으면 상자만 잘라 넣는다 |
| 오차도 `score` | 코사인 거리 × 2/3(`SCORE_SCALE`) — **기본 `face.threshold = 0.4` 그대로**(코사인 0.6 이 0.4) | 예전 dlib 유클리드 크기에 맞춰 학생 코드의 `score < 0.4` 같은 비교가 그대로 통한다. 낮을수록 비슷한 건 같다 |
| 얼굴 정보 파일 `save_db` `load_db` | **JSON**(`format: openpibo-facedb`, `model: face-reidentification-retail-0095`) | pickle 을 열지 않는다. 예전 파일·다른 모델 파일은 '얼굴을 다시 등록해 주세요' 오류. 파일 이름은 넘긴 그대로(확장자 안 붙임) |
| ~~사물 따라가기~~ | — | **261106 에 지웠다(사용자)** — `object_tracker_init`·`track_object`·`track_object_vis`, 블록 3개, 파이보 도구 [카메라] '사물 추적' 타일. 아래 '사물 추적 삭제' |

- **파이썬 API·블록 호환(261104, 사용자): 이름·인자·돌려주는 모양·기준값을 바꾸지 않고 함수 안에서만 바꾼다.** 블록·`examples/vision_face1.json`·`vision_face2.json` 그대로. 달라진 건 `get_db()` 의 숫자 개수(128 → 256)와 얼굴 정보 파일 형식(다시 등록 — 사용자 확인)뿐
- **LFW 공개 사진(성인) 1000쌍으로 비교(261104, 컨테이너 x86)**: 0095 최고 정확도 99.5%(거리 0.676), 0.6 에서 다른 사람 오인 0% · 같은 사람 놓침 2.2%.
  dlib(예전 코드와 같은 68점 → 인코딩)은 최고 97.8%(0.594)인데 **예전 기준 0.4 에서는 같은 사람을 71.6% 놓쳤다**(정확도 64.2%).
  68점 번호 맞추기는 dlib 68점과의 평균 차이가 두 눈꼬리 거리의 5.8%(중간값, p90 10.6% — 턱선은 두 모델의 정의가 달라 차이가 큰 쪽)
- 얼굴 하나 처리(점 찾기 + 정렬 + 0095) x86 13.9ms · dlib 78.2ms. **Pi 4(PiBrain 261106): 0095 33ms · dlib 489ms**, 찾기 0005 64ms('모델 실측 스크립트' 표). **교실 아이 얼굴 인식률은 확인 필요** — 기준값(코사인 0.6 = 오차도 0.4)은 아이들 사진으로 다시 볼 것
- 기능 확인 17/17(컨테이너): 같은/다른 사람, 68점 모양·순서, 얼굴 없는 상자, JSON 왕복, 예전 pickle·다른 모델 거부, 나이·감정·mesh 그대로, 추적기 이동 따라감
- 패키지 `dlib`·`openpibo-dlib-models`(68점 약 99MB + 구분 약 22MB)를 `requirements.txt`·`venv_prune.py`·`venv_rebuild.sh`(컴파일 목록)에서 뺐다 — 새 태그를 올린 뒤 `venv_prune.py --apply`
- **마스크 `mask_face(img, item)` (261104, 일원화 4단계)** → `{"mask": True/False, "score": %, "box"}`. edge-lab 과 같은 `/home/pi/.model/mask/mask.onnx`(임베더 + 분류기 한 개)를 onnxruntime 으로,
  얼굴 상자 둘레 30% 를 붙여 자르고 teach-lab `crop_to`(= TM cropTo, edge-lab `MaskCls._prep` 과 같은 쌍선형) 224, 0~255 float 그대로. 종류 이름은 파일 메타데이터 `edge-lab.classes`. 처음 부를 때 올린다.
  같은 자른 그림에서 edge-lab(OpenVINO f32)과 확률 최대 차이 1.2e-6, 답 120/120 일치. LFW 맨얼굴 60/60 no mask, 그려 넣은 마스크 60/60 mask(진짜 마스크 사진은 확인 필요).
  **블록은 아직 없다** — 파이썬·블록 이름 맞추기(일원화 8단계) 때 같이 정한다
- **0005·0095 파일이 `/home/pi/.model/face/` 에 먼저 있어야 한다**(`sudo bash system/fetch_models.sh` — 이미지 작업. 실행 코드는 내려받지 않는다). 없으면 `Face()` 가 파일 이름을 담은 오류
- **사물 추적 삭제(261106, 사용자 — 쓸모가 작다는 판단, 사물 인식이 대신한다)**: 두 리포의 `Detect.object_tracker_init`·`track_object`·`track_object_vis`(261104 에 CSRT 로 바꿨던 것), IDE 블록 `vision_object_tracker_init`·`vision_object_track`·`vision_object_track_vis`(정의·생성기·툴박스·`ko.js`/`en.js` 문구·블록 가이드 그림),
  파이보 도구의 '사물 추적' 타일·클릭 처리·`object_tracker_init` 소켓. API 호환 규칙의 예외다(사용자). **예전 프로그램은 그대로 열린다** — `customblock_callback.js` 끝 불러오기 감싸개가 추적 블록을 걷어낸다(설정·표시 블록은 빼고 뒤를 당기고, 추적하기 값 블록은 칸을 비움. 컨테이너 Blockly 로 확인). 파이썬에서 부르면 AttributeError
- **도구 [카메라] '얼굴 구분' 타일(261113, 파이보·PiBrain 도구)** — 예전 시험 화면 `system/face_web.py`(261106)를 지우고 도구로 옮겼다. 몸통은 `openpibo/modules/face_tool.py`(`FaceTool`, 두 리포 **같은 파일**) — 라이브러리 `Face` 의 `train_face`·`recognize`·`delete_face`·`save_db`·`load_db` 만 쓴다. 타일을 고르면 패널: 이름 + [등록](지금 카메라 그림의 가장 큰 얼굴) · 등록한 얼굴 목록(이름·장수·×) · [모두 지우기] · [내보내기](`facedb.json`) · [가져오기](형식·모델이 틀리면 목록 그대로). 관리 탭은 따로 두지 않았다(사용자). **목록은 접어 둔다(261113, 사용자)** — 늘 보이는 건 이름 칸·[등록]·[기준] 막대, 목록은 `▸ 등록한 얼굴 · N명` 한 줄(누르면 펼침, 브라우저에 기억 `pibo_face_list`), 내보내기·가져오기·모두 지우기는 `⋯` 메뉴, 긴 안내는 `?` 를 눌러 펼친다(태블릿엔 마우스 올리기가 없어 누르는 방식). REST 는 두 도구가 같다: `GET /face/list` · `POST /face/train {name}` · `POST /face/delete {name|'*'}` · `GET /face/export` · `POST /face/import`(본문 JSON, 5MB) → `{ok,msg,count,name,names,ready,error}`(msg 는 `ko2en.js` 키). 인식 결과는 다른 타일처럼(파이보 socket.io `stream`, PiBrain `/vision_result`) `민수 0.18 | ? 0.62`, 그림에는 파랑(등록)·회색 `?` 상자 + PIL 한글 이름표. **얼굴 정보는 `/home/pi/code/facedb`**(`Face.save_db` JSON, 바뀔 때마다 저장, pi 소유) — IDE 블록 [얼굴 사전 불러오기] 기본값(code · facedb)과 같아 도구에서 등록한 얼굴을 학생 프로그램이 바로 쓴다. 공장 초기화 때 `code/` 와 같이 지워진다. **[기준] 막대(0.1~0.8, 처음 0.4)** — 수업 거리로 바꿀 수 있게(사용자): 낮추면 엄격(같은 사람도 `?`), 올리면 느슨(다른 사람 오인). `POST /face/threshold {value}` → `face.threshold`, 목록 응답에 `threshold`. 라이브러리 기본 `THRESHOLD = 0.4` 는 그대로고 도구를 다시 켜면 0.4. 학생 코드는 `face.threshold = 0.3`(블록은 없다). PiBrain 은 카메라가 꺼져 있으면 `face_err_camera`. 확인(컨테이너, LFW 가짜 카메라, 실제 서버 + 브라우저): 파이보 21/21 · PiBrain 22/22(등록·구분·지우기·내보내기·가져오기·잘못된 파일·파이보 파일을 PiBrain 에서 열기·한/영·390/768/1024 넘침 0). **실기기 확인 필요**

## 사물 인식 (261026) — easydetect ed 모델 파일

`openpibo.vision_detect.Detect.detect_object` 는 **easydetect ed 모델 `.onnx` 파일 하나**를 onnxruntime 으로 돌린다(`openpibo/modules/ed_onnx.py` 의 `EdOnnx`).
easydetect-lab 지시서(`docs/pibo-integration.md`, 473dbe3) 그대로다. **예전 사물 인식 모델(Ultralytics)의 코드·가중치·고지는 261026 에 다 지웠다 — 되돌릴 길을 남기지 않는다**(지시서).
파이보·PiBrain **같은 코드**(`ed_onnx.py` 는 같은 파일, `vision_detect.py` 는 같은 부분을 같이 고칠 것).
(같은 날 지시서가 두 번 바뀌었다: 폴더(`model.onnx`·`labels.txt`·`model.json`) → **파일 하나**. 폴더 형식은 쓰지 않는다)

- **모델 파일**: ONNX opset 17, 입력 `images`, 크기는 파일마다 고정(320·640 …) — **파일에서 읽고 막지 않는다**.
  파일 안 메타데이터(`custom_metadata_map`): `easydetect.names`(이름 JSON `{"0":"person","1":"컵"}`, 없으면 번호) · `easydetect.conf`(문자열 숫자, 없으면 0.5)
- 기본 `/home/pi/.model/object/ed-s-320.onnx`(COCO 80, HF `leeyunjai/themaker` 의 `.model/object/ed-s-320.onnx`) — `vision_detect.py` 의 `OBJECT_MODEL` 한 줄.
  더 좋은 COCO 모델은 같은 이름으로 파일만 바뀐다. lab 에서 받는 모델은 `job<번호>.onnx` 파일 하나다(261028 — 전엔 `pibo-job<번호>.onnx`. 내용·읽는 방식은 같다)
- **lab 의 `pibo/detect.py` 는 불러오지 않는다**(내용만 맞춘다). `EdOnnx` 의 `preprocess`·`postprocess`·`drop_duplicates` 는 그 파일과 같은 계산이고 **비교 기준**이다.
  lab `pibo/detect.py` 가 바뀌면 같이 맞출 것(지시서 4절: letterbox 없이 resize, sigmoid 는 로짓일 때 한 번만, NMS 없음, 클래스 상관없이 IoU 0.7 겹침 제거).
  `detect.py` 는 메타데이터가 없으면 옆의 `labels.txt`·`model.json` 을 찾지만 `EdOnnx` 는 지시서대로 번호·0.5 로 한다(같은 폴더의 엉뚱한 `labels.txt` 를 읽지 않게)
- 출력 둘(boxes `(1,Q,4)` cxcywh 0~1, scores `(1,Q,C)`)은 마지막 차원으로 가른다. **클래스가 4개면 둘 다 4라 못 가르므로 출력 이름 `boxes` 를 쓴다**
  (`detect.py` 는 먼저 나온 것을 상자로 본다 — lab export 는 `boxes` 가 먼저라 결과는 같다)
- conf 는 파일의 `easydetect.conf`(없으면 0.5), iou 는 0.7 — 부를 때 넘기는 값(openpibo 는 늘 0.5·0.4)보다 우선한다. iou 0.4 는 말 위의 사람처럼 실제로 겹친 다른 물체를 지운다
- **점수(%)는 반올림**(`int(round(round(score, 2) * 100))`) — lab·`detect.py` 의 `:.2f` 와 같게(전엔 버림)
- 고르는 법: `Detect(object_model=파일)` · `detect.load_object_model(파일)` · `load_object_model()`(기본으로) ·
  IDE 블록 [사물인식 모델 [폴더] (이름).onnx 불러오기] — 블록이 `폴더+이름+'.onnx'` 를 넘기므로 `/home/pi/code/job3.onnx` 는 [code] (job3). 기본 글자 `job1`(261028, 전엔 `pibo-job1` — 예전에 저장한 프로그램은 적힌 글자 그대로 열린다)
- **못 쓰면 오류를 낸다**(다른 모델로 몰래 바꾸지 않는다): 파일 없음 → `FileNotFoundError`, onnxruntime 1.13 미만·읽기 실패 → `RuntimeError`(이유·버전 포함).
  실패하면 경로는 바뀐 채로 두어 다음 `detect_object` 도 같은 오류를 낸다(예전 모델로 조용히 돌지 않게)
- 모델을 바꿀 때 이전 세션을 놓는다(`EdOnnx.close`). 모델은 처음 `detect_object` 를 부를 때 올린다(QR·마커만 쓰면 메모리 안 씀)
- 이름표 그리기는 PIL: `detect_object_vis`, 파이보 도구 [카메라](`tools/lib.py` `object_detect`, KDL.ttf 22). `cv2.putText` 는 한글을 못 그린다
- **기본 파일이 기기에 없으면 사물 인식이 오류로 멈춘다.** 이 코드를 기기에 올리기 전에 `/home/pi/.model/object/ed-s-320.onnx` 를 먼저 넣을 것(IMAGE.md)
- 확인(컨테이너, onnxruntime 1.20.1 = 기기 버전): 두 리포 22/22 — lab(easydetect 0.7.9 `pibo_export.build`)에서 만든 실제 `pibo-job1.onnx`(당시 이름, ed-n 30에폭, `빨간 공`·`파란 상자`,
  conf 0.45)와 같은 가중치의 640 판이 사진 12장에서 `detect.py` 와 이름·점수·상자(차 0px) 같음, 가짜 파일(로짓·확률·클래스 4개·메타데이터 없음·640·COCO 이름) 같음,
  파일 conf 0.30 이면 0.5 아래 상자도 나옴, sigmoid 두 번 안 함, 오류 네 가지, 열 번 바꿔도 RSS 그대로, 한글 그리기.
  lab 화면(torch, best.pt)과는 17개 중 16개 — 하나는 0.6150(torch)·0.61501(ONNX)로 반올림 경계였고 `detect.py` 도 같은 차이.
  **파이보 실측은 확인 필요**
- **ed-s-320 8비트 판(261116)**: easydetect 가 같은 이름으로 HF 파일을 바꿨다 — ONNX Runtime QDQ 8비트(Conv 만, stem·디코더는 float), 26.7MB, sha256 `c019e6d7…a040`.
  입력 `images` float 0~1 · 출력 `boxes`/`scores` · 메타데이터(이름 80개, conf 0.50)·lab `pibo/detect.py` 가 그대로라 **코드는 고칠 것 없다**.
  확인(컨테이너, onnxruntime 1.20.1 = 기기 버전): 사진 23장에서 `EdOnnx` 와 lab `detect.py` 의 이름·점수·상자 23/23 같음(차 0px), `Detect.detect_object` 두 리포 같음.
  easydetect 기록으로는 Pi 4 에서 318ms · COCO mAP50-95 0.384. **기기에는 새 파일을 넣고 `.model/VERSION` sha256 을 다시 만들 것**(IMAGE.md) — 실측은 `bench_models.py --only ed_s_320`
  **파이보 실측(261116, cd488e95, 20회·스레드 4)**: 올림 1.08초 · 첫 회 326ms · 중간 316ms · p90 354ms · 최고 RSS 177MB(예전 float PiBrain 376ms·181MB). throttled 0xe0000(부팅 뒤 클럭 제한·스로틀·온도 제한 있었음, 저전압 없음), 57.0→67.2°C — 소프트 온도 한계(60°C) 위라 후반에 클럭이 내려갔을 수 있다. 파이보 냉각(방열판·통풍) **확인 필요**
  **PiBrain 실측(261116, fc1a8f31, 같은 조건)**: 올림 1.04초 · 첫 회 296ms · 중간 290ms · p90 310ms · 최고 RSS 179MB, throttled 0x0, 50.1→62.3°C. 같은 보드에서 파이보가 26ms(약 9%) 느린 건 열로 클럭이 내려간 탓으로 본다(파이보만 throttled 비트가 섰다). 깨끗한 값은 290ms — 예전 float 376ms 보다 약 23% 빠르다
- 포즈는 MoveNet 그대로, mediapipe 는 `load_hand_gesture_model` 에서 처음 import 한다(손 제스처를 안 쓰면 안 올라온다)

---

## 화면 v2 (260924) — 시안 B, **유일한 화면**

260924 부터 기본이었고, **260929 에 예전 화면(v1)을 지웠다**(이 절 끝 'v1 삭제'). 이름에 남은 'v2'
(`ide/static/v2/`, `body.pb-v2`, `--v2-*`)는 그대로 둔다 — 바꾸면 고칠 곳만 늘어난다.

**PiBrain(openpibo-os.pibrain)도 같은 화면·키트·분류기를 쓴다(260924).** 원본은 이 리포다.
`design/`·`ide/static/v2/`·`ide/templates/index.html`·`classifier/`·`openpibo/vision_classify.py`·`modules/teachlab/` 을
고치면 PiBrain 에도 옮길 것(키트는 `design/sync.sh ~/openpibo-os.pibrain`). PiBrain 에서 다른 점은
그쪽 CLAUDE.md '화면 v2' · '분류기' 표에 있다(배터리 칸 없음, 언어 키 `classifier_language` 등).
시안 A·B·C(Scratch식·MakeCode식·Arduino식) 중 **B(MakeCode식)** 로 정했다(260924).

- IDE: `run_ide.py` 의 `/ide` 는 늘 `templates/index.html`(`body.v2-app`, 261123 부터 `/` 는 대문 `home.html`). CSS·JS 는 `ide/static/v2/ide.css` · `ide.js`
- `index.js` 는 v1 시절부터 쓰던 한 벌이다. `index.js` 에서 id 를 바꾸거나 새 요소를 찾게 되면 `templates/index.html` 에도 넣을 것.
  v1 용 코드가 조금 남아 있다(편집기 cobalt/duotone-light 스위치 등 — `ide.js` 가 떼어 낸다)
- 도구·분류기: 마크업은 거의 그대로, `<body class="… pb-refresh pb-v2">` 두 층(`pibo-ui.css`)이 색·모양을 바꾼다.
  상단바 노랑, 주 동작 파랑. 도구 왼쪽 메뉴에만 라벨(`.pb-navlabel`)을 넣었다

### A안 배치 (IDE, 261118 — 사용자 확정, 교육 현장 의견)

수업 중 실제로 보는 건 실행·화면 출력·출력·입력이고 파이보 정보는 거의 안 본다는 현장 의견으로, 시안 A(Pibo IDE 시안 캔버스의 'A · 밝고 친근')의 **배치만** 가져왔다
(블록 모양은 시안을 따르지 않는다 — 261118 에 렌더러로 시험했다가 가독성 때문에 그대로 두기로 함, 사용자). PiBrain 도 같다.

- 상단바 48px(**다른 앱과 같은 줄, 261123 사용자 — '대문이 있으면 IDE 상단바도 다른 것과 같아야'**): **[파일](`#v2_side_toggle`, 폴더 아이콘)** · `piBo · 코딩` | 블록/파이썬 | [⋯] · [처음 화면](`#home_bt`) · [전체화면] · [밝기](키트가 끼움) · 언어 select
  - [⋯]: 글자 크기 · 파이썬 편집기 테마(코딩에만 있는 것). 밝기·언어는 상단바로, 공장 초기화·전원 끄기·소스 코드는 대문 [설정]으로 옮겼다
  - 예전 앱 버튼(도구·대화·분류기·로봇 놀이·도움말 — `#tools_bt` 등)은 뺐다. 앱은 대문에서 고른다. 이름은 대문 카드와 같은 '코딩'(`v2_brand`, 탭 제목 `piBo .211 · 코딩` — 전엔 `piBo 메이커`)
- **파일 서랍**(`#v2_side.v2-drawer`, `body[data-side]`): 경로 + [추가](새 파일·새 폴더·올리기) · 목록 · 미리보기. 편집기 **위로** 열린다(밀지 않음, z-index 80).
  처음 열면 열려 있고(파일부터 고르게 — 261102 현장 요청을 이어 감), **파일을 열면(#codepath 가 바뀌면)·편집기나 실행 화면을 누르면·×** 로 닫힌다. 편집기 줄의 파일 이름을 눌러도 열린다
- 편집기 줄: 파일 이름 · 미저장 표시 · [쉬움|전체] · [파이썬 코드] · [저장] · **실행 화면 접기**(`#v2_stage_toggle`)
- **오른쪽 실행 화면**(`#v2_stage`, `body[data-stage]`, 폭 조절 `--pane-stage` 340px · 1100px 이하 300px): [실행][정지] + 실행 상태(`#run_status`) · 화면 출력(`[모니터 화면에 보여주기]` 블록) · 출력(지우기) · 입력.
  접기는 기억한다(`localStorage pibo_v2_stage`, 처음엔 900px 이상이면 펼침). **실행을 시작하거나 화면 출력이 오면 다시 편다** — 실행 중에 직접 접으면 그 실행 동안은 펴지 않는다.
  양쪽(서랍·실행 화면)을 다 닫으면 블록만 넓게 쓴다. **900px 이하**(태블릿 세로)에선 편집기 줄 아래로 블록 위에 뜨고, 블록 쪽을 누르면 접힌다
- **아래 상태 줄은 없앴다(261123, 사용자 — 'IDE 만 하단바가 있는 것도 잔재, 하단바 기능은 대문/설정에')**. 버전·시리얼·WiFi·온도·메모리·켜진 시간·배터리(충전)는 대문 [로봇 상태], WiFi 설정·H/W 검수는 대문 [설정]. 연결이 끊기면 키트 배너(`watchSocket`)가 알린다. 서버의 10초 `system`·배터리 방송(`periodic_system_update`)도 뺐다
- 요소 id 는 그대로 옮기기만 했다 — `index.js` 는 고치지 않았다(`#result_en` 은 실행 화면, `#browser_en` 은 서랍 안). 새 문구 키는 IDE `ko2en.js` 끝(`v2_stage` `v2_files_open` `v2_connected` `v2_disconnected`)
- 예전 B 배치(왼쪽 패널 `[파이보 | 파일]` 탭 + 맨 아래 실행·정지)는 261118 에 바꿨다. 도움말 캡처(`docs/source*/notes/images/ide_*`)·사용법 글(`notes/piboMaker.md` 한·영)은 261120 에 A안으로 다시 만들었다(컨테이너, 가짜 소켓)
- 툴박스: **블록 찾기**(맨 위) + 색 타일 분류(아이콘을 분류 색 칸 안에). `ide.js` 가 Blockly 10 의 `ToolboxCategory` 를 바꿔 끼운다
- 화면 출력은 경로 `/home/pi/.tmp.jpg` 로 구분한다(`ide.js` 의 `LIVE_PATH`). `run_ide.py` 의 `/show` 경로를 바꾸면 같이 바꿀 것
- 확인(컨테이너 미리보기, 파이보·PiBrain): 1920·1366·1024·820 × 한/영 × 부드럽게/어둡게 32경우씩 — 가로 넘침 0 · pageerror 0 · 서랍 열림→파일 열면 닫힘, 서랍·실행 화면 버튼·탭 동작, 파일 열기 확인창. **실기기·실제 태블릿 확인 필요**

### 파일 목록 아이콘 (261102)

`index.js` 의 `fmIcon()`(`update_file_manager` 위) — 종류마다 Font Awesome 아이콘과 색: 폴더(호박색) · `usb` 폴더(fa-brands fa-usb) · `.py` 코드 · `.json` 블록(퍼즐) ·
그림 · 소리 · 영상 · 모델(onnx·tflite·task·bin·gguf, 큐브) · 글(txt·md·csv) · 압축 · 그 밖은 회색 파일. 색은 `v2/ide.css` 의 `--fm-*`(어둡게는 밝은 판).
**클릭 처리는 첫 칸 html 에 `folder`/`file` 이 있는지로 가르므로 아이콘에 `data-kind='folder|file'` 을 꼭 넣을 것.** 줄마다 걸던 jQuery 흐려짐(`animate opacity`)은 뺐다 — 줄 배경(hover)·아이콘 확대로 대신한다(삭제는 빨강)
- **줄 오른쪽 칸 순서: 내려받기 · 이름 바꾸기 · 복사·옮기기(261123) · 지우기.** 복사·옮기기는 `copy_popup()`(`index.js`, 템플릿 `#copyPopup`) → socket `copy`/`move` `{src, dst}` → `run_ide.py` `copy_move`. 받을 폴더는 code · myimage · myaudio · mymodel · usb 고정(서버 `COPY_DESTS` 와 화면 `COPY_DESTS` 를 같이 고칠 것). 장치를 넘어도 되고(USB exFAT ↔ SD), 같은 이름이면 `이름_1`. 결과는 `copy_done`/`move_done`·`err_copy_*` 알림. 자세한 건 IMAGE.md '서랍 [복사·옮기기]'. **실기기 확인 필요**

### 블록 수준 — 쉬움 / 전체 (261116, 사용자)

edge-lab 의 블록 수준을 본떠 IDE 에 **2단계**(사용자: 3단계 대신 2단계)를 넣었다. **편집기 줄의 [파이썬 코드] 왼쪽** [쉬움 | 전체](블록 모드에서만 보인다 — 처음엔 [더보기] 안에 넣었다가 찾기 어려워 밖으로 뺐다, 사용자), 처음엔 **전체**(지금과 같음). 760px 이하는 아이콘만
- 코드는 `ide/static/v2/levels.js` 한 파일(**파이보·PiBrain 같은 파일**, 제품은 `<html data-product>`). `customblock.js`(수정 금지)·`customblock_toolbox.js`(영문판 델타)는 건드리지 않는다 —
  `Blockly.WorkspaceSvg.prototype.updateToolbox` 를 감싸 `toolbox_dict[lang]` 이 오면 쉬움 툴박스로 바꿔 낀다. 그래서 델타 16개는 그대로
- 쉬움 툴박스: 블록 찾기 · 시작·반복(클릭했을 때·**계속 반복**·N번 반복·기다리기) · 만약(만약·만약~아니면·비교·그리고/또는·아니다) · 동작(파이보) · 불빛 · 말·소리 · 화면 · 센서 · AI 눈 · 점수.
  기존 블록은 전체 툴박스 항목(그림자·기본값)을 그대로 가져온다
- 새 블록 `ez_*` 16개 — 카메라·변수·이미지를 블록 안에 숨기고 고르기만 한다: `ez_forever`(while True) · `ez_motion`(로봇 놀이와 같은 동작 16개) · `ez_sound`·`ez_note`(`kids/sounds/*.wav`) ·
  `ez_picture`(`ide/static/ez/<그림>_<가로>x<세로>.png` — `kids/screen.py` 로 미리 그림, 128x64·240x320 두 벌) · `ez_text` · `ez_clear` · `ez_touch`·`ez_pir`(파이보, PIR 은 `send_cmd(30,'on')` 을 한 번) · `ez_button`(PiBrain) ·
  `ez_seen`(얼굴·손·사람) · `ez_gesture`(손동작 7가지) · `ez_emotion`(표정 5가지, 도움 함수 `ez_emotion()`) · `ez_score_add`·`ez_score_reset`·`ez_score`(`ez_score = {'value': 0}` — 함수 안에서도 global 없이 쓰게)
- **더한 쉬움 블록(261116, 사용자)**: 동작에 '멈추기 (처음 자세)'(`stop`) · `ez_mymotion`(도구에서 저장한 `mymotion.json` 이름, 파이보) · `ez_music`(기본 음악 `openpibo-files/audio/music` + **내 음악** `code/`·`myaudio/` 의 mp3·wav, 틀어 두고 다음 블록으로) · `ez_music_stop` · 음 도~높은 도 8개(`kids/sounds/la·si·do2.wav` 추가 — `make_sounds.py`) · [카메라] 분류 `ez_photo`(그대로/얼굴 표시/사물 표시 × 모니터 화면/로봇 화면, 계속 반복 안이면 동영상처럼) · `ez_picture` 에 '모니터 화면' 선택(예전 프로그램은 로봇 화면으로 열림).
  음악·내 동작 목록은 IDE `GET /ez_lists`(`run_ide.py`, 두 리포 같은 코드)에서 받는다. 저장한 값이 지금 목록에 없어도(파일을 지움) 그 값 그대로 열린다(`ez_dyn` 확장). 확인(컨테이너): 파이보 12/12 · PiBrain 11/11 + 기존 17/17. **실기기 확인 필요** — 음악 폴더 내용, `oled.imshow` 로 사진이 OLED 에 보이는 모양
- 만드는 파이썬은 기존 블록과 **같은 definitions_ 열쇠·객체 이름**(camera·_face·detect·oled·device·motion·audio)을 쓴다 — 쉬움·전체 블록을 섞어도 한 번씩만 만든다. 센서·AI 블록은 그 순간 한 번 본다(계속 반복 안에서 쓰는 전제)
- 수준은 브라우저에 기억(`localStorage 'pibo_block_level'`), **파일에는 넣지 않는다**(저장 표시 비교가 꼬인다). 툴박스만 바뀌므로 쉬움에서 전체 수준 파일을 열어도 블록은 다 보인다
- 블록 문구는 `levels.js` 안의 ko/en(`Blockly.Msg.EZ_*`, 툴박스를 그릴 때마다 지금 언어로 넣는다). 메뉴 문구는 IDE `ko2en.js` 의 `v2_level*`
- 확인(컨테이너): 파이보·PiBrain 11/11 — 메뉴, 쉬움 분류(파이보 9·PiBrain 8 + 찾기), 쉬움 블록 25·24개 만들기·코드, 섞은 프로그램의 파이썬(문법·가짜 라이브러리로 실행 순서), 새로 고침 뒤 유지·영문, 전체 예제 열기, 전체로 되돌리기, pageerror 0.
  전체 툴박스 회귀 162·149 블록 오류 0. **실기기 확인 필요** — 센서·카메라 블록 결과, 그림 PNG 가 OLED·LCD 에 맞게 보이는지. 도움말 블록 가이드 끝에 '쉬움 블록' 절이 있다(261120 — `gen_block_guide.py` 가 `PiboLevel.toolbox()` 로 쉬움 툴박스를 받아 `ez_*` 만 그린다. 소제목은 `쉬움 · 동작` 처럼 — 전체 분류와 같은 제목이면 autosectionlabel 경고)

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

- **261101 중간안(사용자)**: 260624v1 의 색 계열(노랑 시작·연보라 논리·연두 반복·하늘 수학·주황 글자 …)로 되돌리되, 블록 위 흰 글자 대비가
  3.3:1 이상이 되도록 OKLCH 로 밝기만 낮췄다(색상각은 그대로, 채도 ×1.15). 260624v1 은 1.9~3.8:1 이라 거의 안 읽혔고, 260924 색은 계열이 전부 달라
  예전 교재와 안 맞았다. 기본 블록의 `colourSecondary` = 기본색 35% 흰색 섞기, `colourTertiary` = 80% 밝기. PiBrain 도 같은 값
  | 분류 | 260624v1 → 지금 | 분류 | 260624v1 → 지금 |
  |---|---|---|---|
  | 시작 | `#E5B900` → `#D1A909` | 논리 | `#B098CB` → `#9C81BA` |
  | 반복 | `#85B687` → `#629A66` | 수학 | `#2196F3` → `#0191F2` |
  | 글자 | `#FFAA08` → `#C18008` | 목록 | `#4DB6AC` → `#099D93` |
  | 색 | `#DFADB2` → `#B47E84` | 변수 | `#EF9A9A` → `#CF7273` |
  | 함수 | `#C7BCB8` → `#968A86` | 소리 | `#7dc37D` → `#4C9E4F` |
  | 수집 | `#7d7db3` → `#7C7CBA` | 장치 | `#d3b28d` → `#AB875D` |
  | 동작 | `#d38d62` → `#C97A47` | 화면 | `#8da2c3` → `#778EB3` |
  | 음성 | `#8dc3d2` → `#5795A6` | 시각 | `#a39c7D` → `#958D69` |
  | 인식 | `#6E92B7` → `#6791BB` | 기타 | `#CC9988` → `#B77E6B` |
  - **시작은 조금만 진하게**(`#D1A909`, 대비 2.2:1, 사용자). 노랑은 밝기를 많이 낮추면 색상각이 같아도 갈색·겨자색이 된다(3.3:1 의 `#AA8903` 이 그랬다).
    흰 글자가 3:1 넘는 노랑은 없다. 글자는 '클릭했을때' 한 줄·깃발 아이콘뿐이라 받아들였다. 글자(주황)는 진하게 해도 주황 계열로 보여 중간안 그대로
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
  [저장](예전 [등록하기])이 그 카드의 꽉 찬 버튼, 지우는 버튼 둘은 판 없는 빨강이고 이름을 갈랐다(`clear_frames` 표 비우기 /
  `remove_all_motions` 동작 모두 지우기). 표는 내용만큼(최대 500px, 예전 고정 높이와 같다)이고 비면 `.motion-empty` 안내, 예제는 알약.
  새 키는 `tools/static/ko2en.js` **끝**에 붙였다(1·2행이 영문판 델타)
  - **로봇 칸은 늘 왼쪽에 고정**(그림을 보며 모터를 맞추는 화면이다). 오른쪽만 스크롤되게 `position: sticky`,
    화면 높이보다 크면 `index.js` 의 `fitRobot()` 이 `zoom` 으로 줄인다(모터 칸이 px 로 자리 잡혀 있어 통째로 줄여야
    모양이 유지된다. 1366×768 에서 0.87). 900px 이하(태블릿 세로)만 위아래로 쌓는다.
    한때 1200px 아래에서 표를 로봇 아래로 내렸는데 표를 보면 로봇이 화면 밖으로 나가서 되돌렸다
  - **점 숫자에 바로 입력(261116, 사용자 — 모터 10개를 빨리 넣게)**: 번호 점 안의 숫자가 입력칸이다(`.mdot__in`, `type=number` — 태블릿에서 '-' 있는 숫자 자판). 누르면 그 모터를 고르고 글자를 전부 골라 둔다 → 바로 치고 Enter = 보내고 **다음 모터**(점 순서 5·4·2·8·3·9·1·7·0·6), Shift+Enter 앞 모터, 마지막 모터에서 Enter 면 [추가·수정] 으로 가서 Enter 한 번 더로 표에 넣는다. ↑↓ 1°(Shift 5°), Esc 되돌림, 나갈 때도 보낸다. 범위 밖은 경고창 없이 끝값 + 점 테두리 잠깐 빨강(`is-clamped`). **레인지는 고른 점 옆에 같은 높이로 붙는 한 줄 상자**(`.mslide`, `placeSlide` — 바깥 팔 2·3/8·9 는 몸 안쪽, 다리 1·0/7·6 은 바깥, 머리는 오른쪽. 위아래로 펴면 1024·태블릿 세로에서 아래 점을 덮었다. 이름·범위는 상자 title). **시간·[추가·수정] 은 [처음 자세] 줄 오른쪽**, 옆 조작 패널(`.mside`/`.mpanel`)은 없앴고 키 안내는 그림 아래 한 줄. 예전 큰 숫자칸(`#mp_num`)·[−5 −1 +1 +5] 는 뺐다(사용자). 확인(컨테이너, 가짜 로봇 + 실제 `run_tools.py`): 22/22 + 레인지 상자 겹침 0(1024·1280·1366·1920·820, 모터 10개마다) — 10개 연속 입력·보낸 값·표 추가·끝값 맞춤·화살표·Esc·레인지·표 줄·처음 자세·1024/1366/1920/820 넘침 0. **실기기·태블릿 자판 확인 필요**
  - **사진 위 번호 점 + 옆 조작 패널 (260928)**: 사진에는 모터 번호와 현재 각도만(`.mdot`, 위치는 `index.js` 의 `MDOT`,
    `pibo_body.min.png` 기준 %), 누른 모터 하나를 옆 패널(`.mpanel`)에서 슬라이더로 조절한다(261116 부터 숫자는 점에서 바로 — 위 줄).
    예전 모터 칸(`#mN_value`/`#mN_range`)은 v2 에서 숨기고 **값 저장소로 그대로** 쓴다 — 표 클릭·처음 자세 등 기존 코드가
    `.val()` 로 바꾸면 300ms 마다 읽어 온다. 보내는 건 기존과 같은 `set_motor` 하나이고, [±] 를 빠르게 눌러도
    150ms 모아서 한 번만 보낸다(서보 명령 폭주 방지). 슬라이더는 놓을 때, 숫자는 Enter·포커스 이동 때 보낸다.
  - **줄 맞춤 (260928, 901px 이상)**: 두 카드를 화면 높이(`--motion-h`, `fitRobot` 이 잰다)에 맞추고 위·아래 끝과 윗줄(40px)을 맞춘다.
    왼쪽 `[처음 자세 · 키 안내]` / `사진 + 조작 패널`, 오른쪽 `[반복 · 실행 · 정지 · (이 줄 지우기) · 표 비우기]` / `표`(여기만 스크롤) / `저장 칸`(140px).
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
    화면의 '연결됨이 되면 처음 자세로' 는 **안 됨 → 됨 으로 바뀔 때 한 번만** 돈다(`robotOn`). 서버가 답하게 되면서 5초마다 자세가 초기화될 뻔했다
  - 준비 전에 [카메라] 탭을 열면 그때 보낸 `vision_sleep` 이 버려지므로, 연결됨이 되면 지금 탭 기준으로 다시 보낸다
  - **[음성] 음성 인식(261027)** — 오른쪽 카드가 [듣기]: [말해 보기](꽉 찬 버튼) → `stt` 이벤트 → `Pibo.stt()` 가 `SpeechToText.listen(timeout=10)`
    (말이 끝나면 0.8초 조용에서 멈춤). 모델(약 240MB)은 처음 누를 때 한 번 올린다(`stt_warm`, 잠금 — 파이보 약 5초, `stt_state` loading → listening → `stt_result {ok,text|error}`).
    녹음과 **같은 마이크라 같은 `mic_lock`** — 듣는 중엔 [녹음]이, 녹음 중엔 [말해 보기]가 잠긴다. [말할 글자로 넣기]는 들은 글자를 왼쪽 말하기 칸에 넣는다(인식 → 합성 체험).
    [녹음]은 같은 카드 아래로 내리고 옅은 파랑. PiBrain 은 마이크가 없어 넣지 않았다.
    **확인 필요(기기):** 도구가 카메라 인식 모델 + 목소리(약 330MB) + 음성 인식(약 240MB)을 같이 올렸을 때의 메모리·스왑, 모터가 움직일 때 인식률.
    컨테이너 시험(가짜 모델) 8/8 — 순서·한 번만 올림·빈 결과·오류·마이크 잠금 양쪽
  - **[음성] 목소리 On/Off 는 없앴다(260929).** 번역·대화가 빠진 뒤로 [말하기]를 막는 것 말고 하는 일이 없었다
  - 검증: 무거운 모듈을 지연 있는 가짜로 바꿔 실제 `run_tools.py` + 브라우저로 돌렸다(연결됨 → 카메라 → 사물·손 → 얼굴 순서, 중간·다 된 뒤
    새로 고침, 처음 자세 재전송 0, 목소리 준비·말하기). **파이보 실기기에서 단계별 시간은 아직 못 쟀다**
- **도구 [카메라] 인식 표시는 라이브러리 `*_vis` 로(261113)**: `tools/lib.py` 의 얼굴·얼굴 점·사물·손·QR·포즈·마커가 직접 그리던 것을 걷고 `detect_face_vis`·`detect_object_vis` 등 라이브러리 함수를 부른다(PiBrain 도구 `process_frame` 과 같은 그림·같은 결과 글자 — 전엔 사물 상자가 파이보 빨강·PiBrain 초록으로 달랐다). 얼굴 분석은 가장 큰 얼굴, 포즈 결과에 `analyze_pose` 를 붙였다. 그림 모양을 바꾸려면 라이브러리를 고칠 것
- **도구 [카메라]·[음성] (260928)**: 카메라는 4:3 화면 칸 + '기다리는 중' 안내(`.v-stage[data-has]`), 방향 슬라이더 정리.
  비전 기능은 select 대신 **타일**(`#v_tiles`, `index.js` 가 select 의 option 으로 만든다 — 누르면 select 값을 바꿔
  원래 `detect` 흐름 그대로). 마커 길이는 마커일 때만(`#article_vision[data-func]`). 음성은 이름표 폭을 맞춘 폼,
  꽉 찬 파랑은 [말하기]·[녹음하기] 하나씩
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
- [WiFi 설정] 팝업의 영어 안내(Scanning… · Scan failed … · Connecting…)를 번역(`wifi_*`). 목록에 뒤늦게 붙는 글자라 `data-key` 로는 안 바뀐다 — `t()` 로
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
  IDE 는 [더보기] 안에서 **상단바**로 옮겼다(261123 부터 다른 앱과 같은 자리 — [처음 화면] 옆, 999px 이하 아이콘만). PiBrain 도구에는 없던 버튼을 넣었다(`nav_fullscreen`)
- 켜면 쿠키 `pibo_fs=1`(포트와 상관없이 세 앱이 같이 본다). **사용자가 끄면**(버튼·Esc) 지운다.
  탭을 바꾸거나 대문 카드·[처음 화면] 으로 페이지를 옮겨 풀린 건 끈 게 아니므로 남긴다(`enterService`·`goHome` 이 `fsLeaving` 을 찍고, 풀린 뒤 400ms 에 화면이 가려져 있으면 남김)
- 쿠키가 있고 전체화면이 아니면: 화면이 보일 때 안내(`fs_tap` '화면을 한 번 누르면 전체화면으로 돌아가요'), **아무 곳이나 처음 누를 때**
  `pointerdown` 에서 다시 켠다(누른 동작은 그대로 된다). 전체화면 버튼을 누른 건 제외(켜자마자 꺼지므로)
- 대화 웹(261026)도 키트를 써서 같은 버튼이 있다(예전 llama.cpp 화면에는 없었다)
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
| 연결 점 숨쉬기 | 도구 `#onoff_val[data-state=on]`(IDE `.v2-dot` 은 아래 상태 줄과 같이 261123 에 없어졌다) | `pb-breathe` |
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

## 디자인 시스템 · 문구 규칙 (261028)

모든 화면(IDE·도구·분류기·대화·대기 페이지·H/W 검수·도움말)을 **한 제품처럼** 맞췄다. 파이보·PiBrain 은 제품 이름·아이콘·하드웨어 기능만 다르다.
전후 캡처는 컨테이너에서만 봤다 — **실기기·실제 학교 노트북·태블릿 확인 필요**.

**구형 브라우저 기준(사용자, 261028)**: Chrome/Edge 88+(Windows 7 마지막 Chrome 109), Safari 14(iPadOS 14), Firefox 78.
우리 코드에 넣지 말 것 — `:has()` `:is()`/`:where()` CSS 중첩 `@container` `@layer` `color-mix()` `backdrop-filter` `dvh/svh` `aspect-ratio`(padding-top 비율로) `inset` 줄임,
`:focus-visible` 만 쓰는 포커스(`:focus` 를 먼저), JS `Array.at` `structuredClone` `Object.hasOwn`. 남겨 둔 것: flex/grid `gap`(Safari 14.1+), `min()`·`calc()`, 장식용 `conic-gradient`·`mask`, `position: sticky`.
세련됨은 새 기능이 아니라 값(색·간격·모서리·글꼴)을 고르게 하는 것으로 낸다

**색 값은 키트 한 곳**(`design/pibo-ui.css` 의 `--v2-*`, `html[data-theme=light|dark]` 로 바꿈). IDE `--c-*`·PiBrain 도구 `--c-*`·예전 `--pb-*` 는 **별칭만** 둔다(`--c-ink: var(--v2-ink)`). 색을 고칠 땐 키트만.
- 주 동작: 밝게·부드럽게 파랑 `#2563eb`, **어둡게는 노랑**(`--v2-dark`). 그 밖의 강조(포커스·슬라이더·선택·모터 번호·진행 막대·링크·상태 줄)는 **세 밝기 모두 파랑**
  (어둡게 `#7aa7ff`, 옅은 칸 `#1f2c4d`, 글자 `#bcd2ff`, 강조 위 글자 `#10131a`) — 사용자 A안. 예전 연보라(#8e98ff 등)는 없앴다
- 보조 글자 `--v2-ink-3` 은 바탕·카드 모두 4.5:1 이상(soft #5f6779 · light #646c7f · dark #8c94a7). 빨강 `#d6393f`(흰 글자 4.5:1), 초록 글자 `#157a4b`
- 크기: 상단바 `--header-h` 48 · 버튼·입력 `--ctl-sm/md/lg` 32/40/48 · 모서리 `--r-chip/ctl/card/dlg/pill` 6/8/12/16/999 · 간격 `--sp-1…5` 4/8/12/16/24 ·
  글자 `--fs-xs…xl` 12/13/14/16/20 · 굵기 400/700 둘뿐(Pretendard 파일이 두 벌이라 600·800 은 700 과 같게 보인다)

**아이콘 (261102)**
- **제품 마크**: 상단바의 Font Awesome `robot`·`brain` 대신 파이보 얼굴(고리 안테나·둥근 눈)·PiBrain 보드(화면·십자 버튼) 그림. 원본 `design/marks/{pibo,pibrain}.svg`(두 리포 같은 파일).
  키트 CSS 가 `.pb-header__brand`·`.v2-brand`·`.v2-stat` 안의 `<i class="fa-robot|fa-brain">` 글리프를 마스크 그림으로 바꾼다(템플릿·체험 앱의 class 전환은 그대로). 도움말 상단바·H/W 검수는 같은 그림을 SVG 로 직접 넣었다
- **탭 아이콘(파비콘)** `*/static/icon.png`·도움말 `_static/icon.png` = 학습지 종이색 둥근 칸 + 갈색 괘선 테두리 + 남색 펜 제품 마크(64px, 261123 — 전엔 노랑 칸). `?ver=261124v1`(회사 캐릭터 마크로). 마크를 바꾸면 다시 만들 것(브라우저로 그려 저장 — 마크 SVG 44px 를 칸 가운데에)
- **앱 아이콘은 어디서나 같게**: 도구 `fa-screwdriver-wrench` · 대화 `fa-comments` · 분류기 `fa-graduation-cap`([AI 가르치기]와 같음) · 로봇 놀이 `fa-gamepad`(261123 전엔 `fa-shapes` — 그건 이제 카드 코딩) · 도움말 `fa-circle-question` — IDE 상단바와 대기 페이지(`launch.html`)
- 대화 화면의 도구 표시는 알약 + 도구 아이콘(불빛·보기·움직이기·멈춤), 실패는 빨간 ✕ 아이콘
- IDE 상단바도 다른 앱과 같이 999px 이하에서만 아이콘만(261123 — 전엔 앱 버튼이 많아 1439·1299px 에서 줄였다)

**화면 규칙**
- **앱을 나가거나 다른 앱으로 옮기면 로봇 화면은 무조건 IP 화면(261116, 사용자).** IDE `run_ide.py` 의 `show_ip(keep)` — `/tools` `/classifier` `/llm` `/kids` `/hwtest` 의 켜기·끄기와 코드 [정지] 때, 끄이는 앱(유닛·대화 웹·체험 앱·검수)이 다 내려간 뒤(최대 20초 기다림) `network_disp.py` 를 띄운다. 코드 실행을 시작할 때는 하지 않는다(학생 프로그램이 그린 것을 덮지 않게). 체험 앱 안에서도 처음 화면으로 돌아오면 IP 화면
- **로봇 화면은 한 번에 한 프로세스만 쓴다(261120, PiBrain 실기기에서 LCD 반전).** `openpibo/oled.py` 의 모든 화면 클래스가 초기화·`show`·`clear` 를 파일 잠금 `/tmp/openpibo_screen.lock`(flock — 프로세스·스레드 모두)으로 감싼다.
  도구를 열면 IDE 의 `show_ip` 와 도구 시작의 `start_network_disp`(PiBrain 도구)가 거의 같이 `network_disp.py` 를 띄워, 두 프로세스가 같은 SPI 에 쓰면서 D/C 핀이 섞여 그림 바이트가 명령으로 들어갔다(흰 바탕 반전·카메라 그림 이상 — 웹 화면은 정상).
  PiBrain LCD(ILI9341)는 리셋 핀이 없어(`rst=None`) **재부팅해도 LCD 상태가 남는다** — 라이브러리 초기화 순서에 반전 끄기가 없어서 `OledByPiBrain()` 이 반전 끔(0x20)·보통 표시(0x13)·8색 모드 끔(0x38)을 보낸다. 소프트 리셋(0x01)은 열 때마다 화면이 하얗게 깜빡여서 뺐다(261120 실기기). 도구는 켜질 때 스스로 IP 화면을 그리므로 IDE `/tools` 는 켤 때 `show_ip` 를 부르지 않는다(같이 그리면 두 번 깜빡였다 — 반전이 261116 의 `show_ip` 부터 생긴 이유). 파이보 OLED(SSD1306)는 초기화 순서에 '반전 아님'이 있어 다시 열면 풀린다.
  화면에 쓰는 코드를 새로 만들면 이 클래스를 거칠 것(`self.oled` 를 밖에서 직접 쓰지 말 것). 확인(컨테이너, 가짜 장치 4프로세스 동시): 예전 코드는 동작 15번 겹침 → 0번. **실기기 확인 필요**
- **상단바 왼쪽 로고를 누르면 로봇 화면(파이보 OLED · PiBrain LCD)이 IP 화면으로 돌아간다(261030, 사용자).** 키트 `pibo-ui.js` 의 `screenReset` 이 모든 앱의 `.pb-header__brand`·IDE `.v2-brand` 에 걸고, IDE(80) `POST /screen_reset` 이 `system/network_disp.py` 를 띄운다([출력 지우기] 의 화면 초기화와 같은 일, 여러 번 눌러도 하나만). 로봇 놀이 키우기 화면도 IP 로 덮는다
- 상단바: 모든 앱 48px + 아래 1px 선, 왼쪽 `[제품 아이콘] piBo · 도구`(코딩은 `piBo · 코딩`), 오른쪽 순서 (앱 동작) · 처음 화면 · 전체화면 · 밝기 · 언어. 언어는 늘 **지금 언어를 보여 주는 select**
- **제품 표기는 `piBo` · `piBrain`(261125, 사용자 — 화면·도움말·캡처에 보이는 글자).** `<html data-product="piBrain">`, 대문·상단바·문구(`ko2en.js`)·도움말 페이지·`.po`·캡처 모두 `piBrain`. **코드 이름은 그대로**(`OledByPiBrain`·`DeviceByPiBrain`·`PiBrainRobot`·`pibrain_chat.PiBrain` 등 — 클래스는 단어마다 대문자, 공개 API 라 바꾸면 예제·블록 생성기·학생 프로그램이 깨진다). 제품을 가르는 비교는 대소문자를 무시한다(`/brain/i.test(data-product)` — `levels.js`·`chat.js`·`home.js`·`pibo-art.js`, 도움말 `base.html` 은 `pb_product|lower`). 주석의 'PiBrain' 은 그대로 둬도 된다
- 브라우저 탭 제목(261125, 사용자 — 탭이 좁으면 '처음 화면 · pi…' 만 보여 기기를 못 갈랐다): **`제품 .IP끝 · 앱`** — `piBo .211 · 도구` / `piBrain .37 · Tools`, `piBo .211 · 처음 화면`. `<html data-product="piBo|PiBrain">` + `<title data-key=…>` 에 앱 이름만 두면 키트 `fixTitle`(`PiboUI.tabPrefix`)이 앞에 붙인다. 주소가 IP 가 아니면(`localhost`) `piBo · 도구`. 키트를 안 쓰는 곳도 같은 꼴: 대기 페이지(`launch.html` `setTitle`)·H/W 검수(`test/index.html` 끝 스크립트 — 인쇄 파일 이름은 따로)·도움말(`_static/pibotheme.js` 의 `fixTitle`, `html_title` 은 `도움말 · piBo` 그대로)·체험 앱(`document.title = 이름` 뒤 키트가 붙임)
- **꽉 찬 버튼은 한 구역(카드)에 하나**: IDE [실행](저장·+추가는 옅은 파랑 `.v2-btn--tint`), 분류기 [AI 가르치기](저장은 옅게), 도구 [동작] 왼쪽 [추가·수정]·오른쪽 저장 칸 [저장], [음성] 카드마다 [말하기]·[녹음하기], 대화상자 [확인]
- 선택 표시는 **옅은 파랑 하나**(타일·목소리·메뉴·표 줄·열린 파일·PiBrain 버튼 칸). 상단 탭·세그먼트만 흰 알약
- 제목: 카드 제목 16/700 + 왼쪽 노랑 막대 4×16(`.pb-title`), 구역 이름 13/700 ink-2(`.pb-label`)
- 대화상자 한 벌(키트): 흐림 없는 어두운 막, 모서리 16, 안쪽 20, 버튼 40. **오류 알림은 빨간 아이콘** — 키트 `markAlerts` 가 `alert_popup` 을 감싸 키 이름(`err*`·`*error`·`*fail`·`*invalid`)으로 가른다
- 알림·띠: 경고 노랑 옅은 칸, 오류 빨강, 정보 파랑(청록 안 씀). 어둡게에서도 어두운 칸
- 카메라 칸 `.pb-stage`, 빈 화면 `.pb-empty`(아이콘 + ink-2 글자 + 버튼) — 도구·분류기·PiBrain 같이. 도구 왼쪽 메뉴는 Font Awesome(예전 PNG 는 안 씀)
- 도움말(8080)도 쿠키 `pibo_theme` 를 따른다(`docs/source/_static/pibotheme.js`, `_templates/base.html` 이 `<head>` 에서 싣는다 — `html_js_files` 는 body 끝이라 늦다). Furo 의 밝기 버튼이 쿠키도 바꾼다.
  **도움말에도 같은 48px 노랑 상단바**(`_templates/base.html`): `[아이콘] piBo · 도움말`(제품 이름은 `html_title` 에서) · 오른쪽 [IDE](80 으로) · [전체화면] · [밝기] · 언어 select — 다른 앱과 같은 순서·같은 글자(261120, 밝기는 Furo 버튼 대신 키트처럼 밝게 → 부드럽게 → 어둡게, 999px 이하 아이콘만, 전체화면은 쿠키 `pibo_fs` 를 같이 본다 — `_static/pibotheme.js`). 데스크톱은 고정, 63em 이하는 Furo 모바일 머리줄을 숨기고 메뉴·목차 버튼을 상단바로 옮긴다. 예전 4px 노랑 줄·사이드바 언어/IDE 알약은 없앴다. 파일은 두 리포 같다
- H/W 검수는 인쇄 보고서라 최소만: 화면에서만 노랑 띠·Pretendard·파랑 #2563eb·모서리 8, 일련번호 제목은 인쇄 때만

**최종 검토 반영(261027v4)** — 두 번째 화면 검토(실사용 상태로 전 화면 캡처)에서 나온 25개:
- 키트: `--v2-on-red`(빨간 꽉 찬 버튼 글자 — 어둡게는 #10131a, 흰 글자는 3.2:1 이라 안 됨), `.pb-result`(인식 결과 칸, 늘이기 손잡이 없음), `.pb-conn`(연결 칩 — PiBrain 도구도 `/health` 로 'PiBrain 연결됨'),
  `.pb-empty` 아이콘 32px, 도구 내용 칸은 가운데 정렬 — 폭은 탭마다: 파이보 [동작] 화면 전체 · [카메라] 최대 1600px · [음성] 1180px, PiBrain 도구는 [카메라] 1600px(넓고 높은 화면은 카메라 칸 450×600)·나머지 1180px(261027v5, 넓은 화면에서 [동작] 양옆이 비어 보인다는 의견). 넓은 화면(1200px 이상)의 비전 타일은 5칸 고정
- IDE: 지우기·공장 초기화·전원 끄기 확인창은 `confirm_popup(msg, {danger, okLabel})` — 버튼에 동사, 빨강, 기본 포커스는 [취소]. WiFi 목록 선택은 `.is-selected`(옅은 파랑),
  파일을 열면 프로그램이 넓을 때 가운데 대신 왼쪽 위가 보이게(`scrollToContent`), 온도 °C, 네트워크 줄은 있는 것만, 빈 소리 재생기 숨김, 홀수 마지막 상태 칸은 한 줄 전체
- 대화: 말풍선 `word-break: keep-all`(한글 단어 중간에서 안 끊음). '말하는 중' 은 지금 말하는 대답에만 — 서버가 `/api/status` 에 `speaking`(대답 재생을 스레드 안에서 끝까지 기다려 끝난 때를 안다)
- 대기 페이지: 단계 이름은 명사(켜기 요청 · 준비 확인 · 열기), 실패한 단계는 빨간 ✕·막대 100% 빨강·안내만. `LAUNCH_VER` 261027v4
- 분류기 보관함 카드: [시험](fa-flask)·[이어서 배우기] + '⋯' 메뉴(이름 바꾸기·내려받기·지우기). 모델이 없으면 [학습하러 가기]
- 도움말: 블록 가이드는 분류를 표로(생성 스크립트 경로 문구 뺌, 제목 '블록 코딩'), 한국어 빌드의 Furo 문구 번역(`docs/source/locale/ko/LC_MESSAGES/sphinx.po`, `.mo` 는 gitignore), 검색칸 모양, 목차 강조 위치
- PiBrain 도구: 말하기·LCD 칸 기본 글은 언어를 따른다(`tts_sample`·`lcd_sample`), 버튼 기록 첫 줄에서 안내 문구 지움, 빠른 색은 지금 RGB 와 같은 것을 선택 표시

**문구(해요체·용어)** — 메시지·확인창·오류·빈 화면은 **해요체 + 마침표**(한/영 모두). 버튼·라벨은 짧게, 마침표 없음. 블록 설명(`ko.js`)·도움말 본문은 합니다체 그대로.
실패는 "~하지 못했어요." / "Could not ~.", 준비는 "○○ 준비 중…" / "Loading ○○…", 말줄임표는 늘 `…`. 조사는 붙인다([추가·수정]을, IDE에서), 숫자+단위 붙임(5초). 영문은 문장형 대소문자.

| 개념 | 한국어 | English |
|---|---|---|
| 동작 | 동작 · 내 동작 (모션 안 씀) | motion |
| 동작 표 / 줄 | 표 / 줄 | table / row |
| 저장 · 열기(파일) · 불러오기(동작·모델) | 저장 · 열기 · 불러오기 | Save · Open · Load |
| 지우기 · 비우기 | 지우기 · 비우기 | Delete · Clear |
| 실행 · 정지 · 말하기 | 실행 · 정지(상태 '멈췄어요') · 말하기 | Run · Stop · Speak |
| 처음 자세 | 처음 자세 (예전 원래자세) | Home pose |
| WiFi | WiFi, 창 이름 'WiFi 설정' | WiFi settings |
| 공장 초기화 · 전원 끄기 | 공장 초기화 · 전원 끄기 | Factory reset · Power off |
| 서비스 다시 켜기 · 다시 시도 | 다시 켜기 · 다시 시도 | Restart · Try again |
| 블록 분류 utils | 기타 (도구 앱과 겹치지 않게) | Utilities |
| 확인 버튼 | 확인 | OK |

바뀐 버튼 이름(261028): [등록하기]→[저장], [원래자세]→[처음 자세], 도구 [음성] [실행하기]→[말하기], [삭제하기]→[지우기], 대화 [멈추기]→[정지], [인터넷 설정]→[WiFi 설정], 더보기 [초기화]→[공장 초기화]·[전원]→[전원 끄기].
도움말 사용법 페이지(`notes/piboMaker.md` 한·영)와 화면 캡처·블록 가이드 그림도 새 화면으로 다시 만들었다(261027v3, 컨테이너에서 가짜 소켓으로 상태를 넣어 찍음 — 카메라 그림·인식 상자는 예전 캡처에서 오려 낸 것)

## 첫 화면(대문) · 학습지 층 (261123, 사용자 — 저연령층용, ai-lab 과 같은 '학습지' 컨셉으로 모든 화면 · 상단바도)

**대문 `/`** — 접속하면 앱을 큰 젤리 아이콘으로 고르고 **같은 탭으로** 들어간다(edge-lab 런처처럼). **앱 서버는 그대로 따로 돈다**(합치지 않는다 — 사용자). IDE 는 **`/ide`**.
- 파일: `ide/templates/home.html`(두 리포 차이는 `data-product`·마크 클래스뿐) · `ide/static/v2/home.js` · `home.css`(**두 리포 같은 파일**). 서버는 `run_ide.py` 의 `/`·`/ide`·`GET /home_info`(상태·최근 파일 4·내가 가르친 AI 3·켜진 앱 — WiFi 비밀번호는 안 보낸다)
- 앱 8개(짝수, 사용자), 줄 셋: **1 만들기**(코딩 → `/ide` · 도구 · AI 가르치기 · 대화) · **2 놀이 · 배우기**(카드 코딩 → `launch.html?svc=cards`(`cards/`, 50060) · 로봇 놀이 → `svc=play`(`play/`, 50070 — 키우기 + 파이보 조종하기 / PiBrain 픽셀 그림, 261123)) · **3 설정 · 도움말**(설정 · 도움말 :8080 — 261124 전 이름 '선생님 · 관리'. 학생도 쓰므로 선생님 말을 뺐다, 사용자)
  - 설정은 대문 안의 창: 화면 밝기 · WiFi 설정(**대문 안의 창**, 261123 — `home.js` `openWifi`, booting.py 8080 `GET /wifi_scan`·`POST /wifi` 를 IDE 예전 창과 같은 규칙으로. 연결은 두 번 누르기. 전엔 `/ide?panel=wifi` 로 IDE 의 창을 열었다) · 로봇 화면 처음으로 · **H/W 검수**(자주 안 써서 설정 안으로 — 사용자, `confirm_hwtest` 한 번 묻고 `svc=hwtest`) · 공장 초기화 · 전원 끄기(두 번 누르기, socket `restore`·`poweroff`) · 소스 코드 · 라이선스. **이것들은 이제 대문에만 있다**(IDE [더보기]·아래 상태 줄에서 뺐다, 261123)
  - **활동지 한 장(261123 개정, 사용자 — '아이콘이 AI 티가 나고 밋밋하다, 디자이너가 한 것처럼')**: 모눈 점 바탕 위에 흰 종이 — 왼쪽 철 구멍 셋 · 빨간 여백선 두 줄, 머리에 캐릭터 · '오늘의 활동지' 이름표 · 형광펜 밑줄 제목 · **켜진 시간 도장**(uptime — 기기는 오프라인이라 날짜·시계를 못 믿어서 날짜 대신, 261123 사용자. `/home_info` 의 `uptime`, 글은 IDE 상태 줄과 같은 `v2_uptime`. 예전 '이름 ___ 날짜 ___' 빈칸은 누를 수 없는데 써야 할 것처럼 보여 뺐다). [이어서 하기]의 때는 '몇 분/시간/일 전' 을 **기기 시계끼리**(`now - mtime`) 센다 — 태블릿 시계와 달라도 맞게.
    활동 1 만들기는 큰 카드 넷, 활동 2·3 은 가로 카드 둘씩(덜 쓰는 것을 작게 — 중요도 차등). 활동마다 펜 색 하나(남색 · 초록 · 갈색) + 번호 동그라미 + 점선 지시선
  - **카드 그림은 파이보 캐릭터가 그 일을 하는 장면(261123, 사용자 — '파이보가 코딩하는 것처럼, 아이콘 좀 잘 그려라')** — `ide/static/v2/pibo-art.js`(`PiboArt.svg(앱)`·`PiboArt.face(제품)`, **두 리포 같은 파일**, 그림 파일 없이 SVG 로 직접 그림 — 라이선스 걱정 없음).
    **회사 파이보 캐릭터 컨셉(261124, 사용자 — 회사 것이라 그대로 따라도 된다)**: **호빵 머리**(위는 좁고 아래가 퍼짐 — path) · 큰 동그란 검은 안경 · 검은 눈 + 반짝임 · 분홍 볼터치 · 벌린 입 + 혀 — 이목구비 크기는 머리 폭 대비 안경 알 지름 35% · 눈 약 17% · 입 폭 20%(보내 주신 그림에서 잰 비율, 사용자가 눈알만 5% 더 키움) · 파란 고리 안테나(작은 고리 둘) · 짧은 몸(가슴의 검은 명찰) · 짧은 팔 + 동그란 손 · 짧은 다리 + 동그란 발(**팔·손, 다리·발 경계선 없이** — pibo-art 는 한 path, pet.js 는 굵은 테두리로 한 번 그리고 테두리 없이 다시 칠하는 `seamless()`). 시안을 사용자에게 보여 승인받은 뒤 반영했다(그림은 먼저 승인). 그 전(261123)엔 실물 사진(네모 머리 · 하늘색 테 눈 · 어깨 판)을 따랐다. **PiBrain 보드 머리는 원래 네모라 모서리만 조금 더 둥글게**(12). 키우기 `pet.js`·PiBrain LCD PNG·상단바 제품 마크(`design/marks/pibo.svg` = 공 머리 + 고리 안테나 + 눈 둘 + 입, 키트 `--pb-mark-pibo`·도움말·H/W 검수)·탭 아이콘도 같이 바꿨다
    장면: 코딩(블록 창 빈자리에 초록 블록 끼우기) · 도구(렌치 + 공구함) · AI 가르치기(학사모 + 사과 카드, 배운 카드에 체크) · 대화(말풍선 둘, 손 흔들기) · 카드 코딩(카드 세 장 부채) · 키우기(하트 안기) · 설정(톱니 돌리기) · 도움말(책 + 물음표).
    큰 카드는 위에 그림 칸(132px), 가로 카드는 왼쪽 84px. 머리 캐릭터도 같은 그림(파이보 얼굴 · PiBrain 은 보드 — 화면 속 얼굴 · 카메라 · 버튼 넷). **PiBrain 대문 카드도 같은 파이보 캐릭터**(따로 말씀 없어 기본값).
    **PiBrain 은 PiBrain 캐릭터**(261123, 사용자) — 몸은 같고 머리가 PiBrain 보드(검은 화면 속 하늘색 얼굴 · 카메라 · 버튼 넷 · 아래 연결부). `PiboArt.svg(앱, 제품)`(제품이 없으면 `<html data-product>`).
    `pibo-art.js` 를 못 읽으면 예전 FA 기호(`APPS[].icon`)로 그린다. 그림을 고치면 어둡게에서도 볼 것
  - **상단바·대기 페이지 아이콘은 작은 Font Awesome 기호 그대로**(261123, 사용자) — 얼굴 + 색 배지 캐릭터 아이콘(`pibo-icons.js`)을 넣었다가 '상단바에 얼굴이 다 나오니 이상하다, 작은 아이콘만이 낫다' 는 의견으로 같은 날 뺐다. 다시 넣지 말 것. 캐릭터는 대문 카드 그림·머리 캐릭터·키우기 친구에만
  - **앱 색(261123, 사용자 B안 — 같은 모양 + 같은 색)** — 키트 `design/pibo-ui.css` 끝 '앱 색' 의 `--app-<앱>`/`--app-<앱>-t`(어둡게는 밝은 판). 코딩 파랑 `#2f72d6` · 도구 주홍 `#d4502a` · AI 가르치기 보라 `#7454d0` · 대화 초록 `#2a8a55` · 카드 코딩 주황 `#c96506`(`--app-kids`) · 로봇 놀이 청록 `#127f86`(`--app-play`, 261123) · 키우기 분홍 `#d4436f` · 설정 회색 `#68737f` · 도움말 황토 `#b07d08`(모두 종이 바탕 3:1 이상).
    칠하는 곳: 체험 앱의 [카드 처음](주황)·[놀이 처음](청록, `body.kids[data-app] #start_bt`) · 대기 페이지 아이콘(`launch.html`) · 대문 카드 그림 바탕(`-t`)·이름 앞 아이콘·누를 때 테두리. **글자는 검정 그대로, 활동 1·2·3 번호·지시선은 줄 색(남색·초록·갈색) 그대로**(전부 앱 색이면 너무 알록달록)
  - **작은 아이콘과 대문 그림을 잇는다(261123, 사용자)** — 대문 카드 이름 앞에 상단바·대기 페이지와 같은 작은 아이콘(`.home-app__nic`, `APPS[].icon`): 코딩 `fa-code`(앱의 [IDE] 버튼과 같게) · 도구 `fa-screwdriver-wrench` · AI 가르치기 `fa-graduation-cap` · 대화 `fa-comments` · 카드 코딩 `fa-shapes`(대기 페이지 `GO.cards` 도) · 로봇 놀이 `fa-gamepad` · 키우기 `fa-heart` · 설정 `fa-gear` · 도움말 `fa-circle-question`. 장면의 소품도 그 기호와 같은 물건(렌치·학사모·말풍선·톱니·물음표)
  - 켜진 앱은 빨간 고무 도장 '켜져 있음', 켜진 게 없으면 마지막에 쓴 앱(`localStorage pibo_home_last`)에 노란 꼬리표 '지난번'(`data-ring="run|last"`, 처음엔 아무것도 없음)
  - 오른쪽: 로봇 상태(괘선 표 — 배터리·메모리는 막대) · 이어서 하기(노란 메모지 + 마스킹 테이프)
  - [이어서 하기] 파일 → `/ide?open=<경로>`(`ide.js` 11 — init 을 놓치면 2.5초 보조 타이머)
- **모든 앱의 [처음 화면](`#home_bt[data-pb-home]`, 집 아이콘)** → 대문(261123 — 예전 [IDE] `#ide_bt` 는 지웠다). 코딩(IDE)의 [처음 화면]은 저장 안 했으면 묻는다(`ide.js` 12, `data-pb-home` 없음). 체험 앱 안의 [처음]은 헷갈리지 않게 카드 코딩 [카드 처음](도형 아이콘) · 로봇 놀이 [놀이 처음](게임패드 아이콘) — id 는 `#start_bt`(261123 전엔 `#home_bt`)
- 대기 페이지 `launch.html`: `svc=hwtest`(50050) · `svc=cards|play[&go=make|pet|drive|art]`(체험 앱의 그 화면, 이름·아이콘·색도 그 화면 것 — `svc=kids` 는 예전 이름 → play). `LAUNCH_VER` 261126v1. 체험 앱은 `?go=` 를 읽고 주소에서 지운다
- 미리보기 `design/preview.py` 와 검사 `design/audit/browser_check.js` 가 대문(`/`)·IDE(`/ide`)를 안다. `AUDIT.md` B2 예외에 대문을 넣었다
- **대문 중심 정리(261123, 사용자 — 'IDE 가 메인이었던 흔적 전수 조사')**: 앱은 대문에서만 고르고, 모든 앱의 상단바는 같은 줄이다.
  - 코딩(IDE): 상단바 앱 버튼·[더보기]의 밝기·언어·공장 초기화·전원 끄기·소스 코드·로고, WiFi 창, 아래 상태 줄을 뺐다 → 대문 [설정]·[로봇 상태]. 이름 `piBo · 코딩`(대문 카드와 같게)
  - 앱의 [IDE] → [처음 화면](`#home_bt[data-pb-home]`, 키트 `goHome`). 키트의 `openService`·`backToIDE`·`popup_blocked`·`data-title="lead"` 를 지웠다. 체험 앱 안 [처음]은 `#start_bt`
  - 분류기의 앱 이름은 대문 카드와 같은 **AI 가르치기 / Teach AI**(상단바·탭 제목·대기 페이지 — 블록·라이브러리 이름 '분류 모델' 은 그대로)
  - H/W 검수 화면 띠에 [처음 화면], 색을 학습지 층으로(밝게는 노랑 → 흰 종이, 주 동작 남색). 도움말 상단바 클래스 `.pb-topbar__home`. 대기 페이지 [닫기] → [처음 화면]
  - 대문 [로봇 상태]에 유선 IP·시리얼·충전 표시(`/home_info` 의 `serial`·`dc`), [설정]에 WiFi 창·소스 코드 · 라이선스
  - 쓰지 않게 된 문구 키 22개를 두 리포 `ko2en.js` 에서 지웠다(`v2_tip_*`·`nav_classifier`·`nav_kids`·`err_init_sysfile` 등)
  - 확인(컨테이너 미리보기): 코딩 상단바 두 제품 × 1366/1024/820 × 한/영 — 순서·제목·이름·하단바 없음·999 기준·넘침·오류 0, 대문 WiFi 창 48/48(목록·고르기·EAP·직접 입력·짧은 비밀번호 막음·두 번 누르기·실패 안내·영문). **실기기 확인 필요** — 대문 WiFi 창으로 실제 연결(AP 모드 포함), `/home_info` 의 충전(`#14`) 값

**학습지 층** — ai-lab(같은 회사, 초등 저학년용)과 한 식구로 보이게(사용자, 261123). 젤리·파스텔 '귀염 층'은 같은 날 시험했다가 이것으로 바꿨다
- **색은 키트 토큰만 바꿨다**(`design/pibo-ui.css` 끝 '학습지 층' — `:root`·`[data-theme=soft|light|dark]` 의 `--v2-*` 를 덮어씀). IDE `--c-*`·PiBrain 도구 `--c-*` 는 별칭이라 같이 바뀐다
  | | 부드럽게(기본) | 밝게 | 어둡게 |
  |---|---|---|---|
  | 바탕 · 상단바 | 미색 종이 `#fbf7ef` | 흰 종이 `#ffffff`(바탕 `#fdfcf9`) | 짙은 종이 `#1c1a16` · 상단바 `#24211c` |
  | 괘선(상단바 아래 · 굵은 줄) | 갈색 `#4a3f2e` | 〃 | `#b9ab92` |
  | 주 색(주 동작 · 강조 · 링크) | 남색 펜 `#1f5f7a`(흰 글자 7:1) | 〃 | `#7fb6cf`(어두운 글자) |
  | 빨강(정지 · 지우기 · 경고) | 빨간 펜 `#b4451c` | 〃 | `#e48a63` |
  | 글자 | `#2a2620` · 보조 `#4a423a` · 힌트 `#6b6255` | 〃 | `#efe8db` · `#d9cfbf` · `#b3a892` |
  - **어둡게의 주 동작은 이제 노랑이 아니라 옅은 남색**이다(261123 전 규칙 '어둡게는 노랑'을 바꿈)
- 모양: 판·카드는 흰 종이 + 옅은 테두리(`--v2-line #dcd5c6`) + 아주 옅은 그림자, 모서리 8/12/14, 버튼은 테두리 단추(주 동작만 남색으로 칠함), 제목(상단바 제품 이름 · 카드 제목 · IDE 서랍 머리 · 대기 페이지 제목)은 **명조 `--serif`(Gowun Batang)**
- **명조 글꼴 Gowun Batang(SIL OFL 1.1)** — `ide/static/fonts/gowun/`(ai-lab 과 같은 글자 묶음 서브셋 191개, 약 3.5MB, 화면에 나온 글자 묶음만 받는다). 키트 맨 위 `@import url("fonts/gowun/gowun.css")`. 도구·분류기·대화·로봇 놀이 서버는 `SharedFonts` 가 `static/fonts/gowun/*` 도 IDE 로 넘긴다(8곳). **도움말(8080)은 명조를 싣지 않았다**(상단바 색만 맞춤). OFL 원문은 같은 폴더 `OFL.txt`(Google Fonts 배포본)
- 상단바는 종이색 + 아래 갈색 괘선 1px(이중 괘선은 시험했다가 AUDIT B2 '아래 1px 선' 규칙대로 되돌림), 앱 이름은 명조 제품 이름 옆 **테 두른 이름표**(`.pb-header__app`, IDE `.v2-brand > span` — 대문 '오늘의 활동지' 와 같은 모양). 도구·분류기 판 바탕은 대문과 같은 모눈 점(`--pb-grid`)
- 대기 페이지도 종이 바탕(빛 번짐 장식 뺌), 도움말 상단바·H/W 검수 띠도 종이색
- 구형 브라우저 기준 그대로(:has·color-mix·backdrop-filter 안 씀). 움직임은 transform·opacity 만, 움직임 줄이기면 멈춘다
- 확인(컨테이너 미리보기): 대문 48경우(두 제품 × 한/영 × 밝기 3 × 1366/1024/820/390) 넘침·잘림·오류 0, 동작 22/22, 설정 창(H/W 검수·두 번 누르기·밝기), 전 앱 캡처(밝기 3 × 1366/1024/820). **실기기·실제 태블릿·학교 노트북 확인 필요**

## 빈 화면 안내 · 읽기 다듬기 (261120, 사용자 — UX 점검 A~F 전부)

처음 화면에서 무엇을 눌러야 할지 몰라 막히는 곳(IDE·대화·분류기)에 갈 길을 보여 준다. 파이보·PiBrain 같은 코드(ide.js·ide.css·chat.js·chat.css 는 같은 파일, 분류기·ko2en 은 같은 부분을 같이).
- **A · IDE 빈 작업판**(`#v2_start`, `ide.js` 3-1): 파일을 안 열었을 때(`#codepath` 비었을 때)만 작업판 가운데 '무엇을 만들어 볼까요?' + [새 파일](서랍 `#add_file` 과 같은 처리) · [예제 열기](블록 모드로 바꾸고 `load_directory('/home/pi/examples')` + 서랍) · [내 파일 열기](서랍).
  바탕은 `pointer-events: none` 이라 툴박스·블록 찾기·작업판은 그대로 쓴다. 블록 모드면 툴박스 폭만큼 오른쪽에(`placeStart`). 블록을 끌 때의 '파일을 고르거나…' 경고는 그대로 둔다. 문구 IDE `ko2en.js` 의 `v2_start_*`
- **B · 대화 모델 카드**(`chat.js` `renderCards`): 고르기 전 빈 화면에 `/api/models` 의 모델마다 카드(이름 · 한 줄 설명 `chat_desc_*` · 도구 모델이면 `불빛 · 보기 · 움직이기`(PiBrain `불빛 · 보기`) · 크기). 누르면 `chooseModel`. 없는 모델은 흐리게 못 누름. 위 select 는 그대로. 목록을 못 받으면 예전 한 줄
- **C · 분류기 학습 단계**(`#learn_steps`, `app.js` `renderSteps`): 오른쪽 칸 위 ① 예시 모으기(종류 칩·장수) ② AI 가르치기(정확도 / 예시가 바뀌면 다시) ③ 저장하고 시험하기. 처음으로 안 끝난 단계 하나만 파랑 테두리(now), 끝난 건 체크.
  `#train_need` 는 단계 1 이 같은 말을 해서 숨긴다. 문구 분류기 `ko2en.js` 끝 `step_*`
- **D · 도구 [동작] 표 머리**(파이보만): `M0` 아래 작게 부위 이름(`motor_s0`~`s9`, 도구 `ko2en.js` 끝)
- **E · 파일 이름**: `/home/pi/code/face.json` → `code › face.json`(`/home/pi/` 를 빼고 폴더는 흐리게, 전체 경로는 title)
- **F · 화면 출력 빈 칸**: 긴 안내(`v2_live_empty`)는 title 로, 보이는 건 한 줄 `v2_live_hint`
- 해 보고 되돌린 것(블록 글자 굵게 260930, 렌더러 261118, iframe, 색 체계)은 이번에도 손대지 않았다
- **도움말도 맞췄다(261120)**: 사용법 글(`notes/piboMaker.md` 한·영 — 처음 화면 카드·`code ›` 파일 이름·모델 카드·학습 순서·표 머리 부위 이름)과 캡처(IDE 블록·파이썬, 파이보 [동작], 분류기 학습)를 다시 만들고 빌드.
  **분류기 캡처의 그림은 직접 그린 것**(빨간 공·파란 상자, PIL) — 출처·라이선스가 확인 안 된 사진(가위바위보 예제 데이터셋 등)을 공개 문서·리포에 넣지 말 것
  IDE 화면 출력(손 모양 + 점·이름표)·도구 [카메라](책상 위 컵·공·책 + 초록 상자) 캡처도 직접 그린 그림으로 바꿨다(261120 — 예전엔 출처 모를 보도 사진·고양이 사진). 그림·캡처 스크립트는 리포 밖(작업 메모리)이라 다시 찍을 땐 같은 방식(PIL 로 그리고 가짜 소켓·가로챈 REST 로 넣기)으로
  `tools/im.jpg`(사람 얼굴이 찍힌 마커 디버그 그림, 아무도 안 씀)를 지웠다 — 히스토리에는 남는다
  도움말 하드웨어 부품 사진(`notes/images/` 의 servo·atmega328p·ssd1306 등, 웹에서 가져온 것으로 보임)은 **그대로 둔다(261120, 사용자 — 중요하지 않음).** 다시 문제 삼지 말 것
- 확인(컨테이너 미리보기): 1366·1024·820(·390 대화) × 한/영 × 부드럽게/어둡게 넘침 0 · pageerror 0, 카드 누르기(예제 → 서랍 열림, 새 파일 → 이름 묻기, 파일 열면 안내 사라짐, 모델 카드 → 그 모델 켜짐·예시 3개), 분류기 사진 올리기 → 단계 now 이동(모으기 → 가르치기 → 저장). **실기기·실제 태블릿 확인 필요**

## USB 카메라 (261120) — `Camera(cam=1…)`

- **`Camera(cam=0)`(기본)은 보드 카메라 그대로, `cam=1` 부터는 USB 카메라**(V4L2 를 지원하면 기종 상관없음 — 사용자). 예전엔 `cam` 인자를 안 썼다(API 호환: 이름·인자 그대로).
  `Camera.usb_cameras()` → `[{'cam','dev','name'}]`. 몸통은 `openpibo/modules/usbcam.py`(**두 리포 같은 파일**)
- 찾기: `/sys/class/video4linux/video*` 중 장치 경로가 `/usbN/` 아래이고 `index` 0 인 노드만 — 보드 카메라(unicam)·코덱·ISP 노드·UVC 메타데이터 노드는 빠진다. `/dev/v4l/by-id` 는 이름에 기종이 들어 있어 안 쓴다.
  번호는 USB 포트 순(장치 경로 순) — 같은 포트면 카메라를 바꿔도 번호가 같다. OpenCV V4L2, MJPG 를 먼저 청한다
- 크기: 안 주면 640x480. 카메라 비율이 다르면(16:9 등) 가운데를 잘라 맞춘 뒤 줄인다 — 기종과 상관없이 같은 크기. 회전·뒤집기 없음(보드 카메라만 기기에 맞춰 돌린다)
- 읽기 실패(뽑았다 꽂음)면 다시 찾아 한 번 연다. 오류는 `한국어 / English`. `cam` 은 정수 0~9
- **보드 카메라도 번호로 열지 않는다**: libcamera 가 USB(UVC) 카메라도 센다(PiBrain 실측: `global_camera_info()` 0 ov5647 · 1 USB 2.0 PC Cam). 그래서 `Camera(0)` 은
  `Id` 에 `usb` 가 없는 첫 카메라의 `Num` 으로 `Picamera2(n)` 을 연다(순서가 바뀌어도 보드 카메라). 없으면 `IndexError` '보드 카메라를 찾지 못했어요 / …'
- 확인(컨테이너, 가짜 sysfs·VideoCapture·Picamera2): 두 리포 17/17
- **PiBrain 실측(261120, fc1a8f31)**: 30만 화소 UVC 1.00 카메라(`USB 2.0 PC Cam`, YUYV 만 — 640x480·352x288·320x240·176x144·160x120, 모두 30fps) → `usb_cameras()` 에 `/dev/video1` 하나만(메타데이터 노드 `video2`·unicam·코덱·ISP 15개 빠짐),
  열기 1.47초, `read` (480,640,3) 중간 120ms(약 8장/초 — 30fps 인데 느린 이유는 노출 우선 설정 추정, **확인 필요**), throttled 0x0. 꽂을 때 두 번 끊겼다 붙음(접점으로 봄)
  **확인 필요** — 보드·USB 동시에 열기, MJPG 카메라, 여러 대, 파이보(서보와 같은 전원)
- **보드 카메라는 처음 `read()` 때 연다(261120)** — `Camera()` 만으로는 Picamera2 를 안 연다(`_open_board`, 잠금으로 한 번만). 그리기·보여주기 블록도 `camera = Camera()` 를 넣어서,
  USB 카메라만 쓰는 프로그램까지 보드 카메라를 열지 않게. 그래서 카메라를 못 열 때 오류가 나는 줄이 `Camera()` 에서 첫 `read()` 로 옮겨 간다.
  **서비스(도구·분류기)는 `Camera(n)` 뒤에 바로 `read()` 를 한 번 불러 열어 본다** — 예전처럼 켤 때 실패를 잡으려고. 새로 카메라를 쓰는 서비스도 그렇게 할 것.
  `release()` 뒤에 다시 `read()` 하면 다시 연다(USB 도)
- **크기**: USB 카메라도 크기를 안 주면 **그 제품의 보드 카메라와 같은 크기·방향** — 파이보 640x480, **PiBrain 480x640(세로, 가운데를 잘라 맞춤)**. PiBrain LCD·분류기가 세로를 전제로 해서다
- **블록 `vision_read_usb` [USB 카메라 (cam1 ▾) 로 사진 찍기]** (`ide/static/v2/usbcam_block.js`, **두 리포 같은 파일**) — 기존 [사진 찍기](`vision_read`)는 그대로 보드 카메라만(사용자: 다른 프로그램이 안 깨지게).
  **선택지는 cam1·cam2 두 개로 확정(사용자, 261120 — 같은 날 cam1~3 → 하나 → 둘로 바뀜)**, 보드 카메라는 없다. 값 `1`·`2` = `Camera(1|2)`(꽂은 USB 포트 순서). 만드는 코드 `camera_usb1 = Camera(1)` → `camera_usb1.read()` — 카메라마다 객체를 따로 만들어 기존 블록과 한 프로그램에 같이 쓴다.
  선택지가 없던 판으로 저장한 블록(cam 값 없음)·3 이상 값은 cam1 로 만든다. 라이브러리는 `Camera(9)` 까지 되지만 블록·화면은 둘까지
  `customblock*.js` 는 안 건드리고, 이 파일이 블록을 정의하고 전체 툴박스 [시각] 의 [사진 찍기] 바로 뒤에 끼운다(`toolbox_dict` 두 언어). 문구는 블록을 만들 때의 `lang`. 쉬움 툴박스에는 안 넣었다
- **도구·분류기 카메라 고르기** — 보드 카메라(기본) + **USB 카메라 cam1·cam2**를 `cam1 · <카메라 이름>` 으로(블록과 같은 이름·같은 개수 — 화면이 서버 목록에서 `cam <= 2` 만 남긴다). 목록은 그 칸을 누를 때·[카메라] 탭을 열 때 새로 읽는다(실행 중에 꽂은 것도).
  고르면 서버가 **새 카메라를 먼저 열어 한 장 읽어 보고** 되면 바꾸고 옛 카메라를 놓는다(읽는 중에 놓지 않게 잠금) — 안 되면 원래 카메라 그대로 + 안내(라이브러리 오류의 지금 언어 쪽만). 지금 카메라가 빠지면 `cam1 · (빠짐)`
  - 파이보 도구: socket `cam_list`·`cam_select`(`tools/lib.py` 의 `cam_list`·`cam_select`, `_cam_lock`), 칸은 [카메라] 제목 줄 [사진 저장] 앞(`#v_cam_sel`)
  - PiBrain 도구: `GET /cam_list`·`GET /cam_select?n=`(꺼져 있으면 고르기만 — 다음에 켤 때 씀), 칸은 [여기에 보기] 옆(`#cam-sel`). `/camera?d=on` 이 실패하면 `{ok:false,error}` → 화면이 버튼을 되돌리고 안내(전엔 켜진 척했다)
  - 분류기(두 리포): socket `cam_list`·`cam_select`, 칸은 [카메라 끄기] 옆(`#cam_sel`). 처음 바꿀 때 '학습할 때와 쓸 때 같은 카메라' 안내를 한 번 띄운다(모델에 카메라를 적어 두는 것은 안 했다)
- 확인(컨테이너): 라이브러리 23/23(두 리포 — 처음 read 때 열기·스레드 5개·release 뒤 다시·그리기만이면 안 엶 포함), 서버 쪽 가짜 Camera 로 파이보 도구 8 · PiBrain 도구 9 · 분류기 9·9,
  화면(가짜 socket.io·fetch) 60/60(목록·고르기·실패·빠짐·한/영·820~1366 넘침 0·pageerror 0), 블록 28/28(툴박스 위치·코드·저장/불러오기·한/영). **실기기 확인 필요** — 도구·분류기에서 실제로 바꾸기, MJPG 카메라가 YUYV 보다 느린 이유(184 vs 120ms)
- **전수조사(261120)** 로 고친 것: ① USB 에 청하는 크기는 늘 640x480(그보다 큰 크기를 달라고 할 때만 그 크기) — 전엔 PiBrain 세로 480x640 이 640x640 을 청해 카메라마다 결과가 달랐다
  ② `cam` 번호는 numpy 정수도 받는다(`numbers.Integral`, bool 은 아님) ③ 파이보 도구는 보드 카메라를 못 열어도 사물·얼굴 모델은 올리고, USB 를 고르면 그때 화면 보내기를 시작한다(전엔 보드 카메라가 없으면 USB 도 못 썼다). 켜는 중의 안내는 두 말
  ④ 분류기는 보드 카메라 오류(`camera_error`) 뒤 USB 를 고르면 카메라를 다시 켠다. 확인(컨테이너): 라이브러리 26/26 · 파이보 도구 11 · PiBrain 도구 9 · 분류기 9·9 · 화면 60/60 · 블록 28/28
- **기기 점검(261120, PiBrain fc1a8f31, USB 카메라 2대)**: 목록 `cam1=/dev/video3 'USB Camera'`(MJPG, 열기 0.65초·한 장 중간 184ms) · `cam2=/dev/video1 'USB 2.0 PC Cam'`(YUYV, 1.41초·120ms), 보드 카메라 첫 장 0.58초(그때 엶)·다음 30ms,
  release 뒤 다시 읽기·잘못된 번호·없는 번호 두 말 오류·cam1 그림으로 사물·얼굴·모니터 화면 모두 통과, throttled 0x0. 점검 스크립트가 보드 카메라를 놓지 않고 한 번 더 연 1건은 스크립트 잘못(같은 카메라는 두 번 못 연다 — 'Camera in Running state')
  고친 점검 스크립트로 다시(261120): USB 없음 9/9 · 1대 11/11 · 2대 11/11(보드 + cam1 동시에 통과, 두 그림 평균 차이 99~110). 두 번째 2대 시험에서 cam1·cam2 이름이 앞 시험과 바뀌었다 —
  번호는 포트 순이라 꽂은 포트를 바꿨으면 맞는 동작. 기기에서 포트를 옮겨 가며 봤다(`1-1.1`~`1-1.4` 네 경로 모두 나옴, 매번 경로 순서대로 번호) — 포트를 바꾸면 번호가 따라 바뀌고, 꽂아 둔 채로는(재부팅 포함) 안 바뀐다
- **번호 방식은 그대로 둔다(261120, 사용자)**: 꽂힌 카메라만 포트 순서대로 cam1·cam2. 한 대가 빠지면 남은 것이 cam1 로 당겨진다(빈 포트가 번호를 차지하는 '단자 고정' 방식은 하나만 꽂았을 때 cam2 가 되어 더 헷갈려서 안 함).
  실제 단자 위치(검정/파랑·위/아래) ↔ `1-1.1`~`1-1.4` 는 **확인 필요**. USB 3.0 카메라는 `usb2` 아래로 잡혀 USB 2.0 카메라 뒤 번호가 될 것으로 본다(**확인 필요**)

## 1차 마감 검토 (261120)

두 제품 전 화면(IDE·도구·분류기·대화·로봇 놀이 × 1366·1024·820 × 한/영)을 컨테이너 미리보기로 찍어 봤다 — 가로 넘침 0, pageerror 0, 영문 화면에 남은 한국어 0.
고친 것: 분류기 세로 태블릿 배치(쌓는 기준 819 → 899px — iPad 세로 820 에서 카메라 칸이 약 170px 였다), 도구 [동작] 키 안내를 1299px 이하에서 모두 숨김(좁은 창에서 발 그림과 겹침, 터치 기기는 원래 숨김),
IDE 화면 출력 안내·툴팁을 블록 이름(`모니터 화면에 보여주기`)에 맞춤, 마지막 수정 뒤 안 올린 `?ver`(IDE `ide.css`·`index.js`·`errhelp.js`·`ko2en.js`, `langFileVersion`) → 261120v1.
**도움말 다시 빌드함(261120)**: 두 리포 한·영, 경고 0, API 13쪽 한·영 개수 같음. 블록 가이드에 쉬움 블록(파이보 19·PiBrain 16), 사용법 글·IDE 캡처는 A안·오류 상자·[쉬움 | 전체] 로, 파이보 [동작] 캡처는 점 숫자 입력으로.
**태그 전에 남은 일**: ① 태그는 사람이(`YYMMDDvN`·`-gl` 같이) ② 실기기 확인(이 문서의 '실기기 확인 필요' 들 — 특히 카메라 재시도·실행 전 서비스 대기·오류 상자 줄 잡기·대화 도구 예시·분류기 태블릿)

**2차 전수조사(261120, 두 리포)** — 문서·주석이 코드보다 늦은 곳을 찾아 고쳤다. 기계 점검: 문법(파이썬·JS·셸) 0 오류, `?ver` 늦은 곳 0, 화면·서버가 쓰는 번역 키 빠진 것 0,
예제(국내·영문 두 판) 블록 열기·코드 만들기 오류 0, 전 화면 × 한/영 pageerror·가로 넘침 0, 도움말 빌드 경고 0·영문 API 번역 빈칸 0.
고친 것: API 설명(`Camera` — USB·처음 `read()` 때 열기·함수 목록 · `Detect` — 없는 `classify_image` 빼고 함수 목록 · 대화 모델 파일 · `transcribe` 빈 글자 · 분류 '파이보' 낱말)과 영문 `.po`,
블록 설명 3개(`ko.js`·`en.js` — 옛 블록 이름·'파이보가'), 도움말 사용법(블록 이름·PiBrain 도구 탭 위치·얼굴 구분·espeak·로봇 놀이·USB 카메라), README 폴더표(chat·kids·docs),
`setup.py`(안 쓰는 `openpibo_face_models` 빼고 라이선스), IMAGE.md(`'llama-server@*'`·모델 크기·실제 파일·**뜨기 전 청소에 로봇 놀이 기록 지우기**), KIDS.md(10차시·저장 한 벌·IDE 버튼),
`design/README.md`(두 리포 같은 파일로), 매뉴얼 생성 스크립트(공유기 제품명 → 일반 명사, 포트 50030·50050·50060, 영문 도움말 있음), 손동작 모델 라이선스 줄(**확인 필요**),
대화 화면 `#model_file` 이 `.model/VERSION` 에서 판 이름을 읽게(261106 실제 파일 뒤로 `themaker-ko` 만 보였다), `gen_block_guide.py` 가 그림을 **다 그린 뒤에만** 옛 그림을 지우게(전엔 IDE 주소가 틀리면 그림이 다 지워진 채 멈췄다), `ide.css` 머리 주석(A안 배치·파랑).
**사용자 결정(261120)**: 매뉴얼 PDF 4개는 리포에서 뺐다(`manual/.gitignore` 에 `*.pdf` — 납품 때마다 태그로 빌드). 안 쓰던 백업 파일(`test/*.bak`, PiBrain `*.bak` 2개)을 지웠다 — PiBrain `test/test` 는 H/W 검수를 손으로 띄우는 스크립트라 남김.
도구·분류기의 `webfonts/` 사본(파이보 도구는 v1 fontello 포함)과 그 마운트를 지웠다 — 260929 부터 `SharedFonts` 가 fa-* 를 IDE 로 넘겨 한 번도 안 쓰였다(컨테이너: 4개 서버 모두 301 → IDE, 첫 화면 200). 아이콘 글꼴은 이제 `ide/webfonts/` 한 벌뿐.
`ide/examples/`(코드가 안 쓰던 옛 사본, 2개는 지운 블록이라 안 열림)를 지웠다 — **예제 원본은 리포 맨 위 `examples/`**(사용자 확인, 공장 초기화가 `/home/pi/examples/` 로 복사).
`rps_recognizer.task` 는 사용자가 MediaPipe Model Maker 예제 데이터(`rps_data_sample.zip`, Google 저장소)로 학습한 것 — 사진은 MediaPipe 팀이 직접 찍은 것이고(노트북 원문 'We already captured a few hundred images') Apache-2.0 튜토리얼 노트북(google-ai-edge/mediapipe-samples `tutorials/gesture_recognizer/WiMLS_2022_…ipynb`, Copyright 2022 The MediaPipe Authors)과 함께 배포됐다. 데이터셋만 따로 적힌 라이선스는 없다(zip 에도 없음, 261124 확인). 모델에는 학습한 가중치만 있고 사진은 없다 — 다시 거론하지 말 것(261124, 사용자)

## 코스웨어 다듬기 (261126, 사용자 — '교육 솔루션처럼 보이게', 회원가입 없이)

**하지 않기로 한 것(사용자)**: '오늘의 수업'(수업은 매번 다르다), 제품 안 수업 가이드(수업 가이드는 따로 낸다). 다시 꺼내지 말 것.
두 제품 같은 코드(아래 파일은 두 리포 같은 파일 — 고치면 같이).

- **예제 갤러리** — 코딩 [예제 열기](빈 작업판 카드 · [⋯] 메뉴)가 파일 목록 대신 카드: 제목 · 한 줄 · 배우는 것 · 난이도 ★1~3 · 시간 · 필요한 것(카메라·스피커·넓은 바닥…).
  누르면 고친 게 있으면 저장할지 묻고 블록으로 연다. [폴더에서 보기]는 예전처럼 서랍에. 코드 `ide/static/v2/examples.js`(카드 표 `EX` · 문구 ko/en 안에 — 영문판 델타 안 늘림),
  서버 `GET /examples_list`(`/home/pi/examples` 의 .json·.py — **기기에 있는 것만** 보인다. 표에 없는 파일은 파일 이름 카드). **예제를 더하거나 바꾸면 `EX` 도 고칠 것**
- **[사용법]**(`?`) — 모든 앱 상단바 [처음 화면] 바로 왼쪽(코딩·도구·AI 가르치기·대화·카드 코딩·로봇 놀이. 대문·도움말·대기 페이지는 없음 — `AUDIT.md` B2).
  `<body data-pb-help="code|tools|classifier|llm|cards|play">` 이면 키트 `addHelpButton` 이 끼운다. 누르면 '이 화면에서 할 수 있는 것' 3~4줄 + 도움말 `notes/piboMaker.html#app-ide|app-tools|app-classifier|app-chat`(MyST 이름표 `(app-…)=` — 지우지 말 것).
  문구는 키트 `HELP` 한 곳(piBrain 은 `kob`/`enb`). **화면의 버튼 이름을 바꾸면 여기 문구도**
- **대문 [설정] → 로봇 정보** — 제품 · 버전(`.OS_VERSION`) · 올린 때(그 파일 시각 — 업데이트할 때는 인터넷에 붙어 있어 시계가 맞다고 본다) · 소스 날짜(받은 커밋, `git -c safe.directory=*`) · 시리얼 · 운영체제 · 저장 공간(막대) · 모델 판(`.model/VERSION` 의 `## sha256` 위 `이름 = 판` 줄). [복사](http 라 clipboard API 가 없으면 textarea). 서버 `GET /robot_info`. **기기 VERSION 줄 모양은 확인 필요**
- **대문 꼬리말** — 제품 · 버전 · © Circulus · 도움말 · 라이선스(Apache-2.0, 소스 링크)
- **대기 페이지 팁** — 기다리는 동안 앱마다 한 줄 팁(6초마다 바뀜, 실패하면 숨김). `launch.html` 의 `TIPS`. `LAUNCH_VER` 261126v1
- **체험 앱 처음 화면 머리말·요약** — 제목 · 한 줄 설명 + 요약 칸: 카드 코딩 = 오늘 차시 · 모은 별(지금 차시까지) · 내 재주 n/24, 로봇 놀이 = 내 친구(이름 · 지금 기분) · 파이보 할 수 있는 동작 / piBrain 그림첩 n/30. 머리말과 카드를 한 덩어리로 가운데에(900px 이하는 위부터)
- **대화** — 모델 카드로 고르는 동안 위 [대화 모델] 칸(`#model_bar`)을 숨긴다. 고른 뒤에 나타나 거기서 바꾼다(목록을 못 받았으면 늘 보임)
- 확인(컨테이너 미리보기, 두 제품 × 한/영): 갤러리·로봇 정보·꼬리말 3폭 전부, 대기 페이지 팁 6앱, 체험 앱 머리말 4폭, [사용법] 6앱 × 3폭(위치·넘침·링크·Esc), 대화 모델 칸. **실기기 확인 필요** — `/robot_info` 의 VERSION 줄·소스 날짜, 예제 폴더 내용

## 오류 쉬운 말 (261119) — 실행 출력 위 빨간 상자

블록·파이썬 실행이 오류로 끝나면 출력 칸 위에 **'어디서 · 무슨 뜻'** 을 한 줄로 보여 준다(사용자 요청). '어떻게 고칠지' 힌트는 다 맞게 쓸 수 없어 뺐다(사용자, 261119). 코드는 `ide/static/v2/errhelp.js` 한 파일
(**파이보·PiBrain 같은 파일**), 상자는 템플릿 `#v2_errbox`, 모양은 `v2/ide.css` 끝 '오류 쉬운 말'.

- **규칙 표로 요약한다 — LLM 은 쓰지 않는다**(사용자 확인). 코드를 실행하면 IDE 가 llama-server 를 끄고, 작은 모델은 틀린 설명을 할 수 있다.
  `ERR_RULES` 는 (오류 이름 정규식, 메시지 정규식, ko, en[, 오류 전문 정규식]). 위에서부터 처음 맞는 것. 우리 라이브러리 오류(카메라 사용 중, `"img" must be image data`,
  모델 파일 없음, 손동작 모델 먼저 등)가 맨 앞이다. 없으면 오류 이름 풀이(`TYPE_NAMES`) + 원래 메시지. 수업에서 자주 나는 오류를 보며 줄을 늘릴 것.
  한국어 문구는 조사가 붙지 않게 쓴다(`모르는 이름이에요: '$1'` — `$1` 뒤에 은/는을 붙이면 받침에 따라 틀린다)
- **줄 번호**: 오류 전문의 `File "...", line N` 중 **실행한 파일**(블록 `/home/pi/.tmp.py`, 파이썬은 열린 파일)을 가리키는 마지막 것 = 학생이 쓴 곳.
  라이브러리 안에서 나도 학생이 부른 줄이 잡힌다. 문법 오류는 Traceback 없이 `File` 줄부터 나와도 읽는다. 실행 파일 줄이 없으면 줄 없이 문구만
- **블록 모드는 줄 → 블록**: 실행할 때 `Blockly.Python.STATEMENT_PREFIX` 로 블록 id 표시(`#@@pibo'id'`)를 끼운 코드를 한 번 더 만들어 표를 만든다.
  **실행하는 코드는 예전 `workspaceToCode` 결과 그대로**이고, 표시를 지운(빈 몸통은 `pass` 로) 코드가 그것과 글자까지 같을 때만 표를 쓴다 — 다르면 블록 표시 없이 문구만.
  오류 블록은 **빨간 테두리만**(`.pibo-errblock`) + 화면 가운데로. 느낌표(경고 말풍선)는 쓰지 않는다(사용자, 261119 — Blockly 10.0 은 이름 붙인 경고를 지워도 느낌표가 남기도 했다).
  블록을 고치면(바꾸기·옮기기·끼우기·지우기) 테두리를 바로 지우고, 다음 실행·닫기·지우개에서도 지운다. [블록 보기]는 그 블록으로 옮기면서 테두리를 다시 단다. 파이썬 모드는 그 줄을 빨갛게(`cm-pibo-errline`, 고치기 시작하면 지움).
  블록 모드인데 블록이 없는 줄(블록이 맨 앞에 넣는 `camera = Camera()` 같은 준비 코드)은 '프로그램 준비 단계(그 코드)' 로 보인다.
  상자에는 원래 오류 전문을 넣지 않는다 — 아래 출력에 그대로 있어 겹친다(사용자)
- **라이브러리 오류 메시지 전수 조사(261119, 사용자)**: `openpibo/` 의 `raise` 약 190개(가져온 코드 teachlab·mtts·oled vendor 제외)를 두 리포에서 봤다. 빈 메시지는 없었다. 고친 것:
  ① 검사와 메시지가 어긋남 — `Motion.set_motor`·`set_speed`·`set_acceleration` 의 모터 번호가 `abs(n) > 9` 라 -9~-1 도 통과해 없는 번호가 서보로 갔다 → `0~9`(메시지대로), 속도·가속도도 `0~255`.
  `Camera.circle` 이 `len(r) must be Integer` → `"r" must be integer type`, `rotate` 메시지 `-360~360` → 실제 검사대로 `-359~359`, `set_motion_raw` 따옴표 빠짐
  ② PiBrain 에서도 '파이보에서 쓸 수 없습니다'(분류 모델 종류) → '이 로봇에서'(두 리포 같은 문장)
  ③ 한국어로만 된 메시지(영문판 학생이 못 읽음)는 **`한국어 / English` 두 말**로 — usb_uart·utils·draw_bitmap·대화 모델(`set_llm_model`·`call_llm`)·분류(`vision_classify`)·사물 인식(`ed_onnx`). 영어 쪽은 대문자로 시작
  ④ 어색한 영어 — `is Number(0~100)` → `must be 0~100`, `is not bool` → `must be True or False`, `not support` → `is not supported`
  오류 상자(`errhelp.js`)는 영문 검사 메시지 모양(`"x" must be 0~9`·`must be integer type`·`is not supported`·`len(...) must be N` 등)을 쉬운 말로 바꾸고,
  `한국어 / English` 메시지는 이미 쉬운 말이라 지금 언어 쪽만 그대로 보인다. **새 오류 메시지를 쓸 때는 이 두 모양 중 하나로 쓸 것**(`"값" must be …` 또는 `한국어 / English`)
- 출력의 터미널 색 코드(libcamera 로그의 `ESC[1;31m` 등)는 `index.js` 가 붙이기 전에 지운다(글자 칸이라 `←[1;31m` 으로 보였다)
- **카메라 실패 줄이기(261119, 기기에서 `Failed to start camera: Input/output error`)**: ① `run_ide.py` 의 코드 실행(`execute`·`executeb`)이 도구·분류기·대화 모델을
  `stop_units_wait()`(`systemctl stop` 을 기다림, 20초 한도)로 **다 내려간 뒤에** 학생 프로그램을 띄운다 — 전엔 Popen 으로 끄라고만 하고 바로 띄워 아직 카메라를 쥔 서비스와 겹칠 수 있었다.
  ② `openpibo.vision_camera.Camera()` 가 시작에 실패(RuntimeError)하면 1초씩 쉬며 세 번까지 다시 연다(카메라가 아예 없으면 IndexError 로 바로 오류). 가짜 Picamera2 로 확인, **실기기 확인 필요**
- 고리는 `index.js` 세 곳뿐: 블록 실행(`PiboErr.prepare('block', …)` 이 실행 코드를 돌려줌), 파이썬 실행(`prepare('python', 경로)`), 실행이 오류로 끝날 때(`PiboErr.show(result.value)`, 예전 오류 감지 자리).
  서버·로그 프로토콜(`record`·`record_add`)은 그대로다. 언어를 바꾸면 상자·말풍선을 다시 그린다. 문구는 이 파일 안 ko/en(`levels.js` 와 같은 방식)
- 확인(컨테이너 미리보기, 두 제품): 해석·블록 표·상자·말풍선·영문·파이썬 빨간 줄·닫기 17/17씩, 예제 전부(파이보 11·PiBrain 10) 코드 같음·표 생김,
  문장 블록 전부(89·78개, 빈 C블록 포함)와 함수(빈 몸통·몸통 안 오류) 코드 같음, 실제 python3.11·3.12 오류 14종 × 2 줄·문구 맞음, 기존 화면 시험 그대로, pageerror 0.
  **실기기 확인 필요**(실제 실행 출력 — 라이브러리 경고가 섞인 로그에서 줄을 바로 잡는지)

## IDE 서버·블록 메모 (260924)

- **IDE 가 띄우는 프로세스는 `bg(cmd)` 로**(261125, 사용자 — 기기 `ps` 에 `[python3] <defunct>`): `subprocess.Popen` 만 하면 끝난 프로세스(IP 화면을 그리고 끝난 `network_disp.py`·`systemctl`·`pkill`)가 IDE 가 다시 물을 때까지 좀비로 남았다. `bg()` 는 띄우고 스레드가 `wait()` 로 거둔다. 새로 띄울 때도 `bg()` 를 쓸 것(학생 프로그램은 asyncio 가 거둔다)
- **첫 화면은 `FileResponse` 로 템플릿 파일을 그대로 보낸다** (`ide/run_ide.py` 의 `/`, `tools/run_tools.py` 의 `/`).
  템플릿에 Jinja 문법이 없어서다. 전에 쓰던 `TemplateResponse(이름, {"request": ...})` 는 starlette 1.0 부터
  받지 않아 첫 화면이 500 이 된다(컨테이너 starlette 1.7 에서 확인). 템플릿에 Jinja 를 쓰게 되면
  `TemplateResponse(request, 이름)` 새 순서로 쓸 것
  - **도움말(8080, `system/booting.py` 의 `/`)도 261120 에 `FileResponse(docs/index.html)` 로 바꿨다** — 그때까지 옛 순서라 starlette 1.0 이상이면 [도움말] 첫 화면이 500 이다(전수 조사 S10 이 찾음). 두 기기(파이보 cd488e95 · PiBrain fc1a8f31) 모두 starlette 0.41.2 라 예전 코드도 돌았고, `261120v1` 로 올린 뒤 `curl localhost:8080/` 200 확인(261120). 패키지를 올리거나 새 이미지에서 1.0 이 되면 터질 것을 미리 막은 것
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

## 전체 검토 수정 (261027v3)

261027 전체 검토(B·C·P 목록)에서 나온 것을 고쳤다. 컨테이너 가짜 장치로만 시험했다 — **실기기 확인 필요**.

- **WiFi 저장(`booting.py` `POST /wifi`)**: SSID 1~32바이트, WPA-PSK 비밀번호 8~63바이트(16진수 64자)를 conwifi.sh 전에 검사한다(conwifi.sh 가 쓰던 연결을 먼저 지우므로).
  실패는 `{'result':'fail','reason':wifi_err_ssid|wifi_err_psk|wifi_err_connect}` — 대문 WiFi 창(261123 전엔 IDE 창)이 `reason` 으로 안내하고 창을 닫지 않는다.
  conwifi.sh 가 실패로 끝나도 **연결 정보가 저장됐으면 예전처럼 재부팅**한다(`wifi_saved` — 지금 없는 공유기를 미리 넣을 때는 `connection up` 만 실패한다). 저장도 안 됐을 때만 재부팅하지 않는다
- **말하기 블록(지금 `speech_tts_play`)은 말을 다 하고 다음 블록으로 간다**(`background=False`). 전엔 둘을 이어 쓰면 같은 `/home/pi/tmp.mp3` 를 덮어써 겹치거나 잘렸다
- **`Audio.play(background=True)` 는 `play` 를 따로 띄운다**(`Popen`, 셸 안 씀). 스레드 안에서 부르면 바로 끝나는 프로그램은 `play` 가 시작되기 전에 파이썬이 끝나 소리가 안 났다. 소리는 프로그램이 끝나도 계속 나고 [정지] 때 꺼진다
- **파이썬 변수 이름**: `Blockly.Python.nameDB_.safeName` 을 바꿔 끼운다(`index.js`) — 영문·숫자·`_`·한글 음절(가-힣)은 그대로, 나머지는 `_`. 전엔 `_XX` 를 모두 되살려서 `pos_10`·`pos_11` 이 둘 다 `pos_` 가 됐다. 겹치는 이름은 Blockly 가 숫자를 붙인다
- 실행 출력은 서버·화면 모두 마지막 약 200KB 만 둔다(`record_*`, 400KB 넘으면 자름). 폴더 내려받기는 요청마다 따로 압축(스레드)
- 라이브러리: 셸 문자열 대신 인자 목록(`Audio.play`·`record`, `Motion` 의 servo, espeak `--`), `Speech.start_llm` 은 `/health` 가 200 일 때까지 최대 120초 기다리고 `call_llm(timeout=120)`,
  `SpeechOnDevice.tts('')` 는 0.1초 무음 파일, MCU 응답이 비면 센서 함수가 `''`, `config.json` 은 바뀔 때만 원자적으로 쓴다(`exec` 안 씀), `Camera(width, height)` 가 실제로 크기를 바꾼다
- 분류기: 카메라를 못 켜면 상태를 켜짐으로 남기지 않고 `camera_error` → 안내(`cam_fail`), 끌 때 읽던 프레임이 끝난 뒤 놓는다, [꾹 눌러 모으기] 중 끊기면 빠른 전송을 푼다
- 도구: 소켓 입력을 숫자로 바꾸고 범위를 자른다(`to_num` — 모터 ±80, 999 는 '그대로', 녹음 1~30초 등), `/import_motion` 은 메모리에서 검사해 틀리면 400 `motion_file_invalid`,
  녹음은 `to_thread`(전엔 도구 서버 전체가 멈춤), 마커 디버그 그림(`im.jpg`) 쓰기 제거
- netwatch: 스캔 실패(nmcli 끝 코드 ≠ 0·시간 초과)는 '모름' 으로 보고 90초 규칙을 따른다(전엔 '안 보임' 으로 바로 AP). SSID 의 `:`·`\` 를 같게 풀고, 숨김 SSID 도 90초. WiFi 저장이 실패하면 `nw.wifi_failed()` 로 AP 를 다시 켠다
- H/W 검수 센서 스트림: 시리얼을 `to_thread` 로, 창을 닫아도 `PIR off` 를 보낸다


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
- **블록 문구 다듬기(261113, 사용자 변경표)**: 이미지·변수 칸을 문장 앞으로(`%3 이미지에서 얼굴 찾기`), 조사 붙이기, IDE→모니터 화면, 화면 보여주기→**로봇 화면**(두 제품 같은 파일이라 '파이보 화면' 안 씀),
  raw→원본 값, 분류기→분류 모델, 분석하기→알아보기, 눈 블록은 **앞 3칸이 오른쪽 눈**(사용자 확인 — 입력 이름 `left`/`right` 는 예전 프로그램 때문에 그대로). `en.js` 도 바뀐 낱말·칸 순서만 맞췄다.
  **Blockly 기본 블록을 다시 정의해야 하는 줄(만약 (이)라면·조건 반복·대/소문자·공백·입력받기·나누기·목록 찾기/가져오기/바꾸기/잘라내기)은 하지 않는다(사용자).** `i`→변수, 'n 번째' 정리도 그대로 둔다

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
- **학생 프로그램은 자기 프로세스 묶음으로 띄운다(`start_new_session`, 261027).** [정지]·다시 실행은 `kill_run()` 이 묶음 전체를 끈다(`os.killpg`).
  전엔 본체만 껐고, 출력이 끝날 때(EOF)까지 기다려서 배경 소리(`Audio.play` 기본 배경)·`os.system('… &')` 같은 하위 프로세스가 출력 통로를 쥐고 있으면
  프로그램이 끝나도 '실행 중' 으로 남고 다음 실행이 그 하위 프로세스가 끝날 때까지 막혔다(재현: 0.2초에 끝난 프로그램이 8초 뒤 [exit]).
  지금은 본체가 끝나면 `EXIT_DRAIN_SEC`(0.3초) 동안 더 나온 출력만 받고 끝낸다(약 0.8초 안에 [exit]). 배경 소리는 프로그램이 끝나도 계속 나고, [정지]·다시 실행 때 같이 꺼진다

대문 `/home_info` 의 `system.sh`·`requests` 는 `run_blocking()` 으로
스레드에서 돈다(261123 전엔 10초 주기 `periodic_system_update` 도 — IDE 아래 상태 줄과 같이 뺐다). 코루틴 안에서 직접 부르면 그동안 IDE 전체(실행 출력·저장)가 멈춘다.
`/device/#14:!`(어댑터) 는 `mcu_control.py` 가 `#15` 와 같이 10초마다 캐시한다.

---

## Claude Code 웹 세션 제약

- `refs/tags/*` push가 403으로 막힌다. **태그는 사람이 직접 만들어야 한다**
  (로컬 CLI 또는 GitHub 웹 Releases). 태그 삭제도 같다
- **원격 브랜치 삭제**(`git push origin --delete …`)도 403 이다. 새 브랜치 push 는 된다
- 사내망 라우팅이 없어 기기 SSH 검증은 못 한다
