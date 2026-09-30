#!/bin/bash
# 매뉴얼 PDF 를 만든다. 내용은 전부 리포에서 뽑으므로 손으로 옮겨 적을 게 없다.
#
#   ./build.sh                    # 영문판 origin/ph + 한글판 origin/main
#   ./build.sh 260915v1-ph        # 영문판만 그 태그로. 한글판은 --ko-ref 로 따로 준다
#   ./build.sh 260915v1-ph --ko-ref=260915v1
#   ./build.sh --en-only | --ko-only
#
# 영문판은 ph(영문 배포판), 한글판은 main 에서 뽑는다. 블록 이름이 다르고
# main 에만 '수집' 카테고리와 collect.json 예제가 있어서 번역이 아니라 따로 뽑는다.
#
# 필요한 것: node, python3, Chromium (또는 CHROME 환경변수로 경로 지정)
#           한글 렌더에는 나눔고딕이 필요하다:  sudo apt install fonts-nanum
set -e
cd "$(dirname "$0")"

EN_REF=""; KO_REF="origin/main"; DO_EN=1; DO_KO=1
for a in "$@"; do
  case "$a" in
    --ko-ref=*) KO_REF="${a#--ko-ref=}" ;;
    --en-only)  DO_KO=0 ;;
    --ko-only)  DO_EN=0 ;;
    -*) echo "모르는 옵션: $a"; exit 1 ;;
    *)  EN_REF="$a" ;;
  esac
done
EN_REF="${EN_REF:-origin/ph}"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

# $1 = ref, $2 = 넣을 디렉토리, $3 = ko.js|en.js
pull() {
  mkdir -p "$2"
  git show "$1:ide/static/customblock_toolbox.js" > "$2/toolbox.js"
  git show "$1:ide/static/customblock.js"         > "$2/customblock.js"
  git show "$1:ide/static/ko2en.js"               > "$2/ko2en.js"
  git show "$1:ide/static/$3"                     > "$2/msgs.js"
}

if [ "$DO_EN" = 1 ]; then
  echo "== 영문판: $EN_REF"
  pull "$EN_REF" "$WORK/en" en.js
  node extract.cjs "$WORK/en" en
  MANUAL_DATA="$WORK/en" MANUAL_TAG="$EN_REF" python3 gen_teacher.py
  MANUAL_DATA="$WORK/en" MANUAL_TAG="$EN_REF" python3 gen_setup.py
fi

if [ "$DO_KO" = 1 ]; then
  echo "== 한글판: $KO_REF"
  pull "$KO_REF" "$WORK/ko" ko.js
  node extract.cjs "$WORK/ko" ko
  MANUAL_DATA="$WORK/ko" MANUAL_TAG="$KO_REF" python3 gen_teacher_ko.py
  MANUAL_DATA="$WORK/ko" MANUAL_TAG="$KO_REF" python3 gen_setup_ko.py
fi

echo "== PDF 렌더"
python3 render_pdf.py

echo
ls -lh *.pdf
