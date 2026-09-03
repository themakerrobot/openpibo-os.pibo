const blang = (navigator.language || navigator.userLanguage).includes('ko')?'ko':'en';
let lang = localStorage.getItem("language")?localStorage.getItem("language"):blang;

const translations = {
  title:            { ko: "이미지 분류",              en: "Image Classifier" },
  class_manage:     { ko: "클래스 관리",              en: "Classes" },
  class_name_ph:    { ko: "클래스 이름",              en: "Class name" },
  class_add:        { ko: "클래스 추가",              en: "Add class" },
  image_train:      { ko: "이미지 학습",              en: "Training" },
  cam_on:           { ko: "카메라 켜기",              en: "Camera on" },
  cam_off:          { ko: "카메라 끄기",              en: "Camera off" },
  add_sample:       { ko: "샘플 추가",                en: "Add samples" },
  train:            { ko: "학습하기",                 en: "Train" },
  epochs:           { ko: "반복 학습 횟수: ",         en: "Epochs: " },
  batch:            { ko: "한번에 학습할 이미지 수: ", en: "Batch size: " },
  result:           { ko: "결과 및 예측",             en: "Results" },
  import_tfjs:      { ko: "불러오기(tfjs)",           en: "Import (tfjs)" },
  export_tfjs:      { ko: "내보내기(tfjs)",           en: "Export (tfjs)" },
  save_keras:       { ko: "mymodel 저장(keras)",      en: "Save to mymodel (keras)" },
  init_wait:        { ko: "초기화 중입니다.",         en: "Initializing..." },
  init_done:        { ko: "초기화를 완료했습니다.",   en: "Ready." },
  predict_title:    { ko: "예측 결과",                en: "Prediction" },
  preview:          { ko: "미리보기",                 en: "Preview" },
  inference:        { ko: "추론하기",                 en: "Infer" },
  no_prediction:    { ko: "아직 예측이 없습니다",     en: "No prediction yet" },
  preview_running:  { ko: "(미리보기 실행 중)",       en: "(Preview running)" },
  infer_running:    { ko: "(추론 실행 중)",           en: "(Inference running)" },
  ok:               { ko: "확인",                     en: "OK" },
  cancel:           { ko: "취소",                     en: "Cancel" },
  download:         { ko: "다운로드",                 en: "Download" },
  upload:           { ko: "업로드",                   en: "Upload" },
  delete:           { ko: "삭제",                     en: "Delete" },
  training:         { ko: "학습 중 ...",              en: "Training ..." },
  train_done:       { ko: "학습 완료",                en: "Training complete" },
  model_loaded:     { ko: "모델을 불러왔습니다.",     en: "Model loaded." },
  converting:       { ko: "모델 변환중",              en: "Converting" },

  select_class:     { ko: "이미지 추가할 클래스를 선택하세요.", en: "Select a class to add images to." },
  no_data:          { ko: "학습할 데이터가 없습니다. 이미지를 추가해주세요.", en: "No training data. Add some images first." },
  no_model:         { ko: "모델이 없습니다. 먼저 학습하기 또는 불러오기를 실행하세요.", en: "No model. Train or import a model first." },
  confirm_del_img:  { ko: "이 이미지를 삭제하시겠습니까?", en: "Delete this image?" },
  export_fail:      { ko: "모델을 내보내는 도중 오류가 발생했습니다.", en: "Failed to export the model." },
  missing_weights:  { ko: "weights.bin 파일이 누락되었습니다.", en: "weights.bin is missing." },
  missing_specs:    { ko: "weightsSpecs.json 파일이 누락되었습니다.", en: "weightsSpecs.json is missing." },
  import_ok:        { ko: "모델을 성공적으로 불러왔습니다.", en: "Model imported successfully." },
  import_fail:      { ko: "모델을 불러오는 중 오류가 발생했습니다.", en: "Failed to import the model." },
  convert_ok:       { ko: "H5 변환 성공! converted_h5.zip이 다운로드 되었습니다.", en: "Converted to H5. converted_h5.zip downloaded." },
  convert_fail:     { ko: "모델 변환 중 오류가 발생했습니다.", en: "Failed to convert the model." },

  confirm_del_class:{ ko: (n) => `${n} 클래스를 삭제하시겠습니까?`, en: (n) => `Delete class "${n}"?` },
  upload_done:      { ko: (n) => `${n} 데이터셋 업로드 했습니다.`, en: (n) => `Dataset uploaded to "${n}".` },
  convert_req_fail: { ko: (m) => `모델 변환 요청 실패: ${m}`, en: (m) => `Conversion request failed: ${m}` },
  prediction:       { ko: (c, p) => `예측 클래스: ${c} (신뢰도: ${p}%)`, en: (c, p) => `Predicted: ${c} (confidence: ${p}%)` },
};

const t = (key, ...args) => {
  const v = (translations[key] || {})[lang];
  if (v === undefined) return key;
  return typeof v === 'function' ? v(...args) : v;
};

const setLanguage = (langCode) => {
  lang = langCode;
  document.documentElement.lang = langCode;
  document.querySelectorAll('[data-key]').forEach(el => {
    const key = el.getAttribute('data-key');
    if (!translations[key]) return;
    if (el.tagName === 'INPUT') el.placeholder = translations[key][langCode];
    else el.textContent = translations[key][langCode];
  });
  localStorage.setItem("language", langCode);
};
