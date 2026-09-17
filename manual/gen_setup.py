#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Setup & Administration Guide — 공유기(AX53)를 pibo 로 세팅해 함께 납품하는 전제."""
import io, os, datetime, html

HERE = os.path.dirname(os.path.abspath(__file__))
TAG  = os.environ.get('MANUAL_TAG', '260915v1-ph').replace('origin/', '')
TODAY = datetime.date.today().isoformat()
esc = lambda s: html.escape(s, quote=False)

def shot(cap):
    return (f'<div class="shot"><div class="shot-i">SCREENSHOT</div>'
            f'<div class="shot-c">{esc(cap)}</div></div>')

def oled(sn='cd488e95', ip='192.168.114.138', ap='pibo'):
    return ('<div class="oled"><div class="oled-s">'
            f'<div>SN: {esc(sn)}</div><div>I P: {esc(ip)}</div><div>AP: {esc(ap)}</div>'
            '</div></div>')

def wifi_dialog():
    """IDE 의 Internet settings 팝업을 그린다."""
    rows = [('pibo', '100%'), ('pibo-24', '92%'), ('school-wifi', '78%')]
    tr = ''.join(f'<div class="w-row"><span class="w-ssid">{esc(s)}</span>'
                 f'<span class="w-meta">{g} &nbsp;\U0001f512 wpa-psk</span></div>' for s, g in rows)
    return f'''<div class="wdlg">
<div class="w-head"><b>Internet settings</b><span class="w-x">✕</span></div>
<div class="w-ip">192.168.114.138 / pibo</div>
<div class="w-sub">Available networks</div>
<div class="w-list">{tr}</div>
<div class="w-manual">Manual Connection / Other Network…</div>
</div>'''

CSS = '''
@page { size: A4; margin: 18mm 16mm 16mm 16mm; }
* { box-sizing: border-box; }
body { font: 10.5pt/1.55 "Helvetica Neue", Helvetica, Arial, sans-serif; color:#1a1a1a; margin:0; }
h1,h2,h3,h4 { line-height:1.25; }
h2 { font-size:15pt; margin:0 0 10pt; padding-bottom:5pt; border-bottom:2.5pt solid #1a1a1a; }
h3 { font-size:12pt; margin:15pt 0 5pt; break-after:avoid; page-break-after:avoid; }
h4 { font-size:10.5pt; margin:12pt 0 3pt; }
p  { margin:0 0 7pt; }
code { font:9.5pt ui-monospace,"SF Mono",Menlo,Consolas,monospace; background:#f0f0f0;
       padding:.5pt 3pt; border-radius:2pt; }
pre  { font:9pt/1.45 ui-monospace,Menlo,Consolas,monospace; background:#f4f4f4;
       border-left:3pt solid #999; padding:7pt 9pt; margin:6pt 0 9pt; white-space:pre-wrap;
       break-inside:avoid; }
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
.shot { border:1pt dashed #aaa; background:#fafafa; padding:14pt; text-align:center;
        margin:8pt 0 10pt; border-radius:3pt; }
.shot-i { font-size:8pt; letter-spacing:1.5pt; color:#999; font-weight:600; }
.shot-c { font-size:9pt; color:#666; margin-top:4pt; }
ol,ul { margin:0 0 8pt; padding-left:17pt; }
li { margin-bottom:3pt; }
.toc { font-size:11pt; }
.toc div { padding:3.5pt 0; border-bottom:.5pt dotted #ccc; }
.toc .n { display:inline-block; width:26pt; color:#888; }
.flow { border:.6pt solid #bbb; border-radius:3pt; padding:9pt 11pt; margin:8pt 0 10pt;
        font-size:10pt; background:#fbfbfb; break-inside:avoid; }
.flow .arrow { color:#999; margin:2pt 0 2pt 6pt; }
.oled { background:#111; border:2.5pt solid #444; border-radius:4pt; padding:7pt 9pt; }
.oled-s { font:11pt/1.5 ui-monospace,"SF Mono",Menlo,Consolas,monospace; color:#e8e8e8;
          min-height:50pt; }
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
    W(f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
      f'<title>Pibo Setup &amp; Administration</title><style>{CSS}</style></head><body>')

    # Cover
    W(f'''<section class="page cover"><div class="top">
