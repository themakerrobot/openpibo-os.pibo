#!/usr/bin/env python3
"""전수 조사 — 파일만 보고 하는 검사(S1~S12). 체크리스트는 리포 맨 위 AUDIT.md.

  python3 design/audit/static_check.py ../openpibo-os.pibrain            # 두 리포
  python3 design/audit/static_check.py ../openpibo-os.pibrain --no-fetch # 원격 global 을 새로 받지 않음

항목마다 OK / FAIL / SKIP 한 줄과 자세한 줄을 찍고, FAIL 이 하나라도 있으면 끝 코드 1.
파이썬 표준 라이브러리 + node(문법·번역 키 검사)만 쓴다. 이 파일은 파이보 리포에만 있다(PiBrain 은 두 번째 인자로).
"""
import os
import re
import sys
import glob
import json
import shutil
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PIBO = os.path.dirname(os.path.dirname(HERE))
RESULTS = []          # (id, 이름, 상태, [자세한 줄])

# S2: 실행비트(100755)가 있어야 하는 파일 — HEAD 의 100755 목록과 정확히 같아야 한다(늘거나 줄면 FAIL → 사람이 판단해 여기를 고친다)
EXEC = {
  'pibo': {'design/sync.sh', 'docs/build.sh', 'manual/build.sh', 'manual/render_pdf.py', 'system/booting.py', 'system/conwifi.sh',
           'system/hotspot.sh', 'system/init', 'system/network_disp.py', 'system/setup_country.sh', 'system/setup_openpibo_src.sh',
           'system/system.sh', 'tools/static/index.js'},
  'pibrain': {'design/sync.sh', 'docs/build.sh', 'system/booting.py', 'system/clear_disp.py', 'system/conwifi.sh', 'system/hotspot.sh',
              'system/init', 'system/network_disp.py', 'system/setup_country.sh', 'system/setup_openpibo_src.sh', 'system/system.sh',
              'test/test'},
}
# S8: global 이 main 과 다른 파일(CLAUDE.md '영문판 델타') — 두 리포 같은 16개
DELTA = {'ide/static/ko2en.js', 'tools/static/ko2en.js', 'classifier/static/ko2en.js', 'ide/static/customblock_toolbox.js',
         'GLOBAL_DELTA.md', 'examples/collect.json'}
SKIP_DIRS = re.compile(r'(^|/)(vendor|blockly|codemirror|tasks-vision|tfjs|build|node_modules|webfonts|fonts)/')


def git(repo, *a, check=False):
  r = subprocess.run(['git', '-C', repo, *a], capture_output=True, text=True)
  if check and r.returncode:
    raise RuntimeError(r.stderr.strip())
  return r.stdout


def files(repo, *pat):
  return [f for f in git(repo, 'ls-files', '-z', *pat).split('\0') if f]


def report(cid, name, bad, info=None, skip=None):
  st = 'SKIP' if skip else ('FAIL' if bad else 'OK')
  RESULTS.append((cid, name, st, (bad or []) + (info or []) + ([skip] if skip else [])))


# ── S1 문법 ──────────────────────────────────────────────────────────────
def s1(repos):
  bad = []
  for name, repo in repos:
    for f in files(repo, '*.py'):
      if SKIP_DIRS.search(f):
        continue
      p = os.path.join(repo, f)
      try:
        compile(open(p, 'rb').read(), p, 'exec')
      except SyntaxError as e:
        bad.append(f'{name}/{f}: {e}')
    for f in files(repo, '*.js'):
      if SKIP_DIRS.search(f) or f.endswith('.min.js') or f.endswith('_compressed.js'):
        continue
      p = os.path.join(repo, f)
      src = open(p, encoding='utf-8', errors='replace').read()
      module = re.search(r'^\s*(import|export)\s', src, re.M) is not None
      cmd = ['node', '--check', '--input-type=module'] if module else ['node', '--check', p]
      r = subprocess.run(cmd, input=src if module else None, capture_output=True, text=True)
      if r.returncode:
        bad.append(f'{name}/{f}: {r.stderr.strip().splitlines()[0] if r.stderr.strip() else "node --check 실패"}')
    for f in files(repo, '*.sh') + [x for x in ('system/init', 'test/test') if os.path.isfile(os.path.join(repo, x))]:
      p = os.path.join(repo, f)
      head = open(p, 'rb').read(64)
      if f.endswith('.sh') or b'bash' in head or b'/sh' in head:
        r = subprocess.run(['bash', '-n', p], capture_output=True, text=True)
        if r.returncode:
          bad.append(f'{name}/{f}: {r.stderr.strip()}')
  report('S1', '문법(파이썬·JS·셸)', bad)


