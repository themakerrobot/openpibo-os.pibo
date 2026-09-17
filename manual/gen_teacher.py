#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Teacher's Guide 생성기 — 리포에서 뽑은 데이터 + 서술을 합쳐 HTML 로 만든다."""
import json, html, io, os, re, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get('MANUAL_DATA', HERE)      # build.sh 가 만든 작업 디렉토리
J = lambda n: json.load(open(os.path.join(DATA, n), encoding='utf-8'))

MSG  = J('msg.json')
CATS = J('cats.json')
MOTIONS = [m.strip() for m in open(os.path.join(DATA, 'motions.txt'), encoding='utf-8') if m.strip()]
MOTIONS = [m for m in MOTIONS if m not in ('name', 'options', 'type', 'field_dropdown')]

TAG = os.environ.get('MANUAL_TAG', '260915v1-ph').replace('origin/', '')

# 소스 툴팁의 오타. 인쇄물에는 고쳐 싣고, 원본은 별도로 보고한다.
TYPO = {
    'diretction': 'direction',
    'int the image': 'in the image',
    'objecs': 'objects',
    'Show QR in in the image.': 'Show QR codes in the image.',
    'Find QR in the image.': 'Find QR codes in the image.',
}

def fix(s):
    for a, b in TYPO.items():
        s = s.replace(a, b)
    return s

def label_of(t):
    m = MSG.get(t.upper())
    if not m:
        return None
    s = re.sub(r'%\{BKY_[A-Z0-9_]+\}', '', m)
    # 블록 라벨은 '%1 %2 ' 로 시작한다 — 아이콘과 빈 입력 자리라 화면에 글자가 없다.
    s = re.sub(r'^%1\s*%2\s*', '', s)
    s = re.sub(r'%\d+', '▢', s)            # 나머지는 입력 슬롯 하나하나
    s = re.sub(r'\[\s*▢\s*', '[', s)      # 'When [▢Run] clicked' 처럼 아이콘이 괄호 안에 든 경우
    s = re.sub(r'\s+', ' ', s).strip()
    return fix(s)

def tip_of(t):
    m = MSG.get(t.upper() + '_TOOLTIP')
    return fix(re.sub(r'\s+', ' ', m).strip()) if m else None

def esc(s):
    return html.escape(s, quote=False)

def slot(s):
    """▢ 를 입력 슬롯 표시로."""
    return esc(s).replace('▢', '<span class="slot"></span>')

# ─────────────────────────────────────────── 서술 데이터

STD_NOTE = {
 'Logic':  'Standard Blockly blocks. Comparisons, AND/OR, NOT, true/false and the if / else-if / else structure. The <b>null</b> block stands for \u201cno value\u201d.',
 'Loops':  'Standard Blockly blocks. Repeat a fixed number of times, repeat while a condition holds, count with a variable, walk through a list, and break / continue.',
 'Math':   'Standard Blockly blocks. Numbers, the four operations, rounding, remainders, random numbers, trigonometry and list arithmetic.',
 'Text':   'Standard Blockly blocks. Build, join, measure, search and edit text. <b>Print</b> writes a line to the Terminal at the bottom of the IDE.',
 'Lists':  'Standard Blockly blocks. Create lists, read and write items by position, take sub-lists, split text into a list, sort and reverse.',
 'Colour': 'Standard Blockly blocks. Pick a colour, make a random one, build one from red/green/blue values, or blend two colours. Colour blocks plug straight into the eye-LED blocks in <b>Device</b>.',
 'Variables': 'Blockly creates these blocks for you. Click <b>Create variable…</b>, give it a name, and the <i>set</i> and <i>get</i> blocks appear in this category.',
 'Functions': 'Blockly creates these blocks for you. Define a named block of code once, then call it from anywhere. Use it when the same steps repeat in several places.',
}