<p class="k">Pibo</p><p class="k" style="font-size:26pt;font-weight:400">Setup &amp; Administration</p>
<p class="s">Robots, routers and the classroom network</p>
<div class="note" style="margin-top:24pt"><b>Who this is for</b>
The person who installs the robots and looks after them — not the teacher running the lesson.
Teachers should use the <i>Pibo Teacher’s Guide</i>.</div></div>
<div class="m"><b>Circulus Inc.</b> &nbsp;·&nbsp; Software version {TAG}
&nbsp;·&nbsp; Issued {TODAY}</div></section>''')

    # Contents
    W('<section class="page"><h2>Contents</h2><div class="toc">')
    for n, t in [('1','How Pibo joins a network'), ('2','The router supplied with the robots'),
                 ('3','Installing in a classroom'),
                 ('4','Preparing tablets and laptops'), ('5','Checking a robot'),
                 ('6','Connecting to a different network'), ('7','Factory reset'),
                 ('8','Troubleshooting'), ('A','Appendix A — Defaults and addresses')]:
        W(f'<div><span class="n">{n}</span>{esc(t)}</div>')
    W('</div>')
    W('''<div class="note" style="margin-top:18pt"><b>The short version</b>
The robots and the router are delivered already matched to each other. Plug the router in, switch the
robots on, and they connect by themselves. Sections 1 and 2 explain why, and what not to change.
</div>
<div class="note warn"><b>One router per room, ten robots</b>
Use a single router in each room, and plan for ten robots on it. Never put two routers with the
robot network in the same room — see section 3.</div></section>''')

    # 1. How Pibo joins
    W('''<section class="page"><h2>1 &nbsp; How Pibo joins a network</h2>
<p class="lead">Every robot leaves the factory set to join a 5&nbsp;GHz network called <code>pibo</code>,
and the router supplied with the robots is already configured to provide exactly that. Nothing has to
be matched up on site.</p>

<h3>At every start-up</h3>
<div class="flow">
<b>1.</b> Pibo looks for the Wi-Fi network stored in its settings — <code>pibo</code>.<br>
<div class="arrow">↓ found</div>
<b>2a.</b> It joins, receives an address, and shows that address on the chest screen. Ready to use.<br>
<div class="arrow">↓ not found</div>
<b>2b.</b> It starts a network of its own named <code>pibo-</code> plus the last eight characters of its
serial number — the same <b>SN</b> shown on the chest screen. This is called <b>AP mode</b>.
</div>
<p>The check repeats every ten seconds for as long as the robot is on. If the router is switched on
later, or comes back after a power cut, the robots join by themselves and shut their own networks
down. They do not need restarting.</p>

<h3>The chest screen</h3>''')
    W('<div class="oled-row">'
      '<div>' + oled() + '<div class="oled-cap">Connected — open the <b>I P</b> address in a browser</div></div>'
      '<div>' + oled(ip='', ap='') + '<div class="oled-cap">AP mode — the router was not found</div></div>'
      '</div>')
    W('''<p><b>SN</b> is the robot’s number, <b>I P</b> the address to open in a browser, and <b>AP</b> the
network it joined. An empty <b>I P</b> line means AP mode. The <b>SN</b> also tells you which
<code>pibo-…</code> network belongs to which robot, which matters when twenty of them are on at once.</p>

<div class="note warn"><b>AP mode means there is no internet</b>
A robot running its own network has no route to the outside world — it only has one radio, and it is
busy being an access point. This is expected behaviour, not a fault.</div></section>''')

    # 2. The router
    W('''<section class="page"><h2>2 &nbsp; The router supplied with the robots</h2>
<p class="lead">A TP-Link Archer AX53 is supplied, already configured. Plug in power, and if the school
has internet, plug the school’s cable into the router’s <b>WAN</b> (internet) port. Nothing else is
needed.</p>

