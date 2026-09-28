let fullscreen = false;

const fullscreenTxt = document.getElementById('fullscreen_txt');
const fullscreenBt = document.getElementById('fullscreen_bt');

const updateIcon = function () {
  fullscreenTxt.innerHTML = fullscreen
    ? '<i class="fa-solid fa-minimize"></i>'
    : '<i class="fa-solid fa-maximize"></i>';
};

updateIcon(); // 초기 아이콘 설정

fullscreenBt.addEventListener('click', (e) => {
  e.preventDefault(); // <a> 태그 기본 동작 방지

  if (!fullscreen && document.documentElement.requestFullscreen) {
    document.documentElement.requestFullscreen();
    fullscreen = true;
  } else if (fullscreen && document.exitFullscreen) {
    document.exitFullscreen();
    fullscreen = false;
  }

  updateIcon();
});

const motor_default = [0, 0, -80, 0, 0, 0, 0, 0, 80, 0];

// 사용자가 ESC 등으로 fullscreen 종료했을 때 아이콘 동기화
document.addEventListener('fullscreenchange', function () {
  fullscreen = !!document.fullscreenElement;
  updateIcon();
});

// --- Get references to popup elements (using provided IDs) ---
const alertPopup = document.getElementById('alertPopup');
const confirmPopup = document.getElementById('confirmPopup');
const promptPopup = document.getElementById('promptPopup');

// --- Get references to internal elements (using NEW specific IDs) ---
// Alert elements
const alertMessageElement = document.getElementById('alertMessageElement');
const alertOkBtn = document.getElementById('alertOkBtn');

// Confirm elements
const confirmMessageElement = document.getElementById('confirmMessageElement');
const confirmOkBtn = document.getElementById('confirmOkBtn');
const confirmCancelBtn = document.getElementById('confirmCancelBtn');

// Prompt elements
const promptMessageElement = document.getElementById('promptMessageElement');
const promptInputElement = document.getElementById('promptInputElement');
const promptOkBtn = document.getElementById('promptOkBtn');
const promptCancelBtn = document.getElementById('promptCancelBtn');

// --- Helper to hide all popups ---
function hidePopups() {
  if (alertPopup) alertPopup.style.display = 'none';
  if (confirmPopup) confirmPopup.style.display = 'none';
  if (promptPopup) promptPopup.style.display = 'none';
}

// --- alert_popup Function (변경 없음) ---
async function alert_popup(message) {
  hidePopups();
  if (!alertPopup || !alertMessageElement || !alertOkBtn) {
    console.error("Alert popup elements not found!");
    return;
  }
  alertMessageElement.textContent = message;
  alertPopup.style.display = 'flex';
  alertOkBtn.focus();

  // --- Use addEventListener with { once: true } for robust cleanup ---
  const handler = function () {
    hidePopups();
  };
  // Remove previous listener just in case, before adding a new one
  alertOkBtn.removeEventListener('click', handler);
  alertOkBtn.addEventListener('click', handler, { once: true }); // Automatically removes after firing
}

// --- confirm_popup Function (수정됨) ---
async function confirm_popup(message) {
  //console.log("confirm_popup: 함수 시작, 메시지:", message); // 디버깅 로그
  return new Promise((resolve) => {
    hidePopups(); // 다른 팝업 숨기기

    // 요소 확인 (중요!)
    const popupElement = document.getElementById('confirmPopup');
    const msgElement = document.getElementById('confirmMessageElement');
    const okButton = document.getElementById('confirmOkBtn');
    const cancelButton = document.getElementById('confirmCancelBtn');

    if (!popupElement || !msgElement || !okButton || !cancelButton) {
      console.error("confirm_popup: 필수 요소를 찾을 수 없습니다!", { popupElement, msgElement, okButton, cancelButton });
      resolve(false); // 요소를 찾을 수 없으면 즉시 false 반환 (오류 상황)
      return;
    }
    //console.log("confirm_popup: 요소 찾음:", { popupElement, msgElement, okButton, cancelButton }); // 디버깅 로그

    msgElement.textContent = message;
    popupElement.style.display = 'flex'; // 팝업 표시
    //console.log("confirm_popup: 팝업 표시됨. 사용자 입력 대기 중..."); // 디버깅 로그
    okButton.focus();

    // --- 이벤트 핸들러 정의 ---
    const okHandler = function () {
      //console.log("confirm_popup: 확인 버튼 클릭됨"); // 디버깅 로그
      cleanup();
      resolve(true); // Promise를 true로 완료
    };

    const cancelHandler = function () {
      //console.log("confirm_popup: 취소 버튼 클릭됨"); // 디버깅 로그
      cleanup();
      resolve(false); // Promise를 false로 완료
    };

    // --- 리스너 정리 함수 ---
    // 이 함수는 버튼이 클릭될 때 호출되어 리스너를 제거하고 팝업을 숨김
    const cleanup = function () {
      //console.log("confirm_popup: 리스너 정리 및 팝업 숨김"); // 디버깅 로그
      okButton.removeEventListener('click', okHandler);
      cancelButton.removeEventListener('click', cancelHandler);
      hidePopups();
    };

    // --- 중요: 기존 리스너 제거 후 새 리스너 추가 ---
    // 이전에 추가된 리스너가 남아있을 수 있으므로, 항상 새로 추가하기 전에 제거
    okButton.removeEventListener('click', okHandler);
    cancelButton.removeEventListener('click', cancelHandler);

    // 새 리스너 추가
    okButton.addEventListener('click', okHandler);
    cancelButton.addEventListener('click', cancelHandler);
    //console.log("confirm_popup: 이벤트 리스너 추가됨"); // 디버깅 로그

    // 이 시점에서는 resolve()가 호출되지 않음! 핸들러 내부에서만 호출됨.
  });
}