# ── S2 실행비트 ──────────────────────────────────────────────────────────
def s2(repos):
  bad = []
  for name, repo in repos:
    head = {l.split('\t')[1] for l in git(repo, 'ls-tree', '-r', 'HEAD').splitlines() if l.startswith('100755')}
    want = EXEC[name]
    for f in sorted(want - head):
      bad.append(f'{name}: {f} 가 100755 가 아니다')
    for f in sorted(head - want):
      bad.append(f'{name}: {f} 가 새로 100755 다(맞으면 static_check.py EXEC 에 넣을 것)')
    for f in sorted(want):
      p = os.path.join(repo, f)
      if os.path.isfile(p) and not os.access(p, os.X_OK):
        bad.append(f'{name}: 작업본 {f} 에 실행비트가 없다(git add 하면 644 로 바뀐다)')
  report('S2', '실행비트', bad)


# ── S3 ?ver ──────────────────────────────────────────────────────────────
def ctime(repo, *a):
  out = git(repo, 'log', '-1', '--format=%ct', *a).strip()
  return int(out) if out else 0


def s3(repos):
  bad, info = [], []
  for name, repo in repos:
    dirty = set(git(repo, 'diff', '--name-only', 'HEAD').split())
    tpls = [f for f in files(repo, '*.html') if not f.startswith('docs/') and not SKIP_DIRS.search(f)]
    for t in tpls:
      src = open(os.path.join(repo, t), encoding='utf-8').read()
      app = t.split('/')[0]
      for m in re.finditer(r'''([\w./:'"+ -]*?)((?:\.\./|/)?static/[^"'?\s]+)\?ver=([\w.]+)''', src):
        ref, ver = m.group(2), m.group(3)
        if not ver[:1].isdigit():
          continue   # 문서 속 자리표시(YYMMDDvN)
        rel = ref.split('static/', 1)[1]
        # 다른 앱(IDE 80)에서 싣는 파일(대화·로봇 놀이의 ko2en.js)은 IDE 쪽 파일
        cross = 'location.hostname' in m.group(0) or ':' in m.group(1)
        cands = [os.path.join('ide', 'static', rel)] if cross else [os.path.join(app, 'static', rel), os.path.join('ide', 'static', rel)]
        f = next((c for c in cands if os.path.isfile(os.path.join(repo, c))), None)
        if not f:
          continue
        needle = f'?ver={ver}'
        if f in dirty and t not in dirty:
          bad.append(f'{name}/{t}: {rel} 를 고쳤는데(커밋 전) ?ver={ver} 그대로')
          continue
        fc = ctime(repo, '--', f)
        vc = ctime(repo, '-S', f'{rel}{needle}', '--', t) or ctime(repo, '-S', needle, '--', t)
        if fc and vc and fc > vc:
          bad.append(f'{name}/{t}: {rel}?ver={ver} — 파일이 그 뒤에 바뀌었다({git(repo, "log", "-1", "--format=%h %cs", "--", f).strip()})')
    # 같은 파일을 여러 화면이 실을 때 번호가 같아야 한다(IDE ko2en.js ← 대화·로봇 놀이)
    vers = {}
    for t in tpls:
      src = open(os.path.join(repo, t), encoding='utf-8').read()
      for m in re.finditer(r'''location\.hostname[^<]*?/static/(ko2en\.js)\?ver=([\w.]+)''', src):
        vers.setdefault(m.group(1), set()).add((t, m.group(2)))
    ide_ver = re.search(r'ko2en\.js\?ver=([\w.]+)', open(os.path.join(repo, 'ide/templates/index.html'), encoding='utf-8').read())
    for t, v in vers.get('ko2en.js', ()):
      if ide_ver and v != ide_ver.group(1):
        bad.append(f'{name}/{t}: IDE ko2en.js?ver={v} — IDE 템플릿은 {ide_ver.group(1)}')
    # customblock 3종은 같은 번호
    src = open(os.path.join(repo, 'ide/templates/index.html'), encoding='utf-8').read()
    cb = set(re.findall(r'customblock(?:_callback|_toolbox)?\.js\?ver=([\w.]+)', src))
    if len(cb) > 1:
      bad.append(f'{name}: customblock 3종 ?ver 가 다르다 {sorted(cb)}')
    # ko.js·en.js 는 index.js 의 langFileVersion 으로 붙는다
    lv = ctime(repo, '-G', r'langFileVersion\s*=', '--', 'ide/static/index.js')
    for f in ('ide/static/ko.js', 'ide/static/en.js'):
      if f in dirty and 'ide/static/index.js' not in dirty:
        bad.append(f'{name}: {f} 를 고쳤는데 langFileVersion(index.js) 그대로')
      elif ctime(repo, '--', f) > lv:
        bad.append(f'{name}: {f} 가 langFileVersion 을 올린 뒤에 바뀌었다')
  report('S3', '?ver·langFileVersion', bad, info)


