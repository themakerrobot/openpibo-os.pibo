# 마스터 이미지 만들기

기기 하나를 완성해 두고, 그 SD카드를 떠서 줄인 뒤 다른 카드에 굽는다.

`system/init` 이 부팅할 때 Pi 시리얼로 hostname 을 다시 잡고 재부팅하므로
(`hostname` → AP SSID `pibo-<시리얼8자리>` → `hotspot.sh` 채널 1/6/11),
같은 이미지를 여러 장에 구워도 기기끼리 구분된다. 이미지에 시리얼을 넣을 필요 없다.

---

## 1. 기준 기기 준비

배포 태그로 클론된 상태여야 한다. `git checkout main` 상태로 두지 말 것.

```bash
cd /home/pi/openpibo-os
git describe --tags           # YYMMDDvN 또는 YYMMDDvN-ph
cat /home/pi/.OS_VERSION      # piBo_YYMMDDvN(-ph)
```

필리핀 배포본이면 `system/ph_setup.sh` 를 돌린다. 여러 번 돌려도 안전하다.

```bash
sudo bash /home/pi/openpibo-os/system/ph_setup.sh
sudo reboot
```

## 2. 뜨기 전 청소

이미지에 개인 정보와 기기별 상태가 딸려간다. 전원 끄기 전에 지운다.

```bash
# 기기별 상태
sudo rm -f  /etc/NetworkManager/system-connections/*.nmconnection*   # WiFi 비번
sudo rm -rf /home/pi/code/* /home/pi/myimage/* /home/pi/myaudio/* 2>/dev/null
sudo rm -f  /home/pi/.bash_history /root/.bash_history

# 로그
sudo journalctl --rotate && sudo journalctl --vacuum-time=1s

# 남아 있으면 안 되는 것들
ls -la /home/pi/.ssh/                 # 개인키가 있으면 지운다. known_hosts 도 사내 호스트가 남는다
ls -d  /home/pi/.git 2>/dev/null      # 있으면 지운다
grep -rIl "token\|password\|secret" /home/pi --exclude-dir=.openpibo-os.pibo 2>/dev/null | head

sudo shutdown -h now
```

**Raspberry Pi Imager 의 "OS 커스터마이즈" 를 쓴 카드는 기준 기기로 쓰지 말 것.**
`/boot/firmware/custom.toml`(구버전은 `firstrun.sh`)이 남아 있으면 첫 부팅에
`raspi-config nonint do_wifi_country` 를 다시 호출해서 `cmdline.txt` 의
`cfg80211.ieee80211_regdom` 값이 `PHPH` 처럼 덧붙는다.

```bash
ls -l /boot/firmware/custom.toml /boot/firmware/firstrun.sh   # 둘 다 없어야 한다
```

## 3. 카드 이미지로 뜨기 (Windows)

Win32DiskImager 나 Raspberry Pi Imager 의 읽기 기능으로 `C:\img\pibo.img` 에 저장한다.
카드 전체 용량만큼 나온다(32GB 카드면 약 30GB).

## 4. PiShrink 로 줄이기 (WSL2)

1. 이미지 파일을 `C:\img\pibo.img` 에 둔다 (경로는 예시)
2. WSL2 Ubuntu 가 없으면 관리자 PowerShell 에서 `wsl --install` 후 재부팅.
   이미 있으면 Ubuntu 실행
3. Ubuntu 터미널에 그대로 붙여넣는다

```bash
sudo apt update && sudo apt install -y parted e2fsprogs wget
cd /mnt/c/img
wget https://raw.githubusercontent.com/Drewsif/PiShrink/master/pishrink.sh
chmod +x pishrink.sh
sudo ./pishrink.sh pibo.img pibo_small.img
```

4. 몇 분 뒤 `C:\img\pibo_small.img` 가 생긴다. 실제 사용량 크기(예: 6~8GB)다
5. Raspberry Pi Imager → **Use custom** → `pibo_small.img` → 새 카드에 굽기.
   **"OS 커스터마이즈" 는 "설정 없음" 으로 둘 것** (2번 항목 참고)
6. 파이에서 첫 부팅 시 카드 전체 용량으로 자동 확장된다

PiShrink 는 `/etc/rc.local` 에 확장 스크립트를 심었다가 첫 부팅 후 원래대로 되돌린다.
구운 카드로 부팅한 뒤 원복됐는지 확인한다.

## 5. 구운 카드 검증

```bash
echo "===== 배포본 ====="
cd /home/pi/openpibo-os
git describe --tags
cat /home/pi/.OS_VERSION
head -n1 ide/static/ko2en.js                                   # PH 는 const blang = 'en';
ls -l system/hotspot.sh system/ph_setup.sh system/booting.py tools/static/index.js
ls /home/pi/examples/                                          # PH 는 10개, collect.json 없음

echo "===== 서비스 ====="
systemctl is-active ide booting                                # active active
systemctl is-active tools classify llama-server                # 전부 inactive 가 정상
curl -s -o /dev/null -w "ide:%{http_code}\n" http://localhost/
curl -s http://localhost:8080/wifi_scan | head -c 200; echo

echo "===== 시스템 ====="
hostname                                                       # 시리얼 8자리
df -h / | tail -1                                              # 카드 용량으로 확장됐는지
timedatectl | grep -i "time zone"                              # PH 는 Asia/Manila
head -13 /etc/rc.local | tail -1                               # system/init 호출 (PiShrink 원복 확인)
ls -l /boot/firmware/custom.toml /boot/firmware/firstrun.sh 2>&1   # 둘 다 없어야 한다

echo "===== 장치 ====="
ls -l /dev/ttyS0 /dev/ttyGS0 /dev/video0
dmesg | grep -iE "error|fail" | grep -vi txcap_blob | tail
```

`/dev/ttyS0` 는 MCU, `/dev/ttyGS0` 는 USB gadget serial 이다.
`mcu_control.py` 는 포트 열기에 실패해도 조용히 `self.ser = None` 으로 넘어가므로,
파일 존재만으로는 부족하고 LED·모터가 실제로 움직이는지 봐야 한다.

`brcmfmac: brcmf_c_process_txcap_blob: no txcap_blob available` 은 정상이다.
이 칩에 국가별 송신 테이블이 없다는 뜻이고, 그래서 `iw reg get` 의 `phy#0` 가
`country 99` (전 대역 20 dBm)로 고정된다.
