/* ==========================================================================
   IDE v2 — templates/index_v2.html 전용. index.js 다음에 싣는다.
   index.js 는 고치지 않는다. 여기서는 v2 배치에만 필요한 것을 붙인다.

     1) 레일: 파일·터미널 패널 여닫기 (폭에 따라 처음 상태를 정하고, 누르면 기억)
     2) 펼침 메뉴(<details>): 바깥을 누르거나 Esc 면 닫힌다
     3) 상단바 파일 이름: #codepath(전체 경로, index.js 가 채운다)에서 이름만
     4) 글자 크기 [-][+]
     5) data-ph-key / data-title-key 번역 (index.js 의 setLanguage 는 textContent 만 바꾼다)
     6) 미리보기: 사진·소리 파일을 열었을 때만 파일 패널 아래에 띄운다
     7) 화면 밝기: 어둡게면 파이썬 편집기도 어두운 테마로 (스위치로 바꿀 수 있다)
   ========================================================================== */
(function () {
  'use strict';
  var $id = function (id) { return document.getElementById(id); };
  var tr = function (key) {
    try { var e = translations[key]; return (e && (e[lang] || e.en)) || ''; } catch (err) { return ''; }
  };
  var fire = function () { window.dispatchEvent(new Event('resize')); };

  /* 1) 레일 ─────────────────────────────────────────────────────────────── */
  var KEY = 'pibo_v2_panes';
  var saved = {};
  try { saved = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { saved = {}; }
  // 저장값이 없으면 폭으로 정한다: 파일은 1200px 이상, 터미널은 900px 이상에서 편다
  var DEFAULT = { browser_en: 1200, result_en: 900 };
  var editor = document.querySelector('.v2-editor');

  function setPane(id, open) {
    var pane = $id(id);
    if (!pane) return;
    pane.hidden = !open;
    var bar = document.querySelector('.pb-resizer[data-target="' + id + '"]');
    if (bar) bar.hidden = !open;
    var btn = document.querySelector('[data-v2-pane="' + id + '"]');
    if (btn) btn.setAttribute('aria-pressed', open ? 'true' : 'false');
  }
  Object.keys(DEFAULT).forEach(function (id) {
    var open = (id in saved) ? !!saved[id] : window.innerWidth >= DEFAULT[id];
    setPane(id, open);
  });
  document.addEventListener('click', function (e) {
    var btn = e.target.closest && e.target.closest('[data-v2-pane]');
    if (!btn) return;
    var id = btn.getAttribute('data-v2-pane');
    var open = btn.getAttribute('aria-pressed') !== 'true';
    setPane(id, open);
    // 편 결과 편집기가 너무 좁으면 반대쪽 패널을 접는다
    if (open && editor.getBoundingClientRect().width < 320) {
      setPane(id === 'browser_en' ? 'result_en' : 'browser_en', false);
    }
    saved[id] = open;
    try { localStorage.setItem(KEY, JSON.stringify(saved)); } catch (err) { /* 무시 */ }
    fire();
  });
  // 편집기가 320px 밑으로 좁아지면 파일 → 터미널 순으로 접는다(저장은 안 한다).
  // 태블릿을 세로로 돌리거나 창을 줄일 때 편집기가 사라지지 않게 한다
  function keepEditor() {
    ['browser_en', 'result_en'].forEach(function (id) {
      if (editor.getBoundingClientRect().width < 320 && !$id(id).hidden) setPane(id, false);
    });
  }
  // 패널을 여닫을 때 쏘는 가짜 resize(isTrusted=false)에는 반응하지 않는다
  window.addEventListener('resize', function (e) { if (e.isTrusted) keepEditor(); });
  keepEditor();

  /* 2) 펼침 메뉴 ─────────────────────────────────────────────────────────── */
  var menus = document.querySelectorAll('details.v2-menu');
  document.addEventListener('click', function (e) {
    Array.prototype.forEach.call(menus, function (d) {
      if (!d.open) return;
      if (!d.contains(e.target)) d.open = false;
      // 메뉴 안의 항목(링크·버튼)을 누르면 닫는다. 입력칸·선택·스위치는 그대로 둔다
      else if (e.target.closest('.v2-pop__item') && !e.target.closest('.v2-pop__item--field')) d.open = false;
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    Array.prototype.forEach.call(menus, function (d) {
      if (d.open) { d.open = false; var s = d.querySelector('summary'); if (s) s.focus(); }
    });
  });
  // 한쪽을 열면 다른 쪽은 닫는다
  Array.prototype.forEach.call(menus, function (d) {
    d.addEventListener('toggle', function () {
      if (!d.open) return;
      Array.prototype.forEach.call(menus, function (o) { if (o !== d) o.open = false; });
    });
  });

  /* 3) 파일 이름 ─────────────────────────────────────────────────────────── */
  var cp = $id('codepath'), nameEl = $id('v2_file_name'), fileBox = $id('v2_file');
  function showName() {
    var full = (cp.textContent || '').trim();
    if (!full) {
      nameEl.textContent = tr('v2_no_file');
      fileBox.setAttribute('data-empty', '');
      fileBox.removeAttribute('title');
    } else {
      nameEl.textContent = full.split('/').pop();
      fileBox.removeAttribute('data-empty');
      fileBox.title = full;
    }
  }
  // setLanguage 가 data-key 로 이 칸을 덮어쓰지 않게 키를 뗀다
  nameEl.removeAttribute('data-key');
  new MutationObserver(showName).observe(cp, { childList: true, characterData: true, subtree: true });
  showName();

  /* 4) 글자 크기 ─────────────────────────────────────────────────────────── */
  var fs = $id('fontsize');
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-step]');
    if (!b || !fs) return;
    var v = Math.max(+fs.min || 5, Math.min(+fs.max || 50, (+fs.value || 14) + (+b.getAttribute('data-step'))));
    fs.value = v;
    fs.dispatchEvent(new Event('change', { bubbles: true }));   // index.js 의 jQuery .on('change') 가 받는다
  });

  /* 5) 자리표시·툴팁 번역 ─────────────────────────────────────────────────── */
  function applyExtra() {
    Array.prototype.forEach.call(document.querySelectorAll('[data-ph-key]'), function (el) {
      el.placeholder = tr(el.getAttribute('data-ph-key'));
    });
    Array.prototype.forEach.call(document.querySelectorAll('[data-title-key]'), function (el) {
      var s = tr(el.getAttribute('data-title-key'));
      el.title = s; el.setAttribute('aria-label', s);
    });
    // 아이콘만 남는 폭에서도 뜻이 보이게 라벨을 툴팁으로 복사한다
    Array.prototype.forEach.call(document.querySelectorAll('.v2-top button, .v2-top a.pb-iconbtn'), function (el) {
      var lab = el.querySelector('[data-key]');
      if (lab && lab.textContent) el.title = lab.textContent;
    });
    showName();
  }
  var langSel = $id('language');
  if (langSel) langSel.addEventListener('change', function () { setTimeout(applyExtra, 0); });
  applyExtra();

  /* 6) 미리보기 ─────────────────────────────────────────────────────────── */
  var browser = $id('browser_en');
  function watchMedia(el, kind) {
    new MutationObserver(function () {
      if (el.getAttribute('src')) { browser.setAttribute('data-media', kind); fire(); }
    }).observe(el, { attributes: true, attributeFilter: ['src'] });
  }
  watchMedia($id('image'), 'image');
  watchMedia($id('audio'), 'audio');
  $id('v2_preview_close').addEventListener('click', function () {
    var a = $id('audio'); try { a.pause(); } catch (e) { /* 무시 */ }
    browser.removeAttribute('data-media'); fire();
  });

  /* 7) 화면 밝기 ─────────────────────────────────────────────────────────── */
  var themeCheck = $id('theme_check');
  function editorFollowsTheme(t) {
    if (!themeCheck) return;
    var want = t === 'dark';
    if (want && !themeCheck.checked) { themeCheck.checked = true; themeCheck.dispatchEvent(new Event('change', { bubbles: true })); }
  }
  window.addEventListener('pibo-theme', function (e) { editorFollowsTheme(e.detail); });

  fire();
})();
