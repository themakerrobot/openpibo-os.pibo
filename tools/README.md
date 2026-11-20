# tools — 동작·카메라·음성 도구 (50000)

IDE [도구] 버튼이 `tools.service` 를 켜고 이 화면을 연다(직접 켤 일은 거의 없다).
패키지는 기기 가상환경에 이미 있다 — 목록은 리포 맨 위 `requirements.txt`.

손으로 띄울 때(시험용):

```bash
sudo systemctl stop tools.service classify.service 'llama-server@*'
cd /home/pi/openpibo-os/tools && sudo /home/pi/.pyenv/bin/python3 run_tools.py --port 50000   # static 을 이 폴더 기준으로 찾는다(아이콘 글꼴은 IDE 가 준다)
```