CAT_INTRO = {
 'Start':  'Every program begins with this block. Blocks that are not connected below it will not run.',
 'Audio':  'Play sound files and record from the microphone. Files live in the robot’s audio folder and appear in the file browser on the left of the IDE.',
 'Device': 'The eye LEDs and the sensors built into Pibo. The <i>Check…</i> blocks report a value, so plug them into a comparison or a <b>Print</b> block.',
 'Motion': 'Move the servo motors. Use a ready-made motion by name, run a motion you recorded yourself in <b>Tools</b>, or drive one motor at a time.',
 'Oled':   'Draw on the small screen on Pibo’s chest. Drawing blocks only prepare the picture — nothing appears until you use <b>Show OLED</b>.',
 'Speech': 'Make Pibo talk, and use the on-board language model. Two voices are available: the on-device voice (natural, handles English and Korean automatically) and the Espeak voice (robotic, very fast).',
 'Vision': 'Take pictures with the camera and edit them. Most blocks take an <i>image</i> and give back a changed image, so you normally store the result in a variable.',
 'Rec':    'Recognition — the AI blocks. Faces, objects, QR codes, hand gestures, body pose, markers, and your own image classifier trained in <b>Classifier</b>. All of it runs on the robot itself; no internet is needed.',
 'Utils':  'Small helpers that are not part of standard Blockly: waiting, the clock, dictionaries, type conversion and angle maths.',
}

CAT_FULL = {'Rec': 'Rec (Recognition)', 'Oled': 'OLED'}

EXAMPLES = [
 ('basic.json', 'Basic', 'Your first program. Prints a line of text, then shows how an <b>if / else</b> block chooses between two messages.',
  ['Print <i>Hello. I am Pibo.</i> to the Terminal.',
   'Ask whether <b>true</b> is true — it always is.',
   'Because the answer is yes, print <i>That’s right.</i> The <i>else</i> branch never runs.'],
  'Change <b>true</b> to <b>false</b> and run it again. Now the other message appears. This is the smallest possible demonstration of a decision in code.'),

 ('device.json', 'Device — sensors and eye LEDs', 'Turns the eye LEDs on, then loops forever reading the human-presence sensor and the touch sensor.',
  ['Print a title line.',
   'Turn both eye LEDs full white (255, 255, 255 on each side).',
   'Start a loop that repeats while <b>true</b> — that is, forever.',
   'Set both eyes to a random colour.',
   'If the presence sensor returns <i>person</i>, print <i>Human detected</i>.',
   'If the touch sensor returns <i>touch</i>, print <i>Touch detected</i>.',
   'Wait 0.5 seconds, then repeat.'],
  'The loop never ends by itself. Press <b>Stop</b> in the IDE to end it. Note how each sensor block is compared against a word using the <b>=</b> block from <b>Logic</b>.'),

 ('gugudan.json', 'Times table', 'Two nested loops print a multiplication table. No robot hardware is used, so it works as a pure programming lesson.',
  ['The outer loop counts <i>i</i> from 1 to 9.',
   'For each <i>i</i>, the inner loop counts <i>j</i> from 1 to 9.',
   'Print <i>i</i> × <i>j</i> = the product, joined into one line of text.'],
  'A good first look at nested loops. Ask the class to predict how many lines will be printed before running it.'),

 ('motion.json', 'Motion', 'Lists the motions the robot knows, then performs one.',
  ['Print a title line.',
   'Print the result of <b>Get motion list</b> — every motion name the robot can perform.',
   'Run the motion <i>wave1</i> once.'],
  'Replace <i>wave1</i> with any name from the printed list. The full list is also in Appendix B. Make sure Pibo has room to move before running motion blocks.'),

 ('speech_tts.json', 'Speech — text to speech', 'Says the same sentence with each of the two voices so the class can hear the difference.',
  ['Say a sentence with the on-device voice <i>m1</i> at volume 80.',
   'Wait 3 seconds.',
   'Say a sentence with the Espeak voice at volume 80.'],
  'The on-device voice sounds natural and detects the language automatically. Espeak is robotic but starts instantly. Voice codes are listed in Appendix C.'),

 ('vision_face1.json', 'Face — direction and distance', 'Watches through the camera and reacts when someone comes close.',
  ['Take a picture and store it in <i>image</i>.',
   'Analyse face direction and distance; store the list in <i>resultList</i>.',
   'For each face found, read the <i>distance</i> value from the result.',
   'If the distance is under 40, flash the eyes a random colour and write <i>Hello!!</i> onto the picture.',
   'Draw the analysis onto the picture and show it in the IDE.',
   'Wait 0.1 s and repeat.'],
  'The live picture appears in the image panel of the IDE. Try changing 40 to a larger number so Pibo greets people from further away.'),

 ('vision_face2.json', 'Face — age, gender, emotion', 'Finds every face in the camera view and labels it.',
  ['Take a picture and store it in <i>image</i>.',
   'Find all faces; store them in <i>faceList</i>.',
   'For each face, analyse age, gender and emotion, and draw the result on the picture.',
   'Draw boxes around all the faces.',
   'Show the picture in the IDE, wait 0.1 s and repeat.'],
  'Estimates are approximate and will sometimes be wrong — that is worth discussing with the class rather than hiding.'),

 ('vision_hand.json', 'Hand gestures', 'Recognises seven hand signs from the camera.',
  ['Print the seven gestures the model knows.',
   'Load the hand-gesture model.',
   'Take a picture, recognise the gesture, draw the result on the picture.',
   'Show the picture in the IDE, wait 0.1 s and repeat.'],
  'The seven signs are Closed Fist, Open Palm, Pointing Up, Thumb Down, Thumb Up, Victory and I Love You. Hold your hand still and well lit.'),

 ('vision_marker.json', 'Markers', 'Detects printed ArUco markers and measures them.',
  ['Take a picture.',
   'Detect markers, told that each printed marker is 8.5 cm across.',
   'Draw the markers on the picture and show it in the IDE.'],
  'The 8.5 number must match the real printed size, otherwise the distance readings are wrong. Print the markers at a known size and measure one with a ruler.'),

 ('vision_object.json', 'Objects and QR codes', 'Recognises everyday objects and reads QR codes at the same time.',
  ['Take a picture.',
   'Find objects in it; store the raw result.',
   'Find QR codes in it; store the raw result.',
   'Draw both results on the picture and show it in the IDE.'],
  'Print a few QR codes beforehand. Objects are recognised from a fixed list — if something is not recognised, that is a limit of the model, not a fault.'),
]