// --- prompt_popup Function (리스너 관리 강화) ---
async function prompt_popup(message, defaultValue = '') {
  //console.log("prompt_popup: 함수 시작, 메시지:", message); // 디버깅 로그
  return new Promise((resolve) => {
    hidePopups();

    const popupElement = document.getElementById('promptPopup');
    const msgElement = document.getElementById('promptMessageElement');
    const inputElement = document.getElementById('promptInputElement');
    const okButton = document.getElementById('promptOkBtn');
    const cancelButton = document.getElementById('promptCancelBtn');

    if (!popupElement || !msgElement || !inputElement || !okButton || !cancelButton) {
      console.error("prompt_popup: 필수 요소를 찾을 수 없습니다!", { popupElement, msgElement, inputElement, okButton, cancelButton });
      resolve(null); // 오류 시 null 반환
      return;
    }
    //console.log("prompt_popup: 요소 찾음:", { popupElement, msgElement, inputElement, okButton, cancelButton }); // 디버깅 로그

    msgElement.textContent = message;
    inputElement.value = defaultValue;
    popupElement.style.display = 'flex';
    inputElement.focus(); // 입력 필드에 포커스
    //console.log("prompt_popup: 팝업 표시됨. 사용자 입력 대기 중..."); // 디버깅 로그

    const okHandler = function () {
      //console.log("prompt_popup: 확인 버튼 클릭됨"); // 디버깅 로그
      cleanup();
      resolve(inputElement.value); // 입력된 값으로 완료
    };

    const cancelHandler = function () {
      //console.log("prompt_popup: 취소 버튼 클릭됨"); // 디버깅 로그
      cleanup();
      resolve(null); // 취소 시 null로 완료
    };

    const enterKeyHandler = (event) => {
      if (event.key === 'Enter') {
        //console.log("prompt_popup: Enter 키 입력됨"); // 디버깅 로그
        okHandler(); // 확인 버튼 클릭과 동일하게 처리
      }
    };

    const cleanup = function () {
      //console.log("prompt_popup: 리스너 정리 및 팝업 숨김"); // 디버깅 로그
      okButton.removeEventListener('click', okHandler);
      cancelButton.removeEventListener('click', cancelHandler);
      inputElement.removeEventListener('keydown', enterKeyHandler);
      hidePopups();
    };

    // 기존 리스너 제거
    okButton.removeEventListener('click', okHandler);
    cancelButton.removeEventListener('click', cancelHandler);
    inputElement.removeEventListener('keydown', enterKeyHandler);

    // 새 리스너 추가
    okButton.addEventListener('click', okHandler);
    cancelButton.addEventListener('click', cancelHandler);
    inputElement.addEventListener('keydown', enterKeyHandler);
    //console.log("prompt_popup: 이벤트 리스너 추가됨"); // 디버깅 로그
  });
}

document.getElementById("logo_bt").addEventListener("click", function () {
  location.href = `http://${location.hostname}`;
});
const socket = io(`http://${location.host}`, { path: "/socket.io" });

const onoffVal = document.getElementById('onoff_val');
const onoffCount = document.getElementById('onoff_count'); 
onoffVal.innerHTML = `<i class="fas fa-toggle-off fa-sm fa-fade" style="--fa-animation-duration: 2s; --fa-fade-opacity: 0.6">&nbsp;off</i>`;
// v2 화면은 'off 1' 대신 상태 칩을 그린다(pibo-ui.css). 글자는 여기서 번역해 data-label 로 넘긴다
const setRobotState = (on) => {
  onoffVal.dataset.state = on ? 'on' : 'off';
  onoffVal.dataset.label = t(on ? 'robot_ready' : 'robot_waiting');
};
setRobotState(false);

let onoff_count = 0;
let onoff_intv = setInterval(() => {
  onoffCount.innerHTML = `<i style="opacity:0.6">${++onoff_count}</i>`;
}, 2000);

setInterval(() => {
  socket.emit("onoff");
}, 5000);

socket.on("onoff", function (data) {
  setRobotState(!!data);
  onoffVal.innerHTML = data?
    `<i class="fas fa-toggle-on">&nbsp;on</i>`
    : `<i class="fas fa-toggle-off fa-sm fa-fade" style="--fa-animation-duration: 2s; --fa-fade-opacity: 0.6">&nbsp;off</i>`
  console.log('onoff', data)

  if (data == true) {
    socket.emit("disp_motion");
    clearInterval(onoff_intv);
    onoffCount.innerHTML = "";
    for (let i = 0; i < 10; i++) {
      $("#m" + i + "_value").val(motor_default[i]);
      $("#m" + i + "_range").val(motor_default[i]);
    }
    socket.emit("set_motors", { pos_lst: motor_default });
  }
});

const getVisions = (socket) => {
  $("#v_img").on("click", (evt) => {
    let rect = evt.target.getBoundingClientRect();
    x = Math.floor(evt.clientX - rect.left);
    y = Math.floor(evt.clientY - rect.top);
    w = Math.floor(rect.right - rect.left);
    h = Math.floor(rect.bottom - rect.top);
    cx = Math.floor((640 * x) / w);
    cy = Math.floor((480 * y) / h);

    x1 = cx<100?0:cx-100;
    y1 = cy<100?0:cy-100;
    x2 = x1+200>640?640:x1+200;
    y2 = y1+200>480?480:y1+200;

    socket.emit("object_tracker_init", {x1:x1,y1:y1, x2:x2, y2:y2});
  });

  let img_x = 0;
  let img_y = 0;
  $("#v_img").on("mousemove", (evt) => {
    let rect = evt.target.getBoundingClientRect();

    x = Math.floor(evt.clientX - rect.left);
    y = Math.floor(evt.clientY - rect.top);
    w = Math.floor(rect.right - rect.left);
    h = Math.floor(rect.bottom - rect.top);
    cx = Math.floor((640 * x) / w);
    cy = Math.floor((480 * y) / h);

    cx = cx<0?0:cx;
    cx = cx>640?640:cx;
    cy = cy<0?0:cy;
    cy = cy>480?480:cy;

    if (Math.abs(img_x - cx) > 10 || Math.abs(img_y - cy) > 10 ) {
      socket.emit('update_img_pointer', {x:cx, y:cy})
      img_x = cx;
      img_y = cy;
    }
  });

  // v2 화면: 비전 기능을 select 대신 타일로 고른다(select 는 그대로 두고 값만 맞춘다 — v1 은 select 그대로).
  // 마커 길이 칸은 마커일 때만 보이게 article 에 지금 기능을 적어 둔다(data-func)
  const V_ICON = {
    camera: "camera", grayscale: "circle-half-stroke", canny: "pen", cartoon: "palette", sketch_rgb: "pencil",
    detail: "magnifying-glass-plus", edgePreservingFilter: "water", qr: "qrcode", face: "face-smile",
    face_landmark: "location-crosshairs", object: "box", hand: "hand", pose: "person-walking",
    track: "arrows-to-dot", marker: "thumbtack"
  };
  const vTiles = document.getElementById("v_tiles");
  const showVisionFunc = (v) => {
    document.getElementById("article_vision").dataset.func = v;
    vTiles.querySelectorAll("button").forEach((b) => b.setAttribute("aria-pressed", b.dataset.v === v ? "true" : "false"));
  };
  $("#v_func_type option").each(function () {
    const b = document.createElement("button");
    b.type = "button"; b.className = "v-tile"; b.dataset.v = this.value;
    b.innerHTML = `<i class="fa-solid fa-${V_ICON[this.value] || "eye"}"></i><span data-key="${this.dataset.key}"></span>`;
    b.addEventListener("click", () => { $("#v_func_type").val(b.dataset.v).trigger("change"); });
    vTiles.appendChild(b);
  });
  showVisionFunc($("#v_func_type").val());

  socket.on("disp_vision", function (data) {
    $("#v_func_type").val(data);
    showVisionFunc(data);
  });

  socket.on("stream", function (data) {
    //console.log('stream', data)
    $("#v_img").prop("src", `data:image/jpeg;charset=utf-8;base64,${data["img"]}`);
    $(".v-stage").attr("data-has", "");   // 첫 그림이 오면 '기다리는 중' 안내를 걷는다
    $("#v_result").text(data["data"]);
  });
  
  $("#v_func_type").change(function () {
    socket.emit("detect", $(this).val());
    showVisionFunc($(this).val());
  });

  socket.emit("marker_length",  Number($('#marker_length').val()));
  $('#marker_length').on("focusout keydown", function (evt) {
    if (
      evt.type == "focusout" ||
      (evt.type == "keydown" && evt.keyCode == 13)
    ) {
      socket.emit("marker_length",  Number($('#marker_length').val()));
    }
  });

  $('#marker_length').on("click", function (evt) {
    socket.emit("marker_length",  Number($('#marker_length').val()));
  });

  $("#v_capture").on("click", function () {
    let capture_a = document.createElement("a");
    capture_a.setAttribute("href", "/download_img");
    capture_a.setAttribute("download", "");
    capture_a.click();
  });

  $("#v_upload_tm").on("change", (e) => {
    let formData = new FormData();
    formData.append("data", $("#v_upload_tm")[0].files[0]);
    $("#v_upload_tm").val("");
    $.ajax({
      url: `/upload_tm`,
      type: "post",
      data: formData,
      contentType: false,
      processData: false,
    }).always(async (xhr, status) => {
      if (status == "success") {
        await alert_popup(translations["file_ok"][lang]);
      } else {
        await alert_popup(`${translations["file_error"][lang]}\n >> ${xhr.responseJSON["result"]}`);
        $("#v_upload_tm").val("");
      }
    });
  });

  $("#v_tilt_range").on("click touchend", function (evt) {
    $("#m5_range").val(Number($("#v_tilt_range").val()));
    $("#m5_value").val(Number($("#v_tilt_range").val()));
    $("#v_location").text(`${$("#m4_range").val()}, ${$("#m5_range").val()}`);
    socket.emit("set_motor", { idx: 5, pos: Number($("#v_tilt_range").val()) });
  });
  $("#v_pan_range").on("click touchend", function (evt) {
    $("#m4_range").val(Number($("#v_pan_range").val()));
    $("#m4_value").val(Number($("#v_pan_range").val()));
    $("#v_location").text(`${$("#m4_range").val()}, ${$("#m5_range").val()}`);
    socket.emit("set_motor", { idx: 4, pos: Number($("#v_pan_range").val()) });
  });

  $("#v_tilt_reset").on("click", function (evt) {
    $("#v_tilt_range").val(0);
    $("#m5_range").val(Number($("#v_tilt_range").val()));
    $("#m5_value").val(Number($("#v_tilt_range").val()));
    $("#v_location").text(`${$("#m4_range").val()}, ${$("#m5_range").val()}`);
    socket.emit("set_motor", { idx: 5, pos: Number($("#v_tilt_range").val()) });
  });
  $("#v_pan_reset").on("click", () => {
    $("#v_pan_range").val(0);
    $("#m4_range").val(Number($("#v_pan_range").val()));
    $("#m4_value").val(Number($("#v_pan_range").val()));
    $("#v_location").text(`${$("#m4_range").val()}, ${$("#m5_range").val()}`);
    socket.emit("set_motor", { idx: 4, pos: Number($("#v_pan_range").val()) });
  });
};

