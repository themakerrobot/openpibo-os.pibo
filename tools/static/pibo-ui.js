/* ==========================================================================
   Pibo UI Kit — 셸 동작  (openpibo-os.pibo / .pibrain 공용)

   빌드 없음. pibo-ui.css 와 짝이다.

     <script src="../static/pibo-ui.js?ver=YYMMDDvN"></script>

   하는 일은 둘뿐이다.
     1) .pb-resizer 를 드래그해 양옆 패널 폭 조절 + localStorage 기억
     2) 패널 폭이 바뀌면 window 에 resize 를 쏜다
        (Blockly 의 svgResize 가 window.onresize 에 물려 있어서 그걸 그대로 탄다)

   원본은 design/pibo-ui.js 하나뿐이다. static/ 쪽 사본은 design/sync.sh 가 만든다.
   ========================================================================== */
(function () {
  'use strict';

  var KEY = 'pibo_panes';
  var MIN = 160;          // 패널 최소 폭
  var MIN_GROW = 320;     // 가운데(늘어나는) 패널이 지켜야 할 최소 폭

  function load() {
    try { return JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { return {}; }
  }
  function save(o) {
    try { localStorage.setItem(KEY, JSON.stringify(o)); } catch (e) { /* 사생활 보호 모드 */ }
  }

  /* 패널 폭은 CSS 변수로 둔다. 앱 CSS 가 flex-basis 로 받아 쓴다:
       #result_en { flex: 0 0 var(--pane-term); }                              */
  function applyWidth(name, px) {
    document.documentElement.style.setProperty('--pane-' + name, px + 'px');
  }

  function fireResize() {
    window.dispatchEvent(new Event('resize'));
  }

  function init() {
    var saved = load();
    Object.keys(saved).forEach(function (k) { applyWidth(k, saved[k]); });

    var bars = document.querySelectorAll('.pb-resizer');
    Array.prototype.forEach.call(bars, function (bar) {
      var name = bar.getAttribute('data-pane');       // --pane-<name> 을 조절한다
      var side = bar.getAttribute('data-side') || 'left';  // 어느 쪽 패널을 키우나
      if (!name) return;

      var target = document.getElementById(bar.getAttribute('data-target') || '');
      // 패널마다 최소 폭이 다르다. 버튼이 한 줄에 들어가는 폭 밑으로는 못 줄인다
      var minW = parseInt(bar.getAttribute('data-min'), 10) || MIN;
      var startX = 0, startW = 0, raf = 0;

      function onMove(e) {
        var x = (e.touches ? e.touches[0].clientX : e.clientX);
        var dx = x - startX;
        var w = startW + (side === 'left' ? dx : -dx);

        // 가운데 패널이 너무 좁아지지 않게 막는다
        var panes = bar.parentNode;
        var room = panes ? panes.getBoundingClientRect().width : window.innerWidth;
        var others = 0;
        Array.prototype.forEach.call(panes.children, function (ch) {
          if (ch !== target && ch.classList &&
              ch.classList.contains('pb-pane') &&
              !ch.classList.contains('pb-pane--grow')) {
            others += ch.getBoundingClientRect().width;
          }
        });
        var max = room - others - MIN_GROW;
        w = Math.max(minW, Math.min(w, Math.max(minW, max)));

        if (raf) return;
        raf = requestAnimationFrame(function () {
          raf = 0;
          applyWidth(name, Math.round(w));
          fireResize();
        });
        if (e.cancelable) e.preventDefault();
      }

      function onUp() {
        bar.removeAttribute('data-dragging');
        document.removeEventListener('pointermove', onMove);
        document.removeEventListener('pointerup', onUp);
        document.body.style.userSelect = '';
        var cur = getComputedStyle(document.documentElement)
                    .getPropertyValue('--pane-' + name).trim();
        var px = parseInt(cur, 10);
        if (px) { var o = load(); o[name] = px; save(o); }
        fireResize();
      }

      bar.addEventListener('pointerdown', function (e) {
        if (!target) return;
        startX = e.clientX;
        startW = target.getBoundingClientRect().width;
        bar.setAttribute('data-dragging', '1');
        document.body.style.userSelect = 'none';
        document.addEventListener('pointermove', onMove);
        document.addEventListener('pointerup', onUp);
        bar.setPointerCapture && bar.setPointerCapture(e.pointerId);
        e.preventDefault();
      });

      // 더블클릭이면 기본값으로 되돌린다
      bar.addEventListener('dblclick', function () {
        document.documentElement.style.removeProperty('--pane-' + name);
        var o = load(); delete o[name]; save(o);
        fireResize();
      });
    });

    /* 패널을 접었다 펴는 버튼:  <button data-toggle-pane="result_en"> */
    document.addEventListener('click', function (e) {
      var btn = e.target.closest && e.target.closest('[data-toggle-pane]');
      if (!btn) return;
      var el = document.getElementById(btn.getAttribute('data-toggle-pane'));
      if (!el) return;
      var on = el.getAttribute('data-force-show') === '1';
      if (on) el.removeAttribute('data-force-show');
      else el.setAttribute('data-force-show', '1');
      btn.setAttribute('aria-pressed', on ? 'false' : 'true');
      fireResize();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
