#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""설치·관리자 가이드(한글) — 국내 배포판(main) 기준.

영문판과 다른 점:
  - 공유기 5GHz 채널 제약이 없다. KR 규제도메인은 149~165 도 열려 있다
    (PH 는 CLM blob 때문에 상위 채널이 막혀 36~48 로 고정해야 한다)
  - 공유기를 함께 납품하는 전제가 아니다. 기관이 이미 쓰는 공유기를 pibo 로
    맞추는 경우를 기본으로 쓰고, 새로 살 때의 권장 기종을 덧붙인다
  - 기기 안 문서(포트 8080)가 한국어라 Guide 버튼을 그대로 쓸 수 있다
"""
import io, os, datetime, html

HERE = os.path.dirname(os.path.abspath(__file__))
TAG  = os.environ.get('MANUAL_TAG', 'origin/main').replace('origin/', '')
TODAY = datetime.date.today().isoformat()
esc = lambda s: html.escape(s, quote=False)


def oled(sn='cd488e95', ip='192.168.114.138', ap='pibo'):
    return ('<div class="oled"><div class="oled-s">'
            f'<div>SN: {esc(sn)}</div><div>I P: {esc(ip)}</div><div>AP: {esc(ap)}</div>'
            '</div></div>')


def wifi_dialog():
    """IDE 의 인터넷 설정 팝업을 그린다. 작아서 찍으면 읽기 어렵다."""
    rows = [('pibo', '100%'), ('pibo-24', '92%'), ('school-wifi', '78%')]
    tr = ''.join(f'<div class="w-row"><span class="w-ssid">{esc(s)}</span>'
                 f'<span class="w-meta">{g} &nbsp;\U0001f512 wpa-psk</span></div>' for s, g in rows)
    return f'''<div class="wdlg">
<div class="w-head"><b>인터넷 설정</b><span class="w-x">✕</span></div>
<div class="w-ip">192.168.114.138 / pibo</div>
<div class="w-sub">연결 가능한 네트워크</div>
<div class="w-list">{tr}</div>
<div class="w-manual">수동 연결 / 기타 네트워크…</div>
</div>'''


CSS = '''
@page { size: A4; margin: 18mm 16mm 16mm 16mm; }
* { box-sizing: border-box; }
body { font: 10.5pt/1.7 "NanumGothic","Nanum Gothic","Noto Sans KR",sans-serif;
       color:#1a1a1a; margin:0; word-break:keep-all; }
h1,h2,h3,h4 { line-height:1.4; }
h2 { font-size:15pt; margin:0 0 10pt; padding-bottom:5pt; border-bottom:2.5pt solid #1a1a1a; }
h3 { font-size:12pt; margin:15pt 0 5pt; break-after:avoid; page-break-after:avoid; }
h4 { font-size:10.5pt; margin:12pt 0 3pt; }
p  { margin:0 0 7pt; }
code { font:9.5pt ui-monospace,Menlo,Consolas,monospace; background:#f0f0f0;
       padding:.5pt 3pt; border-radius:2pt; word-break:break-all; }
pre  { font:9pt/1.5 ui-monospace,Menlo,Consolas,monospace; background:#f4f4f4;
       border-left:3pt solid #999; padding:7pt 9pt; margin:6pt 0 9pt; white-space:pre-wrap;
       break-inside:avoid; word-break:break-all; }
.page { page-break-after: always; }
.page:last-child { page-break-after: auto; }
.cover { height:245mm; display:flex; flex-direction:column; }
.cover .top { margin-top:52mm; }
.cover .k { font-size:34pt; font-weight:700; letter-spacing:-1pt; margin:0; }
.cover .s { font-size:14pt; color:#555; margin:6pt 0 0; }
.cover .m { margin-top:auto; font-size:9pt; color:#666; border-top:1pt solid #ccc; padding-top:8pt; }
.lead { font-size:11pt; color:#444; margin-bottom:12pt; }
table { border-collapse:collapse; width:100%; margin:6pt 0 10pt; font-size:9.5pt; }
th,td { border:.6pt solid #bbb; padding:3.5pt 5pt; text-align:left; vertical-align:top; }
th { background:#ececec; font-weight:600; }
thead { display:table-header-group; }
tr { break-inside:avoid; }
.note { border-left:3pt solid #666; background:#f6f6f6; padding:7pt 10pt; margin:9pt 0; font-size:10pt; }
.note b:first-child { display:block; margin-bottom:2pt; }
.warn { border-left-color:#000; background:#ededed; }
ol,ul { margin:0 0 8pt; padding-left:17pt; }
li { margin-bottom:3pt; }
.toc { font-size:11pt; }
.toc div { padding:3.5pt 0; border-bottom:.5pt dotted #ccc; }
.toc .n { display:inline-block; width:26pt; color:#888; }
.flow { border:.6pt solid #bbb; border-radius:3pt; padding:9pt 11pt; margin:8pt 0 10pt;
        font-size:10pt; background:#fbfbfb; break-inside:avoid; }
.flow .arrow { color:#999; margin:2pt 0 2pt 6pt; }
.oled { background:#111; border:2.5pt solid #444; border-radius:4pt; padding:7pt 9pt; }
.oled-s { font:11pt/1.5 ui-monospace,Menlo,Consolas,monospace; color:#e8e8e8; min-height:50pt; }
.oled-cap { text-align:center; font-size:8.5pt; color:#666; margin-top:3pt; }
.oled-row { display:flex; gap:12pt; margin:10pt 0 12pt; break-inside:avoid; }
.oled-row > div { flex:1; }
.wdlg { border:1pt solid #999; border-radius:4pt; width:88mm; margin:10pt auto 4pt;
        font-size:9.5pt; overflow:hidden; break-inside:avoid; }
.w-head { background:#fff; padding:7pt 9pt 4pt; font-size:12pt; border-bottom:.5pt solid #eee;
          display:flex; justify-content:space-between; align-items:center; }
.w-x { color:#fff; background:#333; border-radius:2pt; padding:0 4pt; font-size:9pt; }
.w-ip { padding:5pt 9pt 2pt; color:#333; font:9.5pt ui-monospace,Menlo,monospace; }
.w-sub { padding:2pt 9pt 5pt; font-weight:600; font-size:11pt; }
.w-list { border:.6pt solid #ccc; border-radius:3pt; margin:0 9pt; }
.w-row { display:flex; justify-content:space-between; padding:5pt 7pt;
         border-bottom:.5pt solid #eee; }
.w-row:last-child { border-bottom:none; }
.w-ssid { font-weight:600; }
.w-meta { color:#555; font-size:8.5pt; }
.w-manual { text-align:right; color:#2a5db0; padding:6pt 9pt 8pt; font-size:9pt; }
.dcap { text-align:center; font-size:8.5pt; color:#666; margin-bottom:10pt; }
'''


def build():
    o = io.StringIO(); W = o.write
    W('<!doctype html><html lang="ko"><head><meta charset="utf-8">'
      '<title>파이보 설치·관리 가이드</title><style>' + CSS + '</style></head><body>')

    # 표지
    W(f'''<section class="page cover"><div class="top">
<p class="k">파이보</p><p class="k" style="font-size:26pt;font-weight:400">설치·관리 가이드</p>
<p class="s">로봇과 공유기, 그리고 교실 네트워크</p>
<div class="note" style="margin-top:24pt"><b>이 문서를 볼 사람</b>
로봇을 설치하고 관리하는 담당자용입니다. 수업을 진행하는 선생님은
<i>파이보 교사용 가이드</i>를 보시면 됩니다.</div></div>
<div class="m"><b>Circulus Inc.</b> &nbsp;·&nbsp; 소프트웨어 버전 {TAG}
&nbsp;·&nbsp; 발행 {TODAY}</div></section>''')

    # 목차
    W('<section class="page"><h2>목차</h2><div class="toc">')
    for n, t in [('1', '파이보가 네트워크에 붙는 방식'), ('2', '공유기 설정'),
                 ('3', '교실에 설치하기'), ('4', '태블릿·노트북 준비'),
                 ('5', '로봇 점검'), ('6', '다른 네트워크로 연결하기'),
                 ('7', '공장초기화'), ('8', '문제 해결'),
                 ('A', '부록 A — 기본값과 주소')]:
        W(f'<div><span class="n">{n}</span>{esc(t)}</div>')
    W('</div>')
    W('''<div class="note" style="margin-top:18pt"><b>요약</b>
로봇은 <code>pibo</code> 라는 5GHz 네트워크를 찾도록 출하됩니다. 공유기를 그 이름으로 맞춰
두면 전원만 켜도 알아서 붙습니다. 1·2장이 그 이유와 건드리면 안 되는 값을 설명합니다.</div>
<div class="note warn"><b>교실 하나에 공유기 하나, 로봇 10대</b>
한 교실에 공유기는 한 대만 둡니다. 같은 이름의 공유기가 두 대 있으면 로봇이 양쪽을
오가며 계속 끊깁니다 — 3장 참고.</div></section>''')

    # 1
    W('''<section class="page"><h2>1 &nbsp; 파이보가 네트워크에 붙는 방식</h2>
<p class="lead">모든 로봇은 <code>pibo</code> 라는 5GHz 네트워크에 접속하도록 설정된 상태로
출하됩니다. 현장에서 로봇마다 WiFi 를 잡아줄 필요가 없습니다.</p>

<h3>전원을 켤 때마다</h3>
<div class="flow">
<b>1.</b> 설정에 저장된 WiFi — <code>pibo</code> — 를 찾습니다.<br>
<div class="arrow">↓ 찾으면</div>
<b>2a.</b> 접속해서 IP 를 받고, 그 주소를 가슴 화면에 띄웁니다. 바로 쓸 수 있습니다.<br>
<div class="arrow">↓ 못 찾으면</div>
<b>2b.</b> <code>pibo-</code> + 시리얼 뒤 8자리 이름으로 <b>자기 WiFi 를 켭니다</b>.
가슴 화면의 <b>SN</b> 이 그 8자리입니다. 이걸 <b>AP 모드</b>라고 합니다.
</div>
<p>이 확인은 로봇이 켜져 있는 동안 10초마다 반복됩니다. 공유기를 나중에 켜거나 정전 후
복구되면 로봇이 스스로 붙고 자기 WiFi 를 내립니다. 재부팅할 필요가 없습니다.</p>

<h3>가슴 화면</h3>''')
    W('<div class="oled-row">'
      '<div>' + oled() + '<div class="oled-cap">접속됨 — <b>I P</b> 주소를 브라우저에 입력</div></div>'
      '<div>' + oled(ip='', ap='') + '<div class="oled-cap">AP 모드 — 공유기를 못 찾음</div></div>'
      '</div>')
    W('''<p><b>SN</b> 은 로봇 번호, <b>I P</b> 는 브라우저에 입력할 주소, <b>AP</b> 는 접속한
네트워크 이름입니다. <b>I P</b> 가 비어 있으면 AP 모드입니다. <b>SN</b> 으로 어느
<code>pibo-…</code> 네트워크가 어느 로봇 것인지 구분합니다 — 20대가 동시에 켜져 있을 때
필요합니다.</p>

<div class="note warn"><b>AP 모드에서는 인터넷이 안 됩니다</b>
자기 WiFi 를 켠 로봇은 바깥으로 나가는 길이 없습니다. 무선 칩이 하나뿐이고 그게 공유기
노릇을 하고 있기 때문입니다. 고장이 아니라 정상 동작입니다.</div></section>''')

    # 2
    W('''<section class="page"><h2>2 &nbsp; 공유기 설정</h2>
<p class="lead">기관에 이미 있는 공유기를 써도 되고 새로 사도 됩니다. 어느 쪽이든
아래 값만 맞으면 됩니다.</p>

<h3>맞춰야 할 값</h3>
<table><thead><tr><th style="width:30%">항목</th><th>값</th><th style="width:38%">이유</th></tr></thead><tbody>
<tr><td>5GHz 네트워크 이름</td><td><code>pibo</code></td><td>로봇이 이 이름을 찾는다</td></tr>
<tr><td>2.4GHz 네트워크 이름</td><td><code>pibo-24</code></td><td>태블릿·구형 노트북용. 이름을
나눠야 단말이 어느 쪽에 붙었는지 알 수 있다</td></tr>
<tr><td>비밀번호(양쪽 동일)</td><td><code>!pibo0314</code></td><td>출하 설정</td></tr>
<tr><td>5GHz 채널</td><td><b>고정</b>. 36·40·44·48 또는 149·153·157·161</td>
<td><b>자동 금지.</b> 자동은 DFS 대역(52~144)으로 옮겨간다</td></tr>
<tr><td>채널 대역폭</td><td>80MHz 이하</td><td>160MHz 블록은 국내에 두 개뿐이고
<b>둘 다 DFS 를 포함한다</b></td></tr>
<tr><td>무선 모드</td><td>11ac</td><td>로봇의 무선 칩(CYW43455)이 11ax 를 지원하지 않는다</td></tr>
<tr><td>보안</td><td>WPA2-PSK (AES)</td><td>WPA3·혼합 모드는 붙지 않는다</td></tr>
<tr><td>밴드 스티어링<br>(Smart Connect)</td><td>끔</td><td>켜면 두 이름이 하나로 합쳐진다</td></tr>
<tr><td>펌웨어 자동 업데이트</td><td>끔</td><td>업데이트가 채널을 <i>자동</i>으로 되돌린다</td></tr>
</tbody></table>

<div class="note warn"><b>DFS 대역(52~144)은 피하세요</b>
이 대역은 레이더 탐지 때문에 접속 전 최대 10분을 기다리고, 레이더를 감지하면 공유기가
말없이 채널을 옮깁니다. 그때 교실의 로봇이 한꺼번에 떨어집니다. 36~48 이나 149~161 중
하나로 <b>고정</b>하세요.</div>

<h3>새로 살 때</h3>
<p>WiFi 6(AX) 제품이어도 상관없습니다. 위 표대로 11ac 로 내려 쓰면 됩니다. 필요한 성능은
높지 않아서 보급형으로 충분합니다. 필리핀 납품분에는 TP-Link Archer AX53 을 <code>pibo</code>
로 세팅해 함께 보내고 있습니다. 중요한 건 성능이 아니라 <b>5GHz 채널을 수동으로 고정할 수
있는지</b>와 <b>밴드 스티어링을 끌 수 있는지</b>입니다. 이 두 가지가 안 되는 기종은 피하세요.</p>

<h3>로봇 몇 대까지</h3>
<p><b>교실 하나에 공유기 한 대, 로봇 10대</b>를 기준으로 잡으세요. 하드웨어는 더 감당하지만
10대가 수업하기 편한 수입니다 — 카메라 영상이 끊기지 않고, 아이들이 동시에 <b>실행</b>을
눌러도 밀리지 않습니다.</p>
<p>같은 교실에 공유기를 한 대 더 놓는 건 도움이 안 되고 오히려 나쁩니다 — 3장 참고.</p>

<h3>인터넷은 없어도 됩니다</h3>
<p>음성·영상·얼굴인식·언어모델이 전부 로봇 안에서 돕니다. 학교 인터넷이 없거나 끊겨도
수업에는 지장이 없습니다. 인터넷 선이 있으면 공유기의 <b>WAN</b> 포트에 꽂으세요 —
선생님 태블릿에 필요한 것이지 로봇에 필요한 게 아닙니다.</p>
</section>''')

    # 3
    W('''<section class="page"><h2>3 &nbsp; 교실에 설치하기</h2>

<h3>로봇 10대, 공유기 1대</h3>
<ol>
<li>공유기를 교실 대부분에서 보이는 자리에 둡니다. 캐비닛 안이나 철제 사물함 뒤는 피하세요.</li>
<li>전원을 연결합니다. 학교 인터넷 선이 있으면 <b>WAN</b> 포트에 꽂습니다.</li>
<li>1분쯤 기다렸다가 태블릿에서 <code>pibo</code> 와 <code>pibo-24</code> 가 보이는지 확인합니다.</li>
<li>로봇을 몇 대씩 나눠 켭니다.</li>
<li>1분쯤 뒤 가슴 화면에 <b>I P</b> 주소가 뜹니다. 로봇마다 SN 과 IP 를 적어 선생님께 드립니다.</li>
<li>태블릿을 <code>pibo-24</code> 에 연결합니다(5GHz 를 지원하면 <code>pibo</code> 도 됩니다).</li>
</ol>

<h3>한 교실에 같은 이름의 공유기를 두 대 두지 마세요</h3>
<div class="note warn"><b>이름이 같은 공유기가 둘이면 로봇이 양쪽을 오갑니다</b>
둘 다 <code>pibo</code> 를 방송하니 로봇이 양쪽을 다 듣고, 계속 반대쪽이 더 좋아 보인다고
판단해 수업 내내 왔다 갔다 합니다. 옮길 때마다 연결이 끊깁니다. 공유기 한 대에 로봇을
많이 붙이는 것보다 나쁘고, 설정은 다 맞아 보여서 원인을 찾기도 어렵습니다.<br><br>
<b>교실 하나에 공유기 하나.</b> 한 대 더 놓지 말고, 이미 돌고 있는 교실에 여분 공유기를
들고 들어가지도 마세요.</div>

<h3>로봇이 10대를 넘으면</h3>
<p>교실을 나누고 각 교실에 공유기를 한 대씩 두되, 한쪽 교실의 로봇이 다른 쪽 공유기를
듣지 못할 만큼 떨어뜨립니다. 보통 벽 하나둘이면 충분합니다. 한 교실에서 태블릿으로
다른 교실 <code>pibo</code> 의 신호가 보이는지 확인하세요 — 아예 안 보이면 충분합니다.</p>
<p>떨어뜨릴 수 없으면 <b>채널을 다르게</b> 주는 게 차선입니다. 다만 이름이 같으면 로봇은
여전히 둘을 한 네트워크로 보고 오갑니다. 확실한 방법은 한쪽 이름을 바꾸고 그쪽 로봇을
6장으로 다시 잡아주는 것입니다.</p>

<h3>로봇을 어디에 두나</h3>
<p>바닥은 피하고 철제 선반에서 떨어뜨리세요. 팔다리가 부딪히지 않게 주변을 비우고,
공유기가 보이는 자리일수록 신호가 좋습니다.</p></section>''')

    # 4
    W('''<section class="page"><h2>4 &nbsp; 태블릿·노트북 준비</h2>
<p class="lead"><code>pibo</code> 네트워크는 보통 인터넷이 없습니다. 윈도우·안드로이드·
iPadOS 는 인터넷이 안 되는 WiFi 를 나쁜 네트워크로 보고 알아서 빠져나갑니다 —
선생님 눈에는 로봇이 끊긴 것처럼 보입니다. 기기당 몇 분이면 영구히 막을 수 있습니다.</p>

<div class="note warn"><b>왜 그러나</b>
세 OS 모두 접속한 WiFi 가 실제로 인터넷에 닿는지 검사합니다. 안 닿는데 저장해 둔 다른
네트워크가 근처에 있으면, 대개 아무 말 없이 그쪽으로 옮겨갑니다. 로봇은 그대로 있고
태블릿이 떠난 것입니다.</div>

<h3>가장 간단한 해법: 공유기에 인터넷을 물린다</h3>
<p>교실까지 학교 인터넷 선이 온다면 공유기 <b>WAN</b> 포트에 꽂으세요. 그러면
<code>pibo</code> 도 인터넷 되는 네트워크가 되어 아무것도 빠져나가려 하지 않고, 이 장의
나머지가 필요 없어집니다. 이것부터 시도하세요.</p>

<h3>윈도우</h3>
<p>윈도우는 저장된 네트워크가 잡히면 다시 붙습니다. 로봇 네트워크 말고는 자동으로 붙지
않게 합니다.</p>
<ol>
<li><b>설정 → 네트워크 및 인터넷 → Wi-Fi → 알려진 네트워크 관리</b>를 엽니다.</li>
<li><code>pibo</code>·<code>pibo-24</code> 를 <b>뺀 모든</b> 네트워크에서
<b>범위에 있을 때 자동으로 연결</b> 을 끕니다. 다시 쓸 일이 없는 건 <b>잊어버리기</b>.</li>
<li><code>pibo</code> 또는 <code>pibo-24</code> 는 <b>자동으로 연결</b> 을 켜 둡니다.</li>
<li>노트북에 LTE 모뎀이나 테더링이 있으면 수업 중에는 끕니다.</li>
</ol>
<div class="note"><b>“인터넷 없음, 보안됨” 은 정상입니다</b>
윈도우가 로봇 네트워크를 그렇게 표시하고 WiFi 아이콘에 경고 표시를 붙입니다. 로봇과의
연결은 멀쩡합니다. 선생님께 미리 알려 두세요 — 안 그러면 누군가 고치겠다고 네트워크를
바꾸는데, 그게 바로 피해야 할 일입니다.</div>

<h3>안드로이드 태블릿</h3>
<ol>
<li><b>설정 → 네트워크 및 인터넷 → 인터넷</b>. 로봇 네트워크 말고 저장된 네트워크마다
톱니바퀴를 눌러 <b>자동 연결</b> 을 끄거나 저장을 지웁니다.</li>
<li>같은 화면의 <b>네트워크 환경설정</b> 에서 <b>모바일 데이터로 자동 전환</b> 을 끕니다.
제조사마다 문구가 조금씩 다릅니다.</li>
<li>SIM 이 있으면 수업 중 모바일 데이터를 꺼 두는 것으로도 충분합니다.</li>
<li><i>이 네트워크는 인터넷에 연결되어 있지 않습니다. 계속 연결할까요?</i> 가 뜨면 예를
누르고 <b>이 네트워크에 대해 다시 묻지 않음</b> 을 체크합니다.</li>
</ol>

<h3>아이패드</h3>
<ol>
<li><b>설정 → Wi-Fi</b>. 다른 네트워크마다 ⓘ 를 눌러 <b>자동 연결</b> 을 끕니다.</li>
<li><code>pibo</code> 의 ⓘ 에서는 <b>자동 연결</b> 이 켜져 있는지 확인합니다.</li>
<li>셀룰러 모델이면 <b>설정 → 셀룰러 → Wi-Fi 지원</b> 을 끕니다.</li>
</ol>

<h3>준비가 됐는지 확인</h3>
<ol>
<li><code>pibo</code> 또는 <code>pibo-24</code> 에 연결합니다.</li>
<li>로봇 주소를 브라우저로 열고 2~3분 그대로 둡니다.</li>
<li>그대로 붙어 있으면 준비 완료. 다른 네트워크로 옮겨갔으면 자동 연결을 하나 빠뜨린 것입니다.</li>
</ol>

<div class="note"><b>기기를 넘기기 전에 한 번에 해 두세요</b>
태블릿 10대를 책상에 늘어놓고 하는 게, 수업 중에 왜 한 아이 화면만 멈추는지 찾는 것보다
훨씬 빠릅니다. 설치 점검표에 넣으세요.</div>
</section>''')

    # 5
    W('''<section class="page"><h2>5 &nbsp; 로봇 점검</h2>
<p class="lead">로봇을 넘기기 전에 확인할 것.</p>
<table><thead><tr><th style="width:26%">확인</th><th>정상</th></tr></thead><tbody>
<tr><td>가슴 화면</td><td>SN, <b>I P</b> 주소, <b>AP</b> 줄에 <code>pibo</code>.</td></tr>
<tr><td>블록 편집기</td><td>브라우저에 IP 를 입력하면 편집기가 한국어로 열린다.</td></tr>
<tr><td>실행 확인</td><td><i>기본</i> 예제를 열고 실행. 터미널에 한 줄이 찍힌다.</td></tr>
<tr><td>소리</td><td><i>음성</i> 예제를 실행. 로봇이 말한다.</td></tr>
<tr><td>움직임</td><td>주변을 비우고 <i>동작</i> 예제를 실행.</td></tr>
<tr><td>카메라</td><td><i>얼굴</i> 예제를 실행. IDE 에 사진이 나온다.</td></tr>
<tr><td>수집</td><td><i>수집</i> 예제를 실행. <b>인터넷이 있어야</b> 날씨·뉴스를 읽어 온다.</td></tr>
</tbody></table>

<div class="note"><b>수집 블록만 인터넷이 필요합니다</b>
위키백과·기상청·JTBC 뉴스를 직접 읽어 옵니다. 나머지 기능은 전부 로봇 안에서 돌기 때문에
인터넷이 없어도 됩니다.</div>

<h3>로봇에서 도는 것</h3>
<p>전부 로봇 자신이 띄웁니다. <code>&lt;ip&gt;</code> 는 가슴 화면의 주소로 바꿔 넣으세요.</p>
<table><thead><tr><th style="width:34%">주소</th><th>내용</th></tr></thead><tbody>
<tr><td><code>http://&lt;ip&gt;</code></td><td>블록 편집기(IDE). 평소 들어가는 곳.</td></tr>
<tr><td><code>http://&lt;ip&gt;:8080</code></td><td>참고 문서. 편집기의 Guide 버튼과 같은 곳.</td></tr>
<tr><td><code>http://&lt;ip&gt;:50000</code></td><td>도구 — 동작 편집기와 녹음기.</td></tr>
<tr><td><code>http://&lt;ip&gt;:50010</code></td><td>분류기 — 이미지 학습.</td></tr>
<tr><td><code>http://&lt;ip&gt;:50020</code></td><td>언어모델 서버.</td></tr>
</tbody></table>
<p>도구·분류기·언어모델은 주소를 직접 치지 말고 편집기의 버튼으로 여세요. 셋 중 하나만
동시에 돌 수 있고, 전환은 편집기가 알아서 합니다.</p>
</section>''')

    # 6
    W('''<section class="page"><h2>6 &nbsp; 다른 네트워크로 연결하기</h2>
<p class="lead">로봇을 <code>pibo</code> 가 아닌 네트워크에 붙여야 할 때만 필요합니다 —
학교 네트워크를 직접 쓰거나, 공장초기화 후 공유기가 없는 경우입니다.
<b>로봇마다 따로</b> 해야 합니다.</p>

<ol>
<li>로봇을 켜고 1분쯤 기다립니다. <code>pibo</code> 가 없으면 자기 WiFi 를 켭니다.</li>
<li>태블릿이나 노트북에서 <code>pibo-</code> + 가슴 화면의 <b>SN</b> 네트워크에 접속합니다.
비밀번호는 <code>!pibo0314</code> 입니다.</li>
<li>브라우저에서 <code>http://192.168.34.1</code> 을 엽니다.</li>
<li><b>인터넷 설정</b>에서 목록의 네트워크를 고르고 비밀번호를 넣어 확인합니다.</li>
<li>로봇이 스스로 재시작합니다. 1분쯤 뒤 가슴 화면에 새 네트워크의 주소가 뜹니다.</li>
<li>태블릿을 그 네트워크로 옮겨 주소를 열어 확인합니다.</li>
</ol>''')
    W(wifi_dialog())
    W('''<div class="dcap">블록 편집기의 인터넷 설정 화면</div>
<div class="note"><b>원하는 네트워크가 목록에 없으면</b>
목록에는 로봇이 실제로 쓸 수 있는 네트워크만 나옵니다. WPA3 를 쓰는 네트워크는 나오지
않습니다. 이름에 공백이 있는 것은 정상 처리됩니다. 맨 아래 <b>수동 연결</b>로 숨긴
네트워크와 WPA-Enterprise(아이디까지 필요)를 처리합니다.</div>

<div class="note warn"><b>확인을 누르면 로봇이 재시작합니다</b>
그 로봇으로 수업 중인 사람이 없는지 확인하세요.</div>

<h3>다시 <code>pibo</code> 로 돌리기</h3>
<p>같은 절차로 <code>pibo</code> 를 고르면 됩니다. 공장초기화(7장)를 해도 WiFi 설정이
<code>pibo</code> 로 돌아갑니다.</p></section>''')

    # 7
    W('''<section class="page"><h2>7 &nbsp; 공장초기화</h2>
<p class="lead">블록 편집기 안에 있습니다. 반을 넘길 때 쓸 만하지만, 생각보다 많은 것을
지우고 되돌릴 수 없습니다.</p>

<h3>무엇이 일어나나</h3>
<table><thead><tr><th style="width:40%">동작</th><th>결과</th></tr></thead><tbody>
<tr><td>저장한 프로그램 삭제</td><td>아이들이 그 로봇에 저장한 것이 전부 사라진다.</td></tr>
<tr><td>녹음·이미지·학습모델 삭제</td><td>직접 만든 동작, 녹음한 소리, 분류기 모델이 지워진다.</td></tr>
<tr><td>예제 프로그램 복원</td><td>기본 예제 11개가 새것으로 돌아온다.</td></tr>
<tr><td><b>WiFi 설정 초기화</b></td><td><code>pibo</code> 로 되돌아간다.</td></tr>
<tr><td><b>로봇 전원 종료</b></td><td>스스로 다시 켜지지 않는다.</td></tr>
</tbody></table>

<div class="note"><b><code>pibo</code> 공유기를 쓰고 있으면 문제없습니다</b>
WiFi 설정이 <code>pibo</code> 로 돌아가는데 그게 원래 쓰던 공유기이므로, 다시 켜면
알아서 붙습니다. 따로 해 줄 일이 없습니다.</div>

<div class="note warn"><b>다른 네트워크로 옮겨 놨다면 이야기가 다릅니다</b>
6장으로 학교 네트워크에 붙여 둔 로봇을 공장초기화하면 그 설정이 날아갑니다. AP 모드로
돌아오므로 6장을 다시 해야 합니다. 그런 경우라면 선생님이 임의로 공장초기화를 하지
않도록 알려 두세요.</div>

<h3>초기화 전에</h3>
<ol>
<li>로봇에 남길 것이 없는지 확인합니다 — 저장한 프로그램, 만든 동작, 학습한 모델.</li>
<li>초기화 후 어느 네트워크에 붙어야 하는지 확인합니다.</li>
<li>초기화하고 전원을 다시 켠 뒤, 가슴 화면에 주소가 뜨는지 확인합니다.</li>
</ol></section>''')

    # 8
    W('''<section class="page"><h2>8 &nbsp; 문제 해결</h2>
<table><thead><tr><th style="width:30%">증상</th><th>원인과 조치</th></tr></thead><tbody>

<tr><td><b>가슴 화면에 IP 가 안 뜬다</b></td>
<td><code>pibo</code> 를 못 찾아 AP 모드로 간 것입니다. 공유기가 켜져 있고 신호를 내보내는지
확인하세요. 그런데도 안 되면 로봇을 공유기 가까이 옮기고 재부팅합니다. 다른 로봇은
멀쩡한데 한 대만 그러면 그 로봇의 WiFi 설정이 바뀐 것일 수 있습니다 — 6장으로 다시 잡습니다.</td></tr>

<tr><td><b>로봇이 한꺼번에 다 끊겼다</b></td>
<td>거의 항상 공유기입니다. 전원을 확인하고, 5GHz 채널이 아직 고정인지, 모드가 11ac 인지
보세요 — 펌웨어 업데이트나 공유기 초기화가 이 값을 기본값으로 되돌립니다. 부록 A 대로
복구하고 로봇을 재부팅합니다.</td></tr>

<tr><td><b>같은 교실에서 어떤 건 붙고 어떤 건 안 붙는다</b></td>
<td>보통 한 공유기에 로봇이 너무 많거나, 몇 대가 거리 밖입니다. 공유기당 대수를 세어 보고
(권장 10대), 거리와 중간의 철제 가구를 확인하세요.</td></tr>

<tr><td><b>붙었다가 계속 끊긴다</b></td>
<td>먼저 <code>pibo</code> 를 방송하는 공유기가 근처에 또 있는지 확인하세요 — 같은 교실에
켜 둔 여분이거나 옆 교실 것입니다. 로봇이 둘 사이를 오가며 끊깁니다. 여분을 끄세요.
아니면 그 자리의 신호가 약한 것입니다.<br><br>
채널이 <b>자동</b>으로 되어 있어도 같은 증상이 납니다. DFS 대역(52~144)으로 옮겨가면
레이더 감지 때마다 채널이 바뀝니다. 36~48 이나 149~161 로 고정하세요.</td></tr>

<tr><td><b>붙었는데 편집기가 안 열린다</b></td>
<td>태블릿이 로봇과 같은 네트워크에 있는지, 주소가 가슴 화면과 같은지 확인하고
<b>Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;R</b> 로 강력 새로고침하세요.</td></tr>

<tr><td><b>카메라·동작 블록이 반응이 없다</b></td>
<td>도구나 분류기가 어딘가 열려 있어 하드웨어를 잡고 있습니다. 그 탭을 닫으세요.
편집기에서 프로그램을 한 번 실행해도 풀립니다.</td></tr>

<tr><td><b>수집 블록만 안 된다</b></td>
<td>공유기에 인터넷이 물려 있는지 확인하세요. 위키백과·기상청·뉴스는 바깥에서 읽어 오므로
인터넷이 필요한 유일한 기능입니다.</td></tr>

<tr><td><b>카메라 영상이 느리다</b></td>
<td>여러 로봇이 동시에 영상을 보내고 있습니다. 공유기당 로봇 수를 줄이거나, 절반은
카메라를 안 쓰는 예제를 하게 하세요.</td></tr>

<tr><td><b>로봇이 안 켜진다</b></td>
<td>전원 어댑터를 확인하세요. 전원이 들어가면 20초 안에 눈에 불이 들어오고 인사말이
나옵니다. 아무 반응이 없으면 A/S 가 필요합니다.</td></tr>
</tbody></table>

<div class="note"><b>문의할 때 보낼 것</b>
가슴 화면의 <b>SN</b>, 소프트웨어 버전, 가슴 화면에 뜬 내용, 그 공유기에 붙은 로봇 수,
한 대만 그런지 전부 그런지. 이 정도면 보통 방문 없이 답할 수 있습니다.</div></section>''')

    # 부록
    W(f'''<section class="page"><h2>부록 A &nbsp; 기본값과 주소</h2>

<h3>공유기 설정 — 초기화됐을 때 이대로 복구</h3>
<table><tbody>
<tr><th style="width:36%">5GHz 네트워크 이름</th><td><code>pibo</code></td></tr>
<tr><th>2.4GHz 네트워크 이름</th><td><code>pibo-24</code></td></tr>
<tr><th>비밀번호</th><td><code>!pibo0314</code></td></tr>
<tr><th>5GHz 채널</th><td>36·40·44·48 또는 149·153·157·161 중 하나로 <b>고정</b>
(자동 금지, DFS 52~144 금지)</td></tr>
<tr><th>2.4GHz 채널</th><td>1·6·11 중 하나로 고정</td></tr>
<tr><th>채널 대역폭</th><td>80MHz 이하</td></tr>
<tr><th>무선 모드</th><td>11ac — WiFi 6 / 11ax 끔</td></tr>
<tr><th>보안</th><td>WPA2-PSK (AES) — WPA3·혼합 아님</td></tr>
<tr><th>밴드 스티어링</th><td>끔</td></tr>
<tr><th>DHCP 풀</th><td>100개 이상</td></tr>
<tr><th>펌웨어 자동 업데이트</th><td>끔</td></tr>
</tbody></table>
<p style="font-size:9.5pt;color:#555">공유기의 설정 백업 파일을 하나 받아 두세요.
복원이 다시 입력하는 것보다 훨씬 빠릅니다.</p>

<h3>출하 시 로봇의 WiFi</h3>
<table><tbody>
<tr><th style="width:36%">찾는 네트워크</th><td><code>pibo</code> (5GHz)</td></tr>
<tr><th>비밀번호</th><td><code>!pibo0314</code></td></tr>
</tbody></table>

<h3>AP 모드</h3>
<table><tbody>
<tr><th style="width:36%">네트워크 이름</th><td><code>pibo-</code> + 가슴 화면의 SN</td></tr>
<tr><th>비밀번호</th><td><code>!pibo0314</code></td></tr>
<tr><th>로봇 주소</th><td><code>192.168.34.1</code></td></tr>
<tr><th>나눠주는 주소</th><td><code>192.168.34.10</code> – <code>192.168.34.50</code></td></tr>
<tr><th>대역</th><td>2.4GHz — 구형 노트북·USB 어댑터도 붙을 수 있게</td></tr>
</tbody></table>

<h3>로봇의 포트</h3>
<table><tbody>
<tr><th style="width:36%">80</th><td>블록 편집기</td></tr>
<tr><th>8080</th><td>참고 문서 (Guide 버튼)</td></tr>
<tr><th>50000</th><td>도구</td></tr>
<tr><th>50010</th><td>분류기</td></tr>
<tr><th>50020</th><td>언어모델</td></tr>
</tbody></table>

<h3>수용 규모</h3>
<table><tbody>
<tr><th style="width:36%">교실당 공유기</th><td><b>1대</b> — 같은 이름으로 두 대는 금지</td></tr>
<tr><th>공유기당 로봇</th><td>10대 권장</td></tr>
<tr><th>10대를 넘으면</th><td>교실을 나누고 각각 공유기 한 대, 신호가 겹치지 않을 만큼 떨어뜨린다</td></tr>
</tbody></table>

<div class="note warn" style="margin-top:14pt"><b>비밀번호는 모든 로봇·공유기가 같습니다</b>
위 값은 전 대수에 동일하게 출하됩니다. 아는 사람은 누구나 붙을 수 있습니다. 그대로 쓸지
바꿀지 기관과 정하고, 정한 값을 기록해 두세요. WiFi 비밀번호를 바꾸면 로봇을 전부 6장으로
다시 잡아야 하므로 설치 전에 정하세요.</div>

<p style="margin-top:20pt;font-size:9pt;color:#777;border-top:1pt solid #ccc;padding-top:8pt">
파이보 설치·관리 가이드 · Circulus Inc. · 소프트웨어 버전 {TAG} · 발행 {TODAY}</p>
</section>''')

    W('</body></html>')
    return o.getvalue()


if __name__ == '__main__':
    out = os.path.join(HERE, 'setup_guide_ko.html')
    open(out, 'w', encoding='utf-8').write(build())
    print('written', out)