# ── S4 번역 키 ───────────────────────────────────────────────────────────
NODE_KEYS = r'''
const fs=require('fs'),vm=require('vm');
function load(f){const ctx={localStorage:{getItem(){return null},setItem(){}},navigator:{language:'ko'},
  document:{querySelectorAll(){return []},addEventListener(){},documentElement:{}},console};ctx.window=ctx;vm.createContext(ctx);
  try{vm.runInContext(fs.readFileSync(f,'utf8')+';this.__T=(typeof translations!=="undefined"?translations:(typeof T!=="undefined"?T:null));',ctx)}catch(e){return {__err:e.message}}
  return ctx.__T||{}}
const out={};for(const f of process.argv.slice(1)){const T=load(f);const half=[];for(const k in T){const v=T[k];
  if(v&&typeof v==='object'&&!('ko' in v&&'en' in v))half.push(k)}out[f]={keys:Object.keys(T),half,err:T.__err||null}}
console.log(JSON.stringify(out));
'''


def s4(repos):
  bad = []
  for name, repo in repos:
    dicts = {a: os.path.join(repo, a, 'static', 'ko2en.js') for a in ('ide', 'tools', 'classifier')}
    r = subprocess.run(['node', '-e', NODE_KEYS, *dicts.values()], capture_output=True, text=True)
    try:
      D = json.loads(r.stdout)
    except ValueError:
      bad.append(f'{name}: ko2en.js 를 읽지 못했다 {r.stderr[:200]}')
      continue
    keys = {}
    for a, p in dicts.items():
      d = D[p]
      if d['err']:
        bad.append(f'{name}/{a}/static/ko2en.js: {d["err"]}')
      keys[a] = set(d['keys'])
      for k in d['half']:
        bad.append(f'{name}/{a}: {k} 에 ko·en 둘 다 없다')
    for f in files(repo, '*.js', '*.html', '*.py'):
      if SKIP_DIRS.search(f) or f.endswith('ko2en.js') or f.endswith('.min.js') or f.startswith('docs/') or f == 'ide/static/launch.html':
        continue
      app = 'tools' if f.startswith('tools/') else 'classifier' if f.startswith('classifier/') else 'ide'
      src = open(os.path.join(repo, f), encoding='utf-8', errors='replace').read()
      pats = [r'''\bt\(\s*['"]([a-zA-Z][a-zA-Z0-9_]+)['"]''', r'''data-(?:title-|aria-|placeholder-)?key=["']([a-zA-Z][a-zA-Z0-9_]+)["']''']
      if f.endswith('.py'):
        pats = [r'''['"](?:dialog|msg|reason|error_key)['"]\s*:\s*['"]([a-z][a-z0-9_]{3,})['"]''']
      for pat in pats:
        for m in re.finditer(pat, src):
          k = m.group(1)
          if k.endswith('_'):
            continue   # t('hint_' + 이름) 처럼 이어 붙이는 키
          pool = set().union(*keys.values()) if f.endswith('.py') else keys[app]
          if k not in pool:
            bad.append(f'{name}/{f}: 없는 키 {k} ({app})')
  report('S4', '번역 키(ko·en 짝, 쓰는 키가 사전에 있음)', sorted(set(bad)))


