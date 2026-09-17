// 리포에서 매뉴얼용 데이터를 뽑는다.
//   node extract.cjs <작업디렉토리>
// 작업디렉토리에는 build.sh 가 미리 넣어둔 소스 사본이 있어야 한다:
//   toolbox.js  ko2en.js  msgs.js   (msgs.js = en.js 또는 ko.js)
// 결과: msg.json (Blockly.Msg), cats.json (카테고리별 블록), motions.txt
'use strict';
const fs = require('fs');
const path = require('path');

const DIR = process.argv[2];
if (!DIR) { console.error('usage: node extract.cjs <workdir>'); process.exit(1); }
const p = (f) => path.join(DIR, f);
const LANG = process.argv[3] || 'en';

// ── Blockly.Msg 사전
const msgSrc = fs.readFileSync(p('msgs.js'), 'utf8');
const MSG = {};
for (const m of msgSrc.matchAll(/Blockly\.Msg\["([A-Z0-9_]+)"\]\s*=\s*("(?:[^"\\]|\\.)*")/g)) {
  try { MSG[m[1]] = JSON.parse(m[2]); } catch (e) { /* 건너뛴다 */ }
}

// ── 툴박스: translations / color_type / lang 만 있으면 평가된다
const ko2en = fs.readFileSync(p('ko2en.js'), 'utf8');
const { translations } = new Function(`
  ${ko2en.replace(/localStorage\.getItem\([^)]*\)/g, 'null')}
  return { translations: typeof translations !== 'undefined' ? translations : {} };
`)();
const color_type = new Proxy({}, { get: () => '#888888' });
const toolbox = new Function('translations', 'color_type', 'lang', `
  ${fs.readFileSync(p('toolbox.js'), 'utf8')}
  return toolbox(lang);
`)(translations, color_type, LANG);

const walk = (c, acc = []) => {
  for (const it of (c.contents || [])) {
    if (it.kind === 'block' && it.type) acc.push(it.type);
    if (it.contents) walk(it, acc);
  }
  return acc;
};
const cats = toolbox.contents
  .filter((c) => c.kind === 'category')
  .map((c) => ({ name: c.name, blocks: [...new Set(walk(c))] }));

// ── 기본 모션 이름: customblock.js 의 motion_set_motion_dropdown 옵션
let motions = [];
if (fs.existsSync(p('customblock.js'))) {
  const src = fs.readFileSync(p('customblock.js'), 'utf8');
  const i = src.indexOf("type: 'motion_set_motion_dropdown'");
  if (i >= 0) {
    // options 배열의 끝까지 — 첫 ']' 는 옵션 한 쌍의 닫는 괄호라 쓸 수 없다.
    const o = src.indexOf('"options"', i);
    const seg = src.slice(o, o + 6000);
    motions = [...new Set(
      [...seg.matchAll(/\[\s*'([a-z_0-9]+)'\s*,\s*'\1'\s*\]/g)].map((m) => m[1])
    )].sort();
  }
}

fs.writeFileSync(p('msg.json'), JSON.stringify(MSG, null, 1));
fs.writeFileSync(p('cats.json'), JSON.stringify(cats, null, 1));
fs.writeFileSync(p('motions.txt'), motions.join('\n') + '\n');

const nBlocks = cats.reduce((a, c) => a + c.blocks.length, 0);
console.log(`  Blockly.Msg ${Object.keys(MSG).length} / 카테고리 ${cats.length} / 블록 ${nBlocks} / 모션 ${motions.length}`);
