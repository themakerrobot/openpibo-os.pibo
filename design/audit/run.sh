#!/usr/bin/env bash
# 전수 조사 — AUDIT.md 의 S(파일)·B(화면) 항목을 한 번에 돌린다. M·D 항목은 사람이 본다.
#   PY=<파이썬> bash design/audit/run.sh ../openpibo-os.pibrain [--quick] [--no-fetch]
# PY: numpy·opencv·babel·pillow·fastapi·uvicorn 이 있는 파이썬(도움말 빌드와 같은 것). 없으면 python3
# 미리보기가 이미 떠 있으면(18999) 그대로 쓰고, 없으면 띄웠다가 끝에 끈다. 끝 코드: FAIL 이 하나라도 있으면 1
set -u
cd "$(dirname "$0")/../.."
PIBRAIN="${1:-}"
shift || true
PY="${PY:-python3}"
OUT="design/audit/out"
QUICK=""; FETCH=""
for a in "$@"; do
  case "$a" in
    --quick) QUICK="--quick" ;;
    --no-fetch) FETCH="--no-fetch" ;;
    *) echo "모르는 옵션: $a"; exit 2 ;;
  esac
done
[ -n "$PIBRAIN" ] && [ ! -d "$PIBRAIN/.git" ] && { echo "!! PiBrain 리포가 아니다: $PIBRAIN"; exit 2; }

echo "== S: 파일 검사"
PY="$PY" python3 design/audit/static_check.py $PIBRAIN $FETCH
s=$?

IP=$(PY="$PY" "$PY" -c 'import sys; sys.path.insert(0, "design"); import preview; print(preview.lan_ip())' 2>/dev/null || hostname -I | awk '{print $1}')
started=""
if ! curl -s -o /dev/null --max-time 2 "http://$IP:18999/"; then
  echo "== 미리보기 띄우기 ($IP)"
  "$PY" design/preview.py $PIBRAIN > /tmp/pibo_audit_preview.log 2>&1 &
  started=$!
  for i in $(seq 1 60); do
    curl -s -o /dev/null --max-time 1 "http://$IP:18160/" && break
    sleep 1
  done
fi

echo "== B: 화면 검사"
rm -rf "$OUT"; mkdir -p "$OUT"
PY="$PY" node design/audit/browser_check.js "$IP" "$PIBRAIN" "$OUT" $QUICK
b=$?

[ -n "$started" ] && { kill "$started" 2>/dev/null; wait "$started" 2>/dev/null; }
echo
echo "== 끝: 파일 검사 $([ $s = 0 ] && echo OK || echo FAIL) · 화면 검사 $([ $b = 0 ] && echo OK || echo FAIL)"
echo "   사람이 볼 것: AUDIT.md 의 M·D 항목, 캡처 $OUT/"
[ $s = 0 ] && [ $b = 0 ]
