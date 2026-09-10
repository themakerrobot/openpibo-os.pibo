# openpibo-os.pibo

Pibo 로봇 OS. Raspberry Pi(`pi` 유저, `/home/pi/openpibo-os`)에서 서비스가 작업본을 직접 실행한다.

주요 디렉토리: `ide/`(Blockly IDE, FastAPI + socket.io), `tools/`(모션·음성 도구),
`classifier/`(이미지 분류기), `system/`(부팅·핫스팟 스크립트).

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

`ph`가 `main`과 다른 부분은 **아래 17개 파일뿐**이다. merge 후 반드시 유지되어야 한다.

| 파일 | 내용 |
|---|---|
| `ide/static/ko2en.js`<br>`tools/static/ko2en.js`<br>`classifier/static/ko2en.js` | 1·2행이<br>`const blang = 'en';`<br>`let lang = localStorage.getItem("language") \|\| blang;` |
| `system/ph_setup.sh` | 신규 파일, 100755. timezone Asia/Manila, wifi country PH, hotspot.sh chmod |
| `examples/*.json` (10개) | 텍스트 리터럴·변수명 영문. `speech_tts.json` 은 `speech_tts_play` 제거 + translate/gtts 대상 `es` |
| `examples/collect.json` | **PH에는 없다.** `Weather.region_list` 가 한국 기상청 지역코드, `News` 가 JTBC RSS라 필리핀에선 동작 불가 |
| `ide/static/customblock_toolbox.js` | **Collect 카테고리 통째로**(wikipedia/weather/news) + **대화 블록 3개**(`speech_get_dialog` `speech_load_dialog` `speech_reset_dialog`) 미노출. 블록 정의(`customblock.js`)와 코드생성기(`customblock_callback.js`)는 `main` 과 동일 |
| `PH_DELTA.md` | **PH 전용 문서.** main 으로 가져오지 않는다 |

검증: `git diff --name-status <국내태그> <PH태그>` 결과가 위 17개 항목이고 **모드 차이 0줄**이어야 한다.

`ide/templates/index.html` 은 일부러 델타에 넣지 않았다. `?ver` 를 올릴 때마다 바뀌는 파일이라
델타로 두면 릴리스마다 충돌한다. PH 전용 파일의 `?ver` 도 `main` 에서 올린다.

### 예제 주의사항

- `examples/` 는 `restore`(공장초기화) 때만 `/home/pi/examples/` 로 복사된다
  (`ide/run_ide.py:369`). 리포만 고쳐서는 기존 기기에 반영되지 않는다 — 수동 복사하거나
  이미지를 다시 만들 것
- **TTS 블록의 언어 제약**: `speech_tts_play`(voice: main/boy/girl/…)와 `speech_otts_play` 는
  `lang` 인자를 넘기지 않는다. 전자는 `speech.py` 의 기본값 `lang="ko"` 로 떨어지므로
  영어 문장을 넣으면 한국어 발음으로 읽는다. 후자는 온디바이스 모델이라 기본값이
  `lang="na"`(자동)여서 영어도 처리된다. `lang` 을 받는 건 `speech_gtts_play`(네트워크 필요)와
  `speech_translate` 뿐. → PH 예제에서 `speech_tts_play` 는 쓰지 않는다
- `speech_translate` 지원 언어: `ko en es fr de zh-CN ja ru ar hi la ms`. **Tagalog(`tl`) 없음**
- 텍스트 블록 기본값 `가나다` 는 `customblock.js`(수정 금지 파일)에 있다. 예제 안의 값을 바꿔도
  새로 끌어다 놓는 블록은 계속 `가나다` 로 뜬다

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
ls -l system/hotspot.sh system/ph_setup.sh system/booting.py

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
ls -l system/hotspot.sh system/ph_setup.sh system/booting.py   # 전부 -rwxr-xr-x
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

남은 문제: **탭 두 개 중 하나만 닫아도 서비스가 죽는다.** 접속 수를 아는 건 tools/classifier
자신뿐이므로, 종료 판단을 그쪽으로 옮겨야 한다. IDE 셸(네비게이터) 작업과 함께 다룰 것.

참고: `@app.sio.on('connect')` / `('disconnect')` 는 `fastapi_socketio` 에서 정상 동작한다(검증함).
`ide/run_ide.py` 의 `@app.sio.on('connection')` 은 Node.js 이벤트 이름이라 **한 번도 안 불린다.**

---

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
3. **실행비트가 필요한 파일** — `system/booting.py`, `system/hotspot.sh`, `system/ph_setup.sh`,
   `tools/static/index.js`. 전부 **100755**여야 한다

---

## 커밋 전 검증

```bash
python3 -m py_compile ide/run_ide.py
node --check ide/static/index.js ide/static/ko2en.js
node --check tools/static/index.js tools/static/ko2en.js classifier/static/ko2en.js
git diff --cached --summary          # 의도치 않은 mode change 없는지
git ls-tree -r HEAD system | grep -E "hotspot|booting|ph_setup"   # 100755 확인
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

`record`(실행 로그)는 `result.value = data["record"]` 로 터미널에 **그대로** 찍힌다.
여기에 넣는 문자열은 양쪽 배포판에 같은 모습으로 보이므로 언어중립으로 쓸 것 (예: `[exit]`).

---

## Claude Code 웹 세션 제약

- `refs/tags/*` push가 403으로 막힌다. **태그는 사람이 직접 만들어야 한다**
  (로컬 CLI 또는 GitHub 웹 Releases). 브랜치 push는 정상
- 사내망 라우팅이 없어 기기 SSH 검증은 못 한다