# ── S5 두 리포 같은 파일 ─────────────────────────────────────────────────
def s5(repos):
  if len(repos) < 2:
    return report('S5', '두 리포 같은 파일', None, skip='PiBrain 리포 경로가 없다')
  a, b = repos[0][1], repos[1][1]
  bad = []
  lst = [l.strip() for l in open(os.path.join(HERE, 'shared_files.txt'), encoding='utf-8') if l.strip() and not l.startswith('#')]
  for f in lst:
    pa, pb = os.path.join(a, f), os.path.join(b, f)
    if not (os.path.isfile(pa) and os.path.isfile(pb)):
      bad.append(f'{f}: 한쪽에 없다')
    elif open(pa, 'rb').read() != open(pb, 'rb').read():
      bad.append(f'{f}: 다르다')
  # 로봇 놀이 템플릿은 탭 아이콘 ?ver 만 다르다
  def kids(p):
    return re.sub(r'icon\.png\?ver=[\w.]+', '', open(p, encoding='utf-8').read())
  if kids(os.path.join(a, 'kids/templates/index.html')) != kids(os.path.join(b, 'kids/templates/index.html')):
    bad.append('kids/templates/index.html: 아이콘 ?ver 말고도 다르다')
  # AUDIT.md 도 같은 파일
  if open(os.path.join(a, 'AUDIT.md'), 'rb').read() != open(os.path.join(b, 'AUDIT.md'), 'rb').read():
    bad.append('AUDIT.md: 다르다')
  report('S5', f'두 리포 같은 파일({len(lst) + 2}개)', bad)


# ── S6 키트 사본 ─────────────────────────────────────────────────────────
def s6(repos):
  bad = []
  for name, repo in repos:
    r = subprocess.run(['bash', os.path.join(PIBO, 'design/sync.sh'), '--check', repo], capture_output=True, text=True, cwd=PIBO)
    for l in r.stdout.splitlines():
      if l.strip() and not l.strip().startswith('ok'):
        bad.append(f'{name}: {l.strip()}')
    if r.returncode and not bad:
      bad.append(f'{name}: sync.sh --check 실패 {r.stderr.strip()[:200]}')
  report('S6', '키트(pibo-ui·글꼴) 사본이 design/ 과 같음', bad)


