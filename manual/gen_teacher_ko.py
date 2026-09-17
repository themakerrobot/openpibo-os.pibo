#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""교사용 가이드(한글) 생성기 — 국내 배포판(main) 기준.

영문판과 다른 점:
  - 블록 이름을 ko.js 에서 읽는다
  - '수집' 카테고리와 collect.json 예제가 더 있다 (PH 에는 없다)
  - 공유기 채널 제약이 없다 (KR 규제도메인은 상위 채널도 열려 있다)
"""
import json, html, io, os, re, datetime, base64

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get('MANUAL_DATA', HERE)
J = lambda n: json.load(open(os.path.join(DATA, n), encoding='utf-8'))

MSG    = J('msg.json')
CATS   = J('cats.json')
KEYMAP = J('keymap.json')
MOTIONS = sorted({m.strip() for m in open(os.path.join(DATA, 'motions.txt'), encoding='utf-8')
                  if m.strip()})

TAG = os.environ.get('MANUAL_TAG', 'origin/main').replace('origin/', '')
TODAY = datetime.date.today().isoformat()


def label_of(t):
    m = MSG.get(KEYMAP.get(t, t).upper())
    if not m:
        return None
    s = re.sub(r'%\{BKY_[A-Z0-9_]+\}', '', m)
    s = re.sub(r'^%1\s*%2\s*', '', s)          # 아이콘 + 빈 입력 자리
    s = re.sub(r'%\d+', '▢', s)
    s = re.sub(r'\[\s*▢\s*', '[', s)
    return re.sub(r'\s+', ' ', s).strip()


def tip_of(t):
    m = MSG.get(KEYMAP.get(t, t).upper() + '_TOOLTIP')
    return re.sub(r'\s+', ' ', m).strip() if m else None


esc = lambda s: html.escape(s, quote=False)
slot = lambda s: esc(s).replace('▢', '<span class="slot"></span>')

_cache = {}
def data_uri(path):
    if path not in _cache:
        with open(path, 'rb') as f:
            _cache[path] = 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode()
    return _cache[path]


# img/ 의 화면 사진은 영문 배포판(ph) 기기에서 찍은 것이라 블록 이름이 영문이다.
# 한글판에는 넣을 수 없으므로 img/ko/ 에 같은 이름으로 국내판 화면을 넣어야 나온다.
# 없으면 그림 없이 글만 나간다 (영문 화면을 국내 매뉴얼에 싣지 않는다).
NEUTRAL = {'로봇 정면'}          # 로봇 사진은 언어와 무관하다
MISSING = []

def img_path(key, fn):
    ko = os.path.join(HERE, 'img', 'ko', fn)
    if os.path.exists(ko):
        return ko
    if key in NEUTRAL:
        return os.path.join(HERE, 'img', fn)
    if key not in MISSING:
        MISSING.append(key)
    return None

IMG = {
 '로봇 정면': 'image1.jpg',
 'IDE 첫 화면': 'image2.jpg',
 'basic.json': 'image3.jpg',
 'device.json': 'image4.jpg',
 'gugudan.json': 'image5.jpg',
 'motion.json': 'image6.jpg',
 'speech_tts.json': 'image7.jpg',
 'vision_face1.json': 'image8.jpg',
 'vision_face2.json': 'image9.jpg',
 'vision_hand.json': 'image10.jpg',
 'vision_marker.json': 'image11.jpg',
 'vision_object.json': 'image12.jpg',
 '도구 — 동작 편집': 'image13.jpg',
 '분류기 — 학습 화면': 'image16.jpg',
}


def fig(key, cap):
    fn = IMG.get(key)
    path = img_path(key, fn) if fn else None
    if not path:
        return ''
    return (f'<figure class="fig"><img src="{data_uri(path)}" alt="">'
            f'<figcaption>{esc(cap)}</figcaption></figure>')


def oled(sn='cd488e95', ip='192.168.114.138', ap='pibo'):
    return ('<div class="oled"><div class="oled-s">'
            f'<div>SN: {esc(sn)}</div><div>I P: {esc(ip)}</div><div>AP: {esc(ap)}</div>'
            '</div></div>')


# ──────────────────────────────────────── 서술

STD_NOTE = {
 '논리': 'Blockly 기본 블록. 비교, 그리고/또는, 아니다, 참/거짓, 그리고 만약–아니면 구조. <b>빈 값</b>은 "값이 없음"을 뜻한다.',
 '반복': 'Blockly 기본 블록. 정해진 횟수 반복, 조건이 참인 동안 반복, 변수로 세면서 반복, 목록을 하나씩 훑기, 그리고 반복 중단·건너뛰기.',
 '수학': 'Blockly 기본 블록. 숫자, 사칙연산, 반올림, 나머지, 난수, 삼각함수, 목록 연산.',
 '문자': 'Blockly 기본 블록. 글자를 만들고 잇고 세고 찾고 고친다. <b>출력</b> 블록이 쓴 내용은 IDE 아래쪽 터미널에 나온다.',
 '목록': 'Blockly 기본 블록. 목록을 만들고, 위치로 읽고 쓰고, 일부를 잘라내고, 글자를 목록으로 나누고, 정렬하고 뒤집는다.',
 '색상': 'Blockly 기본 블록. 색을 고르거나, 무작위로 만들거나, 빨강·초록·파랑 값으로 만들거나, 두 색을 섞는다. <b>장치</b>의 눈 불빛 블록에 그대로 꽂아 쓴다.',
 '변수': 'Blockly 가 만들어 주는 블록이다. <b>변수 만들기</b>를 눌러 이름을 정하면 값을 넣고 꺼내는 블록이 이 자리에 생긴다.',
 '함수': 'Blockly 가 만들어 주는 블록이다. 자주 쓰는 여러 단계를 하나로 묶어 이름을 붙이고, 필요할 때마다 부른다. 같은 코드가 여러 번 나올 때 쓴다.',
}

CAT_INTRO = {
 '시작': '모든 프로그램은 이 블록에서 시작한다. 이 블록 아래에 붙지 않은 블록은 실행되지 않는다.',
 '소리': '소리 파일을 재생하고 마이크로 녹음한다. 파일은 로봇 안의 오디오 폴더에 있고, IDE 왼쪽 파일 목록에서 볼 수 있다.',
 '수집': '위키백과·날씨·뉴스를 가져온다. <b>이 카테고리는 인터넷이 있어야 동작한다.</b> 나머지 블록은 전부 로봇 안에서 처리되지만 이것만 예외다. 또한 날씨는 기상청, 뉴스는 국내 언론사라 국내 전용이다.',
 '장치': '파이보에 달린 눈 불빛과 센서들. <i>확인하기</i>·<i>감지하기</i> 블록은 값을 돌려주므로, 비교 블록이나 <b>출력</b> 블록에 꽂아서 쓴다. <b>RGB 눈 불빛 바꾸기</b>는 숫자 여섯 개를 받는다 — 오른쪽 눈의 빨강·초록·파랑, 그다음 왼쪽 눈의 세 값이고 각각 0~255다.',
 '동작': '서보 모터를 움직인다. 미리 들어 있는 동작을 이름으로 부르거나, <b>도구</b>에서 직접 만든 동작을 부르거나, 모터를 하나씩 움직인다.',
 '화면': '가슴의 작은 화면에 그린다. 그리기 블록은 내용을 준비만 하고, <b>화면 표시하기</b>를 해야 실제로 보인다.',
 '음성': '파이보가 말하게 하고, 로봇 안의 언어모델을 쓴다. 목소리는 둘이다 — 온디바이스(자연스럽고 한국어·영어를 알아서 구분한다)와 E-speak(기계음이지만 즉시 시작한다).',
 '시각': '카메라로 사진을 찍고 편집한다. 대부분 이미지를 받아 바뀐 이미지를 돌려주므로, 결과를 변수에 담아 쓰는 것이 보통이다.',
 '인식': '인공지능 블록들. 얼굴, 사물, QR코드, 손동작, 사람 포즈, 마커, 그리고 <b>분류기</b>에서 직접 학습시킨 이미지 모델. <b>전부 로봇 안에서 돌아가므로 인터넷이 필요 없다.</b>',
 '도구': 'Blockly 기본 블록에 없는 것들 — 기다리기, 시간, 사전(dictionary), 형 변환, 각도 계산.',
}

EXAMPLES = [
 ('basic.json', '기본', '가장 작은 프로그램. 글자를 하나 출력하고, <b>만약–아니면</b> 블록이 두 갈래 중 하나를 고르는 것을 보여준다.',
  ['터미널에 <i>안녕하세요. 파이보입니다.</i> 를 출력한다.',
   '<b>참</b>이 참인지 묻는다 — 언제나 참이다.',
   '참이므로 <i>맞아요.</i> 를 출력한다. <i>아니면</i> 쪽은 실행되지 않는다.'],
  '<b>참</b>을 <b>거짓</b>으로 바꾸고 다시 실행해 보게 한다. 반대쪽 글자가 나온다. 코드가 판단을 내린다는 것을 가장 짧게 보여주는 예제다.'),

 ('device.json', '장치 — 센서와 눈 불빛', '눈 불빛을 켜고, 사람 감지 센서와 터치 센서를 계속 읽는다.',
  ['제목 줄을 출력한다.',
   '양쪽 눈을 흰색으로 켠다 (각각 255, 255, 255).',
   '<b>참</b>인 동안 반복 — 즉 무한 반복을 시작한다.',
   '양쪽 눈을 무작위 색으로 바꾼다.',
   '사람 감지 결과가 <i>person</i> 이면 <i>사람 감지</i> 를 출력한다.',
   '터치 감지 결과가 <i>touch</i> 면 <i>터치 감지</i> 를 출력한다.',
   '0.5초 기다리고 반복한다.'],
  '스스로 멈추지 않는다. IDE 의 <b>정지</b>를 눌러야 끝난다. 센서 블록을 <b>논리</b>의 <b>=</b> 블록으로 글자와 비교하는 부분을 같이 읽으면 좋다.'),

 ('gugudan.json', '구구단', '반복 블록 두 개를 겹쳐서 구구단을 출력한다. 로봇 하드웨어를 쓰지 않아 순수한 프로그래밍 수업으로 쓸 수 있다.',
  ['바깥 반복이 <i>i</i> 를 1부터 9까지 센다.',
   '<i>i</i> 마다 안쪽 반복이 <i>j</i> 를 1부터 9까지 센다.',
   '<i>i</i> × <i>j</i> = 곱셈 결과를 한 줄로 이어 출력한다.'],
  '겹친 반복을 처음 보기에 좋다. 실행 전에 몇 줄이 나올지 먼저 맞혀 보게 하면 이해가 빠르다.'),

 ('motion.json', '동작', '로봇이 아는 동작 목록을 출력하고 그중 하나를 실행한다.',
  ['제목 줄을 출력한다.',
   '<b>동작 목록 가져오기</b> 결과를 출력한다 — 로봇이 할 수 있는 동작 이름 전부.',
   '<i>wave1</i> 동작을 한 번 실행한다.'],
  '<i>wave1</i> 을 출력된 목록의 다른 이름으로 바꿔 보게 한다. 전체 목록은 부록 B 에도 있다. <b>동작 블록을 실행하기 전에 로봇 주변을 비워 둘 것.</b>'),

 ('speech_tts.json', '음성 — 말하기', '같은 문장을 두 목소리로 말해서 차이를 들려준다.',
  ['온디바이스 목소리 <i>m1</i> 로, 크기 80 으로 말한다.',
   '3초 기다린다.',
   'E-speak 목소리로, 크기 80 으로 말한다.'],
  '온디바이스 목소리는 자연스럽고 글자의 언어를 알아서 판단한다. E-speak 는 기계음이지만 바로 소리가 난다. 목소리 코드는 부록 C 에 있다.'),

 ('collect.json', '수집 — 날씨와 뉴스 읽어주기', '<b>함수</b>를 써서 오늘 날씨와 뉴스를 가져와 소리로 읽어준다. 예제 중 가장 복잡하고, 함수를 처음 가르칠 때 쓰기 좋다.',
  ['<i>날씨읽어주기</i> 함수와 <i>뉴스읽어주기</i> 함수를 차례로 부른다.',
   '<i>날씨읽어주기</i> — 서울 날씨 예보를 가져와 앞뒤에 인사말을 붙여 한 문장으로 만들고, 출력한 뒤 말한다.',
   '<i>뉴스읽어주기</i> — 속보 뉴스 목록의 첫 번째 내용을 가져와 같은 방식으로 말한다.'],
  '<b>이 예제는 인터넷이 있어야 동작한다.</b> 날씨 지역(<i>서울</i>)과 뉴스 분야(<i>속보</i>)를 바꿔 보게 하면 좋다. 함수 두 개가 같은 모양으로 짜여 있으니, 같은 일을 묶어 이름 붙이는 것이 왜 편한지 보여주기 좋다.'),

 ('vision_face1.json', '얼굴 — 방향과 거리', '카메라로 계속 보다가 사람이 가까이 오면 반응한다.',
  ['사진을 찍어 <i>image</i> 에 담는다.',
   '얼굴 방향과 거리를 분석해 <i>resultList</i> 에 담는다.',
   '찾은 얼굴마다 결과에서 <i>distance</i> 값을 꺼낸다.',
   '거리가 40 보다 작으면 눈을 무작위 색으로 켜고 사진에 <i>Hello!!</i> 를 쓴다.',
   '분석 결과를 사진에 그려 IDE 에 보여준다.',
   '0.1초 기다리고 반복한다.'],
  '사진은 IDE 의 이미지 칸에 계속 갱신되며 나온다. 40 을 더 큰 숫자로 바꾸면 더 멀리서도 인사한다.'),

 ('vision_face2.json', '얼굴 — 나이·성별·감정', '카메라에 보이는 얼굴을 모두 찾아 분석 결과를 표시한다.',
  ['사진을 찍어 <i>image</i> 에 담는다.',
   '얼굴을 모두 찾아 <i>faceList</i> 에 담는다.',
   '얼굴마다 나이·성별·감정을 분석해 사진에 그린다.',
   '찾은 얼굴에 네모를 그린다.',
   'IDE 에 보여주고 0.1초 기다린 뒤 반복한다.'],
  '추정값이라 틀릴 때가 있다. 감추기보다 "인공지능도 틀린다"를 이야기할 기회로 쓰는 편이 낫다.'),

 ('vision_hand.json', '손동작', '카메라로 손 모양 일곱 가지를 알아본다.',
  ['알아볼 수 있는 손동작 일곱 가지를 출력한다.',
   '손동작 모델을 불러온다.',
   '사진을 찍어 손동작을 인식하고 결과를 사진에 그린다.',
   'IDE 에 보여주고 0.1초 기다린 뒤 반복한다.'],
  '주먹·보·검指·엄지아래·엄지위·브이·사랑해 일곱 가지다. 손을 밝은 곳에서 멈춰 보여줘야 잘 인식한다.'),

 ('vision_marker.json', '마커', '인쇄한 마커(ArUco)를 찾아 크기를 잰다.',
  ['사진을 찍는다.',
   '마커 한 변이 8.5cm 라고 알려주고 찾는다.',
   '찾은 마커를 사진에 그려 IDE 에 보여준다.'],
  '<b>8.5 는 실제로 인쇄한 크기와 같아야 한다.</b> 다르면 거리 값이 틀리게 나온다. 정해진 크기로 인쇄하고 자로 한 번 재 보게 하면 좋다.'),

 ('vision_object.json', '사물과 QR코드', '사물과 QR코드를 동시에 알아본다.',
  ['사진을 찍는다.',
   '사물을 찾아 결과를 담는다.',
   'QR코드를 찾아 결과를 담는다.',
   '둘 다 사진에 그려 IDE 에 보여준다.'],
  'QR코드를 몇 장 인쇄해 두면 좋다. 사물은 정해진 80종 안에서만 인식하므로, 못 알아보는 물건이 있는 것은 고장이 아니라 모델의 한계다.'),
]

MOTORS = [('0','오른발','± 25°'), ('1','오른다리','± 35°'), ('2','오른팔','± 80°'),
          ('3','오른손','± 30°'), ('4','목(좌우)','± 50°'), ('5','머리(상하)','± 25°'),
          ('6','왼발','± 25°'), ('7','왼다리','± 35°'), ('8','왼팔','± 80°'),
          ('9','왼손','± 30°')]

VOICES = ['m1','m2','m3','m4','m5','f1','f2','f3','f4','f5']

TROUBLE = [
 ('가슴 화면에 IP 주소가 없다',
  '로봇이 교실 WiFi 를 못 찾아서 자기 네트워크를 켠 상태다. 네트워크 이름은 <code>pibo-</code> 뒤에 가슴 화면의 <b>SN</b> 이 붙은 형태다. 수업 중에 고칠 일이 아니니 관리자에게 알린다.'),
 ('IDE 페이지가 안 열린다',
  '태블릿이 로봇과 같은 네트워크에 있는지 확인한다. 그다음 <b>Ctrl + Shift + R</b> 로 강력 새로고침한다 — 그냥 새로고침하면 예전 화면이 그대로 나올 수 있다.'),
 ('태블릿이 자꾸 로봇에서 떨어진다',
  '교실 WiFi 에 인터넷이 없으면 태블릿·노트북이 스스로 다른 네트워크로 옮겨간다. 다시 붙이고, 관리자에게 다른 네트워크의 자동 연결을 꺼 달라고 한다. 기기마다 한 번만 해 두면 된다.'),
 ('"인터넷 없음" 이라고 나온다',
  '정상이다. 수업에 쓰는 기능은 전부 로봇 안에서 돌아가므로 인터넷이 필요 없다. 경고를 없애려고 다른 네트워크로 옮기지 않는다. 단 <b>수집</b> 블록만은 인터넷이 있어야 한다.'),
 ('실행했는데 아무 일도 없다',
  '블록이 <b>클릭했을때</b> 아래에 붙어 있는지 본다. 화면에 따로 떨어져 있는 블록 묶음은 실행되지 않는다. 가장 흔한 원인이다.'),
 ('동작 블록이 안 움직인다',
  '동작 이름이 <b>동작 목록 가져오기</b> 결과와 같은지 확인하고, 로봇의 팔다리에 걸리는 것이 없는지 본다.'),
 ('카메라 화면이 멈춰 있다',
  '카메라는 한 번에 하나만 쓸 수 있다. <b>분류기</b>와 <b>도구</b> 탭을 닫고 다시 실행한다.'),
 ('소리가 너무 작거나 크다',
  '말하기·소리 블록마다 크기 입력이 있다. 교실에서는 80 정도가 적당하다.'),
 ('프로그램이 안 멈춘다',
  '<i>참인 동안 반복</i>은 원래 끝나지 않는다. IDE 의 <b>정지</b>를 누른다.'),
 ('처음 상태로 되돌리고 싶다',
  '공장초기화는 예제를 되살리고 저장한 프로그램·녹음·학습 모델을 <b>모두 지운다</b>. WiFi 설정도 되돌리고 <b>전원이 꺼진다</b>. 되돌릴 수 없으니 관리자와 상의한 뒤에 한다.'),
]

CSS = '''
@page { size: A4; margin: 18mm 16mm 16mm 16mm; }
* { box-sizing: border-box; }
body { font: 10.5pt/1.7 "NanumGothic","Nanum Gothic","Noto Sans KR",sans-serif;
       color:#1a1a1a; margin:0; word-break:keep-all; }
h1,h2,h3,h4 { line-height:1.4; }
h1 { font-size:22pt; margin:0 0 6pt; }
h2 { font-size:15pt; margin:0 0 10pt; padding-bottom:5pt; border-bottom:2.5pt solid #1a1a1a; }
h3 { font-size:12pt; margin:15pt 0 5pt; break-after:avoid; page-break-after:avoid; }
h4 { font-size:10.5pt; margin:12pt 0 3pt; }
p  { margin:0 0 7pt; }
code { font:9.5pt ui-monospace,Menlo,Consolas,monospace; background:#f0f0f0;
        padding:.5pt 3pt; border-radius:2pt; }
.page { page-break-after: always; }
.page:last-child { page-break-after: auto; }
.cover { height:245mm; display:flex; flex-direction:column; }
.cover .top { margin-top:48mm; }
.cover .k { font-size:34pt; font-weight:700; letter-spacing:-1pt; margin:0; }
.cover .s { font-size:14pt; color:#555; margin:6pt 0 0; }
.cover .m { margin-top:auto; font-size:9pt; color:#666; border-top:1pt solid #ccc; padding-top:8pt; }
.cover-img { width:72%; margin:18pt auto 0; display:block; }
.lead { font-size:11pt; color:#444; margin-bottom:12pt; }
table { border-collapse:collapse; width:100%; margin:6pt 0 10pt; font-size:9.5pt; }
th,td { border:.6pt solid #bbb; padding:4pt 5pt; text-align:left; vertical-align:top; }
th { background:#ececec; font-weight:600; }
thead { display:table-header-group; }
tr { break-inside:avoid; }
table.blocks td.bl { width:45%; }
.slot { display:inline-block; width:15pt; height:8.5pt; border:.8pt solid #999;
         border-radius:2pt; background:#fafafa; vertical-align:-1pt; margin:0 1.5pt; }
.fig { margin:8pt 0 10pt; break-inside:avoid; }
.fig img { width:100%; border:.6pt solid #ccc; border-radius:2pt; display:block; }
.fig figcaption { font-size:8.5pt; color:#666; margin-top:3pt; }
.shot { border:1pt dashed #aaa; background:#fafafa; padding:14pt; text-align:center;
         margin:8pt 0 10pt; border-radius:3pt; }
.shot-i { font-size:8pt; letter-spacing:1.5pt; color:#999; font-weight:600; }
.shot-c { font-size:9pt; color:#666; margin-top:4pt; }
.oled { background:#111; border:2.5pt solid #444; border-radius:4pt; padding:7pt 9pt; }
.oled-s { font:11pt/1.5 ui-monospace,Menlo,Consolas,monospace; color:#e8e8e8; min-height:50pt; }
.oled-cap { text-align:center; font-size:8.5pt; color:#666; margin-top:3pt; }
.oled-row { display:flex; gap:12pt; margin:10pt 0 12pt; break-inside:avoid; }
.oled-row > div { flex:1; }
.note { border-left:3pt solid #666; background:#f6f6f6; padding:7pt 10pt; margin:9pt 0; font-size:10pt; }
.note b:first-child { display:block; margin-bottom:2pt; }
.warn { border-left-color:#000; background:#ededed; }
ol,ul { margin:0 0 8pt; padding-left:17pt; }
li { margin-bottom:3pt; }
.toc { font-size:11pt; }
.toc div { padding:3.5pt 0; border-bottom:.5pt dotted #ccc; }
.toc .n { display:inline-block; width:26pt; color:#888; }
.cols { column-count:4; column-gap:12pt; font-size:9pt; }
.cols div { break-inside:avoid; padding:1pt 0; }
.cat-intro { font-size:10pt; color:#333; margin-bottom:8pt; }
'''


def blocks_table(cat):
    rows = []
    for t in cat['blocks']:
        lab = label_of(t)
        if not lab:
            continue
        rows.append(f'<tr><td class="bl">{slot(lab)}</td>'
                    f'<td>{esc(tip_of(t) or "")}</td></tr>')
    if not rows:
        return ''
    return ('<table class="blocks"><thead><tr><th>블록</th><th>하는 일</th></tr></thead>'
            '<tbody>' + ''.join(rows) + '</tbody></table>')


def build():
    o = io.StringIO(); W = o.write
    W(f'<!doctype html><html lang="ko"><head><meta charset="utf-8">'
      f'<title>파이보 교사용 가이드</title><style>{CSS}</style></head><body>')

    # 표지
    W(f'''<section class="page cover"><div class="top">
<p class="k">파이보</p><p class="k" style="font-size:26pt;font-weight:400">교사용 가이드</p>
<p class="s">블록 코딩으로 수업하기</p>
<img class="cover-img" src="{data_uri(img_path('로봇 정면', 'image1.jpg'))}" alt="">
</div><div class="m"><b>Circulus Inc.</b> &nbsp;·&nbsp; 소프트웨어 {TAG}
&nbsp;·&nbsp; {TODAY}</div></section>''')

    # 목차
    W('<section class="page"><h2>차례</h2><div class="toc">')
    for n, t in [('1','첫 수업 전에'), ('2','IDE 시작하기'), ('3','블록 목록'),
                 ('4','기본 예제 11개'), ('5','도구와 분류기'), ('6','문제가 생기면'),
                 ('A','부록 A — 모터'), ('B','부록 B — 동작 이름'), ('C','부록 C — 목소리')]:
        W(f'<div><span class="n">{n}</span>{esc(t)}</div>')
    W('</div>')
    W('''<div class="note" style="margin-top:20pt"><b>이 책 쓰는 법</b>
1장과 2장은 첫 수업 전에 한 번 읽어 두면 좋다. 3장은 찾아보는 곳이지 통독하는 곳이 아니다.
4장은 로봇에 이미 들어 있는 예제 11개를 하나씩 설명하므로, 수업 준비가 가장 빠른 길이다.</div>
</section>''')

    # 1장
    W('''<section class="page"><h2>1 &nbsp; 첫 수업 전에</h2>
<p class="lead">파이보는 아이들이 화면에서 블록을 이어 붙여 프로그래밍하는 작은 로봇이다.
타자를 칠 필요가 없고, <b>인터넷도 필요 없다</b> — 음성·시각·인식이 전부 로봇 안에서 돌아간다.
(단 <b>수집</b> 블록만은 예외다.)</p>

<h3>준비물</h3>
<ul>
<li>파이보 로봇. 충전돼 있거나 어댑터에 연결돼 있을 것</li>
<li>웹 브라우저가 있는 태블릿이나 노트북. 크롬을 권한다</li>
<li>교실 WiFi 공유기</li>
</ul>

<h3>전원 켜기</h3>
<ol>
<li>어댑터를 연결하거나, 충전돼 있으면 전원 버튼을 누른다.</li>
<li>눈에 불이 들어오고 인사말이 나온다. 준비되기까지 1분쯤 걸린다.</li>
<li>가슴 화면에 주소가 나오면 준비가 끝난 것이다.</li>
</ol>

<h3>가슴 화면 읽기</h3>''')
    W('<div class="oled-row">'
      '<div>' + oled() + '<div class="oled-cap">정상 — <b>I P</b> 주소를 브라우저에 입력</div></div>'
      '<div>' + oled(ip='', ap='') + '<div class="oled-cap">연결 안 됨 — 6장 참고</div></div>'
      '</div>')
    W('''<p><b>SN</b> 은 로봇 번호, <b>I P</b> 는 브라우저에 칠 주소, <b>AP</b> 는 접속한 WiFi 이름이다.
로봇마다 주소가 다르므로 <b>앞에 있는 로봇의 화면</b>을 보고 친다. 지난 시간 번호를 그대로 쓰면 안 된다.</p>
<p><b>I P</b> 줄이 비어 있으면 로봇이 WiFi 를 못 찾은 것이다 — 6장을 본다.</p>

<h3>IDE 열기</h3>
<p>가슴 화면의 주소를 브라우저에 치면 블록 편집기가 열린다. 설치할 것은 없다.</p>

<div class="note"><b>로봇 하나에 태블릿 하나</b>
태블릿 두 대로 같은 로봇을 열 수는 있지만 작업 화면을 함께 쓰게 된다 — 한쪽이 고치면 다른 쪽에도
그대로 보인다. 모둠 활동에는 쓸모가 있지만, 개인 활동이라면 아이마다 로봇을 하나씩 준다.</div>
</section>''')

    # 2장
    W('<section class="page"><h2>2 &nbsp; IDE 시작하기</h2>')
    W(fig('IDE 첫 화면', 'IDE 첫 화면 — 블록 서랍, 작업 공간, 터미널, 도구 모음'))
    W('''<h3>화면 구성</h3>
<table><tbody>
<tr><th style="width:22%">블록 서랍</th><td>왼쪽. 분류를 누르면 블록이 펼쳐지고, 끌어다 작업 공간에 놓는다.</td></tr>
<tr><th>작업 공간</th><td>가운데. 블록을 이어 붙인다. 떼어내려면 끌어내고, 지우려면 휴지통에 끌어놓거나 Delete 를 누른다.</td></tr>
<tr><th>터미널</th><td>아래쪽. <b>출력</b> 블록이 쓴 내용과 오류 메시지가 나온다.</td></tr>
<tr><th>이미지 칸</th><td><b>이미지 IDE에 보여주기</b> 블록이 보낸 사진이 나온다. 카메라 예제가 전부 이 칸을 쓴다.</td></tr>
<tr><th>도구 모음</th><td>오른쪽 위 — 실행·정지·저장·불러오기와 다른 도구들.</td></tr>
</tbody></table>

<h3>프로그램 만들고 실행하기</h3>
<ol>
<li><b>시작</b> 분류에서 <b>클릭했을때</b> 블록을 작업 공간에 끌어다 놓는다.</li>
<li>그 아래에 블록을 붙인다. 퍼즐처럼 딸깍 붙는다.</li>
<li><b>실행</b>을 누른다. 출력은 터미널에서 본다.</li>
<li>끝나지 않는 프로그램은 <b>정지</b>로 멈춘다.</li>
</ol>
<div class="note"><b>블록은 반드시 이어져 있어야 한다</b>
<b>클릭했을때</b> 아래에 붙은 블록만 실행된다. 작업 공간에 따로 떨어져 있는 블록 묶음은 무시된다 —
"실행했는데 아무 일도 없다"의 가장 흔한 원인이다.</div>

<h3>저장하고 불러오기</h3>
<p>도구 모음의 <b>저장</b>으로 로봇에 저장하고, <b>불러오기</b>로 다시 연다. 예제 11개도 여기서 연다.
파일은 태블릿이 아니라 <b>로봇 안에</b> 저장되므로, 같은 로봇으로 돌아오면 하던 작업이 그대로 있다.</p>

<h3>언어 바꾸기</h3>
<p>IDE 에 언어 선택이 있다. 블록 이름과 메뉴가 바로 바뀌며, 만들어 둔 블록은 영향받지 않는다.</p>
</section>''')

    # 3장 블록
    W('''<section class="page"><h2>3 &nbsp; 블록 목록</h2>
<p class="lead">블록 서랍에 나오는 순서 그대로다. 화면에 보이는 이름과 글자까지 같으므로,
찾는 블록을 여기서 읽고 서랍에서 그대로 찾으면 된다.</p>
<p>회색 칸 <span class="slot"></span> 은 값을 넣는 자리다 — 숫자, 글자, 색, 또는 다른 블록을 꽂는다.</p>
<div class="note"><b>기본 블록과 파이보 블록</b>
앞쪽 아홉 분류는 다른 블록코딩 도구에도 있는 Blockly 기본 블록이다. 그 뒤 — 소리·수집·장치·동작·
화면·음성·시각·인식·도구 — 가 파이보를 움직이는 블록이다.</div>''')
    for cat in CATS:
        name = cat['name']
        W(f'<h3>{esc(name)}</h3>')
        if name in CAT_INTRO:
            W(f'<p class="cat-intro">{CAT_INTRO[name]}</p>')
        if name in STD_NOTE:
            W(f'<p class="cat-intro">{STD_NOTE[name]}</p>')
        else:
            tbl = blocks_table(cat)
            if tbl:
                W(tbl)
        if name == '동작':
            W('<p style="font-size:9.5pt;color:#555">동작 이름은 부록 B, 모터 번호와 각도 한계는 '
              '부록 A 에 있다.</p>')
        if name == '음성':
            W('<p style="font-size:9.5pt;color:#555">목소리 코드는 부록 C 에 있다.</p>')
    W('</section>')

    # 4장 예제
    W('''<section class="page"><h2>4 &nbsp; 기본 예제 11개</h2>
<p class="lead">모든 로봇에 이미 들어 있는 프로그램이다. 도구 모음의 <b>불러오기</b>로 연다.
수업 준비에 가장 빠른 길이다 — 하나 실행해 보고, 같이 읽고, 숫자 하나만 바꿔서 다시 실행한다.</p>
<table><thead><tr><th style="width:34%">예제</th><th>배우는 것</th></tr></thead><tbody>''')
    teach = ['출력, 만약–아니면', '센서, 반복, 눈 불빛', '겹친 반복, 변수', '로봇 동작 부르기',
             '말하기, 두 가지 목소리', '<b>함수</b>, 인터넷에서 가져오기', '카메라 반복, 사전',
             '얼굴 분석, 목록', '학습된 인공지능 모델', '카메라로 길이 재기', '인식 두 가지 동시에']
    for (f, t, _, _, _), tc in zip(EXAMPLES, teach):
        W(f'<tr><td><b>{esc(t)}</b></td><td>{tc}</td></tr>')
    W('</tbody></table>')
    W('''<div class="note"><b>수업에서 잘 통하는 순서</b>
먼저 설명 없이 실행해서 무엇을 하는지 보여준다. 그다음 블록을 열어 같이 읽는다. 마지막으로
<b>딱 한 가지</b>만 바꿔서 — 숫자 하나, 낱말 하나, 색 하나 — 다시 실행한다. 아이들은 설명보다
자기가 바꾼 것을 훨씬 오래 기억한다.</div></section>''')

    for fn, title, summ, steps, note in EXAMPLES:
        W('<section class="page">')
        W(f'<h3 style="margin-top:0">{title}</h3>'
          f'<div style="font:9pt ui-monospace,Menlo,monospace;color:#777;margin-bottom:6pt">{fn}</div>')
        W(f'<p class="lead">{summ}</p>')
        W(fig(fn, f'{fn} 을 불러온 화면'))
        W('<h4>블록이 하는 일</h4><ol>')
        for s in steps:
            W(f'<li>{s}</li>')
        W('</ol>')
        W(f'<div class="note"><b>수업에서</b>{note}</div>')
        W('</section>')

    # 5장
    W('''<section class="page"><h2>5 &nbsp; 도구와 분류기</h2>
<p class="lead">IDE 도구 모음에서 여는 프로그램 둘. 열려 있는 동안 로봇을 붙잡고 있으므로,
다 쓰면 탭을 닫는다.</p>

<h3>도구</h3>
<ul>
<li><b>동작 만들기</b> — 로봇을 손으로 잡거나 슬라이더로 자세를 만들고, 자세마다 저장해서 하나의
동작으로 묶는다. 저장하면 <b>내 동작 실행하기</b> 블록에서 부를 수 있다.</li>
<li><b>준비될 때까지 기다린다.</b> 도구를 열면 모터 버튼이 <b>OFF</b> 로 20초쯤 있다가 <b>ON</b> 으로
바뀐다. 바뀐 뒤에 시작한다.</li>
<li><b>녹음</b> — 마이크로 소리를 녹음해 파일로 저장한다. <b>오디오 재생하기</b> 블록에서 쓸 수 있다.</li>
</ul>''')
    W(fig('도구 — 동작 편집', '도구 — 동작 편집 화면'))
    W('''<h3>분류기</h3>
<p>직접 정한 분류로 사진을 구별하도록 로봇을 학습시킨다 — 예를 들어 과일 세 종류, 또는 정리된
책상과 어질러진 책상.</p>
<ol>
<li>분류를 만들고 이름을 붙인다.</li>
<li>물건을 카메라 앞에 두고 사진을 여러 장 찍는다. 분류마다 20장 이상이면 잘 된다.</li>
<li>분류마다 반복한다.</li>
<li>학습시키고, 물건을 들어 보여 확인한다.</li>
</ol>
<p>학습이 끝나면 블록 편집기에서 <b>인식</b> 분류의 <b>이미지 모델 설정하기</b> 다음에
<b>이미지 모델로 분류하기</b> 로 쓴다.</p>''')
    W(fig('분류기 — 학습 화면', '분류기 — 학습 화면'))
    W('''<div class="note"><b>다 쓰면 탭을 닫는다</b>
도구와 분류기는 각각 카메라와 모터를 붙잡는다. 카메라 블록이 멈춰 있거나 동작 블록이 안 움직이면,
어딘가에 도구나 분류기 탭이 열려 있을 가능성이 높다.</div></section>''')

    # 6장
    W('<section class="page"><h2>6 &nbsp; 문제가 생기면</h2>'
      '<table><thead><tr><th style="width:31%">증상</th><th>할 일</th></tr></thead><tbody>')
    for s, a in TROUBLE:
        W(f'<tr><td><b>{esc(s)}</b></td><td>{a}</td></tr>')
    W('</tbody></table>')
    W('''<div class="note"><b>도움을 청하기 전에</b>
IDE 아래쪽의 일련번호, 무엇을 하던 중이었는지, 터미널에 빨간 글씨로 나온 내용을 적어 둔다.
대개 이것만으로 원인을 찾을 수 있다.</div></section>''')

    # 부록 A
    W('<section class="page"><h2>부록 A &nbsp; 모터</h2>'
      '<p class="lead"><b>모터를 도로 이동하기</b> 블록에서 쓰는 번호와 움직일 수 있는 범위다. '
      '왼쪽·오른쪽은 <b>파이보 기준</b>이지 보는 사람 기준이 아니다.</p>'
      '<table><thead><tr><th style="width:14%">번호</th><th style="width:46%">위치</th>'
      '<th>범위</th></tr></thead><tbody>')
    for n, p_, r in MOTORS:
        W(f'<tr><td>{n}</td><td>{esc(p_)}</td><td>{esc(r)}</td></tr>')
    W('</tbody></table>')
    W('''<div class="note warn"><b>범위를 넘기지 않는다</b>
한계를 넘는 각도를 주면 모터에 무리가 가고 로봇이 넘어질 수 있다. 동작 블록을 실행할 때는
로봇 주변을 비워 둔다.</div>''')

    W('<h2 style="margin-top:22pt">부록 C &nbsp; 목소리</h2>'
      '<p class="lead"><b>말하기(ondevice)</b> 블록에서 쓰는 목소리 코드다. '
      '글자의 언어는 알아서 판단하므로 한국어와 영어를 섞어 써도 된다.</p>'
      '<table style="width:62%"><thead><tr><th>코드</th><th>목소리</th></tr></thead><tbody>')
    for c in VOICES:
        W(f'<tr><td><code>{c}</code></td>'
          f'<td>{"남성" if c[0]=="m" else "여성"} {c[1]}</td></tr>')
    W('</tbody></table>')
    W('<p style="font-size:9.5pt;color:#555">E-speak 블록은 목소리가 하나뿐이라 코드를 받지 않는다. '
      '기계음이지만 바로 소리가 난다.</p></section>')

    # 부록 B
    W('<section class="page"><h2>부록 B &nbsp; 동작 이름</h2>'
      '<p class="lead"><b>동작 실행하기</b> 블록에 넣을 수 있는 이름이다. '
      '로봇에서 <b>동작 목록 가져오기</b> 로도 볼 수 있다.</p><div class="cols">')
    for m in MOTIONS:
        W(f'<div>{esc(m)}</div>')
    W('</div>')
    W(f'''<div class="note" style="margin-top:14pt"><b>직접 만든 동작</b>
<b>도구</b>에서 만든 동작은 이 목록에 없다. <b>내 동작 실행하기</b> 블록을 쓰거나,
<b>내 동작 목록 가져오기</b> 로 이름을 확인한다.</div>
<p style="margin-top:20pt;font-size:9pt;color:#777;border-top:1pt solid #ccc;padding-top:8pt">
파이보 교사용 가이드 · Circulus Inc. · 소프트웨어 {TAG} · {TODAY}</p></section>''')

    W('</body></html>')
    return o.getvalue()


if __name__ == '__main__':
    out = os.path.join(HERE, 'teacher_guide_ko.html')
    open(out, 'w', encoding='utf-8').write(build())
    n = sum(1 for c in CATS for t in c['blocks'] if label_of(t))
    print('written', out)
    print(f'  파이보 블록 {n}개 / 동작 {len(MOTIONS)}개 / 예제 {len(EXAMPLES)}개')
    if MISSING:
        print(f'  !! 국내판 화면 사진 없음 {len(MISSING)}장 — img/ko/ 에 넣으면 들어간다:')
        for k in MISSING:
            print('     -', k, '->', 'img/ko/' + IMG[k])