<h3>What is already set</h3>
<table><thead><tr><th style="width:34%">Setting</th><th>Value</th></tr></thead><tbody>
<tr><td>5&nbsp;GHz network name</td><td><code>pibo</code> &nbsp;— the robots join this one</td></tr>
<tr><td>2.4&nbsp;GHz network name</td><td><code>pibo-24</code> &nbsp;— for tablets and older laptops</td></tr>
<tr><td>Password (both)</td><td><code>!pibo0314</code></td></tr>
<tr><td>5&nbsp;GHz channel</td><td>36, fixed</td></tr>
<tr><td>Channel width</td><td>80&nbsp;MHz</td></tr>
<tr><td>Wireless mode</td><td>11ac (Wi-Fi 6 / 11ax turned off)</td></tr>
<tr><td>Security</td><td>WPA2-PSK (AES)</td></tr>
<tr><td>Band steering (Smart Connect)</td><td>Off, so the two names stay separate</td></tr>
<tr><td>Automatic firmware update</td><td>Off</td></tr>
</tbody></table>

<div class="note warn"><b>Do not change the wireless settings</b>
Each value above is there for a reason, and several of them will stop the robots connecting if
changed. In particular: the channel must stay fixed rather than <i>Auto</i>, the mode must stay 11ac,
and the security must stay WPA2-PSK.<br><br>
Leave automatic firmware update switched off as well. An update can put the channel back to
<i>Auto</i>, which takes every robot in the room off the network at the same time.</div>

<h3>How many robots per router</h3>
<p><b>One router per room, and plan for ten robots on it.</b> The hardware can carry more, but ten
keeps the classroom comfortable: pictures from the camera keep flowing, and a room full of children
pressing <b>Run</b> at the same moment does not cause a queue.</p>
<p>Adding a second router to the same room does not help, and makes things worse — see section 3.</p>

<h3>Internet is optional</h3>
<p>Speech, vision, face recognition and the language model all run on the robot itself. If the school
has no internet, or its internet fails, the lesson is unaffected. Connect the school’s cable to the
<b>WAN</b> port when it is available — it is useful for the teacher’s tablet, not for the robots.</p>
</section>''')

    # 3. Installing
    W('''<section class="page"><h2>3 &nbsp; Installing in a classroom</h2>

<h3>Ten robots, one router</h3>
<ol>
<li>Place the router where it can be seen from most of the room, not inside a cupboard or behind a
metal cabinet.</li>
<li>Connect power. If the school has internet, connect its cable to the <b>WAN</b> port.</li>
<li>Wait about a minute, then check on a tablet that the networks <code>pibo</code> and
<code>pibo-24</code> are visible.</li>
<li>Switch the robots on, a few at a time.</li>
<li>After about a minute each chest screen shows an <b>I P</b> address. Write down the SN and IP of
each robot and give the list to the teacher.</li>
<li>Connect the tablets to <code>pibo-24</code> (or to <code>pibo</code> if they support 5&nbsp;GHz).</li>
</ol>

<h3>Never use two robot routers in one room</h3>
<div class="note warn"><b>Two routers with the same network name make the robots flap</b>
Both would broadcast <code>pibo</code>. Each robot then hears two of them, keeps deciding the other
one looks better, and moves back and forth all lesson — dropping its connection every time. This is
worse than having too many robots on a single router, and it is hard to diagnose because everything
looks correctly configured.<br><br>
<b>One room, one router.</b> Do not add a second, and do not bring a spare router into a room where
one is already running.</div>

<h3>More than ten robots at a school</h3>
<p>Split them between rooms, one router in each, and keep the rooms far enough apart that a robot in
one room cannot hear the other room’s router. A wall or two of separation is usually enough; check by
standing in one room with a tablet and looking at how strong the other <code>pibo</code> network
appears — if it does not show up at all, the separation is sufficient.</p>
<p>If the robots must all be in one room, keep them on the single router and expect the camera
examples to feel slower when every child runs one at the same moment. Having half the class work on
non-camera examples spreads the load.</p>