# ── S7 유출 ──────────────────────────────────────────────────────────────
def s7(repos):
  bad, info = [], []
  words = []
  wf = os.environ.get('PIBO_AUDIT_WORDS', '')
  if wf and os.path.isfile(wf):
    words = [w.strip() for w in open(wf, encoding='utf-8') if w.strip() and not w.startswith('#')]
  for name, repo in repos:
    pats = [(r'claude\.ai/code/session_', '세션 링크'), (r'Claude-Session:', 'Claude-Session 줄'),
            (r'[A-Za-z0-9._%+-]+@gmail\.com', '개인 메일'), (r'(?i)(api[_-]?key|secret|token)\s*[=:]\s*["\'][A-Za-z0-9_\-]{16,}', '키처럼 보이는 값'),
            (r'gh[pousr]_[A-Za-z0-9]{30,}|hf_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9]{30,}', '토큰')]
    pats += [(re.escape(w), '업체·제품 이름') for w in words]
    for f in files(repo):
      if SKIP_DIRS.search(f) or re.search(r'\.(png|jpg|gif|woff2?|ttf|onnx|task|tflite|wav|mp3|whl|pdf|gz|zip|bin|cur)$', f):
        continue
      if f in ('THIRD_PARTY_NOTICES.md', 'LICENSE'):
        continue
      try:
        src = open(os.path.join(repo, f), encoding='utf-8').read()
      except (UnicodeDecodeError, IsADirectoryError, FileNotFoundError):
        continue
      for pat, what in pats:
        for m in re.finditer(pat, src):
          line = src.count('\n', 0, m.start()) + 1
          if f == 'CLAUDE.md' and what in ('세션 링크', 'Claude-Session 줄'):
            continue   # 규칙 설명 자체
          if f == 'design/audit/static_check.py' or f == 'AUDIT.md':
            continue
          bad.append(f'{name}/{f}:{line}: {what}')
    # 261101 뒤 커밋 메시지
    log = git(repo, 'log', '--since=2026-11-02', '--format=%h%x00%B%x01')
    for ent in log.split('\x01'):
      if '\0' not in ent:
        continue
      h, body = ent.strip().split('\0', 1)
      if re.search(r'claude\.ai/code/session_|Claude-Session:', body):
        bad.append(f'{name}: 커밋 {h} 메시지에 세션 링크')
  if not words:
    info.append('업체·제품 이름 목록이 없어 그 검사는 건너뜀 — PIBO_AUDIT_WORDS=<리포 밖 파일> (AUDIT.md S7)')
  report('S7', '유출(세션 링크·메일·키·업체 이름)', bad, info)


# ── S8 global 델타 ───────────────────────────────────────────────────────
def s8(repos, fetch):
  bad, info = [], []
  for name, repo in repos:
    if fetch:
      git(repo, 'fetch', '-q', 'origin', '+refs/heads/global:refs/remotes/origin/global', '+refs/heads/main:refs/remotes/origin/main')
    m, g = 'origin/main', 'origin/global'
    if not git(repo, 'rev-parse', '--verify', '-q', g).strip():
      bad.append(f'{name}: origin/global 이 없다')
      continue
    ns = git(repo, 'diff', '--name-status', m, g).splitlines()
    names = {l.split('\t')[-1] for l in ns}
    ex = {f for f in names if f.startswith('examples/') and f != 'examples/collect.json'}
    core = names - ex
    if core != DELTA:
      bad.append(f'{name}: 델타가 다르다 — 더 있음 {sorted(core - DELTA)} · 없음 {sorted(DELTA - core)}')
    if len(names) != 16:
      bad.append(f'{name}: 델타 {len(names)}개(16개여야)')
    modes = git(repo, 'diff', '--summary', m, g)
    if 'mode change' in modes:
      bad.append(f'{name}: 모드 차이 {modes.count("mode change")}줄')
    for f in ('ide/static/ko2en.js', 'tools/static/ko2en.js', 'classifier/static/ko2en.js'):
      first = git(repo, 'show', f'{g}:{f}').split('\n', 1)[0].strip()
      if first != "const blang = 'en';":
        bad.append(f'{name}: global {f} 1행 = {first!r}')
      if git(repo, 'show', f'{m}:{f}').split('\n', 1)[0].strip() == "const blang = 'en';":
        bad.append(f'{name}: main {f} 1행이 영문판 값')
    behind = git(repo, 'rev-list', '--count', f'{g}..{m}').strip()
    if behind != '0':
      bad.append(f'{name}: global 이 main 보다 {behind}커밋 뒤(merge 할 것)')
    local = git(repo, 'rev-list', '--count', f'{m}..HEAD').strip()
    if local != '0':
      info.append(f'{name}: 지금 브랜치가 origin/main 보다 {local}커밋 앞(아직 push·merge 안 함)')
  report('S8', 'global 델타 16개·모드 0·ko2en 1행·main 반영', bad, info)


