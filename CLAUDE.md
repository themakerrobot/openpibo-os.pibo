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
- **기존 태그는 이동·삭제하지 않는다.** 새 릴리스는 항상 새 태그
- 기기가 `git reset --hard <태그>`로 배포본을 받으므로, 태그는 반드시 원격에 push되어 있어야 한다

---

## PH 델타

`ph`가 `main`과 다른 부분은 **아래 4개 파일뿐**이다. merge 후 반드시 유지되어야 한다.

| 파일 | 내용 |
|---|---|
| `ide/static/ko2en.js`<br>`tools/static/ko2en.js`<br>`classifier/static/ko2en.js` | 1·2행이<br>`const blang = 'en';`<br>`let lang = localStorage.getItem("language") \|\| blang;` |
| `system/ph_setup.sh` | 신규 파일, 100755. timezone Asia/Manila, wifi country PH, hotspot.sh chmod |

검증: `git diff --stat <국내태그> <PH태그>` 결과가 위 4개 파일뿐이고 **모드 차이 0줄**이어야 한다.

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

```bash
ssh pi@<IP> 'cd /home/pi/openpibo-os && git fetch origin --tags \
  && git reset --hard YYMMDDv1-ph \
  && head -n1 ide/static/ko2en.js \
  && echo piBo_YYMMDDv1-ph > /home/pi/.OS_VERSION \
  && sudo systemctl restart ide.service && sleep 3 \
  && systemctl is-active ide.service booting.service'
```

기기를 `git checkout main` 상태로 두지 말 것 — 서비스가 작업본을 직접 실행한다.

기기 작업본 구조:

- `/home/pi/openpibo-os` 는 심볼릭 링크(root 소유) → `/home/pi/.openpibo-os.pibo` (실제 클론, pi 소유)
- systemd 유닛(`ide.service`, `booting.service`)은 링크 경로를 쓴다. 링크는 건드리지 말 것
- 클론이 **shallow(`grafted`)** 라서 `git fetch origin --tags` 로는 새 태그를 못 받는다.
  태그를 콕 집어 받을 것: `git fetch --depth=1 origin tag <태그>`
- 재클론이 더 깨끗하면 `git clone --depth 1 --branch <태그> <url>` 후
  `sudo chown -R pi:pi` 하고 링크 대상 자리에 넣는다

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