const getMotions = (socket) => {
  for (let i = 0; i < 10; i++) {
    let tval = "#m" + i + "_value";
    let trange = "#m" + i + "_range";

    $(trange).on("input", function (evt) {
      $(tval).val($(trange).val());
    });

    $(trange).on("click touchend", function (evt) {
      socket.emit("set_motor", { idx: i, pos: Number($(trange).val()) });
    });

    $(tval).on("focusout keydown", async function (evt) {
      if (
        evt.type == "focusout" ||
        (evt.type == "keydown" && evt.keyCode == 13)
      ) {
        let pos = Number($(this).val());
        let min = Number($(this).attr("min"));
        let max = Number($(this).attr("max"));

        if (isNaN(pos) || pos < min || pos > max) {
          $(this).val($(trange).val());
          await alert_popup(translations["range_warn"][lang](min, max));
        } else {
	        $(trange).val(pos);
          socket.emit("set_motor", { idx: i, pos: pos });
        }
      }
    });

    $(tval).on("click", function (evt) {
      let pos = $(tval).val();
      $(trange).val(pos);
      socket.emit("set_motor", { idx: i, pos: Number(pos) });
    });
  }

  /* v2 [동작]: 로봇 사진 위에는 번호 점(현재 각도)만, 조작은 사진 옆 패널에서 한다.
     예전 모터 칸 10개(#mN_value/#mN_range)는 v2 에서 숨기고 값 저장소로 그대로 쓴다 — 표 클릭·원래자세 등
     기존 코드가 그 값을 바꾸면 아래 sync 가 읽어 온다. 로봇에 보내는 건 기존과 같은 set_motor 한 가지.
     점 위치는 pibo_body.min.png(840×1145) 기준 %. 로봇 기준 오른쪽(M0~M3)이 화면 왼쪽이다 */
  if (document.body.classList.contains("pb-v2")) {
    const MDOT = [[5, 50, 12], [4, 50, 34.5], [2, 16.7, 49], [8, 83.3, 49], [3, 9.5, 63], [9, 91.7, 63],
                  [1, 37.5, 77], [7, 62.5, 77], [0, 35, 92.5], [6, 66.7, 92.5]];
    const sec = document.querySelector("#article_motion > .pibo-section");
    const img = sec.querySelector(":scope > img");
    const body = document.createElement("div"); body.className = "mbody";
    const stage = document.createElement("div"); stage.className = "mstage";
    img.parentNode.insertBefore(body, img); body.appendChild(stage); stage.appendChild(img);
    const dots = {};
    MDOT.forEach(([m, x, y]) => {
      const d = document.createElement("button");
      d.type = "button"; d.className = "mdot"; d.dataset.m = m;
      d.style.left = `${x}%`; d.style.top = `${y}%`;
      d.innerHTML = `<b>${m}</b><span class="mdot__v"></span>`;
      d.addEventListener("click", () => select(m));
      stage.appendChild(d); dots[m] = d;
    });
    const panel = document.createElement("div"); panel.className = "mpanel";
    panel.innerHTML = `<div class="mpanel__name" id="mp_name"></div>
      <div class="mpanel__val"><input type="number" id="mp_num" inputmode="numeric" /><span>°</span></div>
      <input type="range" id="mp_range" />
      <div class="mpanel__steps"><button type="button" data-d="-5">−5</button><button type="button" data-d="-1">−1</button><button type="button" data-d="1">+1</button><button type="button" data-d="5">+5</button></div>
      <div class="mpanel__lim" id="mp_lim"></div>`;
    const side = document.createElement("div"); side.className = "mside";
    body.appendChild(side); side.appendChild(panel);
    const mpNum = panel.querySelector("#mp_num"), mpRange = panel.querySelector("#mp_range");
    const lim = (m) => [Number($(`#m${m}_range`).attr("min")), Number($(`#m${m}_range`).attr("max"))];
    const cur = (m) => Number($(`#m${m}_value`).val()) || 0;
    let sel = 2, dragging = false, sendTimer = 0, mirrorOn = false;
    // [팔·손 좌우 같이]: 한쪽을 움직이면 반대쪽을 부호만 바꿔 같이 움직인다. 기본 자세가 -80/80·-25/25 이고
    // 예제(motion_db)의 박수·환영도 반대 부호라 팔·손은 확실하다. 다리·발은 예제만으로 규칙을 못 정해 뺐다
    const TWIN = { 2: 8, 8: 2, 3: 9, 9: 3 };
    const twinOf = (m) => (mirrorOn && m in TWIN ? TWIN[m] : null);

    const paint = () => {
      MDOT.forEach(([m]) => {
        dots[m].querySelector(".mdot__v").textContent = $(`#m${m}_value`).val() === "" ? "–" : cur(m);
        dots[m].setAttribute("aria-pressed", m === sel ? "true" : "false");
        dots[m].toggleAttribute("data-twin", m === twinOf(sel));
      });
      const [lo, hi] = lim(sel);
      panel.querySelector("#mp_name").textContent = t(`motor_m${sel}`);
      panel.querySelector("#mp_lim").textContent = `${lo} ~ ${hi}`;
      mpRange.min = lo; mpRange.max = hi; mpNum.min = lo; mpNum.max = hi;
      if (!dragging) mpRange.value = cur(sel);
      if (document.activeElement !== mpNum) mpNum.value = cur(sel);
    };
    const select = (m) => { sel = m; paint(); };
    const store = (m, v) => {                     // 저장소(숨긴 칸)와 점을 같이 바꾼다
      $(`#m${m}_value`).val(v); $(`#m${m}_range`).val(v);
      dots[m].querySelector(".mdot__v").textContent = v;
    };
    const setVal = (v) => {
      store(sel, v); mpRange.value = v; mpNum.value = v;
      const w = twinOf(sel);
      if (w !== null) { const [lo, hi] = lim(w); store(w, Math.max(lo, Math.min(hi, -v))); }
    };
    const send = (now) => {                       // [±] 를 빠르게 눌러도 서보 명령은 모아서 한 번
      clearTimeout(sendTimer);
      const ms = [sel, twinOf(sel)].filter((m) => m !== null);
      const go = () => ms.forEach((m) => socket.emit("set_motor", { idx: m, pos: cur(m) }));
      if (now) go(); else sendTimer = setTimeout(go, 150);
    };
    const nudge = (d) => { const [lo, hi] = lim(sel); setVal(Math.max(lo, Math.min(hi, cur(sel) + d))); send(false); };
    mpRange.addEventListener("input", () => { dragging = true; setVal(Number(mpRange.value)); });
    mpRange.addEventListener("change", () => { dragging = false; send(true); });
    panel.querySelectorAll(".mpanel__steps button").forEach((b) => b.addEventListener("click", () => nudge(Number(b.dataset.d))));
    const commitNum = async () => {
      const v = Number(mpNum.value), [lo, hi] = lim(sel);
      if (mpNum.value === "" || isNaN(v) || v < lo || v > hi) {
        mpNum.value = cur(sel);
        await alert_popup(translations["range_warn"][lang](lo, hi));
        return;
      }
      if (v !== cur(sel)) { setVal(v); send(true); }
    };
    mpNum.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); mpNum.blur(); } });
    mpNum.addEventListener("blur", commitNum);
    // 표 클릭·원래자세·불러오기 등이 숨긴 칸 값을 바꾸면 따라간다(이벤트 없이 .val() 로 바꾸는 코드가 많다)
    let last = "";
    setInterval(() => {
      if (document.getElementById("article_motion").offsetParent === null) return;
      const now = MDOT.map(([m]) => $(`#m${m}_value`).val()).join(",");
      if (now !== last) { last = now; paint(); }
      markChip();
    }, 300);

    /* ── 장면 만들기(260928) ─────────────────────────────────────────────
       '모션 하나 만드는 데 오래 걸린다'는 의견으로: 시간을 매번 적지 않게 [장면 추가] 뒤 시간이 간격만큼
       저절로 늘고, 표 줄을 누르면 그 장면을 [고치기]·[끝에 붙이기](같은 자세 반복)·[지우기] 할 수 있다.
       서버 쪽은 그대로(add_frame 은 같은 시간이면 덮어쓰고, 아니면 끼워 넣는다) */
    const scene = document.createElement("div"); scene.className = "mscene";
    scene.innerHTML = `<div class="mscene__title" data-key="scene_title"></div>
      <div class="mscene__row"><span class="mscene__lbl" data-key="time"></span><span id="ms_time_slot"></span></div>
      <div class="mscene__row"><span class="mscene__lbl" data-key="scene_step"></span><select id="ms_step">${
        [0.3, 0.5, 1, 1.5, 2].map((v) => `<option value="${v}">${v}</option>`).join("")}</select><span class="motion-unit" data-key="sec"></span></div>
      <div id="ms_add_slot"></div>
      <div class="mscene__sub"><button type="button" id="ms_append"><i class="fa-solid fa-arrow-down"></i><span data-key="scene_append"></span></button><button type="button" id="ms_delete"><i class="fa-solid fa-trash-can"></i><span data-key="scene_delete"></span></button></div>
      <label class="mscene__mirror"><input type="checkbox" id="ms_mirror" /><span data-key="scene_mirror"></span></label>
      <div class="mscene__keys" data-key="scene_keys"></div>`;
    side.appendChild(scene);
    const topRow = sec.querySelector(":scope > div:first-child");
    const timeIn = document.getElementById("m_time_val");
    scene.querySelector("#ms_time_slot").append(timeIn, topRow.querySelector(".motion-unit"));
    const addBt = document.getElementById("add_frame_bt");
    scene.querySelector("#ms_add_slot").replaceWith(addBt);
    stage.appendChild(document.getElementById("init_bt"));    // [원래자세] 는 사진 왼쪽 위 빈 자리로
    topRow.style.display = "none";
    const addIcon = addBt.querySelector("i"), addLbl = addBt.querySelector("span");
    const stepSel = scene.querySelector("#ms_step"), appendBt = scene.querySelector("#ms_append");
    const delBt = scene.querySelector("#ms_delete"), mirror = scene.querySelector("#ms_mirror");
    document.querySelector("#article_motion .motion-empty").dataset.key = "frames_empty_v2";
    const tr8 = () => document.querySelectorAll("#article_motion [data-key]").forEach((e) => {
      const v = translations[e.dataset.key] && translations[e.dataset.key][lang];
      if (typeof v === "string") e.textContent = v;
    });

    try { stepSel.value = localStorage.getItem("motion_step") || "0.5"; } catch (e) { stepSel.value = "0.5"; }
    if (!stepSel.value) stepSel.value = "0.5";
    try { mirrorOn = mirror.checked = localStorage.getItem("motion_mirror") === "1"; } catch (e) {}

    let frames = [];                                   // 표에 있는 장면 시간(ms), 서버가 정렬해서 준다
    const stepMs = () => Math.round(Number(stepSel.value) * 1000);
    const timeMs = () => Math.round(Number(timeIn.value) * 1000);
    const nextTime = () => (frames.length ? frames[frames.length - 1] + stepMs() : 0) / 1000;
    const updateScene = () => {
      const ms = timeMs(), editing = frames.includes(ms);
      addLbl.dataset.key = editing ? "scene_edit" : "scene_add";
      addLbl.textContent = t(addLbl.dataset.key);
      addIcon.className = editing ? "fa-solid fa-pen" : "fa-solid fa-plus";
      scene.toggleAttribute("data-editing", editing);
      delBt.disabled = !editing; appendBt.disabled = !frames.length;
      document.querySelectorAll("#motor_table > tbody > tr").forEach((tr, i) => tr.toggleAttribute("data-sel", editing && frames[i] === ms));
    };
    // 표가 바뀌면(추가·고치기·지우기·불러오기) 다음 시간 = 마지막 장면 + 간격
    window.afterMotionTable = (data) => {
      frames = data.map((f) => Math.round(Number(f.seq)));
      timeIn.value = +nextTime().toFixed(3);
      timeIn.classList.remove("is-bumped"); void timeIn.offsetWidth; timeIn.classList.add("is-bumped");
      updateScene();
    };
    timeIn.addEventListener("input", updateScene);
    timeIn.addEventListener("change", updateScene);
    document.querySelector("#motor_table > tbody").addEventListener("click", updateScene);   // 줄 클릭(jQuery)이 시간을 먼저 바꾼다
    stepSel.addEventListener("change", () => {
      try { localStorage.setItem("motion_step", stepSel.value); } catch (e) {}
      if (!frames.includes(timeMs())) timeIn.value = +nextTime().toFixed(3);
      updateScene();
    });
    appendBt.addEventListener("click", () => { if (frames.length) socket.emit("add_frame", Math.round(nextTime() * 1000)); });
    delBt.addEventListener("click", async () => {
      const ms = timeMs();
      if (!frames.includes(ms)) return;
      if (await confirm_popup(t("confirm_frame_delete", ms / 1000))) socket.emit("delete_frame", ms);
    });
    mirror.addEventListener("change", () => {
      mirrorOn = mirror.checked;
      try { localStorage.setItem("motion_mirror", mirrorOn ? "1" : "0"); } catch (e) {}
      paint();
    });

    // 키보드(노트북): ← → 모터 고르기, ↑ ↓ 1°(Shift 5°), Enter 장면 추가. 입력칸·팝업에 있을 때는 건드리지 않는다
    const ORDER = MDOT.map(([m]) => m);
    document.addEventListener("keydown", (e) => {
      if (e.ctrlKey || e.metaKey || e.altKey || e.isComposing) return;
      if (document.getElementById("article_motion").offsetParent === null) return;
      if (["alertPopup", "confirmPopup", "promptPopup"].some((id) => { const p = document.getElementById(id); return p && p.style.display !== "none"; })) return;
      const tg = e.target, tag = tg.tagName;
      if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT" || tg.isContentEditable) return;
      if (tag === "BUTTON" && !tg.closest(".mstage, .mpanel")) return;
      if (e.key === "ArrowLeft" || e.key === "ArrowRight") {
        const i = ORDER.indexOf(sel);
        select(ORDER[(i + (e.key === "ArrowRight" ? 1 : ORDER.length - 1)) % ORDER.length]);
      } else if (e.key === "ArrowUp" || e.key === "ArrowDown") {
        nudge((e.key === "ArrowUp" ? 1 : -1) * (e.shiftKey ? 5 : 1));
      } else if (e.key === "Enter") {
        addBt.click();
      } else return;
      e.preventDefault();
    });

    /* ── 저장 칸(내 동작): 표 아래 한 덩어리로 모은다. 저장된 이름은 칩 — 누르면 이름 칸에 들어가고
       [불러오기]·[삭제하기] 가 그 이름에 쓰인다. 두 번 누르면 바로 [불러오기] */
    const rec = document.querySelector("#article_motion .motion-record");
    const nameWrap = rec.querySelector(".motion-name-wrap"), pathBox = rec.querySelector(".motion-path");
    const nameIn = document.getElementById("motion_name_val");
    const lib = document.createElement("div"); lib.className = "mlib";
    const head = document.createElement("div"); head.className = "mlib__head";
    const libTools = document.createElement("div"); libTools.className = "mlib__tools";
    libTools.append(document.getElementById("export_motion_bt"), nameWrap.querySelector('label[for="v_import_motion"]'),
                    nameWrap.querySelector(".filebox"), document.getElementById("reset_motion_bt"));
    head.append(pathBox.querySelector(".motion-saved-title"), document.getElementById("motion-path-disabled"), libTools);
    const chips = document.createElement("div"); chips.className = "mlib__chips"; chips.id = "mlib_chips";
    lib.append(head, nameWrap, chips, pathBox.querySelector(".motion-samples"));
    rec.parentNode.appendChild(lib);
    Array.from(nameWrap.childNodes).forEach((n) => { if (n.nodeType === 3) n.remove(); });   // ':' 글자
    nameWrap.querySelectorAll(".pb-sep").forEach((n) => n.remove());
    const markChip = () => {
      const v = nameIn.value.trim();
      chips.querySelectorAll(".mchip").forEach((c) => c.setAttribute("aria-pressed", c.dataset.name === v ? "true" : "false"));
    };
    window.afterMotionRecord = (names) => {
      chips.replaceChildren();
      if (!names.length) {
        const e = document.createElement("span"); e.className = "mlib__empty"; e.dataset.key = "saved_empty"; e.textContent = t("saved_empty");
        chips.appendChild(e); return;
      }
      names.forEach((n) => {
        const c = document.createElement("button");
        c.type = "button"; c.className = "mchip"; c.dataset.name = n; c.textContent = n;
        c.addEventListener("click", () => { nameIn.value = n; markChip(); });
        c.addEventListener("dblclick", () => { nameIn.value = n; markChip(); document.getElementById("load_motion_bt").click(); });
        chips.appendChild(c);
      });
      markChip();
    };
    nameIn.addEventListener("input", markChip);
    window.afterMotionRecord([]);

    const nameHint = () => {
      nameIn.placeholder = t("motion_name"); nameIn.setAttribute("aria-label", t("motion_name"));
      libTools.querySelectorAll("[data-key]").forEach((e) => e.parentNode.title = t(e.dataset.key));   // 좁은 폭엔 아이콘만 보인다
    };
    nameHint();
    window.refreshMotorPanel = () => { paint(); tr8(); updateScene(); nameHint(); };
    tr8(); updateScene();
    paint();
  }

  $("#m_time_val").on("focusout keydown", async function (evt) {
    if (
      evt.type == "focusout" ||
      (evt.type == "keydown" && evt.keyCode == 13)
    ) {
      let pos = Number($(this).val());
      let min = Number($(this).attr("min"));
      let max = Number($(this).attr("max"));

      if (isNaN(pos) || pos < min || pos > max) {
        $(this).val(0);
        await alert_popup(translations["range_warn"][lang](min, max));
      }
    }
  });

  $("#init_bt").on("click", function () {
    for (let i = 0; i < 10; i++) {
      $("#m" + i + "_value").val(motor_default[i]);
      $("#m" + i + "_range").val(motor_default[i]);
    }
    socket.emit("set_motors", { pos_lst: motor_default });
  });

  // 저장 버튼
  $("#add_frame_bt").on("click", function () {
    socket.emit("add_frame", Math.round($("#m_time_val").val() * 1000));
  });

  socket.on("disp_motion", function (datas) {
    // 모터 값 로드
    if ("pos" in datas) {
      let data = datas["pos"];
      for (let i = 0; i < 10; i++) {
        let tval = "#m" + i + "_value";
        let trange = "#m" + i + "_range";
        $(tval).val(data[i]);
        $(trange).val(data[i]);
      }
    }

    // json 로드
    if ("record" in datas) {
      let res = [];
      for(name in datas["record"]) {
        res.push(name);
      }
      $('#motor_record').text(res.join(', '));
      if (window.afterMotionRecord) window.afterMotionRecord(res);
    }

    // 테이블 로드
    if ("table" in datas) {
      let data = datas["table"];

      for (let i = 0; i < data.length; i++) {
        if (i != 0)
          for (let j = 0; j < 10; j++) {
            data[i].d[j] =
              data[i].d[j] == 999 ? data[i - 1].d[j] : data[i].d[j];
          }
      }

      $("#motor_table > tbody").empty();
      for (let i = 0; i < data.length; i++) {
        $("#motor_table > tbody").append(
          $("<tr>")
            .append(
              $("<td>").append(data[i].seq / 1000 + t("sec")),
              $("<td>").append(data[i].d[0]),
              $("<td>").append(data[i].d[1]),
              $("<td>").append(data[i].d[2]),
              $("<td>").append(data[i].d[3]),
              $("<td>").append(data[i].d[4]),
              $("<td>").append(data[i].d[5]),
              $("<td>").append(data[i].d[6]),
              $("<td>").append(data[i].d[7]),
              $("<td>").append(data[i].d[8]),
              $("<td>").append(data[i].d[9])
            )
            .hover(
              function () {
                $(this).animate({ opacity: "0.5" }, 100);
              },
              function () {
                $(this).animate({ opacity: "1" }, 100);
              }
            )
            .click(function () {
              let pos_lst = [];
              let lst = $(this).children();
              lst.each((idx) => {
                if (idx == 0) {
                  $("#m_time_val").val(
                    parseFloat(lst.eq(idx).text())
                  );
                  return;
                } else {
                  let val = Number(lst.eq(idx).text());
                  $("#m" + (idx - 1) + "_value").val(val);
                  $("#m" + (idx - 1) + "_range").val(val);
                  pos_lst[idx - 1] = val;
                }
              });

              socket.emit("set_motors", { pos_lst: pos_lst });
            })
            .dblclick(async function () {
              let tv = $(this).text().split(" ")[0];
              if (await confirm_popup(t("confirm_frame_delete", tv))) {
                socket.emit("delete_frame", Math.round(Number(tv) * 1000));
                $(this).remove();
              }
            })
        );
      }
      if (window.afterMotionTable) window.afterMotionTable(data);
    }
  });

  $("#export_motion_bt").on("click", function() {
    let motion_a = document.createElement("a");
    if($("#motion_name_val").val() == "") motion_a.setAttribute("href", `/export_motion/all`);
    else motion_a.setAttribute("href", `/export_motion/${$("#motion_name_val").val()}`); 
    motion_a.setAttribute("download", "");
    motion_a.click()
  });

  $("#v_import_motion").on("change", (e) => {
    let formData = new FormData();
    formData.append("data", $("#v_import_motion")[0].files[0]);
    $("#v_import_motion").val("");
    $.ajax({
      url: `/import_motion`,
      type: "post",
      data: formData,
      contentType: false,
      processData: false,
    }).always( async (xhr, status) => {
      if (status == "success") {
        await alert_popup(translations["file_ok"][lang]);
      } else {
        await alert_popup(`${translations["file_error"][lang]}\n >> ${xhr.responseJSON["result"]}`);
        $("#v_import_motion").val("");
      }
    });
  });

  // 테이블 초기화
  $("#init_frame_bt").on("click", async function () {
    if (await confirm_popup(translations["confirm_motion_delete_all"][lang])) {
      socket.emit("init_frame");
      $("#motor_table > tbody").empty();
    }
  });

  // 동작 재생
  $("#play_frame_bt").on("click", async function () {
    if ($("#motor_table > tbody").text()) {
      let cycle = $("#play_cycle_val").val();
      socket.emit("play_frame", cycle);
    } else {
      await alert_popup(translations["motion_empty"][lang]);
    }
  });

  $("#play_cycle_val").on("focusout keydown", async function (evt) {
    if (
      evt.type == "focusout" ||
      (evt.type == "keydown" && evt.keyCode == 13)
    ) {
      let val = Number($(this).val());
      let min = Number($(this).attr("min"));
      let max = Number($(this).attr("max"));

      if (!Number.isInteger(val) || val < min || val > max) {
        await alert_popup(translations["range_warn"][lang](min, max));
        $(this).val(1);
      }
    }
  });

  // 동작 정지
  $("#stop_frame_bt").on("click", function () {
    socket.emit("stop_frame");
  });

  // 모션 추가
  $("#add_motion_bt").on("click", async function () {
    let motionName = $("#motion_name_val").val().trim();

    if (motionName == "") {
      await alert_popup(translations["motion_name_empty"][lang]);
      return;
    }  
    if (await confirm_popup(translations["confirm_motion_register"][lang](motionName))) {
      socket.emit("add_motion", motionName);
      $("#motion_name_val").val("");
    }
  });

  // 모션 불러오기
  $("#load_motion_bt").on("click", async function () {
    let motionName = $("#motion_name_val").val().trim();

    if (motionName == "") {
      await alert_popup(translations["motion_name_empty"][lang]);
      return;
    }

    if (await confirm_popup(translations["confirm_motion_load"][lang](motionName))) {
      socket.emit("load_motion", motionName);
      $("#motion_name_val").val("");
    }
  });

  const sample_motions = [
   'left', 'left_half', 'right', 'right_half', 'forward1', 'backward1', 'step1', 'cheer1', 'cheer2', 'wave1', 'think1', 'wake_up3', 'yes_h', 'no_h', 'head_h', 'spin_h', 'clapping1', 'handshaking', 'greeting', 'hand1', 'foot1', 'speak1', 'speak2', 'welcome', 'dance1', 'dance2', 'dance3', 'dance4', 'dance5'
  ];

  $('#motion_samples').html(sample_motions.map((e)=>{
    return `<a id="motion_${e}_bt" style="color:#df7e3d;cursor:pointer">${e}</a>`
  }).join(', '));

  // v2: 예제 알약은 접어 둔다(펼친 상태는 기억). 펼치면 표가 그만큼 줄어든다 — 오른쪽 칸은 화면 높이에 맞춰져 있다
  const samplesBox = document.querySelector(".motion-samples");
  const samplesToggle = document.getElementById("motion_samples_toggle");
  const setSamplesOpen = (open) => {
    if (open) samplesBox.setAttribute("data-open", ""); else samplesBox.removeAttribute("data-open");
    try { localStorage.setItem("motion_samples_open", open ? "1" : "0"); } catch (e) {}
  };
  window.updateSamplesToggle = () => { $("#motion_samples_toggle_txt").text(t("samples_toggle", sample_motions.length)); };
  let samplesOpen = false;
  try { samplesOpen = localStorage.getItem("motion_samples_open") === "1"; } catch (e) {}
  setSamplesOpen(samplesOpen);
  window.updateSamplesToggle();
  samplesToggle.addEventListener("click", () => setSamplesOpen(!samplesBox.hasAttribute("data-open")));

  for (idx in sample_motions) {
    $(`#motion_${sample_motions[idx]}_bt`).on("click", function () {
      let i = sample_motions.indexOf($(this).text());
      socket.emit("load_motion", sample_motions[i]);
    });
  }

  // 모션 삭제
  $("#delete_motion_bt").on("click", async function () {
    let motionName = $("#motion_name_val").val().trim();

    if (motionName == "") {
      await alert_popup(translations["motion_name_empty"][lang]);
      return;
    }
    if (await confirm_popup(translations["confirm_motion_delete"][lang](motionName))) {
      socket.emit("delete_motion", motionName);
      $("#motion_name_val").val("");
    }
  });

  // 모션 삭제
  $("#reset_motion_bt").on("click", async function () {
    if (await confirm_popup(translations["confirm_motion_delete_all"][lang])) socket.emit("reset_motion");
  });
};

