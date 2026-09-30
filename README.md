# openpibo-os — piBo

교육용 로봇 **piBo**(Raspberry Pi 4)의 OS 소프트웨어입니다. 블록·파이썬 코딩 IDE, 로봇 도구, AI 분류기와
`openpibo` 파이썬 라이브러리가 들어 있습니다. 음성 합성·인식, 사물·얼굴·손 인식, 대화(LLM)는 모두 **기기 안에서** 돕니다.

| 폴더 | 내용 | 포트 |
|---|---|---|
| `ide/` | 블록·파이썬 IDE (FastAPI + socket.io) | 80 |
| `tools/` | 동작·카메라·음성 도구 | 50000 |
| `classifier/` | AI 분류기 — 이미지·손·얼굴·포즈 가르치기 | 50010 |
| `openpibo/` | 파이썬 라이브러리 (`from openpibo.motion import Motion` …) | — |
| `system/` | 부팅·WiFi·핫스팟 스크립트 | 8080 |
| `examples/` | 예제 프로그램 | — |

- 문서: [openpibo 가이드](https://themakerrobot.github.io/openpibo-os.pibo/build/html/index.html)
- 배포: 기기가 태그(`YYMMDDvN`, 영문판 `YYMMDDvN-ph`)를 받아 `/home/pi/openpibo-os` 에서 그대로 실행합니다
- 파이썬 패키지: `requirements.txt` · 모델 파일(`/home/pi/.model`)과 이미지 만들기: `IMAGE.md`

## 라이선스

[GNU AGPL-3.0](LICENSE). 포함된 다른 소프트웨어·모델의 라이선스는 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)에 있습니다.
