# piBo Maker

piBo Maker is the piBo development environment you open in a web browser. When your tablet or laptop is on the same WiFi
as piBo, type **piBo's IP address** (shown on piBo's screen) into the address bar. There is nothing to install.

The address opens the **home screen** (a worksheet page). Tap a big picture button to enter an app, and use [Home] (house button) in an app's top bar to come back.
Row 1 **Make** (Coding · Tools · Teach AI · Chat), row 2 **Play & learn** (Card coding · Robot Play), row 3 **Settings and help** (Settings · Help).
The app that is running now gets a red 'Running' stamp and the one you used last gets a yellow tag; on the right are the robot status and [Continue] (recent files, AI you taught).
[Settings] has screen brightness, WiFi settings (pick and join a WiFi right there), reset robot screen, H/W check, **robot info** (version, install date, storage and model versions — [Copy] it when you contact support), factory reset, power off and the source code and license. The bottom of the home screen shows the product, version, Help and license.
The robot status (battery, temperature, memory, WiFi, serial, uptime) is on the home screen too. Every app has the same top bar — the app name on the left, and (app actions) · **[How to]** · [Home] · [Full screen] · [Brightness] · language on the right. [How to] shows a few lines on what you can do on that screen and a link to the matching part of this help.

| Screen | What it does | Where to open it |
|---|---|---|
| **Coding** | Build and run programs with blocks or Python | `http://<piBo IP>` → home screen [Coding] |
| **Tools** | Try the motors, camera and voice right away, without code | Home screen [Tools] |
| **Chat** | Chat in text with the language model (LLM) running inside piBo | Home screen [Chat] |
| **Teach AI** | Collect examples with the camera and teach your own AI | Home screen [Teach AI] |
| **Card coding** | Elementary students teach the robot friend tricks with cards (no coding) — Challenges · Make · My tricks. The top of its start screen shows today's lesson, stars and tricks | Home screen [Card coding] |
| **Robot Play** | **Pet** (look after your robot friend) and **Remote control** (buttons move the robot right away — arrows and motions that don't use the legs) | Home screen [Robot Play] |
| **Help** | This document | Home screen [Help] |

```{note}
Everything runs **inside piBo** (voices, speech recognition, chat and the classifier included). Only the blocks in the
[Collect] category (Wikipedia, weather, news) need the internet, and that category is only in the Korean edition.
```

(app-ide)=
## Coding (IDE)

![Coding with blocks](images/ide_block.png)

- **Top bar**: the folder button on the far left opens the **file drawer**. [Blocks | Python] in the middle switches the editor. On the right are [⋯] (font size · Python editor theme · open an example) · [How to] · [Home] · [Full screen] · [Brightness] · language, the same as every other app
- **File drawer**: the file list, [Add] (new file / new folder / upload) and a preview for pictures and sounds. It is open at first and closes when you open a file or tap the editor.
  Tapping the file name in the editor bar opens it again. The icons on each file download, rename, **copy or move** and delete it.
  To copy or move, choose a folder (code · myimage · myaudio · mymodel · usb) and tap [Copy] or [Move]. It works between a USB drive and the robot too.
  If the name is already taken, the copy gets a new name like `name_1`
- **Start screen**: before you open a file, the workspace shows **[New file] · [Open an example] · [Open my file]**. [Open an example] shows the examples as **cards** (title, what you learn, level ★, time, what you need); tap a card to open it in blocks. After a file is open, use [⋯] → [Open an example] at the top ([Show folder] opens the examples folder in the drawer).
  Once a file is open, the editor bar shows the folder and name, like `code › hand.json` (hover to see the full path)
- **Run panel on the right**: **[Run] [Stop]** with the run status, screen output (pictures sent with the `Show image … on the monitor` block), program output and sending input to the program.
  The button at the right end of the editor bar hides or shows it, and it opens again when you run a program. Hide both the drawer and the run panel to give the blocks the whole width
- **Blocks**: drag blocks out of the categories on the left. Type a word such as "sound" or "face" into **Search blocks** at the top to find blocks.
  Choose [Easy] in **[Easy | All]** on the editor bar to see only beginner blocks (repeat forever, motions, lights, sounds, sensors, AI eyes, score and more).
  [Python code] shows the Python code your blocks make. See **Blocks** on the left for every block.
- **When there is an error**: a red box above the output says where (the block outlined in red in block mode, or the line number in Python) and what went wrong in plain words.
  [Show block] / [Show line] takes you there, and the red outline goes away when you change the block

![Coding with Python](images/ide_python.png)

- **Python**: the `openpibo` package gives you every piBo feature. `print` goes to [Output] on the right and `input` reads from the input box below it.
  See **Python** on the left for the API
- Programs run inside piBo. Press [Stop] to stop one

(app-tools)=
## Tools

Try piBo's features one at a time, without code. Pick [Motion], [Camera] or [Speech] on the left.

![Tools: Motion](images/tools_motion.jpg)

- **Motion**: type an angle into the number on a dot on the photo and press Enter — that motor moves and the next motor is selected (you can also use the slider next to the dot).
  When the pose is right, press **[Add or update]** at the top to add a row to the table on the right (the time goes up by 0.5 s each time). [Run] plays the table;
  type a name and press **[Save]** to use it later with the `Run my motion … times` block. The table header shows the body part under each motor number (R foot, Head, …)

![Tools: Camera](images/tools_vision.jpg)

- **Camera**: apply vision features (grayscale, edges, cartoon, QR code, face analysis, object detection, hand gestures, pose, markers…)
  to piBo's camera view. The result also appears as text under [Result].
  **Face ID** recognizes faces you have named and [Registered] (programs can use them too, with the `Load the face dictionary from code facedb` block).
  If a USB camera is plugged in, switch between the **board camera and USB cameras** in the picker above the camera view (any USB camera that supports V4L2)

![Tools: Speech](images/tools_speech.png)

- **Speech**: pick one of ten voices (Male 1–5, Female 1–5) or the robot voice (espeak) and let piBo say your text. Korean and English are
  detected automatically. [Speak] says it. Under [Listen], press [Try speaking] and talk: piBo stops by itself when you finish and shows
  what it heard as text (up to 10 seconds, processed on piBo). [Use as text to speak] puts that text into the box on the left so piBo can say it back.
  The first time takes a few seconds while speech recognition loads. [Record] records piBo's microphone and [Play again] plays it back

(app-classifier)=
## Teach AI (classifier)

![Teach AI: Train](images/classifier_learn.jpg)

Collect examples with the camera and teach the AI, for example "this is a cat, this is food".

**Training steps** at the top of the right panel (① Collect examples → ② Teach the AI → ③ Save and test) outline the step to do now in blue and check off finished steps.

1. **What should it learn from?** — Image (the whole picture) · Hand (hand shape) · Face (expression) · Pose (body posture)
2. Name each **class** and keep pressing **[Hold to collect]** to collect examples. You can also upload files with [Photos].
   The picker under the camera switches to a USB camera — use the same camera for training and for use for better results
3. **[Teach the AI]** — the tablet or laptop browser learns in a few seconds and shows the accuracy, a confusion table and live scores
4. **[Save]** — saved on piBo in `/home/pi/mymodel/<model name>`
5. In Coding use `Load classification model (mymodel) (model name)` → `Classify image (image) with the classification model`.
   `Show the classification result on image (image)` draws the hand, face or body points and the class name on the picture

The [Test] tab tries a saved model again. [Models] lets you test, keep training, rename, download (zip) or delete a model.

```{tip}
Teach AI downloads its AI files (about 10 MB) the first time it opens. Open it once on every tablet before class and it
will start right away during class.
```

(app-chat)=
## Chat

Chat in text with the language model (LLM) that runs inside piBo. Choose a model from the **model cards** on the start screen, and the model loads then. After that, **[Chat model]** appears at the top so you can switch
(the first time takes several tens of seconds). Changing the model starts the chat over.

| Model | What it is |
|---|---|
| General | Chats in Korean and English. No tools |
| TheMaker KO | A Korean model trained to talk with students. You can ask piBo to do things (tools below) |
| TheMaker EN | The English version of TheMaker. If the model file is not on the robot, it shows "(not installed)" and can't be chosen |

TheMaker listens and **chooses a tool by itself**. The tool it ran appears in small text under the answer (for example `Light red`).

| Tool | Try saying | What it does |
|---|---|---|
| Light | "Turn on the red light", "Turn off the light" | Changes or turns off the eye light (red, orange, yellow, green, blue, sky blue, purple, pink, white) |
| Look | "What do you see?" | Looks with the camera and says what it sees |
| Move | "Say hello", "Can you dance?" | greeting, wave, dance, clap, high five, nod, head shake, forward, backward, left, right |

- Say **"Stop"** and it stops right away, without asking the model.
- Moves that change place (forward, backward, left, right) happen only when your words name a direction. Be careful near the edge of a desk.
- Say "Let's just talk" to stop using tools, and "You can move now" to use them again.
- Turn on [Speak out loud] and piBo speaks the answer (you can choose the voice and volume).

Programs can use it too, with the `Choose chat model`, `Start LLM server` and `Say … to AI` blocks in [Speech].
Blocks chat in text only and do not run tools.

```{note}
Tools, Chat, Teach AI, Card coding/Robot Play and H/W check run **one at a time**. Opening one closes the others, and running a program in Coding closes them too
(they share the camera, speaker and memory). A closed screen shows [Restart].
```