const getSpeech = (socket) => {
  const max_tts_length = 30;

  // 목소리: v2 화면은 select 대신 타일(select 값은 그대로 맞춘다 — v1 은 select). PiBrain 도구와 같은 10가지 + espeak
  const voiceSel = document.querySelector("select[name=s_voice_type]");
  const voiceTiles = document.getElementById("s_voice_tiles");
  voiceSel.parentNode.appendChild(voiceTiles);   // [음성종류] 이름표 옆으로(select 자리)
  const showVoice = () => voiceTiles.querySelectorAll("button").forEach((b) => b.setAttribute("aria-pressed", b.dataset.v === voiceSel.value ? "true" : "false"));
  Array.from(voiceSel.options).forEach((o) => {
    const b = document.createElement("button");
    b.type = "button"; b.className = "s-voice"; b.dataset.v = o.value;
    const icon = o.value === "espeak" ? "robot" : (o.value[0] === "f" ? "person-dress" : "person");
    b.innerHTML = `<i class="fa-solid fa-${icon}"></i><span data-key="${o.dataset.key}"></span>`;
    b.addEventListener("click", () => { voiceSel.value = o.value; showVoice(); });
    voiceTiles.appendChild(b);
  });
  voiceSel.addEventListener("change", showVoice);
  showVoice();

  const ttsStatus = document.getElementById("s_tts_status");
  const setTtsStatus = (text, kind) => { ttsStatus.textContent = text; ttsStatus.dataset.kind = kind || ""; };
  socket.on("tts_status", (d) => {
    if (d && d.stopped) setTtsStatus(t("tts_stopped"));
    else if (d && d.ok) setTtsStatus(t("tts_done"), "ok");
    else setTtsStatus(t("tts_error", (d && d.error) || ""), "err");
  });
  $("#s_tts_stop_bt").on("click", () => socket.emit("tts_stop"));
  $("#s_tts_bt").on("click", async function () {
    if ($("input[name=s_voice_en]:checked").val() == "off") {
      await alert_popup(translations["voice_enable"][lang]);
      return;
    }

    let string = $("#s_tts_val").val().trim();
    if (string == "") {
      await alert_popup(translations["text_empty"][lang]);
      return;
    }
    if (string.length > max_tts_length) {
      await alert_popup(translations["text_size_limit"][lang](max_tts_length));
      return;
    }
    setTtsStatus(t("tts_speaking"));
    socket.emit("tts", {
      text: string,
      voice_type: $("select[name=s_voice_type]").val(),
      volume: Number($("#volume").val()),
    });
  });

  $("#s_tts_val").on("keypress", async function (evt) {
    if (evt.keyCode == 13) {
      if ($("input[name=s_voice_en]:checked").val() == "off") {
        await alert_popup(translations["voice_enable"][lang]);
        return;
      }
      let string = $("#s_tts_val").val().trim();
      if (string == "") {
        await alert_popup(translations["text_empty"][lang]);
        return;
      }
      if (string.length > max_tts_length) {
        await alert_popup(translations["text_size_limit"][lang](max_tts_length));
        return;
      }
      setTtsStatus(t("tts_speaking"));
      socket.emit("tts", {
        text: string,
        voice_type: $("select[name=s_voice_type]").val(),
        volume: Number($("#volume").val()),
      });
    }
  });


  let micTimer = null;

  socket.on("mic", function (d) {
    //console.log('mic', d)
    $("#mic_status").text(d);
    micIndicatorStop();
  });

  /* 녹음 중 표시.
     막대는 "녹음이 돌고 있다"는 신호일 뿐 실제 마이크 레벨이 아니다. 녹음은
     로봇에서 Audio.record() 가 파일로 받아서 브라우저로 오는 오디오 스트림이
     없다. 마이크가 죽었는지는 이걸로 판단하면 안 되고, 녹음 후 재생으로 봐야
     한다. 아래 진행 막대는 실제 남은 시간을 그린다. */
  function micIndicator(seconds) {
    const wave = document.getElementById("mic_wave");
    const bars = wave.querySelectorAll("span");
    const prog = document.getElementById("mic_progress");
    const fill = prog.firstElementChild;

    micIndicatorStop();
    wave.hidden = false;
    prog.hidden = false;
    fill.style.width = "0%";

    const started = Date.now();
    const total = seconds * 1000;

    micTimer = setInterval(() => {
      const passed = Date.now() - started;
      fill.style.width = Math.min(100, (passed / total) * 100) + "%";
      bars.forEach((b, i) => {
        // 가운데가 높은 완만한 형태에 흔들림을 얹는다. 가만히 있는 것보다
        // 녹음 중임이 분명해진다.
        const center = 1 - Math.abs(i - (bars.length - 1) / 2) / bars.length;
        b.style.height = Math.round((12 + center * 55 * (0.35 + Math.random())) ) + "%";
      });
      if (passed >= total) micIndicatorStop();
    }, 100);
  }

  function micIndicatorStop() {
    if (micTimer) {
      clearInterval(micTimer);
      micTimer = null;
    }
    const wave = document.getElementById("mic_wave");
    const prog = document.getElementById("mic_progress");
    if (wave) wave.hidden = true;
    if (prog) prog.hidden = true;
  }

  $("#mic_bt").on("click", async function () {
    let tmictime = "#mic_time_val";
    let val = Number($(tmictime).val());
    let min = Number($(tmictime).attr("min"));
    let max = Number($(tmictime).attr("max"));

    if (isNaN(val) || val < min || val > max) {
      await alert_popup(translations["audio_input_error"][lang]);
      return;
    }

    $("#mic_status").html(`<i class='fa-solid fa-fade'>${t("recording")}</i>`);
    micIndicator(val);
    socket.emit("mic", {
      time: val,
      volume: Number($("#volume").val()),
    });
  });

  $("#mic_replay_bt").on("click", function () {
    socket.emit("mic_replay", { volume: Number($("#volume").val()) });
  });



};