MOTORS = [('0','Right foot','± 25°'), ('1','Right leg','± 35°'), ('2','Right arm','± 80°'),
          ('3','Right hand','± 30°'), ('4','Neck (pan)','± 50°'), ('5','Head (tilt)','± 25°'),
          ('6','Left foot','± 25°'), ('7','Left leg','± 35°'), ('8','Left arm','± 80°'),
          ('9','Left hand','± 30°')]

VOICES = [('m1','k0'),('m2','k1'),('m3','k2'),('m4','k3'),('m5','k4'),
          ('f1','k5'),('f2','k6'),('f3','k7'),('f4','k8'),('f5','k9')]

TROUBLE = [
 ('The chest screen shows no IP address', 'Pibo could not find the classroom Wi-Fi, so it has started a network of its own named <code>pibo-</code> followed by the <b>SN</b> shown on the chest screen. This is an administrator job rather than a classroom one — report the robot instead of trying to fix it during a lesson.'),
 ('The IDE page will not open', 'Check that the tablet is on the same network as the robot. Then reload with <b>Ctrl + Shift + R</b> — an ordinary reload can serve an old cached page.'),
 ('The tablet keeps dropping the robots', 'The robot network normally has no internet, and tablets and laptops try to leave a network that has none. The tablet has moved to another Wi-Fi network by itself. Reconnect it to <code>pibo</code>, and ask your administrator to turn off automatic joining for the other networks — it is a one-off setting per device.'),
 ('Windows says “No internet, secured”', 'That is normal and nothing is wrong. Everything in the lesson runs on the robot itself, so no internet is needed. Do not switch to another network to make the warning go away.'),
 ('Code runs but Pibo does nothing', 'Blocks must be attached under <b>When Run clicked</b>. A stack sitting loose on the canvas is ignored.'),
 ('A motion block does nothing', 'Check the spelling of the motion name against <b>Get motion list</b>, and make sure nothing is blocking the robot’s arms or legs.'),
 ('The camera image is frozen', 'Only one tool may use the camera at a time. Close the <b>Classifier</b> and <b>Tools</b> tabs, then run your program again.'),
 ('Sound is too quiet or too loud', 'Every speech and audio block has a volume input. 80 is a good classroom level.'),
 ('A program will not stop', 'Loops that repeat <i>while true</i> run forever by design. Press <b>Stop</b> in the IDE.'),
 ('I want to start over', 'Factory reset puts the example files back and deletes saved work, recordings and trained models. It <b>also resets the Wi-Fi setting and switches the robot off</b>, so unless your network is named <code>pibo</code> somebody will have to set the Wi-Fi again before the robot can be used. Ask whoever set the robots up before using it.'),
]

