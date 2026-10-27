const blang = 'en';
let lang = localStorage.getItem("language") || blang;

// 도구 화면 문구. 261028: 말투·용어 정리(해요체, 동작·저장·지우기 …), 쓰지 않던 옛 키(시퀀스·OLED·눈 색 등) 정리.
// 새 키는 파일 끝에 붙인다(1·2행이 영문판 델타라 그 근처는 피한다)
const translations = {
  nav_tools_title: { ko: "도구",     en: "Tools" },
  nav_fullscreen:  { ko: "전체화면", en: "Full screen" },
  nav_motion:      { ko: "동작",     en: "Motion" },
  nav_vision:      { ko: "카메라",   en: "Camera" },
  nav_speech:      { ko: "음성",     en: "Speech" },
  sec:       { ko: "초", en: " s" },
  recording: { ko: "녹음 중…", en: "Recording…" },
  confirm:   { ko: "확인", en: "OK" },
  cancel:    { ko: "취소", en: "Cancel" },
  volume:    { ko: "음량", en: "Volume" },
  second:    { ko: "초",   en: "s" },
  record:    { ko: "녹음", en: "Record" },
  replay:    { ko: "다시 듣기", en: "Play again" },
  stop:      { ko: "정지", en: "Stop" },
  init_motors: { ko: "처음 자세", en: "Home pose" },
  time:        { ko: "시간", en: "Time" },
  add:         { ko: "추가", en: "Add" },
  play_cycle:  { ko: "반복", en: "Repeat" },
  execute:     { ko: "실행", en: "Run" },
  motion_name: { ko: "동작 이름", en: "Motion name" },
  register:    { ko: "저장", en: "Save" },
  load:        { ko: "불러오기", en: "Load" },
  remove:      { ko: "지우기", en: "Delete" },
  example:     { ko: "예제", en: "Examples" },
  camera:      { ko: "카메라", en: "Camera" },
  vision_use:       { ko: "비전 기능", en: "Vision features" },
  function_setting: { ko: "기능 고르기", en: "Choose a feature" },
  v_grayscale:            { ko: "흑백",         en: "Grayscale" },
  v_canny:                { ko: "윤곽선",       en: "Edges" },
  v_edgePreservingFilter: { ko: "흐리게",       en: "Soften" },
  v_cartoon:              { ko: "만화",         en: "Cartoon" },
  v_sketch_rgb:           { ko: "스케치 (컬러)", en: "Sketch (color)" },
  v_detail:               { ko: "선명하게",     en: "Sharpen" },
  v_qr:                   { ko: "QR 코드",      en: "QR code" },
  v_face:                 { ko: "얼굴 분석",    en: "Face analysis" },
  v_face_landmark:        { ko: "얼굴 특징점",  en: "Face landmarks" },
  v_object:               { ko: "사물 인식",    en: "Object detection" },
  v_hand:                 { ko: "손동작 인식",  en: "Hand gesture" },
  v_pose:                 { ko: "포즈 인식",    en: "Pose detection" },
  v_track:                { ko: "사물 추적",    en: "Object tracking" },
  v_marker:               { ko: "마커 인식",    en: "Marker detection" },
  v_marker_length:        { ko: "마커 길이",    en: "Marker length" },
  save_image:      { ko: "사진 저장", en: "Save photo" },
  camera_position: { ko: "카메라 위치", en: "Camera position" },
  result:          { ko: "결과", en: "Result" },
  speak:           { ko: "말하기", en: "Speak" },
  voice_type:      { ko: "목소리", en: "Voice" },
  espeak:          { ko: "기계음 (espeak)", en: "Robot voice (espeak)" },
  file_ok:    { ko: "파일을 올렸어요.", en: "File uploaded." },
  file_error: { ko: "파일을 올리지 못했어요.", en: "Could not upload the file." },
  range_warn: {
    ko: (min, max) => `${min}~${max} 사이의 값을 적어 주세요.`,
    en: (min, max) => `Enter a value between ${min} and ${max}.`
  },
  motion_empty:      { ko: "표가 비어 있어요. 먼저 자세를 표에 추가해 주세요.", en: "The table is empty. Add a pose to the table first." },
  motion_name_empty: { ko: "먼저 동작 이름을 적어 주세요.", en: "Enter a motion name first." },
  text_empty:        { ko: "말할 글자를 적어 주세요.", en: "Enter the text to speak." },
  text_size_limit: {
    ko: (max_limit) => `글자는 ${max_limit}자까지 쓸 수 있어요.`,
    en: (max_limit) => `You can enter up to ${max_limit} characters.`
  },
  audio_input_error: { ko: "녹음 시간은 1~30초로 적어 주세요.", en: "Enter a recording time from 1 to 30 s." },
  confirm_motion_delete: {
    ko: (name) => `"${name}" 동작을 지울까요?`,
    en: (name) => `Delete the motion "${name}"?`
  },
  confirm_motion_delete_all: { ko: "저장된 동작을 모두 지울까요?\n되돌릴 수 없어요.", en: "Delete all saved motions?\nThis cannot be undone." },
  confirm_motion_register: {
    ko: (name) => `"${name}" 이름으로 동작을 저장할까요?`,
    en: (name) => `Save the motion as "${name}"?`
  },
  confirm_motion_load: {
    ko: (name) => `"${name}" 동작을 불러올까요?`,
    en: (name) => `Load the motion "${name}"?`
  },
  text:   { ko: "말할 글자", en: "Text to speak" },
  import: { ko: "가져오기", en: "Import" },
  export: { ko: "내보내기", en: "Export" },
  // [동작] 화면 정리(260928)
  motor_m0: { ko: "M0 오른발",     en: "M0 Right foot" },
  motor_m1: { ko: "M1 오른다리",   en: "M1 Right leg" },
  motor_m2: { ko: "M2 오른팔",     en: "M2 Right arm" },
  motor_m3: { ko: "M3 오른손",     en: "M3 Right hand" },
  motor_m4: { ko: "M4 고개 좌우",  en: "M4 Head left/right" },
  motor_m5: { ko: "M5 고개 위아래", en: "M5 Head up/down" },
  motor_m6: { ko: "M6 왼발",       en: "M6 Left foot" },
  motor_m7: { ko: "M7 왼다리",     en: "M7 Left leg" },
  motor_m8: { ko: "M8 왼팔",       en: "M8 Left arm" },
  motor_m9: { ko: "M9 왼손",       en: "M9 Left hand" },
  clear_frames:       { ko: "표 비우기",        en: "Clear table" },
  remove_all_motions: { ko: "동작 모두 지우기", en: "Delete all motions" },
  saved_motions: { ko: "저장된 동작", en: "Saved motions" },
  robot_ready:   { ko: "로봇 연결됨",  en: "Robot connected" },
  robot_waiting: { ko: "로봇 준비 중…", en: "Loading robot…" },
  // [카메라]·[음성] 정리(260928)
  v_camera:       { ko: "카메라", en: "Camera" },
  camera_waiting: { ko: "카메라 화면을 기다리는 중…", en: "Waiting for the camera…" },
  // [음성] 목소리 10가지 — PiBrain 도구와 같다(SpeechOnDevice m1~m5 / f1~f5)
  voice_m1: { ko: "남성 1", en: "Male 1" },  voice_m2: { ko: "남성 2", en: "Male 2" },
  voice_m3: { ko: "남성 3", en: "Male 3" },  voice_m4: { ko: "남성 4", en: "Male 4" },
  voice_m5: { ko: "남성 5", en: "Male 5" },
  voice_f1: { ko: "여성 1", en: "Female 1" }, voice_f2: { ko: "여성 2", en: "Female 2" },
  voice_f3: { ko: "여성 3", en: "Female 3" }, voice_f4: { ko: "여성 4", en: "Female 4" },
  voice_f5: { ko: "여성 5", en: "Female 5" },
  tts_speaking: { ko: "말하는 중…", en: "Speaking…" },
  tts_done:     { ko: "다 말했어요", en: "Done" },
  tts_stopped:  { ko: "멈췄어요",   en: "Stopped" },
  tts_error:    { ko: (e) => `말하지 못했어요. ${e}`, en: (e) => `Could not speak. ${e}` },
  samples_toggle: { ko: (n) => `예제 동작 ${n}개`, en: (n) => `Sample motions (${n})` },
  // [동작] 표에 추가(260928)
  scene_delete: { ko: "이 줄 지우기", en: "Delete row" },
  add_or_edit:  { ko: "추가·수정", en: "Add or update" },
  scene_help:   { ko: "누를 때마다 시간 +0.5초", en: "Time +0.5 s on each press" },
  add_or_edit_tip: { ko: "지금 자세를 이 시간에 넣어요. 표에 같은 시간이 있으면 그 줄을 고쳐요.", en: "Puts this pose at this time. If the table already has this time, that row is updated." },
  scene_keys:   { ko: "← → 모터 · ↑ ↓ 1° (Shift 5°) · Enter 추가·수정", en: "← → motor · ↑ ↓ 1° (Shift 5°) · Enter add or update" },
  frames_empty_v2: {
    ko: "표가 비어 있어요. 왼쪽에서 자세를 잡고 [추가·수정]을 누르세요.",
    en: "The table is empty. Pose the robot on the left and press [Add or update]."
  },
  confirm_frame_delete: { ko: (s) => `${s}초 줄을 지울까요?`, en: (s) => `Delete the row at ${s} s?` },
  // 준비 단계(260929): [로봇 연결됨] 뒤에 카메라 쪽을 이어서 올린다
  vs_camera:    { ko: "카메라 켜는 중…",        en: "Starting the camera…" },
  vs_detect:    { ko: "사물·손 인식 준비 중…",   en: "Loading object and hand recognition…" },
  vs_face:      { ko: "얼굴 인식 준비 중…",      en: "Loading face recognition…" },
  vs_ready:     { ko: "카메라 준비됐어요",      en: "Camera ready" },
  vs_error:     { ko: (e) => `카메라를 준비하지 못했어요. ${e}`, en: (e) => `Could not start the camera. ${e}` },
  vs_tile_wait: { ko: "준비 중", en: "Loading" },
  voice_loading:{ ko: "목소리 준비 중… (처음 한 번만 몇 초 걸려요)", en: "Loading voices… (a few seconds, first time only)" },
  voice_ready:  { ko: "목소리 준비됐어요", en: "Voices ready" },
  voice_error:  { ko: "목소리를 준비하지 못했어요.", en: "Could not load the voices." },
  saved_empty:  { ko: "아직 저장한 동작이 없어요.", en: "No saved motions yet." },
  // 동작 파일 가져오기(261027): 서버가 400 과 함께 이 키를 보낸다
  motion_file_invalid: { ko: "동작 파일이 아니거나 내용이 잘못됐어요.", en: "This is not a motion file, or its content is invalid." },
  not_ready:    { ko: "로봇이 아직 준비되지 않았어요.", en: "The robot is not ready yet." },
  // 261028 — 말투 정리 때 더한 키
  confirm_clear_frames: { ko: "표를 비울까요?", en: "Clear the table?" },
  tts_err_voice:      { ko: "쓸 수 없는 목소리예요.", en: "This voice is not available." },
  motion_export_none: { ko: "저장된 동작이 없어요.", en: "There are no saved motions." },
  motion_not_found:   { ko: "고른 동작이 없어요. 이름을 확인해 주세요.", en: "That motion does not exist. Check the name." },
  camera_not_ready:   { ko: "카메라가 아직 준비되지 않았어요.", en: "The camera is not ready yet." },
  download_failed:    { ko: "내려받지 못했어요.", en: "Could not download." },
  language:           { ko: "언어", en: "Language" },
};

// 키 → 현재 언어 문자열. 모르는 키(일반 문자열)는 그대로 반환.
const t = (key, ...args) => {
  const v = (translations[key] || {})[lang];
  if (v === undefined) return key;
  return typeof v === 'function' ? v(...args) : v;
};