<h3>Where to put the robots</h3>
<p>Keep robots off the floor and away from metal shelving, and leave a clear space around each one so
it can move its arms and legs without hitting anything. Line of sight to the router gives the best
signal.</p></section>''')

    # 4. 태블릿·노트북 준비 — 인터넷 없는 망에서 OS 가 빠져나가는 문제
    W('''<section class="page"><h2>4 &nbsp; Preparing tablets and laptops</h2>
<p class="lead">The <code>pibo</code> network usually has no internet behind it. Windows, Android and
iPadOS all treat a network with no internet as a poor one and move away from it on their own \u2014 which
looks, to the teacher, like the robots disconnecting. A few minutes per device prevents this for good.</p>

<div class="note warn"><b>Why it happens</b>
Each of these systems checks whether a Wi-Fi network can actually reach the internet. When it cannot,
and another remembered network is within range, the device switches to that one instead, usually
without saying anything. The robots are still there; it is the tablet that left.</div>

<h3>The simplest fix: give the router internet</h3>
<p>If a school network cable can reach the classroom, connect it to the router\u2019s <b>WAN</b> port. The
<code>pibo</code> network then has internet like any other, nothing tries to leave it, and the rest of
this section becomes unnecessary. Try this first.</p>

<h3>Windows</h3>
<p>Windows rejoins any remembered network when it comes into range. Stop it joining anything but the
robot network.</p>
<ol>
<li>Open <b>Settings \u2192 Network &amp; internet \u2192 Wi-Fi \u2192 Manage known networks</b>.</li>
<li>For <b>every</b> network except <code>pibo</code> and <code>pibo-24</code>, open it and turn
<b>Connect automatically when in range</b> off. Networks that will never be used again can be removed
with <b>Forget</b>.</li>
<li>Open <code>pibo</code> or <code>pibo-24</code> and make sure <b>Connect automatically</b> is on.</li>
<li>If the laptop has mobile broadband or a tethered phone, switch it off during lessons.</li>
</ol>
<div class="note"><b>\u201cNo internet, secured\u201d is normal</b>
Windows labels the robot network this way and puts a warning mark on the Wi-Fi icon. The connection to
the robots works perfectly. Tell teachers to expect it \u2014 otherwise somebody will try to fix it by
switching networks, which is the very thing to avoid.</div>

<h3>Android tablets</h3>
<ol>
<li><b>Settings \u2192 Network &amp; internet \u2192 Internet</b>. Open the gear beside each saved network
other than the robot network and turn <b>Auto-connect</b> off, or forget it.</li>
<li>In the same screen open <b>Network preferences</b> and turn off <b>Switch to mobile data
automatically</b>. The wording varies slightly between manufacturers.</li>
<li>If the tablet has a SIM, simply turning mobile data off during the lesson is just as effective.</li>
<li>Android may ask <i>This network has no internet access. Stay connected?</i> \u2014 answer yes and tick
<b>Don\u2019t ask again for this network</b>.</li>
</ol>

<h3>iPad</h3>
<ol>
<li><b>Settings \u2192 Wi-Fi</b>. Tap the \u24d8 beside each other network and turn <b>Auto-Join</b> off.</li>
<li>Tap \u24d8 beside <code>pibo</code> and make sure <b>Auto-Join</b> is on.</li>
<li>On models with mobile data, turn <b>Settings \u2192 Mobile Data \u2192 Wi-Fi Assist</b> off.</li>
</ol>

<h3>Checking a device is ready</h3>
<ol>
<li>Connect it to <code>pibo</code> or <code>pibo-24</code>.</li>
<li>Open a robot\u2019s address in the browser and leave the page open for two or three minutes.</li>
<li>Still connected \u2014 the device is ready. Moved to another network \u2014 one auto-join setting was
missed.</li>
</ol>

<div class="note"><b>Do this once, before handing the devices over</b>
Preparing ten tablets on a table is far quicker than working out mid-lesson why one child\u2019s screen
keeps going blank. Put it on the installation checklist.</div>
</section>''')

    # 5. Checking
    W('''<section class="page"><h2>5 &nbsp; Checking a robot</h2>
