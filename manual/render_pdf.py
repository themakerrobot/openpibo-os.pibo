#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HTML 을 A4 PDF 로 렌더한다. Chromium 경로는 CHROME 환경변수로 덮어쓸 수 있다."""
import asyncio, os, glob, sys

HERE = os.path.dirname(os.path.abspath(__file__))

CANDIDATES = [
    os.environ.get('CHROME'),
    '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    '/usr/bin/chromium', '/usr/bin/chromium-browser', '/usr/bin/google-chrome',
]
CANDIDATES += sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome'))

PAGES = [('teacher_guide.html',  'Pibo_Teachers_Guide.pdf'),
         ('setup_guide.html',    'Pibo_Setup_Administration.pdf'),
         ('teacher_guide_ko.html', 'Pibo_교사용_가이드.pdf'),
         ('setup_guide_ko.html',   'Pibo_설치_관리_가이드.pdf')]


def chrome_path():
    for c in CANDIDATES:
        if c and os.path.exists(c):
            return c
    return None


async def main():
    from playwright.async_api import async_playwright
    exe = chrome_path()
    async with async_playwright() as p:
        browser = await (p.chromium.launch(executable_path=exe) if exe
                         else p.chromium.launch())
        page = await browser.new_page()
        for src, out in PAGES:
            src_path = os.path.join(HERE, src)
            if not os.path.exists(src_path):
                continue
            await page.goto('file://' + src_path)
            await page.emulate_media(media='print')
            await page.wait_for_timeout(600)          # 이미지 디코딩 대기
            await page.pdf(path=os.path.join(HERE, out), format='A4',
                           print_background=True)
            print('  ', out)
        await browser.close()


if __name__ == '__main__':
    try:
        import playwright  # noqa: F401
    except ImportError:
        sys.exit('playwright 가 없다:  pip install playwright')
    asyncio.run(main())
