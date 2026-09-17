# 납품 매뉴얼

필리핀·말레이시아 납품용 인쇄 매뉴얼 2종. 내용은 **리포에서 직접 뽑으므로**
블록이 바뀌면 다시 빌드만 하면 된다. 손으로 옮겨 적은 블록 목록은 없다.

| 파일 | 대상 | 분량 |
|---|---|---|
| `Pibo_Teachers_Guide.pdf` | 교사 | A4 28쪽 |
| `Pibo_Setup_Administration.pdf` | 설치·관리자 | A4 13쪽 |

## 빌드

```bash
./build.sh                 # origin/ph 기준
./build.sh 260915v1-ph     # 특정 태그 기준
```

필요한 것: `node`, `python3`, `playwright`(+Chromium). Chromium 경로는
`CHROME` 환경변수로 덮어쓸 수 있다.

```bash
pip install playwright && playwright install chromium
```

## 리포에서 뽑는 것

`build.sh` 가 지정한 ref 에서 소스를 꺼내 `extract.cjs` 로 다음을 만든다.

| 뽑는 것 | 출처 |
|---|---|
| 블록 라벨·툴팁 102개 | `ide/static/en.js` |
| 카테고리 17개와 블록 배치 | `ide/static/customblock_toolbox.js` |
| 기본 모션 이름 82개 | `ide/static/customblock.js` 의 `motion_set_motion_dropdown` |
| 카테고리 표시명 | `ide/static/ko2en.js` |

**툴박스는 평가해서 읽는다.** `customblock_toolbox.js` 는 `toolbox(lang)` 함수라
`translations` / `color_type` / `lang` 만 채워 넣으면 그대로 실행된다. 정규식으로
긁지 않는 이유다 — 블록 순서가 바뀌어도 따라간다.

## 손으로 쓴 부분

블록 목록 밖의 서술(예제 10개 해설, 설치 절차, 문제해결)은 `gen_teacher.py`,
`gen_setup.py` 안에 파이썬 리터럴로 들어 있다. 고칠 일이 있으면 그 파일을 고친다.

`img/` 의 사진은 기기에서 찍어 넣은 것이다. 캡션 → 파일 매핑은
`gen_teacher.py` 의 `IMG` 사전에 있다.

가슴 OLED 화면과 WiFi 설정 팝업은 사진이 아니라 **HTML/CSS 로 그린다**
(`oled()`, `wifi_dialog()`). 작아서 찍으면 읽기 어렵다.

## 소스 문구와 다른 곳

`en.js` 의 오타 몇 개는 인쇄물에 고쳐 실었다. `gen_teacher.py` 의 `TYPO` 사전을
볼 것. 260917 에 en.js 원본도 고쳤으므로 그 이후 태그로 빌드하면 사전이 비어도
결과가 같다.

## 안 되어 있는 것

- 한글판. 국내 배포판(`main`)은 블록 이름이 한글이고 Collect 카테고리와 예제가
  하나 더 있어서, 번역이 아니라 `main` 기준으로 다시 뽑아야 한다
- 기기 안 문서(`docs/`, Guide 버튼, 포트 8080)는 아직 한국어다. 매뉴얼이 그걸
  대신하고 있다
