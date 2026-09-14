#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Google 번역 호출. 공개 API 는 translate() 하나뿐이고 openpibo.speech 의
Dialog.translate() 가 쓴다.

원래 구현(Arnaud Aliès 의 mtranslate, 아래 MIT 라이선스)은
http://translate.google.com/m 페이지를 받아 class="t0" / "result-container"
를 정규식으로 긁는 방식이었다. Google 이 그 페이지를 바꾸면서 매칭이 0건이
되었고, 예외도 없이 빈 문자열만 돌려주게 되어 통째로 교체했다.

지금은 JSON 엔드포인트 두 곳을 순서대로 시도한다. 한쪽이 지역이나 방화벽
정책으로 막혀도 다른 쪽으로 넘어간다 — 실제로 한쪽만 403 이 나는 환경을
확인했다. 둘 다 실패하면 예전과 같이 빈 문자열을 돌려준다.

MIT License

Copyright (c) 2016 Arnaud Aliès

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import html
import json
import urllib.request
import urllib.parse

# 교실 네트워크가 느릴 수 있으나, 엔드포인트가 둘이라 최악이 이 값의 두 배다.
# 원래 구현에는 타임아웃이 아예 없어 응답이 없으면 무한정 매달렸다.
TIMEOUT = 5

HEADERS = {
    "User-Agent": ("Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"),
    "Accept-Language": "ko,en;q=0.9",
}

# (URL 틀, 응답 파서). 틀의 %s 는 순서대로 sl, tl, q 다.
APIS = [
    ("https://clients5.google.com/translate_a/t"
     "?client=dict-chrome-ex&dt=t&sl=%s&tl=%s&q=%s",
     # 문자열 목록으로 오기도, [번역, 원문] 쌍 목록으로 오기도 한다.
     lambda d: "".join(x[0] if isinstance(x, list) else x for x in d)),

    ("https://translate.googleapis.com/translate_a/single"
     "?client=gtx&dt=t&sl=%s&tl=%s&q=%s",
     # [[[번역, 원문, ...], ...], ...] 형태. 문장 단위로 쪼개져 오므로 이어붙인다.
     lambda d: "".join(x[0] for x in d[0] if x and x[0])),
]


def translate(to_translate, to_language="auto", from_language="auto"):
    """문장을 번역해 돌려준다. 실패하면 빈 문자열.

    언어는 두 글자 코드다 (en, ko, es, fr ...). "auto" 면 Google 이 판별한다.

    Example:
      translate("안녕하세요! 만나서 정말 반가워요!", "en")
      # "hello! It's really nice to meet you!"
    """
    text = str(to_translate or "").strip()
    if not text:
        return ""

    # safe="" 로 두어야 '/' 와 '&' 까지 인코딩된다. q 는 인자로 넘어가므로
    # 인코딩 결과의 % 가 아래 % 포매팅에 다시 걸리지 않는다.
    q = urllib.parse.quote(text, safe="")

    for url, parse in APIS:
        try:
            req = urllib.request.Request(
                url % (from_language, to_language, q), headers=HEADERS)
            with urllib.request.urlopen(req, timeout=TIMEOUT) as res:
                result = parse(json.loads(res.read().decode("utf-8")))
            if result:
                # 번역문에 &#39; 같은 엔티티가 섞여 오는 경우가 있다.
                return html.unescape(result)
        except Exception:
            continue

    return ""


if __name__ == "__main__":
    print(translate("안녕하세요! 만나서 정말 반가워요!", "en"))
