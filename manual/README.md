# 납품 매뉴얼

인쇄용 매뉴얼 4종 (영문 2 + 한글 2). 내용은 **리포에서 직접 뽑으므로** 블록이 바뀌면
다시 빌드만 하면 된다. 손으로 옮겨 적은 블록 목록은 없다.

| 파일 | 대상 | 기준 브랜치 | 분량 |
|---|---|---|---|
| `Pibo_Teachers_Guide.pdf` | 교사 (PH·MY) | `ph` | A4 28쪽 |
| `Pibo_Setup_Administration.pdf` | 설치·관리자 (PH·MY) | `ph` | A4 13쪽 |
| `Pibo_교사용_가이드.pdf` | 교사 (국내) | `main` | A4 28쪽 |
| `Pibo_설치_관리_가이드.pdf` | 설치·관리자 (국내) | `main` | A4 14쪽 |

**한글판은 영문판의 번역이 아니다.** `main` 에서 따로 뽑는다. 블록 이름이 `ko.js` 에 있고,
`main` 에만 **수집** 카테고리(블록 4개)와 `collect.json` 예제가 있어서 블록 106개·예제 11개로
영문판(102개·10개)과 수가 다르다. 공유기 안내도 다르다 — KR 규제도메인은 149~165 가 열려
있어 채널을 36~48 로 묶을 필요가 없다(`CLAUDE.md` 의 '현장 네트워크' 참고).

## 빌드

```bash
./build.sh                                  # 영문 origin/ph + 한글 origin/main
./build.sh 260915v1-ph --ko-ref=260915v1    # 태그 기준
./build.sh --ko-only                        # 한쪽만
```

필요한 것: `node`, `python3`, `playwright`(+Chromium), 한글 렌더용 나눔고딕.

```bash
pip install playwright && playwright install chromium
sudo apt install fonts-nanum
```

Chromium 경로는 `CHROME` 환경변수로 덮어쓸 수 있다. 표지·꼬리말의 버전 문자열은 빌드에 쓴
ref 를 그대로 찍으므로 **납품본은 태그로 빌드할 것** (브랜치로 빌드하면 `main` 이라고 찍힌다).

## 리포에서 뽑는 것

`build.sh` 가 지정한 ref 에서 소스를 꺼내 `extract.cjs` 로 다음을 만든다.

| 뽑는 것 | 출처 |
|---|---|
| 블록 라벨·툴팁 | `ide/static/en.js` (영문판) / `ide/static/ko.js` (한글판) |
| 카테고리와 블록 배치 | `ide/static/customblock_toolbox.js` |
| 블록 타입 → Msg 키 (`keymap.json`) | `ide/static/customblock.js` 의 `message0` |
| 기본 동작 이름 82개 | `ide/static/customblock.js` 의 `motion_set_motion_dropdown` |
| 카테고리 표시명 | `ide/static/ko2en.js` |

**툴박스는 평가해서 읽는다.** `customblock_toolbox.js` 는 `toolbox(lang)` 함수라
`translations` / `color_type` / `lang` 만 채워 넣으면 그대로 실행된다. 정규식으로 긁지 않는
이유다 — 블록 순서가 바뀌어도 따라간다.

블록 타입과 Msg 키가 항상 같지는 않다 (`wikipedia_search` → `COLLECT_WIKIPEDIA`). 그래서
`customblock.js` 의 `message0: '%{BKY_…}'` 에서 대응표를 따로 뽑는다.

## 손으로 쓴 부분

블록 목록 밖의 서술(예제 해설, 설치 절차, 문제해결)은 생성기 안에 파이썬 리터럴로 들어 있다.

| 파일 | 내용 |
|---|---|
| `gen_teacher.py` / `gen_setup.py` | 영문판 |
| `gen_teacher_ko.py` / `gen_setup_ko.py` | 한글판 |

가슴 OLED 화면과 WiFi 설정 팝업은 사진이 아니라 **HTML/CSS 로 그린다**
(`oled()`, `wifi_dialog()`). 작아서 찍으면 읽기 어렵다.

## 사진

`img/` 의 화면 사진은 **영문 배포판 기기에서 찍은 것**이라 블록 이름이 영문이다.
한글판은 이걸 쓰지 않는다 — `img/ko/` 에 같은 파일명으로 국내판 화면을 넣어야 들어가고,
없으면 **그림 없이 글만** 나간다. 빌드할 때 없는 목록을 찍어 준다.

로봇 사진(`image1.jpg`)만 언어와 무관해서 양쪽에 그대로 쓴다.
캡션 → 파일 매핑은 각 `gen_teacher*.py` 의 `IMG` 사전에 있다.

## 소스 문구와 다른 곳

`en.js` 의 오타 몇 개는 인쇄물에 고쳐 실었다. `gen_teacher.py` 의 `TYPO` 사전을 볼 것.
260917 에 en.js 원본도 고쳤으므로 그 이후 태그로 빌드하면 사전이 비어도 결과가 같다.

## 안 되어 있는 것

- 국내판 화면 사진 13장 (위 '사진' 참고)
- 기기 안 문서(`docs/`, Guide 버튼, 포트 8080)는 한국어뿐이다. 영문 배포판에서는
  매뉴얼이 그걸 대신하고 있다
