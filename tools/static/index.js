// 전체화면 버튼(#fullscreen_bt)은 pibo-ui.js 가 맡는다(260930) — 탭을 바꿔 풀린 전체화면을 한 번 눌러 되살린다

const motor_default = [0, 0, -80, 0, 0, 0, 0, 0, 80, 0];

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
// 기다리는 동안은 몇 초째인지 같이 보인다(무작정 기다리지 않게)
let onoff_count = 0;
const setRobotState = (on) => {
  onoffVal.dataset.state = on ? 'on' : 'off';
  onoffVal.dataset.label = on ? t('robot_ready') : `${t('robot_waiting')} · ${onoff_count}${t('sec')}`;
};
setRobotState(false);

let onoff_intv = setInterval(() => {
  onoffCount.innerHTML = `<i style="opacity:0.6">${++onoff_count}</i>`;
  if (onoffVal.dataset.state !== 'on') setRobotState(false);
}, 1000);

// 준비될 때까지만 5초마다 묻는다. 서버는 접속하는 순간에도 알려 준다(run_tools.py 의 send_state)
let robotOn = false;
setInterval(() => {
  if (!robotOn) socket.emit("onoff");
}, 5000);
socket.on("disconnect", () => { robotOn = false; setRobotState(false); });

socket.on("onoff", function (data) {
  const was = robotOn;
  robotOn = !!data;
  setRobotState(!!data);
  onoffVal.innerHTML = data?
    `<i class="fas fa-toggle-on">&nbsp;on</i>`
    : `<i class="fas fa-toggle-off fa-sm fa-fade" style="--fa-animation-duration: 2s; --fa-fade-opacity: 0.6">&nbsp;off</i>`
  console.log('onoff', data)

  if (data == true && !was) {   // 준비 안 됨 → 됨 으로 바뀔 때 한 번만(원래자세로 모터를 보낸다)
    // 준비 전에 [카메라] 탭을 열었으면 그때 보낸 켜기 요청은 버려졌다(서버가 아직 없었다) → 지금 탭 기준으로 다시 알린다
    const menu = $("nav button.menu-selected").attr("name") || "";
    socket.emit("vision_sleep", menu.split("_ds")[0] === "vision" && !document.hidden ? "off" : "on");
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

  /* 준비 상태(260929): 서버가 [로봇 연결됨] 뒤에 카메라 → 사물·손 인식 → 얼굴 인식 순으로 올리며
     vision_state 를 보낸다. 카메라 칸 위에 단계·막대·경과 초를 보이고, 아직 안 올라온 기능 타일에는 '준비 중' 을 단다
     (눌러 둘 수는 있다 — 올라오면 그때부터 결과가 나온다) */
  const NEEDS = { face: "face", face_landmark: "face", qr: "detect", object: "detect", hand: "detect", pose: "detect", track: "detect", marker: "detect" };
  const vBoot = document.createElement("div"); vBoot.className = "v-boot"; vBoot.hidden = true;
  vBoot.innerHTML = `<div class="v-boot__row"><i class="fa-solid fa-spinner fa-spin"></i><span class="v-boot__txt"></span><span class="v-boot__n"></span></div><div class="v-boot__bar"><i></i></div>`;
  document.querySelector("#article_vision .v-stage").before(vBoot);
  let vState = null, vSec = 0;
  const paintVision = () => {
    const s = vState;
    if (!s) return;
    const done = s.key === "vs_ready" && !s.error;
    vBoot.hidden = done;
    vBoot.dataset.kind = s.error ? "err" : "";
    vBoot.querySelector(".v-boot__txt").textContent = s.error ? t("vs_error", s.error) : t(s.key);
    vBoot.querySelector(".v-boot__n").textContent = s.error ? "" : `${s.step}/${s.total} · ${vSec}${t("sec")}`;
    vBoot.querySelector(".v-boot__bar > i").style.width = `${Math.max(6, Math.round((s.step - 1) / s.total * 100))}%`;
    vTiles.querySelectorAll("button").forEach((b) => {
      const need = NEEDS[b.dataset.v], wait = !!(need && !s[need]);
      b.toggleAttribute("data-wait", wait);
      b.dataset.waitLabel = wait ? t("vs_tile_wait") : "";
    });
  };
  socket.on("vision_state", (s) => { vState = s; paintVision(); });
  setInterval(() => { if (vState && vState.key !== "vs_ready" && !vState.error) { vSec++; paintVision(); } }, 1000);
  window.refreshVisionState = paintVision;

  socket.on("disp_vision", function (data) {
    $("#v_func_type").val(data);
    showVisionFunc(data);
  });

  // 카메라 한 장은 JPEG 바이트로 온다(260929, 예전 서버는 base64 문자열 — 둘 다 받는다). 이전 주소는 풀어 준다
  let streamUrl = "";
  socket.on("stream", function (data) {
    const img = data["img"];
    if (typeof img === "string") {
      $("#v_img").prop("src", `data:image/jpeg;charset=utf-8;base64,${img}`);
    } else {
      const url = URL.createObjectURL(new Blob([img], { type: "image/jpeg" }));
      $("#v_img").prop("src", url);
      if (streamUrl) URL.revokeObjectURL(streamUrl);
      streamUrl = url;
    }
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
    let sel = 2, dragging = false, sendTimer = 0;

    // 번호 점의 각도 링(pibo-ui.css '움직임' 3): 한쪽 끝까지 가면 한 바퀴, + 는 시계 방향·− 는 반대
    const gauge = (m) => {
      const v = cur(m), [lo, hi] = lim(m);
      const f = v >= 0 ? (hi > 0 ? v / hi : 0) : (lo < 0 ? v / lo : 0);
      const a = Math.round(Math.min(1, Math.abs(f)) * 360);
      const b = dots[m].firstElementChild;
      b.style.setProperty("--g-a", `${a}deg`);
      b.style.setProperty("--g-s", `${v < 0 ? -a : 0}deg`);
    };
    const paint = () => {
      MDOT.forEach(([m]) => {
        dots[m].querySelector(".mdot__v").textContent = $(`#m${m}_value`).val() === "" ? "–" : cur(m);
        gauge(m);
        dots[m].setAttribute("aria-pressed", m === sel ? "true" : "false");
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
      gauge(m);
    };
    const setVal = (v) => { store(sel, v); mpRange.value = v; mpNum.value = v; };
    const send = (now) => {                       // [±] 를 빠르게 눌러도 서보 명령은 모아서 한 번
      clearTimeout(sendTimer);
      const m = sel;
      const go = () => socket.emit("set_motor", { idx: m, pos: cur(m) });
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

    /* ── 표에 추가(260928) ─────────────────────────────────────────────
       '모션 하나 만드는 데 오래 걸린다'는 의견으로 시간을 매번 적지 않게 했다: 표가 바뀔 때마다 시간 칸이
       '마지막 줄 + 0.5초' 로 채워진다. 나머지는 원래 도구 규칙 그대로(줄을 누르면 그 자세·시간을 불러오고,
       같은 시간이면 그 줄을 바꾼다 → 버튼 이름 [추가·수정]).
       자리: 시간·[추가·수정] 은 조작 패널 맨 아래(각도를 맞추고 바로 아래에서 누른다),
       [이 줄 지우기] 는 표 쪽 버튼 줄(표를 다루는 버튼이라 [표 비우기] 옆).
       ※ 따로 상자(왼쪽 아랫줄 140px)로 두었더니 내용은 한 줄인데 상자만 커서 뺐다(260928).
         간격 고르기·[끝에 붙이기]·이름이 바뀌는 버튼·[팔·손 좌우 같이] 도 '더 헷갈린다'는 의견으로 뺐다 */
    const STEP_MS = 500;
    /* 배치(v2, 901px 이상, pibo-ui.css 의 '줄 맞춤'): 두 카드 같은 폭·같은 높이.
         왼쪽   [원래자세 · 키 안내] / 사진 + 조작 패널(아래에 시간·추가·수정)
         오른쪽 [반복 · 실행 · 정지 · (이 줄 지우기) · 표 비우기] / 표 / 저장 칸 */
    const addBox = document.createElement("div"); addBox.className = "mpanel__add";
    addBox.innerHTML = `<div class="mpanel__time"><span data-key="time"></span><span id="ms_time_slot"></span></div>
      <span id="ms_add_slot"></span>
      <div class="mpanel__hint" data-key="scene_help"></div>`;
    panel.appendChild(addBox);
    const delBt = document.createElement("button");
    delBt.type = "button"; delBt.id = "ms_delete"; delBt.hidden = true;
    delBt.innerHTML = `<i class="fa-solid fa-delete-left"></i><span data-key="scene_delete"></span>`;   // [표 비우기](휴지통)와 다른 아이콘
    const clearBt = document.getElementById("init_frame_bt");
    clearBt.parentNode.insertBefore(delBt, clearBt);
    const mhead = document.createElement("div"); mhead.className = "mhead";
    mhead.innerHTML = `<span class="mhead__keys" data-key="scene_keys"></span>`;
    mhead.prepend(document.getElementById("init_bt"));
    sec.insertBefore(mhead, body);
    const topRow = sec.querySelector(":scope > div:first-child");   // 예전 윗줄(시간·추가하기). 요소만 옮기고 숨긴다
    const timeIn = document.getElementById("m_time_val");
    addBox.querySelector("#ms_time_slot").append(timeIn, topRow.querySelector(".motion-unit"));
    const addBt = document.getElementById("add_frame_bt");
    addBox.querySelector("#ms_add_slot").replaceWith(addBt);
    topRow.style.display = "none";

    // 사진 크기: 가운데 줄 높이·폭에 맞춘다(그림 비율 840×1145). 점은 % 자리라 따라온다
    const fitStage = () => {
      if (window.innerWidth <= 900 || !body.clientHeight) { stage.style.width = ""; return; }
      const col = getComputedStyle(body).flexDirection === "column";   // 1199px 이하: 패널이 사진 아래
      const w = col ? Math.min((body.clientHeight - side.offsetHeight - 12) / 1.363, body.clientWidth - 24, 520)   // 점이 그림 밖으로 조금 나간다
                    : Math.min(body.clientHeight / 1.363, body.clientWidth - side.offsetWidth - 14, 520);
      stage.style.width = `${Math.max(180, Math.floor(w))}px`;
    };
    if (window.ResizeObserver) new ResizeObserver(fitStage).observe(body);
    window.addEventListener("resize", fitStage);
    addBt.querySelector("span").dataset.key = "add_or_edit";   // 같은 시간이면 그 줄을 바꾸므로 [추가·수정] (v1 은 [추가하기] 그대로)
    document.querySelector("#article_motion .motion-empty").dataset.key = "frames_empty_v2";
    const tr8 = () => document.querySelectorAll("#article_motion [data-key]").forEach((e) => {
      const v = translations[e.dataset.key] && translations[e.dataset.key][lang];
      if (typeof v === "string") e.textContent = v;
    });

    let frames = [];                                   // 표에 있는 줄의 시간(ms), 서버가 정렬해서 준다
    const timeMs = () => Math.round(Number(timeIn.value) * 1000);
    // 시간 칸이 표에 있는 줄과 같으면 그 줄을 표시하고 [이 줄 지우기] 를 보인다(줄을 누르면 그렇게 된다)
    const updateScene = () => {
      const ms = timeMs(), picked = frames.includes(ms);
      delBt.title = t("scene_delete");                // 좁은 폭에선 아이콘만 보인다
      clearBt.title = t("clear_frames");
      addBt.title = t("add_or_edit_tip");
      delBt.hidden = !picked;
      document.querySelectorAll("#motor_table > tbody > tr").forEach((tr, i) => tr.toggleAttribute("data-sel", picked && frames[i] === ms));
    };
    window.afterMotionTable = (data) => {
      frames = data.map((f) => Math.round(Number(f.seq)));
      timeIn.value = frames.length ? (frames[frames.length - 1] + STEP_MS) / 1000 : 0;
      timeIn.classList.remove("is-bumped"); void timeIn.offsetWidth; timeIn.classList.add("is-bumped");
      updateScene();
    };
    timeIn.addEventListener("input", updateScene);
    timeIn.addEventListener("change", updateScene);
    document.querySelector("#motor_table > tbody").addEventListener("click", updateScene);   // 줄 클릭(jQuery)이 시간을 먼저 바꾼다
    delBt.addEventListener("click", async () => {
      const ms = timeMs();
      if (!frames.includes(ms)) return;
      if (await confirm_popup(t("confirm_frame_delete", ms / 1000))) socket.emit("delete_frame", ms);
    });

    // 키보드(노트북): ← → 모터 고르기, ↑ ↓ 1°(Shift 5°), Enter [추가하기]. 입력칸·팝업에 있을 때는 건드리지 않는다
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
    const libTitle = pathBox.querySelector(".motion-saved-title");
    libTitle.title = document.getElementById("motion-path-disabled").value;    // ~/mymotion.json
    libTools.prepend(pathBox.querySelector(".motion-samples"));               // [예제 동작 ▾] — 표 위로 뜨는 목록
    head.append(libTitle, libTools);
    const chips = document.createElement("div"); chips.className = "mlib__chips"; chips.id = "mlib_chips";
    lib.append(head, nameWrap, chips);
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

  // v2: 예제 알약은 [예제 동작 N개 ▾] 를 누르면 저장 칸 위로 뜬다. 바깥을 누르거나 하나 고르면 닫힌다
  const samplesBox = document.querySelector(".motion-samples");
  const samplesToggle = document.getElementById("motion_samples_toggle");
  const setSamplesOpen = (open) => {
    if (open) samplesBox.setAttribute("data-open", ""); else samplesBox.removeAttribute("data-open");
    samplesToggle.setAttribute("aria-expanded", open ? "true" : "false");
  };
  window.updateSamplesToggle = () => { $("#motion_samples_toggle_txt").text(t("samples_toggle", sample_motions.length)); };
  setSamplesOpen(false);
  window.updateSamplesToggle();
  samplesToggle.addEventListener("click", () => setSamplesOpen(!samplesBox.hasAttribute("data-open")));
  document.addEventListener("click", (e) => { if (!samplesBox.contains(e.target)) setSamplesOpen(false); });
  $("#motion_samples").on("click", "a", () => setSamplesOpen(false));

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
  // 예전 서버 TTS 시절 30자였다. 지금 합성(mtts.py)은 긴 글을 한국어 120자·영어 300자 단위로 나눠 만든다(260929).
  // 길수록 합성이 오래 걸린다 — 파이보에서 200자에 몇 초인지는 확인 필요
  const max_tts_length = 200;

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
  // kind 'speak' 이면 앞에 이퀄라이저 막대(pibo-ui.css '움직임' 10)를 붙인다 — 말하는 중 표시일 뿐 실제 소리 크기가 아니다
  const setTtsStatus = (text, kind) => {
    ttsStatus.textContent = text;
    if (kind === "speak") ttsStatus.insertAdjacentHTML("afterbegin", '<span class="pb-eq" aria-hidden="true"><i></i><i></i><i></i><i></i></span>');
    ttsStatus.dataset.kind = kind === "speak" ? "" : (kind || "");
  };
  socket.on("tts_status", (d) => {
    if (d && d.stopped) setTtsStatus(t("tts_stopped"));
    else if (d && d.ok) setTtsStatus(t("tts_done"), "ok");
    else setTtsStatus(t("tts_error", (d && d.error) || ""), "err");
  });
  $("#s_tts_stop_bt").on("click", () => socket.emit("tts_stop"));
  // 목소리 모델은 음성 탭을 열 때 서버가 미리 올린다(handleMenu → voice_warm). 처음 한 번 몇 초 걸린다
  let voicePrev = "", ttsPending = false;
  socket.on("tts_status", () => { ttsPending = false; });
  socket.on("voice_state", (st) => {
    if (st === "loading") setTtsStatus(t("voice_loading"), "load");
    else if (st === "ready" && voicePrev === "loading") setTtsStatus(ttsPending ? t("tts_speaking") : t("voice_ready"), ttsPending ? "speak" : "ok");
    else if (st === "error" && voicePrev === "loading") setTtsStatus(t("voice_error"), "err");
    voicePrev = st;
  });
  async function speak() {
    let string = $("#s_tts_val").val().replace(/\s+/g, " ").trim();   // 여러 줄 칸이라 줄바꿈은 띄어쓰기로
    if (string == "") {
      await alert_popup(translations["text_empty"][lang]);
      return;
    }
    if (string.length > max_tts_length) {
      await alert_popup(translations["text_size_limit"][lang](max_tts_length));
      return;
    }
    setTtsStatus(t("tts_speaking"), "speak"); ttsPending = true;
    socket.emit("tts", {
      text: string,
      voice_type: $("select[name=s_voice_type]").val(),
      volume: Number($("#volume").val()),
    });
  }
  $("#s_tts_bt").on("click", speak);
  // Enter 로 말하기(Shift+Enter 는 줄바꿈). 한글 입력기 조합 중의 Enter 는 넘긴다
  $("#s_tts_val").on("keydown", function (evt) {
    if (evt.key === "Enter" && !evt.shiftKey && !evt.originalEvent.isComposing) {
      evt.preventDefault();
      speak();
    }
  });
  // 남은 글자 수 (200자 제한)
  const ttsCount = () => $("#s_tts_count").text(`${$("#s_tts_val").val().length} / ${max_tts_length}`)
    .toggleClass("s-count--full", $("#s_tts_val").val().length >= max_tts_length);
  $("#s_tts_val").on("input", ttsCount);
  ttsCount();


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

/* [동작] v2 는 두 카드를 화면 높이(--motion-h)에 맞춘 세 줄 격자로 놓는다(pibo-ui.css '줄 맞춤').
   사진 크기는 index.js getMotions 의 fitStage 가 가운데 줄에 맞춘다. 900px 이하(태블릿 세로)는 위아래로 쌓는다 */
const fitRobot = () => {
  const sec = document.querySelector("#article_motion > .pibo-section");
  const pane = document.querySelector("main > div.content");
  if (!sec || !pane || !document.body.classList.contains("pb-v2")) return;
  const cs = getComputedStyle(pane);
  const avail = pane.clientHeight - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom) - 8;
  document.getElementById("article_motion").style.setProperty("--motion-h", `${Math.floor(avail)}px`);
};
window.addEventListener("resize", fitRobot);
window.addEventListener("load", fitRobot);
if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitRobot);   // 글꼴이 바뀌면 높이도 바뀐다

// 탭이 가려지면(다른 탭·앱으로 전환, 태블릿 화면 꺼짐) 카메라 보내기를 멈추고, 돌아오면 지금 탭 기준으로 되살린다(260929).
// 서비스는 끄지 않는다(beforeunload 만 끈다 — CLAUDE.md '도구 서비스 수명'). 방치된 탭이 공유기 대역을 계속 쓰던 것
document.addEventListener("visibilitychange", () => {
  const menu = ($("nav button.menu-selected").attr("name") || "").split("_ds")[0];
  socket.emit("vision_sleep", !document.hidden && menu === "vision" ? "off" : "on");
});

const handleMenu = (name) => {
  if (name === "vision") {
    $("#v_tilt_range").val($("#m5_range").val());
    $("#v_pan_range").val($("#m4_range").val());
    $("#v_location").text(`${$("#m4_range").val()}, ${$("#m5_range").val()}`);
    socket.emit("disp_vision");
  } else if (name === "motion") {
    socket.emit("disp_motion");
  } else if (name === "speech") {
    socket.emit("voice_warm");   // 목소리 모델을 미리 올린다(이미 올라와 있으면 서버가 무시)
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
  if (window.refreshVisionState) window.refreshVisionState();
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