# ─────────────────────────────────────────── HTML

def blocks_table(cat):
    rows = []
    for t in cat['blocks']:
        lab = label_of(t)
        if not lab:
            continue
        tip = tip_of(t) or ''
        rows.append(f'<tr><td class="bl">{slot(lab)}</td><td class="bd">{esc(tip)}</td></tr>')
    if not rows:
        return ''
    return ('<table class="blocks"><thead><tr><th>Block</th><th>What it does</th></tr></thead>'
            '<tbody>' + ''.join(rows) + '</tbody></table>')


# ── 사진: docx 로 받은 것을 캡션에 매핑. 자체 포함 HTML 이 되게 base64 로 넣는다.
import base64
IMG = {
 'Pibo robot, front view': 'image1.jpg',
 'IDE main screen, with the toolbox, canvas, terminal and toolbar marked': 'image2.jpg',
 'IDE canvas with basic.json loaded': 'image3.jpg',
 'IDE canvas with device.json loaded': 'image4.jpg',
 'IDE canvas with gugudan.json loaded': 'image5.jpg',
 'IDE canvas with motion.json loaded': 'image6.jpg',
 'IDE canvas with speech_tts.json loaded': 'image7.jpg',
 'IDE canvas with vision_face1.json loaded': 'image8.jpg',
 'IDE canvas with vision_face2.json loaded': 'image9.jpg',
 'IDE canvas with vision_hand.json loaded': 'image10.jpg',
 'IDE canvas with vision_marker.json loaded': 'image11.jpg',
 'IDE canvas with vision_object.json loaded': 'image12.jpg',
 'Tools \u2014 motion editor': 'image13.jpg',
 'Classifier \u2014 training screen': 'image16.jpg',
}
_cache = {}
def data_uri(fn):
    if fn not in _cache:
        with open(os.path.join(HERE, 'img', fn), 'rb') as f:
            _cache[fn] = 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode()
    return _cache[fn]

def oled(sn='cd488e95', ip='192.168.114.138', ap='pibo'):
    return ('<div class="oled"><div class="oled-s">'
            f'<div>SN: {esc(sn)}</div><div>I P: {esc(ip)}</div><div>AP: {esc(ap)}</div>'
            '</div></div>')

def shot(cap):
    fn = IMG.get(cap)
    if fn:
        return (f'<figure class="fig"><img src="{data_uri(fn)}" alt="">'
                f'<figcaption>{esc(cap)}</figcaption></figure>')
    return f'<div class="shot"><div class="shot-i">SCREENSHOT</div><div class="shot-c">{esc(cap)}</div></div>'