/* [동작] 왼쪽 로봇 칸은 그림을 보며 모터를 맞추는 곳이라 늘 한 화면에 다 보여야 한다.
   v2 에서는 오른쪽(표·저장)만 스크롤되게 로봇 칸을 붙여 두고(sticky, pibo-ui.css),
   화면 높이보다 크면 zoom 으로 줄인다. 로봇 그림 위 모터 칸이 px 로 자리 잡혀 있어 통째로 줄여야 모양이 유지된다 */
const fitRobot = () => {
  const sec = document.querySelector("#article_motion > .pibo-section");
  const pane = document.querySelector("main > div.content");
  if (!sec || !pane) return;
  sec.style.zoom = "";
  if (!document.body.classList.contains("pb-v2") || !sec.offsetHeight) return;
  const cs = getComputedStyle(pane);
  const avail = pane.clientHeight - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom) - 8;
  // 오른쪽 칸(표·저장)도 이 높이에 맞춘다 — 표만 스크롤되고 위아래 버튼 줄은 늘 보이게(pibo-ui.css 의 --motion-h)
  document.getElementById("article_motion").style.setProperty("--motion-h", `${Math.floor(avail)}px`);
  if (window.innerWidth <= 900) return;   // 태블릿 세로는 위아래로 쌓고 페이지가 스크롤된다
  const z = Math.min(1, avail / sec.offsetHeight);
  if (z < 1) sec.style.zoom = Math.max(0.6, z).toFixed(3);
};
window.addEventListener("resize", fitRobot);
window.addEventListener("load", fitRobot);
if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitRobot);   // 글꼴이 바뀌면 높이도 바뀐다

