"""로봇 화면에 짧은 글 몇 줄을 띄운다(261102 — USB 업데이트 진행 표시. system/init 이 부른다).

  /home/pi/.pyenv/bin/python3 /home/pi/openpibo-os/system/msg_disp.py "USB update" "running..."

영문만 쓴다(기본 글꼴이 한글을 못 그릴 수 있다). 실패해도 init 이 멈추지 않게 늘 끝 코드 0.
"""
import sys

def run(lines):
  try:
    from openpibo.oled import Oled
    o = Oled()
    o.set_font(size=13)
    for i, line in enumerate(lines[:3]):
      o.draw_text((0, 5 + i * 20), str(line))
    o.show()
    return True, ""
  except Exception as ex:
    return False, str(ex)

if __name__ == "__main__":
  print(run(sys.argv[1:]))
