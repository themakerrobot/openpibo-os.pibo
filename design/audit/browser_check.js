/* 전수 조사 — 화면 검사(B1~B4). 체크리스트는 리포 맨 위 AUDIT.md. design/audit/run.sh 가 미리보기(design/preview.py)를 띄우고 부른다.

  node design/audit/browser_check.js <PC IP> <PiBrain 리포> <결과 폴더> [--quick] [--only=B2,B3]

  B1 전 화면 × 폭 × 한/영 × 밝기: pageerror 0 · HTTP 오류 0 · 가로 넘침 0 · 영문 화면에 한글 0
  B2 상단바 규칙(AUDIT.md 'B2 상단바 규칙' — 높이·색·이름·버튼 순서·글자·크기)
  B3 예제(국내 main · 영문 global)가 블록으로 열리고 코드가 만들어짐
  B4 사람이 볼 캡처를 결과 폴더에 남김(상단바 모음 · 화면 전체)
  playwright 는 컨테이너에 깔린 것을 쓴다(require('playwright')). 끝 코드: FAIL 이 있으면 1 */
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), cp = require('child_process');

const [IP, PIBRAIN, OUT] = process.argv.slice(2);
const QUICK = process.argv.includes('--quick');
const ONLY = ((process.argv.find(a => a.startsWith('--only=')) || '').slice(7)).toUpperCase().split(',').filter(Boolean);   // 예 --only=B2,B3
const PIBO = path.resolve(__dirname, '..', '..');
fs.mkdirSync(OUT, { recursive: true });
const H = `http://${IP}`;
const PRODUCTS = [['pibo', 18000, 'piBo', PIBO]].concat(PIBRAIN ? [['pibrain', 18100, 'piBrain', path.resolve(PIBRAIN)]] : []);
const APPS = { home: '처음 화면|Home', ide: '코딩|Coding', tools: '도구|Tools', classifier: 'AI 가르치기|Teach AI', chat: '대화|Chat', kids: '로봇 놀이|Robot Play', cards: '카드 코딩|Card coding', docs: '도움말|Help', launch: '' };
function pages() {
  const out = [];
  for (const [p, b, prod] of PRODUCTS) {
    const ide = b + 80;
    // 대문(261123): / 는 첫 화면, IDE 는 /ide
    out.push({ p, prod, app: 'home', url: `${H}:${ide}/` }, { p, prod, app: 'ide', url: `${H}:${ide}/ide` }, { p, prod, app: 'tools', url: `${H}:${b}/` },
      { p, prod, app: 'classifier', url: `${H}:${b + 10}/` }, { p, prod, app: 'chat', url: `${H}:${b + 30}/?ide=${ide}` },
      { p, prod, app: 'kids', url: `${H}:${b + 70}/?ide=${ide}` }, { p, prod, app: 'cards', url: `${H}:${b + 60}/?ide=${ide}` },   // 체험 앱 둘(261123): 로봇 놀이 play/ 50070 · 카드 코딩 cards/ 50060
      { p, prod, app: 'docs', url: `${H}:${b + 88}/build/html/index.html`, en: `${H}:${b + 88}/build/en/index.html` },
      { p, prod, app: 'launch', url: `${H}:${ide}/static/launch.html?svc=tools` });
  }
  return out;
}
// 미리보기에만 있는 빈 곳(로봇 서버가 없어서) — 기기에서는 생기지 않는 요청
const PREVIEW_ONLY = /socket\.io|\/api\/|enable=|favicon|odml|\/device\/|\/cam_list|\/health|\/face\/|\/ez_lists|\/mymotion|\/button_stream/;
const results = [];   // [id, 이름, 상태, 줄들]
function report(id, name, bad, info = []) { results.push([id, name, bad.length ? 'FAIL' : 'OK', bad.concat(info)]); }