const handleMenu = (name) => {
  if (name === "vision") {
    $("#v_tilt_range").val($("#m5_range").val());
    $("#v_pan_range").val($("#m4_range").val());
    $("#v_location").text(`${$("#m4_range").val()}, ${$("#m5_range").val()}`);
    socket.emit("disp_vision");
  } else if (name === "motion") {
    socket.emit("disp_motion");
  }

  socket.emit("vision_sleep", name=="vision"?"off":"on");
  if (name != "motion") {
    socket.emit("set_motor", { idx: 0, pos: 0});
    socket.emit("set_motor", { idx: 6, pos: 0});
  }

  $("h4#content_header").text(name.toUpperCase());
  $("nav").find("button").removeClass("menu-selected");
  $(`button[name=${name}]`).addClass("menu-selected");
  $("article").not(`#article_${name}`).hide("slide");
  $(`main>div.content`).removeClass("modal");
  $(`#article_${name}`).show("slide", () => { if (name === "motion") fitRobot(); });
  if (name === "motion") setTimeout(fitRobot, 0);
};

getVisions(socket);
getMotions(socket);
getSpeech(socket);

handleMenu("motion");
const menus = $("nav").find("button");
menus.each((idx) => {
  const element = menus.get(idx);
  const name = element.getAttribute("name");
  element.addEventListener("click", () => handleMenu(name));
});

