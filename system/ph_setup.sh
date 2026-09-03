#!/bin/bash
# 필리핀 납품용 기기 설정 — 이미지 생성 시 1회 실행
set -e
sudo timedatectl set-timezone Asia/Manila
sudo raspi-config nonint do_wifi_country PH
sudo chmod +x /home/pi/openpibo-os/system/hotspot.sh
echo "done. reboot required."