async function open(br, url, { w, lang, theme }) {
  const ctx = await br.newContext({ viewport: { width: w, height: w < 500 ? 800 : 768 } });
  await ctx.addCookies([{ name: 'pibo_theme', value: theme, url }]);
  await ctx.addInitScript(l => { try { for (const k of ['language', 'tools_language', 'classifier_language', 'kids_language']) localStorage.setItem(k, l); } catch (e) { /* */ } }, lang);
  const pg = await ctx.newPage(); const errs = [], http = [];
  pg.on('pageerror', e => errs.push(e.message.slice(0, 140)));
  pg.on('response', r => { if (r.status() >= 400 && !PREVIEW_ONLY.test(r.url())) http.push(r.status() + ' ' + r.url().replace(/^https?:\/\/[^/]+/, '')); });
  try { await pg.goto(url, { waitUntil: 'load', timeout: 20000 }); await pg.waitForTimeout(1500); } catch (e) { errs.push('열기 실패 ' + e.message.slice(0, 80)); }
  return { ctx, pg, errs, http };
}

// ── B1 ────────────────────────────────────────────────────────────────
async function b1(br) {
  const bad = []; let n = 0;
  const combos = [];
  const widths = QUICK ? [1366, 820] : [1366, 1024, 820, 390];
  for (const w of widths) for (const lang of ['ko', 'en']) combos.push({ w, lang, theme: 'soft' });
  for (const lang of ['ko', 'en']) combos.push({ w: 1366, lang, theme: 'dark' });
  for (const pgi of pages()) for (const c of combos) {
    const url = c.lang === 'en' && pgi.en ? pgi.en : pgi.url;
    const { ctx, pg, errs, http } = await open(br, url, c); n++;
    const over = await pg.evaluate(() => document.documentElement.scrollWidth - innerWidth).catch(() => -1);
    let ko = [];
    if (c.lang === 'en') {
      ko = await pg.evaluate(() => {
        let t = (document.body ? document.body.innerText : '').replace(/한국어/g, '');
        // 사용자 자료(대문 [이어서 하기] 의 파일·모델 이름 — data-user)는 사람이 지은 이름이라 뺀다
        document.querySelectorAll('[data-user]').forEach(e => { t = t.split(e.innerText).join(''); });
        return (t.match(/[가-힣][가-힣 ]*/g) || []).slice(0, 4);
      }).catch(() => []);
    }
    const tag = `${pgi.p}/${pgi.app} ${c.w} ${c.lang} ${c.theme}`;
    if (errs.length) bad.push(`${tag}: pageerror ${errs[0]}`);
    if (http.length) bad.push(`${tag}: HTTP ${http.slice(0, 3).join(', ')}`);
    if (over > 0) bad.push(`${tag}: 가로 넘침 ${over}px`);
    if (ko.length) bad.push(`${tag}: 영문 화면에 한글 ${ko.join(' / ')}`);
    if (c.w === 1366 && c.theme === 'soft') await pg.screenshot({ path: path.join(OUT, `page_${pgi.p}_${pgi.app}_${c.lang}.png`) }).catch(() => {});
    await ctx.close();
  }
  report('B1', `전 화면 오류·넘침·영문 한글(${n}번 열기)`, bad);
}

