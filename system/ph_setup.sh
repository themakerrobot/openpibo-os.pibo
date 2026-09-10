#!/bin/bash
# 필리핀 납품용 기기 설정 — 이미지 생성 시 1회 실행
set -e
sudo timedatectl set-timezone Asia/Manila
sudo raspi-config nonint do_wifi_country PH

# 베이스 이미지에 남아있는 brcmfmac 국가코드 잔재를 제거한다.
#   /etc/modprobe.d/brcmfmac.conf: options brcmfmac country=US
# 현재 드라이버(BCM4345/6, 7.45.265)는 이 파라미터를 지원하지 않아
# "brcmfmac: unknown parameter 'country' ignored" 로 무시하지만,
# 지원하는 버전으로 올라가면 기기가 US 도메인이 된다.
# 2.4GHz 최대 EIRP 가 PH 20 dBm / US 30 dBm 이라 10배 초과 송신이 된다.
# 규제 도메인은 cmdline.txt 의 cfg80211.ieee80211_regdom=PH 로 설정된다.
sudo rm -f /etc/modprobe.d/brcmfmac.conf

sudo chmod +x /home/pi/openpibo-os/system/hotspot.sh
echo "done. reboot required."