# ── S9 도움말 최신 ───────────────────────────────────────────────────────
def s9(repos):
  bad = []
  for name, repo in repos:
    src = ['docs/source', 'docs/source_en', 'docs/tools', 'openpibo', 'ide/static/ko.js', 'ide/static/en.js',
           'ide/static/customblock.js', 'ide/static/v2/levels.js', 'ide/static/v2/usbcam_block.js']
    s = ctime(repo, '--', *src)
    b = ctime(repo, '--', 'docs/build')
    dirty = [l for l in git(repo, 'status', '--porcelain', '--', *src).splitlines()]
    dirty_b = git(repo, 'status', '--porcelain', '--', 'docs/build').strip()
    if s > b:
      bad.append(f'{name}: 도움말 원본이 마지막 빌드 뒤에 바뀌었다({git(repo, "log", "-1", "--format=%h %cs %s", "--", *src).strip()[:70]}) — bash docs/build.sh')
    if dirty and not dirty_b:
      bad.append(f'{name}: 도움말 원본을 고쳤는데(커밋 전) 빌드 안 함: {", ".join(l[3:] for l in dirty[:4])}')
    py = os.environ.get('PY') or sys.executable   # babel 이 있는 파이썬(도움말 빌드와 같은 PY=)
    r = subprocess.run([py, os.path.join(repo, 'docs/tools/update_po.py'), '--check'], capture_output=True, text=True, cwd=repo)
    out = (r.stdout + r.stderr).strip()
    if r.returncode:
      bad.append(f'{name}: update_po.py --check — {out.splitlines()[-1] if out else r.returncode}')
  report('S9', '도움말 빌드·영문 번역(.po)', bad)


# ── S10 CLAUDE.md 규칙 grep ──────────────────────────────────────────────
def s10(repos):
  bad = []
  for name, repo in repos:
    def grep(pat, globs, why, allow=()):
      for f in files(repo, *globs):
        if SKIP_DIRS.search(f) or f in allow:
          continue
        src = open(os.path.join(repo, f), encoding='utf-8', errors='replace').read()
        for m in re.finditer(pat, src, re.M):
          line = src.count('\n', 0, m.start()) + 1
          text = src.splitlines()[line - 1].strip()
          if text.startswith('#') or text.startswith('//'):
            continue
          bad.append(f'{name}/{f}:{line}: {why}')
    grep(r'https?://[\w.-]*circul\.us', ['*.py', '*.js', '*.html'], '자사 서버(circul.us) — 260914v6 에 다 뺐다')
    grep(r'[\'"]llama-server\.service[\'"]', ['*.py', '*.js'], '예전 llama-server.service — 템플릿 유닛 llama-server@* 로')
    grep(r'TemplateResponse\(\s*["\']', ['*.py'], 'TemplateResponse(이름, …) 옛 순서 — starlette 1.0 에서 500')
    grep(r'sio\.on\(\s*[\'"]connection[\'"]', ['*.py'], "'connection' 은 안 불리는 이름 — 'connect'")
    for f in files(repo, '*.js', '*.html'):
      if SKIP_DIRS.search(f):
        continue
      src = open(os.path.join(repo, f), encoding='utf-8', errors='replace').read()
      for m in re.finditer(r'fetch\([^;]*?enable=off[^;]*?\)', src):
        if 'keepalive' not in m.group(0):
          bad.append(f'{name}/{f}:{src.count(chr(10), 0, m.start()) + 1}: enable=off fetch 에 keepalive 없음(탭을 닫으면 취소된다)')
    # 도움말 대표 주소(html_baseurl)는 그 리포의 GitHub Pages — 예전 리포 이름이 남으면 없는 주소(404)가 된다(261120)
    url = git(repo, 'remote', 'get-url', 'origin').strip()
    rname = re.sub(r'\.git$', '', url.rstrip('/').split('/')[-1])
    m = re.search(r"^html_baseurl\s*=\s*'([^']*)'", open(os.path.join(repo, 'docs/source/conf.py'), encoding='utf-8').read(), re.M)
    if rname and m and m.group(1) != f'https://themakerrobot.github.io/{rname}/':
      bad.append(f'{name}/docs/source/conf.py: html_baseurl {m.group(1)} — https://themakerrobot.github.io/{rname}/ 이어야')
    # 서버(run_ide.py)는 한글 문장이 아니라 키를 보낸다 — 독스트링 말고 문자열에 한글이 있으면 안 된다(주석은 괜찮다)
    import ast
    tree = ast.parse(open(os.path.join(repo, 'ide/run_ide.py'), encoding='utf-8').read())
    docs = set()
    for n in ast.walk(tree):
      body = getattr(n, 'body', None)
      if isinstance(body, list) and body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
         and isinstance(body[0].value.value, str):
        docs.add(id(body[0].value))
    for n in ast.walk(tree):
      if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in docs and re.search(r'[가-힣]', n.value):
        bad.append(f'{name}/ide/run_ide.py:{n.lineno}: 문자열에 한글(서버는 키를 보낸다) {n.value[:30]!r}')
  report('S10', 'CLAUDE.md 규칙(옛 서버·유닛·keepalive·서버 한글)', bad)


