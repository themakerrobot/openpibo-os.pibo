"""학교 WiFi ↔ AP(핫스팟) 전환 판단 (260929).

booting.py 의 wifi_update 가 10초마다 step(has_ip) 을 부른다.

전에는 IP 가 한 번만 없어도 바로 AP 로 넘어갔고, hotspot.sh 가 AP 를 켜기 전에 학교 WiFi 연결
(pibo-wifi)을 직접 내려서 NetworkManager 가 다시 붙지 않았다. 수업에서 30대가 한꺼번에 붙어
DHCP 가 밀리면 일부가 AP 로 넘어가 그대로 갇혔다(재부팅 말고는 복귀 불가).

지금 규칙 — 저장된 WiFi 는 늘 있다(납품 때 pibo / !pibo0314, 사용자가 바꿀 수 있다):

  IP 있음                         → 아무것도 안 한다(스캔도 안 한다). AP 였으면 끈다
  IP 없음 + 저장된 SSID 안 보임     → 바로 AP (공유기가 없다 — 꺼짐·다른 장소·이름 바뀜)
  IP 없음 + 저장된 SSID 보임        → 기다린다. 9번 연속(90초)이면 AP
                                     (NetworkManager DHCP 기본 대기 45초 × 2)
  AP 모드                         → 스스로 끄지 않는다. AP 로 계속 쓰는 수업도 있다.
                                     [인터넷 설정] 으로 학교 WiFi 를 잡아 IP 를 받거나 재부팅하면 나온다

스캔은 AP 로 넘어가기 전, IP 가 없을 때만 본다(--rescan auto: 마지막 스캔이 30초보다 오래됐을 때만
새로 스캔 — 끊겨 있을 때 NetworkManager 가 스스로 하는 스캔을 재사용). AP 모드에서는 스캔하지 않는다
(스캔은 된다 — [인터넷 설정] 의 WiFi 목록이 AP 모드에서 뜬다. AP 를 스스로 끄지 않으니 판단할 게 없을 뿐).
※ AP 모드에서 아무도 안 붙어 있으면 2분마다 학교 WiFi 로 돌아가 보는 자력 복귀를 넣었다가 뺐다(260929) —
  AP 로 계속 쓰는 경우가 있어 로봇이 스스로 AP 를 끄면 안 된다

실행하는 명령은 ops 로 바꿔 끼울 수 있다(기기 없이 시험하려고).
"""
import subprocess

import wifi

HOTSPOT = '/home/pi/openpibo-os/system/hotspot.sh'
WIFI_CON = 'pibo-wifi'

AP_WAIT_CHECKS = 9      # 저장된 SSID 가 보이는데 IP 가 없을 때: 10초 × 9 = 90초 기다린 뒤 AP


def _run(args, timeout):
  try:
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout)
  except Exception as ex:
    print(f'[netwatch] {args[0]} 실패: {ex}', flush=True)
    return None


def saved_ssid():
  r = _run(['nmcli', '-g', '802-11-wireless.ssid', 'connection', 'show', WIFI_CON], 10)
  return r.stdout.strip() if r and r.returncode == 0 else ''


def visible_ssids(force=False):
  r = _run(['nmcli', '-t', '-f', 'SSID', 'dev', 'wifi', 'list', '--rescan', 'yes' if force else 'auto'], 30)
  if not r or r.returncode != 0:
    return set()
  return {wifi.split_terse(line)[0] for line in r.stdout.splitlines() if line.strip()}


def hotspot(cmd):
  _run([HOTSPOT, cmd], 120)


DEFAULT_OPS = {
  'saved_ssid': saved_ssid,
  'visible_ssids': visible_ssids,
  'hotspot': hotspot,
}


class NetWatch:
  def __init__(self, ops=None):
    self.ops = dict(DEFAULT_OPS, **(ops or {}))
    self.apmode = False
    self.miss = 0                   # 'IP 없음 + SSID 보임' 연속 횟수

  def _ap_on(self, why):
    print(f'[netwatch] AP 켬: {why}', flush=True)
    self.ops['hotspot']('start')
    self.apmode = True
    self.miss = 0

  def step(self, has_ip):
    """10초마다 한 번. 무엇을 했는지 짧은 문자열로 돌려준다(로그·시험용)"""
    if has_ip:
      done = 'ok'
      if self.apmode:
        print('[netwatch] IP 받음 → AP 끔', flush=True)
        self.ops['hotspot']('stop')
        done = 'ap_off'
      self.apmode = False
      self.miss = 0
      return done

    if self.apmode:
      return 'ap'           # AP 는 스스로 끄지 않는다(IP 를 받거나 재부팅할 때만)

    ssid = self.ops['saved_ssid']()
    if not ssid or ssid not in self.ops['visible_ssids'](False):
      self._ap_on(f'저장된 SSID {ssid!r} 가 안 보임')
      return 'ap_on_absent'
    self.miss += 1
    if self.miss >= AP_WAIT_CHECKS:
      self._ap_on(f'{ssid!r} 는 보이는데 {self.miss * 10}초 동안 IP 를 못 받음')
      return 'ap_on_timeout'
    print(f'[netwatch] IP 없음, {ssid!r} 보임 → 기다림 {self.miss}/{AP_WAIT_CHECKS}', flush=True)
    return 'wait'