<p class="lead">What to confirm before handing a robot over.</p>
<table><thead><tr><th style="width:30%">Check</th><th>Expected</th></tr></thead><tbody>
<tr><td>Chest screen</td><td>SN, an <b>I P</b> address, and <code>pibo</code> on the <b>AP</b> line.</td></tr>
<tr><td>Block editor</td><td>Opening the IP address in a browser shows the editor, in English.</td></tr>
<tr><td>A test program</td><td>Open the <i>Basic</i> example and run it. A line appears in the Terminal.</td></tr>
<tr><td>Sound</td><td>Open the <i>Speech</i> example and run it. The robot speaks.</td></tr>
<tr><td>Movement</td><td>Open the <i>Motion</i> example and run it, with space around the robot.</td></tr>
<tr><td>Camera</td><td>Open the <i>Face</i> example and run it. A picture appears in the IDE.</td></tr>
</tbody></table>

<h3>What runs on the robot</h3>
<p>Everything is served by the robot itself. Replace <code>&lt;ip&gt;</code> with the address on the chest
screen.</p>
<table><thead><tr><th style="width:34%">Address</th><th>What it is</th></tr></thead><tbody>
<tr><td><code>http://&lt;ip&gt;</code></td><td>Block editor (IDE). The normal way in.</td></tr>
<tr><td><code>http://&lt;ip&gt;:8080</code></td><td>Reference documentation, also reached from the Guide button.</td></tr>
<tr><td><code>http://&lt;ip&gt;:50000</code></td><td>Tools — motion editor and sound recorder.</td></tr>
<tr><td><code>http://&lt;ip&gt;:50010</code></td><td>Classifier — image model training.</td></tr>
<tr><td><code>http://&lt;ip&gt;:50020</code></td><td>Language model server.</td></tr>
</tbody></table>
<p>Open Tools, Classifier and the language model from the buttons in the editor rather than typing
the addresses — only one of the three may run at a time, and the editor handles the switching.</p>

<div class="note"><b>The documentation on the robot is in Korean</b>
The Guide button on port 8080 still serves the Korean reference text in this software version. Use the
printed <i>Teacher’s Guide</i> instead. An English version is planned for a later release.</div>
</section>''')

    # 5. Different network
    W('''<section class="page"><h2>6 &nbsp; Connecting to a different network</h2>
<p class="lead">Only needed if a robot has to join a network other than the supplied router — for
example a school network, or after a factory reset when the router is not available. It has to be done
on each robot separately.</p>

<ol>
<li>Switch the robot on and wait about a minute. With no <code>pibo</code> network present it starts its
own.</li>
<li>On a tablet or laptop, join the Wi-Fi network <code>pibo-</code> followed by the <b>SN</b> shown on the
chest screen. The password is <code>!pibo0314</code>.</li>
<li>Open <code>http://192.168.34.1</code> in a browser.</li>
<li>Open <b>Internet settings</b>, choose the network from the list, enter its password and confirm.</li>
<li>The robot restarts by itself. After about a minute the chest screen shows an address on the new
network.</li>
<li>Reconnect the tablet to that network and open the address to check.</li>
</ol>''')
    W(wifi_dialog())
    W('<div class="dcap">Internet settings, reached from the block editor</div>')
    W('''<div class="note"><b>If the network you want is not in the list</b>
The list only shows networks the robot can actually use. A 5&nbsp;GHz network on a high channel, or one
using WPA3, will not appear. Networks whose names contain spaces are handled correctly. <b>Manual
Connection</b> at the bottom covers hidden networks and WPA-Enterprise, which needs an identity as
well as a password.</div>

<div class="note warn"><b>Confirming restarts the robot</b>
Make sure nobody is in the middle of a lesson on that robot.</div>

<h3>Going back to the supplied router</h3>
<p>Set the Wi-Fi again by the same steps, choosing <code>pibo</code>. A factory reset (section 6) also
puts the setting back to <code>pibo</code>.</p></section>''')

    # 6. Factory reset
    W('''<section class="page"><h2>7 &nbsp; Factory reset</h2>