# ── S12 docstring :param 이름 = 실제 인자 ────────────────────────────────
def s12(repos):
  import ast
  bad = []
  for name, repo in repos:
    for f in files(repo, 'openpibo/*.py'):
      if SKIP_DIRS.search(f) or '/modules/' in f:
        continue   # modules/ 는 가져온 코드가 많다(teachlab·mtts·oled)
      src = open(os.path.join(repo, f), encoding='utf-8').read()
      for n in ast.walk(ast.parse(src)):
        if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
          continue
        doc = ast.get_docstring(n) or ''
        args = {a.arg for a in n.args.args + n.args.kwonlyargs + n.args.posonlyargs}
        if n.args.vararg: args.add(n.args.vararg.arg)
        if n.args.kwarg: args.add(n.args.kwarg.arg)
        for m in re.finditer(r':param\s+(?:[\w\[\], .|]+\s+)?(\w+)\s*:', doc):
          if m.group(1) not in args:
            bad.append(f'{name}/{f}:{n.lineno}: {n.name}() 설명의 :param {m.group(1)} — 인자에 없다({", ".join(sorted(args - {"self"})) or "인자 없음"})')
  report('S12', 'API 설명(:param)의 이름 = 실제 인자', bad)


# ── S11 남은 작업 표시 ────────────────────────────────────────────────────
def s11(repos):
  info = []
  for name, repo in repos:
    st = git(repo, 'status', '--porcelain').splitlines()
    if st:
      info.append(f'{name}: 커밋 안 한 변경 {len(st)}개 — ' + ', '.join(l[3:] for l in st[:6]) + (' …' if len(st) > 6 else ''))
  report('S11', '작업본 상태(정보)', None, info)


def main():
  args = [a for a in sys.argv[1:] if not a.startswith('--')]
  fetch = '--no-fetch' not in sys.argv
  repos = [('pibo', PIBO)] + ([('pibrain', os.path.abspath(args[0]))] if args else [])
  for f in (s1, s2, s3, s4, s5, s6, s7, s10, s12, s9, s11):
    try:
      f(repos)
    except Exception as e:   # 검사 하나가 죽어도 나머지는 돈다
      report(f.__name__.upper(), f.__name__, [f'검사 오류: {e}'])
  try:
    s8(repos, fetch)
  except Exception as e:
    report('S8', 'global 델타', [f'검사 오류: {e}'])
  RESULTS.sort(key=lambda r: int(re.sub(r'\D', '', r[0]) or 0))
  fails = 0
  for cid, name, st, lines in RESULTS:
    print(f'{st:4} {cid:4} {name}')
    for l in lines[:40]:
      print(f'          {l}')
    if len(lines) > 40:
      print(f'          … {len(lines) - 40}줄 더')
    fails += st == 'FAIL'
  print(f'\n정적 검사: FAIL {fails} / {len(RESULTS)}')
  sys.exit(1 if fails else 0)


if __name__ == '__main__':
  main()