// ── B2 상단바 ─────────────────────────────────────────────────────────
async function b2(br) {
  const bad = [];
  const ref = {};
  const names = {};   // 제품/언어 → { home: {앱: 대문 카드 이름}, 앱: 상단바 앱 이름 }
  for (const w of [1366, 820]) for (const lang of ['ko', 'en']) {
    const strips = [];
    for (const pgi of pages()) {
      const url = lang === 'en' && pgi.en ? pgi.en : pgi.url;
      const { ctx, pg } = await open(br, url, { w, lang, theme: 'soft' });
      const d = await pg.evaluate(() => {
        const h = document.querySelector('header.pb-header, header.pb-topbar');
        if (!h) return null;
        const vis = e => { if (!e) return false; const r = e.getBoundingClientRect(), s = getComputedStyle(e); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
        const box = e => { const r = e.getBoundingClientRect(); return { x: Math.round(r.left), w: Math.round(r.width), h: Math.round(r.height) }; };
        const label = e => {   // 아이콘 말고 보이는 글자
          if (!e) return null;
          const spans = [...e.querySelectorAll('span')].filter(s => !s.querySelector('svg,i') && s.textContent.trim());
          const s = spans.find(vis); if (!s) return '';
          const cs = getComputedStyle(s); return { text: s.textContent.trim(), fs: cs.fontSize, fw: cs.fontWeight };
        };
        const pick = sel => { const e = [...h.querySelectorAll(sel)].find(vis); return e || null; };
        const std = { help: pick('#pb_help_bt'), home: pick('#home_bt, .pb-topbar__home'), fs: pick('#fullscreen_bt, .pb-topbar__fs'),
          theme: pick('#pb_theme_bt, #theme_bt, .pb-topbar__theme'), lang: pick('select') };
        const cs = getComputedStyle(h);
        const brand = h.querySelector('.pb-header__brand, .v2-brand, .pb-topbar__brand');
        const btns = [...h.querySelectorAll('a.pb-iconbtn, button.pb-iconbtn, .tl-hbtn, .pb-topbar__btn, #fullscreen_bt, #home_bt')].filter(vis);
        const out = { h: Math.round(h.getBoundingClientRect().height), bg: cs.backgroundColor, bb: cs.borderBottomWidth,
          brand: brand ? brand.innerText.replace(/\s+/g, ' ').trim() : '', title: document.title, std: {},
          heights: [...new Set(btns.map(b => Math.round(b.getBoundingClientRect().height)))] };
        for (const k in std) out.std[k] = std[k] ? Object.assign(box(std[k]), { label: k === 'lang' ? null : label(std[k]) }) : null;
        // 표준 버튼보다 오른쪽에 있는 다른 버튼(앱 동작은 [처음 화면] 왼쪽에 둔다)
        const homeX = std.home ? std.home.getBoundingClientRect().left : 1e9;
        out.rightExtra = btns.filter(b => !Object.values(std).includes(b) && b.getBoundingClientRect().left > homeX).map(b => b.id || b.className.split(' ')[0]);
        // 대문 카드 이름 — 각 앱 상단바의 앱 이름과 같아야 한다(261123 — 전엔 IDE 상단바의 앱 버튼 글자와 견줬다)
        const CARD = { code: 'ide', tools: 'tools', classifier: 'classifier', llm: 'chat', cards: 'cards', play: 'kids', guide: 'docs' };
        out.cards = {};
        document.querySelectorAll('.home-app[data-app]').forEach(a => { const k = CARD[a.getAttribute('data-app')], b = a.querySelector('b'); if (k && b) out.cards[k] = b.textContent.trim(); });
        const appEl = brand && brand.querySelector('.pb-header__app, .pb-topbar__app');
        out.appName = appEl ? appEl.textContent.trim() : '';
        return out;
      }).catch(e => ({ err: e.message }));
      const tag = `${pgi.p}/${pgi.app} ${w} ${lang}`;
      const hdr = await pg.$('header.pb-header, header.pb-topbar');
      if (hdr) { const f = path.join(OUT, `hdr_${pgi.p}_${pgi.app}_${w}_${lang}.png`); await hdr.screenshot({ path: f }).catch(() => {}); strips.push(f); }
      await ctx.close();
      if (!d || d.err) { bad.push(`${tag}: 상단바를 못 찾음 ${d && d.err || ''}`); continue; }
      if (w === 1366) { const k = `${pgi.p}/${lang}`; (names[k] = names[k] || {})[pgi.app] = pgi.app === 'home' ? d.cards : d.appName; }
      if (!ref.bg) ref.bg = d.bg;
      if (d.h !== 48) bad.push(`${tag}: 높이 ${d.h}px(48)`);
      if (d.bb !== '1px') bad.push(`${tag}: 아래 선 ${d.bb}(1px)`);
      if (d.bg !== ref.bg) bad.push(`${tag}: 바탕 ${d.bg}(다른 앱 ${ref.bg})`);
      const appRe = APPS[pgi.app];
      if (pgi.app !== 'launch') {
        if (!new RegExp(`^${pgi.prod}( \\.\\d+)? · (${appRe})$`).test(d.title)) bad.push(`${tag}: 탭 제목 '${d.title}'(${pgi.prod} .IP끝 · 앱)`);   // 261125 — 탭이 좁아도 기기를 가르게 제품 + IP 끝자리를 앞에
        const bn = d.brand.replace(/\s+/g, '');
        if (pgi.app === 'home') { if (bn !== pgi.prod) bad.push(`${tag}: 왼쪽 이름 '${d.brand}'(대문은 제품 이름만)`); }
        else if (!new RegExp(`^${pgi.prod}·?(${appRe.replace(/ /g, '')})$`).test(bn))   // 가운데 점은 CSS ::before 라 글자에 없을 수 있다
          bad.push(`${tag}: 왼쪽 이름 '${d.brand}'(${pgi.prod} · 앱)`);
      }
      if (pgi.app === 'launch') continue;   // 대기 페이지는 예외(AUDIT.md B2). IDE 도 261123 부터 같은 규칙
      const s = d.std;
      for (const k of ['home', 'fs', 'theme']) if (!s[k] && !(k === 'home' && pgi.app === 'home')) bad.push(`${tag}: ${k} 버튼 없음`);   // 대문은 [처음 화면] 이 없다(자기가 처음 화면)
      if (!s.lang) bad.push(`${tag}: 언어 select 없음`);
      // [사용법](261126): 앱 화면(대문·도움말 빼고)은 [처음 화면] 바로 왼쪽에 하나
      const HELP_APPS = ['ide', 'tools', 'classifier', 'chat', 'kids', 'cards'];
      if (HELP_APPS.includes(pgi.app) && !s.help) bad.push(`${tag}: [사용법] 버튼 없음`);
      if (!HELP_APPS.includes(pgi.app) && s.help) bad.push(`${tag}: [사용법] 버튼이 있으면 안 됨`);
      const order = ['help', 'home', 'fs', 'theme', 'lang'].filter(k => s[k]);
      for (let i = 1; i < order.length; i++) if (s[order[i]].x <= s[order[i - 1]].x) bad.push(`${tag}: 순서 ${order[i - 1]} → ${order[i]} 가 아님`);
      const extra = d.rightExtra;
      if (extra.length) bad.push(`${tag}: [처음 화면] 오른쪽에 다른 버튼 ${extra.join(',')}(앱 동작은 [처음 화면] 왼쪽)`);
      if (d.heights.some(x => x !== 32)) bad.push(`${tag}: 버튼 높이 ${d.heights.join('/')}(32)`);
      for (const k of ['help', 'home', 'fs', 'theme']) {
        if (!s[k]) continue;
        const L = s[k].label;
        if (w >= 1000) {
          if (!L) bad.push(`${tag}: ${k} 글자 없음`);
          else if (L.fs !== '13px' || !(+L.fw >= 700)) bad.push(`${tag}: ${k} 글자 ${L.fs}/${L.fw}(13px/700)`);
        } else if (L) bad.push(`${tag}: ${k} 글자 '${L.text}' — 999px 이하는 아이콘만`);
      }
    }
    // 상단바 모음 한 장(사람이 눈으로 — B4)
    try {
      const py = `
import sys
from PIL import Image, ImageDraw
fs = sys.argv[2:]; ims = [Image.open(f) for f in fs]
W = max(i.width for i in ims); H = sum(i.height + 18 for i in ims)
o = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(o); y = 0
for f, i in zip(fs, ims):
    d.text((4, y + 3), f.rsplit('/', 1)[-1], fill='black'); y += 18; o.paste(i, (0, y)); y += i.height
o.save(sys.argv[1])`;
      cp.execFileSync(process.env.PY || 'python3', ['-c', py, path.join(OUT, `headers_${w}_${lang}.png`), ...strips], { stdio: 'ignore' });
      strips.forEach(f => fs.unlinkSync(f));
    } catch (e) { /* PIL 이 없으면 낱장으로 둔다 */ }
  }
  for (const k in names) {
    const cards = names[k].home || {};
    for (const app of ['ide', 'tools', 'chat', 'classifier', 'kids', 'cards', 'docs']) {
      if (cards[app] && names[k][app] !== undefined && cards[app] !== names[k][app])
        bad.push(`${k}: 대문 카드 '${cards[app]}' ≠ ${app} 상단바 이름 '${names[k][app]}'(같은 이름이어야)`);
    }
  }
  report('B2', '상단바 규칙(높이·색·이름·순서·글자·크기·대문 카드 = 앱 이름)', bad);
}

// ── B3 예제 ───────────────────────────────────────────────────────────
function exampleSets(repo) {
  const sets = [];
  const main = fs.readdirSync(path.join(repo, 'examples')).filter(f => f.endsWith('.json')).map(f => [f, fs.readFileSync(path.join(repo, 'examples', f), 'utf8')]);
  sets.push(['main', 'ko', main]);
  try {
    const ls = cp.execFileSync('git', ['-C', repo, 'ls-tree', '--name-only', 'origin/global', 'examples/']).toString().split('\n').filter(f => f.endsWith('.json'));
    sets.push(['global', 'en', ls.map(f => [path.basename(f), cp.execFileSync('git', ['-C', repo, 'show', `origin/global:${f}`]).toString()])]);
  } catch (e) { /* origin/global 없음 */ }
  return sets;
}
async function b3(br) {
  const bad = []; let n = 0;
  for (const [p, b, , repo] of PRODUCTS) for (const [set, lang, list] of exampleSets(repo)) {
    const ctx = await br.newContext();
    await ctx.addInitScript(`try{localStorage.setItem('language','${lang}')}catch(e){}`);
    await ctx.route('**/socket.io.min.js*', r => r.fulfill({ status: 200, contentType: 'application/javascript', body: 'window.io=function(){return {on(){},emit(){},connected:false}}' }));
    const pg = await ctx.newPage(); const errs = []; pg.on('pageerror', e => errs.push(e.message));
    await pg.goto(`${H}:${b + 80}/ide`);
    await pg.waitForFunction("typeof Blockly!=='undefined' && typeof toolbox_dict!=='undefined' && Blockly.Msg && Object.keys(Blockly.Msg).length>500", null, { timeout: 30000 });
    await pg.waitForTimeout(800);
    for (const [f, txt] of list) {
      n++;
      const r = await pg.evaluate((j) => {
        const types = new Set(); (function walk(o) { if (o && typeof o === 'object') { if (typeof o.type === 'string' && o.type && o.id && o.name === undefined) types.add(o.type); /* 블록 객체만(변수 정의 {name,id,type:''}·필드 이름 type 제외) */ for (const k in o) walk(o[k]); } })(j);
        const unknown = [...types].filter(t => !Blockly.Blocks[t]);
        const ws = new Blockly.Workspace(); let err = '', code = ''; const warn = [];
        const ow = console.warn; console.warn = (...a) => warn.push(a.join(' '));
        try { Blockly.serialization.workspaces.load(j, ws); code = Blockly.Python.workspaceToCode(ws); } catch (e) { err = e.message; }
        console.warn = ow; const k = ws.getAllBlocks(false).length; ws.dispose();
        return { unknown, err, k, code: code.length, warn: warn.slice(0, 2) };
      }, JSON.parse(txt));
      if (r.unknown.length || r.err || !r.k || !r.code || r.warn.length)
        bad.push(`${p}/${set}/${f}: ${r.unknown.length ? '없는 블록 ' + r.unknown.join(',') : ''}${r.err ? ' 오류 ' + r.err.slice(0, 100) : ''}${r.warn.length ? ' 경고 ' + r.warn.join(' | ').slice(0, 120) : ''}${!r.k ? ' 블록 0' : ''}`);
    }
    if (errs.length) bad.push(`${p}/${set}: pageerror ${errs[0].slice(0, 120)}`);
    await ctx.close();
  }
  report('B3', `예제 열기·코드 만들기(${n}개)`, bad);
}

(async () => {
  const br = await chromium.launch({ args: ['--no-proxy-server'] });
  for (const f of [b2, b3, b1]) {
    if (ONLY.length && !ONLY.includes(f.name.toUpperCase())) continue;
    try { await f(br); } catch (e) { report(f.name.toUpperCase(), f.name, ['검사 오류: ' + e.message.slice(0, 200)]); }
  }
  await br.close();
  results.push(['B4', `사람이 볼 캡처 → ${OUT}`, 'INFO', ['headers_<폭>_<언어>.png(상단바 모음) · page_<제품>_<앱>_<언어>.png(1366 화면 전체)']]);
  results.sort((a, b) => a[0].localeCompare(b[0]));
  let fails = 0;
  for (const [id, name, st, lines] of results) {
    console.log(`${st.padEnd(4)} ${id.padEnd(4)} ${name}`);
    lines.slice(0, 40).forEach(l => console.log('          ' + l));
    if (lines.length > 40) console.log(`          … ${lines.length - 40}줄 더`);
    if (st === 'FAIL') fails++;
  }
  console.log(`\n화면 검사: FAIL ${fails} / ${results.length - 1}`);
  process.exit(fails ? 1 : 0);
})();
