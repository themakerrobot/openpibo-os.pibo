#!/bin/bash
# 필리핀 납품용 기기 설정 — 이미지 생성 시 실행.
# 여러 번 돌려도 결과가 같아야 한다(멱등). 검증 중에 재실행하는 일이 잦다.
set -e

sudo timedatectl set-timezone Asia/Manila
sudo raspi-config nonint do_wifi_country PH

# raspi-config 는 cmdline.txt 의 cfg80211.ieee80211_regdom 값을 교체하지 못하고
# 덧붙이는 경우가 있다. 재실행했더니 실제로 '=PHPH' 가 됐다(260910v4-ph 검증 중).
# 유효한 2글자 국가코드가 아니게 되고 raspi-config nonint get_wifi_country 도
# 빈 값을 돌려주므로, 실행할 때마다 값을 정규화한다.
# cmdline.txt 는 반드시 한 줄이어야 하니 개행을 넣는 편집은 하지 않는다.
CMDLINE=/boot/firmware/cmdline.txt
[ -f "$CMDLINE" ] || CMDLINE=/boot/cmdline.txt
if grep -q 'cfg80211\.ieee80211_regdom=' "$CMDLINE"; then
  sudo sed -i 's/cfg80211\.ieee80211_regdom=[A-Za-z]*/cfg80211.ieee80211_regdom=PH/' "$CMDLINE"
else
  sudo sed -i '1 s/$/ cfg80211.ieee80211_regdom=PH/' "$CMDLINE"
fi

# 베이스 이미지에 남아있는 brcmfmac 국가코드 잔재를 제거한다.
#   /etc/modprobe.d/brcmfmac.conf: options brcmfmac country=US
# 현재 드라이버(BCM4345/6, 7.45.265)는 이 파라미터를 지원하지 않아
# "brcmfmac: unknown parameter 'country' ignored" 로 무시하지만,
# 지원하는 버전으로 올라가면 기기가 US 도메인이 된다.
sudo rm -f /etc/modprobe.d/brcmfmac.conf

sudo chmod +x /home/pi/openpibo-os/system/hotspot.sh

echo "done. reboot required."
echo "확인: cat $CMDLINE   → cfg80211.ieee80211_regdom=PH 가 한 번만, 파일은 한 줄"