def build():
    o = io.StringIO()
    W = o.write
    today = datetime.date.today().isoformat()

    W(f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Pibo Teacher's Guide</title><style>
@page {{ size: A4; margin: 18mm 16mm 16mm 16mm; }}
* {{ box-sizing: border-box; }}
body {{ font: 10.5pt/1.55 "Helvetica Neue", Helvetica, Arial, sans-serif; color:#1a1a1a; margin:0; }}
h1,h2,h3,h4 {{ line-height:1.25; }}
h1 {{ font-size:22pt; margin:0 0 6pt; letter-spacing:-.3pt; }}
h2 {{ font-size:15pt; margin:0 0 10pt; padding-bottom:5pt; border-bottom:2.5pt solid #1a1a1a; }}
h3 {{ font-size:12pt; margin:15pt 0 5pt; break-after:avoid; page-break-after:avoid; }}
thead {{ display:table-header-group; }}
tr {{ break-inside:avoid; }}
h4 {{ font-size:10.5pt; margin:12pt 0 3pt; }}
p  {{ margin:0 0 7pt; }}
code {{ font:9.5pt ui-monospace,"SF Mono",Menlo,Consolas,monospace; background:#f0f0f0;
        padding:.5pt 3pt; border-radius:2pt; }}
.page {{ page-break-after: always; }}
.page:last-child {{ page-break-after: auto; }}
.cover {{ height:245mm; display:flex; flex-direction:column; }}
.cover .top {{ margin-top:52mm; }}
.cover .k {{ font-size:34pt; font-weight:700; letter-spacing:-1pt; margin:0; }}
.cover .s {{ font-size:14pt; color:#555; margin:6pt 0 0; }}
.cover-img {{ width:74%; margin:20pt auto 0; display:block; }}
.cover .m {{ margin-top:auto; font-size:9pt; color:#666; border-top:1pt solid #ccc; padding-top:8pt; }}
.lead {{ font-size:11pt; color:#444; margin-bottom:12pt; }}
table {{ border-collapse:collapse; width:100%; margin:6pt 0 10pt; font-size:9.5pt; }}
th,td {{ border:.6pt solid #bbb; padding:3.5pt 5pt; text-align:left; vertical-align:top; }}
th {{ background:#ececec; font-weight:600; }}
table.blocks td.bl {{ width:47%; }}
table.blocks td.bd {{ color:#333; }}
.slot {{ display:inline-block; width:15pt; height:8.5pt; border:.8pt solid #999;
         border-radius:2pt; background:#fafafa; vertical-align:-1pt; margin:0 1.5pt; }}
.fig {{ margin:8pt 0 10pt; break-inside:avoid; }}
.fig img {{ width:100%; border:.6pt solid #ccc; border-radius:2pt; display:block; }}
.fig figcaption {{ font-size:8.5pt; color:#666; margin-top:3pt; }}
.oled {{ background:#111; border:2.5pt solid #444; border-radius:4pt; padding:7pt 9pt; }}
.oled-s {{ font:11pt/1.5 ui-monospace,"SF Mono",Menlo,Consolas,monospace; color:#e8e8e8;
          min-height:50pt; }}
.oled-cap {{ text-align:center; font-size:8.5pt; color:#666; margin-top:3pt; }}
.oled-row {{ display:flex; gap:12pt; margin:10pt 0 12pt; break-inside:avoid; }}
.oled-row > div {{ flex:1; }}
.shot {{ border:1pt dashed #aaa; background:#fafafa; padding:14pt; text-align:center;
         margin:8pt 0 10pt; border-radius:3pt; }}
.shot-i {{ font-size:8pt; letter-spacing:1.5pt; color:#999; font-weight:600; }}
.shot-c {{ font-size:9pt; color:#666; margin-top:4pt; }}
.note {{ border-left:3pt solid #666; background:#f6f6f6; padding:7pt 10pt; margin:9pt 0; font-size:10pt; }}
.note b:first-child {{ display:block; margin-bottom:2pt; }}
ol,ul {{ margin:0 0 8pt; padding-left:17pt; }}
li {{ margin-bottom:2.5pt; }}
.toc {{ font-size:11pt; }}
.toc div {{ padding:3.5pt 0; border-bottom:.5pt dotted #ccc; }}
.toc .n {{ display:inline-block; width:26pt; color:#888; }}
.cols {{ column-count:4; column-gap:12pt; font-size:9pt; }}
.cols div {{ break-inside:avoid; padding:1pt 0; }}
.cat-intro {{ font-size:10pt; color:#333; margin-bottom:8pt; }}
.avoid {{ break-inside:avoid; }}
.ex h3 {{ margin-top:0; }}
.ex .file {{ font:9pt ui-monospace,Menlo,monospace; color:#777; margin-bottom:6pt; }}
</style></head><body>''')

    # ── Cover
    W(f'''<section class="page cover"><div class="top">
<p class="k">Pibo</p><p class="k" style="font-size:26pt;font-weight:400">Teacher’s Guide</p>
<p class="s">Block coding with the Pibo robot</p>
<img class="cover-img" src="{data_uri('image1.jpg')}" alt=""></div>
<div class="m"><b>Circulus Inc.</b> &nbsp;·&nbsp; Software version {TAG}
&nbsp;·&nbsp; Issued {today}</div></section>''')

    # ── Contents
    W('<section class="page"><h2>Contents</h2><div class="toc">')
    toc = [('1','Before the first lesson'), ('2','Getting started with the IDE'),
           ('3','Block reference'), ('4','The ten built-in examples'),
           ('5','Tools and Classifier'), ('6','When something goes wrong'),
           ('A','Appendix A — Motors'), ('B','Appendix B — Motion names'),
           ('C','Appendix C — Voices')]
    for n, t in toc:
        W(f'<div><span class="n">{n}</span>{esc(t)}</div>')
    W('</div>')
    W('''<div class="note" style="margin-top:20pt"><b>How to use this guide</b>
Sections 1 and 2 are worth reading once before your first lesson. Section 3 is a reference — look
things up rather than reading it through. Section 4 walks through the ten programs that are already
on the robot, and is the fastest way to prepare a lesson.</div>''')
    W('</section>')

    # ── 1. Before the first lesson
    W('''<section class="page"><h2>1 &nbsp; Before the first lesson</h2>
<p class="lead">Pibo is a small robot that children program by joining coloured blocks together on a
screen. No typing is needed, and no internet connection is required — everything runs on the robot.</p>

<h3>What you need</h3>
<ul>
<li>A Pibo robot, charged or on its power adapter.</li>
<li>A tablet or laptop with a web browser. Chrome is recommended.</li>
<li>The classroom Wi-Fi router, switched on.</li>
</ul>

<h3>Turning Pibo on</h3>
<ol>
<li>Connect the power adapter, or press the power button if the robot is charged.</li>
<li>Pibo’s eyes light up and it greets you. Starting up takes about a minute.</li>
<li>When the eyes settle and the chest screen shows an address, Pibo is ready.</li>
</ol>
<div class="note"><b>Read the address from the chest screen</b>
The chest screen shows three lines: <b>SN</b> (this robot’s number), <b>I P</b> (the address to type
into the browser) and <b>AP</b> (the Wi-Fi network it joined). Each robot has its own address, so read
the screen of the robot in front of you rather than reusing a number from another lesson.
<br><br>If the <b>I P</b> line is empty, the robot did not find the Wi-Fi network — see section 6.</div>''')
    W('<div class="oled-row">'
      '<div>' + oled() + '<div class="oled-cap">Connected — open the <b>I P</b> address</div></div>'
      '<div>' + oled(ip='', ap='') + '<div class="oled-cap">Not connected — see section 6</div></div>'
      '</div>')
    W('''<h3>Opening the IDE</h3>
<p>Type the address from the chest screen into the browser and press Enter. The block editor opens.
Nothing needs to be installed.</p>

<div class="note"><b>If the address does not work</b>
Check that the tablet is connected to the same Wi-Fi network as the robot. If there is a network
whose name begins with <code>pibo-</code>, see section 6 — the robot has not joined the classroom
network and needs its Wi-Fi set again.</div>

<h3>One robot, one tablet</h3>
<p>Two tablets can open the same robot, but they share one workspace — what one child changes,
the other sees. For group work this is useful; for individual work give each child their own robot.</p>
</section>''')

    # ── 2. Getting started
    W('''<section class="page"><h2>2 &nbsp; Getting started with the IDE</h2>''')
    W(shot('IDE main screen, with the toolbox, canvas, terminal and toolbar marked'))
    W('''<h3>The screen</h3>
<table><tbody>
<tr><th style="width:22%">Toolbox</th><td>Down the left. Click a category to open its blocks, then drag
one onto the canvas.</td></tr>
<tr><th>Canvas</th><td>The middle. Join blocks here. Drag a block away to detach it; drag it to the
bin, or press Delete, to remove it.</td></tr>
<tr><th>Terminal</th><td>Along the bottom. Everything a <b>Print</b> block writes appears here, and so
do error messages.</td></tr>
<tr><th>Image panel</th><td>Shows pictures sent by <b>Display image variable on IDE</b>. Used by all the
camera examples.</td></tr>
<tr><th>Toolbar</th><td>Top right — run, stop, save, open, and the other tools.</td></tr>
</tbody></table>

<h3>Writing and running a program</h3>
<ol>
<li>Open the <b>Start</b> category and drag <b>When Run clicked</b> onto the canvas.</li>
<li>Add blocks underneath it. They click together like jigsaw pieces.</li>
<li>Press <b>Run</b>. Watch the Terminal for printed output.</li>
<li>Press <b>Stop</b> to end a program that is still running.</li>
</ol>
<div class="note"><b>Blocks must be connected</b>
Only blocks joined under <b>When Run clicked</b> will run. A stack left loose on the canvas is
ignored — this is the most common reason a program “does nothing”.</div>

<h3>Saving and opening</h3>
<p>Use <b>Save</b> on the toolbar to keep a program on the robot, and <b>Open</b> to load it again or to
load one of the ten examples. Files are stored on the robot, not on the tablet, so a child returning
to the same robot finds their work waiting.</p>

<h3>Changing the language</h3>
<p>The language selector is in the IDE. Block names, menus and messages switch immediately; your
blocks are not affected.</p>
</section>''')

    # ── 3. Block reference
    W('''<section class="page"><h2>3 &nbsp; Block reference</h2>
<p class="lead">Every block in the toolbox, in the order the categories appear. The wording matches
the English interface exactly, so you can search for a block by reading it here.</p>
<p>A grey box <span class="slot"></span> marks a place where something is filled in — a number, a piece
of text, a colour, or another block plugged in.</p>
<div class="note"><b>Standard blocks and Pibo blocks</b>
The first eight categories are the standard Blockly blocks used in most block-coding tools. The rest
— Audio, Device, Motion, OLED, Speech, Vision, Rec and Utils — control the robot itself.</div>''')

    for cat in CATS:
        name = cat['name']
        title = CAT_FULL.get(name, name)
        tbl = blocks_table(cat)
        W(f'<h3>{esc(title)}</h3>')
        if name in CAT_INTRO:
            W(f'<p class="cat-intro">{CAT_INTRO[name]}</p>')
        if name in STD_NOTE:
            W(f'<p class="cat-intro">{STD_NOTE[name]}</p>')
        if tbl and name not in STD_NOTE:
            W(tbl)
        elif name not in STD_NOTE:
            W('<p class="cat-intro">No blocks in this category.</p>')
        if name == 'Motion':
            W('<p style="font-size:9.5pt;color:#555">Motion names are listed in Appendix B; '
              'motor numbers and their limits in Appendix A.</p>')
        if name == 'Speech':
            W('<p style="font-size:9.5pt;color:#555">Voice codes are listed in Appendix C.</p>')
    W('</section>')

    # ── 4. Examples
    W('''<section class="page"><h2>4 &nbsp; The ten built-in examples</h2>
<p class="lead">These ten programs are already on every robot. Open them with <b>Open</b> on the
toolbar. They are the quickest way to prepare a lesson: run one, read it together, then change one
number and run it again.</p>
<table><thead><tr><th style="width:34%">Example</th><th>Teaches</th></tr></thead><tbody>''')
    teach = ['printing, if / else', 'sensors, loops, LEDs', 'nested loops, variables',
             'calling robot motions', 'text to speech, two voices', 'camera loop, dictionaries',
             'face analysis, lists', 'a loaded AI model', 'measurement from a camera',
             'two recognisers at once']
    for (f, t, _, _, _), tc in zip(EXAMPLES, teach):
        W(f'<tr><td><b>{esc(t)}</b></td><td>{esc(tc)}</td></tr>')
    W('</tbody></table>')
    W('''<div class="note"><b>A lesson shape that works</b>
Run the example first without explaining it, and let the class see what it does. Then open the blocks
and read them together. Then change exactly one thing — a number, a word, a colour — and run it
again. Children remember the change far better than the explanation.</div></section>''')

    for fn, title, summ, steps, note in EXAMPLES:
        W('<section class="page ex">')
        W(f'<h3>{title}</h3><div class="file">{esc(fn)}</div>')
        W(f'<p class="lead">{summ}</p>')
        W(shot(f'IDE canvas with {fn} loaded'))
        W('<h4>What the blocks do</h4><ol>')
        for s in steps:
            W(f'<li>{s}</li>')
        W('</ol>')
        W(f'<div class="note"><b>In the classroom</b>{note}</div>')
        W('</section>')

    # ── 5. Tools & Classifier
    W('''<section class="page"><h2>5 &nbsp; Tools and Classifier</h2>
<p class="lead">Two extra programs open from the IDE toolbar. Each one takes over the robot while it
is open, so close the tab when you have finished.</p>

<h3>Tools</h3>
<p>Used to record things the block editor then plays back.</p>
<ul>
<li><b>Motion</b> — pose the robot by hand or with sliders, capture each pose, and save the sequence
as your own motion. It then appears in the <b>Execute my motion</b> block.</li>
<li><b>Wait until it is ready.</b> When Tools opens, the motor button reads <b>OFF</b> for about twenty
seconds while the robot prepares itself. Begin once it turns to <b>ON</b>.</li>
<li><b>Recording</b> — record a sound through the microphone and save it as a file, which the
<b>Play audio</b> block can then use.</li>
</ul>''')
    W(shot('Tools — motion editor'))
    W('''<h3>Classifier</h3>
<p>Trains the robot to tell apart categories of pictures that you choose — for example three kinds
of fruit, or tidy versus untidy desks.</p>
<ol>
<li>Create a category and give it a name.</li>
<li>Hold an object in front of the camera and capture a number of images. Twenty or more per
category works well.</li>
<li>Repeat for each category.</li>
<li>Train, then test by holding up an object.</li>
</ol>
<p>Once trained, the model is used from the block editor with <b>Set My Image model</b> followed by
<b>Classify image using My Image model</b>, in the <b>Rec</b> category.</p>''')
    W(shot('Classifier — training screen'))
    W('''<div class="note"><b>Close the tab when you finish</b>
Tools and Classifier each hold the camera and the motors. If a camera block seems frozen, or motion
blocks do nothing, a Tools or Classifier tab is probably still open somewhere.</div></section>''')

    # ── 6. Troubleshooting
    W('<section class="page"><h2>6 &nbsp; When something goes wrong</h2>'
      '<table><thead><tr><th style="width:33%">Symptom</th><th>What to do</th></tr></thead><tbody>')
    for s, a in TROUBLE:
        W(f'<tr><td><b>{esc(s)}</b></td><td>{a}</td></tr>')
    W('</tbody></table>')
    W('''<div class="note"><b>Before calling for help</b>
Note the serial number shown at the bottom of the IDE, what you were doing, and anything printed in
red in the Terminal. That is usually enough to identify the problem without visiting the classroom.</div>
</section>''')

    # ── Appendices
    W('<section class="page"><h2>Appendix A &nbsp; Motors</h2>'
      '<p class="lead">Motor numbers used by <b>Move motor by degrees</b>, and how far each one turns. '
      'Left and right are Pibo’s own left and right, not yours.</p>'
      '<table><thead><tr><th style="width:14%">No.</th><th style="width:46%">Position</th>'
      '<th>Range</th></tr></thead><tbody>')
    for n, p, r in MOTORS:
        W(f'<tr><td>{n}</td><td>{esc(p)}</td><td>{esc(r)}</td></tr>')
    W('</tbody></table>')
    W('''<div class="note"><b>Stay inside the range</b>
Asking a motor to go past its limit strains it and can make the robot fall over. Keep a clear space
around Pibo whenever motion blocks are running.</div>''')

    W("</section>")

    # Appendix B — 모션 이름
    W('<section class="page"><h2>Appendix B &nbsp; Motion names</h2>'
      '<p class="lead">Names accepted by <b>Execute motion</b>. The robot can also list them at run '
      'time with <b>Get motion list</b>.</p><div class="cols">')
    for m in sorted(MOTIONS):
        W(f'<div>{esc(m)}</div>')
    W('</div>')
    W('<div class="note" style="margin-top:14pt"><b>Motions you record yourself</b>'
      'Motions made in <b>Tools</b> are not in this list. Use <b>Execute my motion</b> for those, or '
      '<b>Get my motion list</b> to see their names.</div>')

    # Appendix C — 목소리
    W('<h2 style="margin-top:26pt">Appendix C &nbsp; Voices</h2>'
      '<p class="lead">Codes for <b>Say \u2026 with \u2026 voice</b>, the on-device voice. '
      'The voice detects the language of the text by itself.</p>'
      '<table style="width:62%"><thead><tr><th>Code</th><th>Voice</th></tr></thead><tbody>')
    for c, _ in VOICES:
        kind = 'Male' if c.startswith('m') else 'Female'
        W(f'<tr><td><code>{c}</code></td><td>{kind} {c[1]}</td></tr>')
    W('</tbody></table>')
    W('<p style="font-size:9.5pt;color:#555">The Espeak blocks have a single fixed voice and take no '
      'voice code. Espeak sounds robotic but begins speaking instantly.</p>')
    W(f'<p style="margin-top:22pt;font-size:9pt;color:#777;border-top:1pt solid #ccc;padding-top:8pt">'
      f'Pibo Teacher\u2019s Guide \u00b7 Circulus Inc. \u00b7 software version {TAG} \u00b7 issued {today}</p>'
      '</section>')

    W('</body></html>')
    return o.getvalue()

if __name__ == '__main__':
    out = os.path.join(HERE, 'teacher_guide.html')
    open(out, 'w', encoding='utf-8').write(build())
    n = sum(1 for c in CATS for t in c['blocks'] if label_of(t))
    print('written', out)
    print('Pibo blocks documented:', n, '/ motions:', len(MOTIONS), '/ examples:', len(EXAMPLES))
