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
socket.on("onoff", function (data) {
  document.getElementById('onoff_val').innerHTML = 
    data
    ? '<i class="fas fa-toggle-on">&nbsp;on</i>'
    : '<i class="fas fa-toggle-off">&nbsp;off</i>'
  console.log('onoff', data)
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

  socket.on("disp_vision", function (data) {
    $("#v_func_type").val(data);
  });

  socket.on("stream", function (data) {
    //console.log('stream', data)
    $("#v_img").prop("src", `data:image/jpeg;charset=utf-8;base64,${data["img"]}`);
    $("#v_result").text(data["data"]);
  });
  
  $("#v_func_type").change(function () {
    socket.emit("detect", $(this).val());
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
  const motor_default = [0, 0, -80, 0, 0, 0, 0, 0, 80, 0];

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
    socket.emit("add_frame", $("#m_time_val").val() * 1000);
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
              $("<td>").append(data[i].seq / 1000 + " 초"),
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
                    Number(lst.eq(idx).text().split(" 초")[0])
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
              let t = $(this).text().split(" 초")[0];
              if (await confirm_popup(translations["confirm_motion_delete"][lang](t))) {
                socket.emit("delete_frame", Number(t) * 1000);
                $(this).remove();
              }
            })
        );
      }
    }
  });

  $("#export_motion_bt").on("click", function() {
    let motion_a = document.createElement("a");
    if($("#motion_name_val").val() == "") motion_a.setAttribute("href", `/export_motion/all`);
    else motion_a.setAttribute("href", `/export_motion/${$("#motion_name_val").val()}`); 
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
      socket.emit("tts", {
        text: string,
        voice_type: $("select[name=s_voice_type]").val(),
        volume: Number($("#volume").val()),
      });
    }
  });

  $("#s_upload_csv").on("change", (e) => {
    let formData = new FormData();
    formData.append("data", $("#s_upload_csv")[0].files[0]);
    $("#s_upload_csv").val("");
    $.ajax({
      url: `/upload_csv`,
      type: "post",
      data: formData,
      contentType: false,
      processData: false,
    }).always(async (xhr, status) => {
      if (status == "success") {
        await alert_popup(translations["file_ok"][lang]);
      } else {
        await alert_popup(`${translations["file_error"][lang]}\n >> ${xhr.responseJSON["result"]}`);
        $("#s_upload_csv").val("");
      }
    });
  });

  $("#s_reset_csv_bt").on("click", async function () {
    socket.emit("reset_csv", {lang: lang});
    $("#s_upload_csv").val("");
    await alert_popup(translations["reset_ok"][lang]);
  });

  $("#s_question_val").on("keyup", function () {
    $(this).val(
      $(this)
        .val()
        // .replace(/[^ㄱ-ㅣ가-힣 | 0-9 |?|.|,|'|"|!]/g, "")
    );
  });

  $("#s_question_val").on("keypress", async function (evt) {
    if (evt.keyCode == 13) {
      // enter
      q = $("#s_question_val").val().trim();
      if (q == "") {
        await alert_popup(translations["text_empty"][lang]);
        return;
      }

      $("#s_question_val").prop("disabled", true);

      setTimeout(function () {
        $("#s_question_val").val(".");
      }, 200);
      setTimeout(function () {
        $("#s_question_val").val("..");
      }, 400);
      setTimeout(function () {
        $("#s_question_val").val("...");
      }, 600);

      setTimeout(function () {
        socket.emit("question", {
          question: q.toLowerCase(),
          n: lang=="ko"?2:4,
          voice_en: $("input[name=s_voice_en]:checked").val(),
          voice_type: $("select[name=s_voice_type]").val(),
          volume: Number($("#volume").val()),
        });
        $("#s_question_val").prop("disabled", false);
        $("#s_question_val").val(q);
      }, 800);
    }
  });

  $("#s_chat_bt").on("click", async function () {
    q = $("#s_question_val").val().trim();

    if (q == "") {
      await alert_popup(translations["text_empty"][lang]);
      return;
    }

    $("#s_question_val").prop("disabled", true);
    setTimeout(function () {
      $("#s_question_val").val(".");
    }, 200);
    setTimeout(function () {
      $("#s_question_val").val("..");
    }, 400);
    setTimeout(function () {
      $("#s_question_val").val("...");
    }, 600);

    setTimeout(function () {
      socket.emit("question", {
        question: q.toLowerCase(),
        n: lang=="ko"?2:4,
        voice_en: $("input[name=s_voice_en]:checked").val(),
        voice_type: $("select[name=s_voice_type]").val(),
        volume: Number($("#volume").val()),
      });
      $("#s_question_val").prop("disabled", false);
      $("#s_question_val").val(q);
    }, 800);
  });

  $("#s_translate_bt").on("click", async () => {
    txt = $("#s_translate_val").val().trim();
    if (txt == "") {
      await alert_popup(translations["text_empty"][lang]);
      return;
    }

    socket.emit("translate", {
      langtype:$("select[name=s_lang_type]").val(),
      voice_en: $("input[name=s_voice_en]:checked").val(),
      volume: Number($("#volume").val()),
      text: txt
    });
  });

  $("#s_translate_val").on("keypress", async function (evt) {
    if (evt.keyCode == 13) {
      txt = $("#s_translate_val").val().trim();
      if (txt == "") {
        await alert_popup(translations["text_empty"][lang]);
        return;
      }
  
      socket.emit("translate", {
        langtype:$("select[name=s_lang_type]").val(),
        voice_en: $("input[name=s_voice_en]:checked").val(),
        volume: Number($("#volume").val()),
        text: txt
      });
    }
  });

  socket.on("disp_translate", (data) => {
    $("#s_translate_result_val").val(data);
  });


  socket.on("mic", function (d) {
    //console.log('mic', d)
    $("#mic_status").text(d);
  });

  $("#mic_bt").on("click", async function () {
    let tmictime = "#mic_time_val";
    let val = Number($(tmictime).val());
    let min = Number($(tmictime).attr("min"));
    let max = Number($(tmictime).attr("max"));

    if (isNaN(val) || val < min || val > max) {
      await alert_popup(translations["audio_input_error"][lang]);
      return;
    }

    $("#mic_status").html("<i class='fa-solid fa-fade'>녹음 중</i>");
    socket.emit("mic", {
      time: val,
      volume: Number($("#volume").val()),
    });
  });

  $("#mic_replay_bt").on("click", function () {
    socket.emit("mic_replay", { volume: Number($("#volume").val()) });
  });



  socket.on("disp_speech", function (data) {
    if ("answer" in data) {
      $("#s_answer_val").val(data["answer"]);
    }

    if ("chat_list" in data) {
      $("#s_record_tb > tbody").empty();
      rec = data["chat_list"];

      for (idx in rec) {
        if (rec[idx].length == 0) continue;

        $("#s_record_tb").append(
          $("<tr>").append(
            $("<td>").append(rec[idx][0]),
            $("<td>").append(rec[idx][1]),
            $("<td>").append(rec[idx][2])
          )
        );
      }
    }
  });
};

const handleMenu = (name) => {
  if (name === "speech") {
    $("#s_question_val").val("");
    $("#s_answer_val").val("");
    socket.emit("disp_speech");
  } else if (name === "vision") {
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
  $(`#article_${name}`).show("slide");
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


fetch(`http://${location.hostname}/tools?enable=on`)
.then(response => {
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.text();
})
.then(data => {
//   //console.log('데이터 수신 성공:', data);
})
.catch(error => {
//   console.error('데이터 요청 중 에러 발생:', error);
})

window.addEventListener('beforeunload', (evt) => {
  fetch(`http://${location.hostname}/tools?enable=off`)
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.text();
  })
  .then(data => {
  //   //console.log('데이터 수신 성공:', data);
  })
  .catch(error => {
  //   console.error('데이터 요청 중 에러 발생:', error);
  })
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
  localStorage.setItem("language", lang);
});