const menus_ds = $("#article_home").find("a");
menus_ds.each((idx) => {
  const element = menus_ds.get(idx);
  const name = element.getAttribute("name");
  element.addEventListener("click", () => handleMenu(name.split('_ds')[0]));
});

// keepalive 가 없으면 언로드 중 브라우저가 요청을 취소한다. 이 한 옵션이 전부다.
window.addEventListener('beforeunload', () => {
  fetch(`http://${location.hostname}/tools?enable=off`, { method: 'GET', keepalive: true })
    .catch(() => {});
});

const setLanguage = (lang) => {
  const elements = document.querySelectorAll('[data-key]');
  elements.forEach(element => {
      const key = element.getAttribute('data-key');
      if (translations[key] && translations[key][lang]) {
          element.textContent = translations[key][lang];
      }
  });
}

const language = document.getElementById("language");
language.value = lang;
setLanguage(lang);

localStorage.setItem("language", lang);
language.addEventListener("change", () => {
  lang = language.value;
  setLanguage(lang);
  setRobotState(onoffVal.dataset.state === 'on');
  if (window.updateSamplesToggle) window.updateSamplesToggle();
  if (window.refreshMotorPanel) window.refreshMotorPanel();
  localStorage.setItem("language", lang);
});


/* ==========================================================================
   [IDE] — IDE 가 연 탭이면 닫아서 원래 IDE 탭으로 돌아간다. 주소를 직접 쳐서
   연 탭은 닫을 수 없으니 IDE 주소로 이동한다. 어느 쪽이든 beforeunload 가
   이 서비스를 끈다.
   (오른쪽 끝 THE MAKER 로고도 IDE 로 가지만, 돌아가기 버튼인지 알아볼 수 없었다)
   ========================================================================== */
document.getElementById("ide_bt").addEventListener("click", () => PiboUI.backToIDE());

/* ==========================================================================
   연결 끊김 — 이 탭은 서비스가 꺼지면 소켓이 끊긴다. IDE 에서 다른 도구를 켜거나
   코드를 실행하면 서버가 이 서비스를 끄기 때문이다. 그때 배너로 알린다.
   ========================================================================== */
PiboUI.watchSocket(socket, {
  banner: () => ({
    text: PiboUI.text("svc_stopped"),
    kind: "warn",
    actions: [
      { label: PiboUI.text("restart"), primary: true, onClick: () => PiboUI.restartSelf("tools") },
      { label: PiboUI.text("close"), onClick: () => PiboUI.backToIDE() }
    ]
  })
});
