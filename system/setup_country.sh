#!/bin/bash
# 납품 국가 설정 — 마스터 이미지 만들 때 한 번 실행한다.
# 여러 번 돌려도 결과가 같아야 한다(멱등). 검증 중에 재실행하는 일이 잦다.
#
#   sudo bash /home/pi/openpibo-os/system/setup_country.sh PH
#
# 260914v7 까지 쓰던 system/ph_setup.sh 를 대신한다. 하는 일은 같고
# 국가만 인자로 받는다. 필리핀·말레이시아처럼 영문 배포판이 여럿이어도
# 브랜치를 나눌 필요가 없다.
set -e

CC="$(echo "${1:-}" | tr '[:lower:]' '[:upper:]')"

# 국가코드 → timezone. 추측으로 채우지 말 것.
# 새 국가를 추가할 때는 `timedatectl list-timezones | grep -i <도시>` 로
# 실제 존재하는 이름인지 확인하고 넣는다.
case "$CC" in
  KR) TZNAME=Asia/Seoul ;;
  PH) TZNAME=Asia/Manila ;;
  MY) TZNAME=Asia/Kuala_Lumpur ;;
  *)
    echo "Usage: $0 {KR|PH|MY}"
    echo "  등록되지 않은 국가코드다. timezone 을 확인한 뒤 이 스크립트의 case 에 추가할 것."
    exit 1
    ;;
esac

echo "== country=$CC timezone=$TZNAME =="

sudo timedatectl set-timezone "$TZNAME"
sudo raspi-config nonint do_wifi_country "$CC"

# raspi-config 는 cmdline.txt 의 cfg80211.ieee80211_regdom 값을 교체하지 못하고
# 덧붙이는 경우가 있다. 재실행했더니 실제로 '=PHPH' 가 됐다(260910v4-ph 검증 중).
# 유효한 2글자 국가코드가 아니게 되고 raspi-config nonint get_wifi_country 도
# 빈 값을 돌려주므로, 실행할 때마다 값을 정규화한다.
# cmdline.txt 는 반드시 한 줄이어야 하니 개행을 넣는 편집은 하지 않는다.
CMDLINE=/boot/firmware/cmdline.txt
[ -f "$CMDLINE" ] || CMDLINE=/boot/cmdline.txt
if grep -q 'cfg80211\.ieee80211_regdom=' "$CMDLINE"; then
  sudo sed -i "s/cfg80211\.ieee80211_regdom=[A-Za-z]*/cfg80211.ieee80211_regdom=$CC/" "$CMDLINE"
else
  sudo sed -i "1 s/\$/ cfg80211.ieee80211_regdom=$CC/" "$CMDLINE"
fi

# 베이스 이미지에 남아있는 brcmfmac 국가코드 잔재를 제거한다.
#   /etc/modprobe.d/brcmfmac.conf: options brcmfmac country=US
# 현재 드라이버(BCM4345/6, 7.45.265)는 이 파라미터를 지원하지 않아
# "brcmfmac: unknown parameter 'country' ignored" 로 무시하지만,
# 지원하는 버전으로 올라가면 기기가 US 도메인이 된다.
sudo rm -f /etc/modprobe.d/brcmfmac.conf

# 실행비트. git clone 으로 받으면 이미 100755 지만, tarball 로 덮어썼거나
# 파일을 손으로 옮긴 기기에서는 벗겨져 있다.
for f in system/booting.py system/hotspot.sh system/setup_country.sh \
         system/setup_openpibo_src.sh tools/static/index.js; do
  [ -f "/home/pi/openpibo-os/$f" ] && sudo chmod +x "/home/pi/openpibo-os/$f"
done

echo
echo "done. reboot required."
echo "확인:"
echo "  cat $CMDLINE                 → cfg80211.ieee80211_regdom=$CC 가 한 번만, 파일은 한 줄"
echo "  timedatectl | grep 'Time zone'  → $TZNAME"
echo "  raspi-config nonint get_wifi_country  → $CC"