<p class="lead">Factory reset is in the block editor. It is useful when handing a robot to a new class,
but it does more than most people expect and cannot be undone.</p>

<h3>What it does</h3>
<table><thead><tr><th style="width:44%">Action</th><th>Effect</th></tr></thead><tbody>
<tr><td>Deletes saved programs</td><td>Everything children have saved on that robot is gone.</td></tr>
<tr><td>Deletes recordings, images and trained models</td><td>Custom motions, recorded sounds and any
Classifier model are removed.</td></tr>
<tr><td>Restores the example programs</td><td>The ten built-in examples are put back as new.</td></tr>
<tr><td><b>Resets the Wi-Fi setting</b></td><td>Back to <code>pibo</code>.</td></tr>
<tr><td><b>Switches the robot off</b></td><td>It does not restart by itself.</td></tr>
</tbody></table>

<div class="note"><b>With the supplied router this is harmless</b>
The Wi-Fi setting goes back to <code>pibo</code>, which is what the supplied router provides — so the
robot rejoins by itself when switched back on. Nothing needs to be set again.</div>

<div class="note warn"><b>But not if the robot was moved to another network</b>
If you pointed the robot at a school network using section 6, a factory reset throws that setting away.
The robot will come back in AP mode and section 6 has to be repeated. Tell teachers not to use factory
reset on their own in that case.</div>

<h3>Before resetting</h3>
<ol>
<li>Check nothing on the robot is worth keeping — saved programs, recorded motions, trained models.</li>
<li>Note which network the robot should be on afterwards.</li>
<li>Reset, then switch the robot back on and confirm the chest screen shows an address.</li>
</ol></section>''')

    # 7. Troubleshooting
    W('''<section class="page"><h2>8 &nbsp; Troubleshooting</h2>
<table><thead><tr><th style="width:32%">Symptom</th><th>Cause and remedy</th></tr></thead><tbody>

<tr><td><b>Chest screen shows no IP address</b></td>
<td>The robot did not find <code>pibo</code> and is in AP mode. Check the router is switched on and
broadcasting. If it is, move the robot closer and restart it. If one robot alone behaves this way while
the others are fine, its Wi-Fi setting may have been changed — set it again using section 6.</td></tr>

<tr><td><b>All the robots went offline at once</b></td>
<td>Almost always the router. Check it has power, and that the 5&nbsp;GHz channel is still fixed at 36
and the mode still 11ac — a firmware update or a factory reset of the router puts these back to
defaults. Restore the settings in Appendix A, then restart the robots.</td></tr>

<tr><td><b>Some robots connect, others do not, in the same room</b></td>
<td>Usually too many robots on one router, or one of them is out of range. Count how many are on the
router — ten is the recommended limit — and check the distance and any metal furniture in the way.</td></tr>

<tr><td><b>Robot connects, then drops repeatedly</b></td>
<td>First check whether a second router broadcasting <code>pibo</code> is within range — a spare one
left switched on in the same room, or one in an adjoining room. The robot will move between the two
and drop each time. Switch the extra one off. Otherwise the signal where the robot sits is too weak.</td></tr>

<tr><td><b>Connected, but the editor will not open</b></td>
<td>Check the tablet is on the same network as the robot, and that the address matches the chest
screen. Then force a reload with <b>Ctrl&nbsp;+&nbsp;Shift&nbsp;+&nbsp;R</b>.</td></tr>

<tr><td><b>Camera or motion blocks do nothing</b></td>
<td>Tools or Classifier is open somewhere and is holding the hardware. Close those tabs. Running any
program from the editor also releases them.</td></tr>

<tr><td><b>Pictures from the camera are slow</b></td>
<td>Several robots streaming video at once on a crowded router. Reduce the number of robots per
router, or have half the class work on non-camera examples.</td></tr>

<tr><td><b>Robot will not start</b></td>
<td>Check the power adapter. The eyes light and a greeting plays within about twenty seconds of power
being applied; if nothing happens at all, the robot needs service.</td></tr>
</tbody></table>

