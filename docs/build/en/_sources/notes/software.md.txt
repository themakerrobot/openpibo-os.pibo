# Software

piBo's features are used through the **openpibo** Python package. Blocks also turn into Python code that calls this package
(see it with the [Python code] button). The source is on [GitHub](https://github.com/themakerrobot/openpibo-os.pibo) (AGPL-3.0).

## Package layout

```
openpibo
├── audio.py            play, stop and record sound
├── collect.py          Wikipedia, weather, news (internet, Korean edition)
├── device.py           eye LEDs, battery, touch, PIR … (MCU)
├── motion.py           motors and motions
├── oled.py             OLED display
├── pibo_graphics.py    turtle graphics for the display
├── speech.py           voices (TTS), speech recognition (STT), chat (LLM)
├── usb_uart.py         USB serial
├── utils.py            other tools
├── vision_camera.py    camera and image editing
├── vision_detect.py    object, QR, pose, hand gesture and marker recognition
├── vision_face.py      find, analyze and learn faces
└── vision_classify.py  load models taught in the Classifier
```

See **Python** on the left for every class and method.

## Writing Python

```python
from openpibo.<library> import <Class>

<instance> = <Class>()
<instance>.<method>(<arguments>)
```

Example: play a sound and stop it.

```python
from openpibo.audio import Audio
import time

audio = Audio()
audio.play('/home/pi/openpibo-files/audio/system/opening.mp3', volume=80)
time.sleep(3)
audio.stop()
```

Example: make a voice inside piBo and speak (no internet; Korean and English are detected automatically).

```python
from openpibo.speech import SpeechOnDevice
from openpibo.audio import Audio

tts = SpeechOnDevice()
tts.tts('Hello! I am piBo.', filename='/home/pi/hello.wav', voice='f1')
Audio().play('/home/pi/hello.wav', background=False)
```

Example: classify the camera view with a model saved in the Classifier.

```python
from openpibo.vision_camera import Camera
from openpibo.vision_classify import CustomClassifier

camera = Camera()
cf = CustomClassifier()
cf.load('fruit')                     # /home/pi/mymodel/fruit
img = camera.read()
name, probs = cf.predict(img, draw=True)   # draws the hand/face/body points and the class name on img
print(name)
camera.imwrite('/home/pi/result.jpg', img)
```

```{note}
Code run from the IDE runs inside piBo as **root** (so it can use the camera, GPIO and other hardware).
```
