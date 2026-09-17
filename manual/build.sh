#!/bin/bash
# 매뉴얼 PDF 를 만든다. 내용은 전부 리포에서 뽑으므로 손으로 옮겨 적을 게 없다.
#
#   ./build.sh                    # origin/ph (영문 배포판) 기준
#   ./build.sh 260915v1-ph        # 특정 태그 기준
#
# 필요한 것: node, python3, Chromium (또는 CHROME 환경변수로 경로 지정)
set -e
cd "$(dirname "$0")"

REF="${1:-origin/ph}"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

echo "== $REF 에서 소스를 꺼낸다"
git show "$REF:ide/static/customblock_toolbox.js" > "$WORK/toolbox.js"
git show "$REF:ide/static/customblock.js"         > "$WORK/customblock.js"
git show "$REF:ide/static/ko2en.js"               > "$WORK/ko2en.js"
git show "$REF:ide/static/en.js"                  > "$WORK/msgs.js"
mkdir -p "$WORK/examples"
for f in $(git ls-tree --name-only "$REF" examples/); do
  git show "$REF:$f" > "$WORK/examples/$(basename "$f")"
done

echo "== 블록·모션 목록 추출"
node extract.cjs "$WORK" en

echo "== HTML 생성"
MANUAL_DATA="$WORK" MANUAL_TAG="$REF" python3 gen_teacher.py
MANUAL_DATA="$WORK" MANUAL_TAG="$REF" python3 gen_setup.py

echo "== PDF 렌더"
MANUAL_DATA="$WORK" python3 render_pdf.py

echo
ls -lh Pibo_Teachers_Guide.pdf Pibo_Setup_Administration.pdf