<div class="note"><b>What to send when reporting a problem</b>
The <b>SN</b> from the chest screen, the software version, what the chest screen shows, how many robots
are on that router, and whether the problem affects one robot or all of them. That is usually enough
to answer without a site visit.</div></section>''')

    # Appendix
    W(f'''<section class="page"><h2>Appendix A &nbsp; Defaults and addresses</h2>

<h3>Router settings — restore these if the router is reset</h3>
<table><tbody>
<tr><th style="width:38%">5&nbsp;GHz network name</th><td><code>pibo</code></td></tr>
<tr><th>2.4&nbsp;GHz network name</th><td><code>pibo-24</code></td></tr>
<tr><th>Password</th><td><code>!pibo0314</code></td></tr>
<tr><th>5&nbsp;GHz channel</th><td>36, fixed</td></tr>
<tr><th>2.4&nbsp;GHz channel</th><td>1, fixed</td></tr>
<tr><th>Channel width</th><td>80&nbsp;MHz</td></tr>
<tr><th>Wireless mode</th><td>11ac — Wi-Fi 6 / 11ax off</td></tr>
<tr><th>Security</th><td>WPA2-PSK (AES) — not WPA3 or mixed</td></tr>
<tr><th>Band steering</th><td>Off</td></tr>
<tr><th>DHCP pool</th><td>100 addresses or more</td></tr>
<tr><th>Automatic firmware update</th><td>Off</td></tr>
</tbody></table>
<p style="font-size:9.5pt;color:#555">Keep a settings backup file from the router’s own
backup / restore page. Restoring it is far quicker than re-entering everything.</p>

<h3>Wi-Fi as the robots are shipped</h3>
<table><tbody>
<tr><th style="width:38%">Network the robot looks for</th><td><code>pibo</code> (5&nbsp;GHz)</td></tr>
<tr><th>Password</th><td><code>!pibo0314</code></td></tr>
</tbody></table>

<h3>AP mode</h3>
<table><tbody>
<tr><th style="width:38%">Network name</th><td><code>pibo-</code> + the SN from the chest screen</td></tr>
<tr><th>Password</th><td><code>!pibo0314</code></td></tr>
<tr><th>Robot’s address</th><td><code>192.168.34.1</code></td></tr>
<tr><th>Addresses given out</th><td><code>192.168.34.10</code> – <code>192.168.34.50</code></td></tr>
<tr><th>Band</th><td>2.4&nbsp;GHz, so older laptops and USB adapters can connect</td></tr>
</tbody></table>

<h3>Ports on the robot</h3>
<table><tbody>
<tr><th style="width:38%">80</th><td>Block editor</td></tr>
<tr><th>8080</th><td>Reference documentation</td></tr>
<tr><th>50000</th><td>Tools</td></tr>
<tr><th>50010</th><td>Classifier</td></tr>
<tr><th>50020</th><td>Language model</td></tr>
</tbody></table>

<h3>Capacity</h3>
<table><tbody>
<tr><th style="width:38%">Routers per room</th><td><b>1</b> — never two with the robot network</td></tr>
<tr><th>Robots per router</th><td>10 recommended</td></tr>
<tr><th>More than 10 robots</th><td>Split between rooms, one router each, far enough apart that the
networks do not overlap</td></tr>
</tbody></table>

<div class="note warn" style="margin-top:14pt"><b>Passwords are the same on every robot and router</b>
The values above are shipped identically on all units. Anyone who knows them can join. Decide with the
school whether to keep them or set your own, and record whatever you choose. Changing the Wi-Fi
password means setting every robot again by section 6, so decide before installation rather than
after.</div>

<p style="margin-top:20pt;font-size:9pt;color:#777;border-top:1pt solid #ccc;padding-top:8pt">
Pibo Setup &amp; Administration · Circulus Inc. · software version {TAG} · issued {TODAY}</p>
</section>''')

    W('</body></html>')
    return o.getvalue()

if __name__ == '__main__':
    out = os.path.join(HERE, 'setup_guide.html')
    open(out, 'w', encoding='utf-8').write(build())
    print('written', out)
