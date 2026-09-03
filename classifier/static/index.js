let fullscreen = false;

const fullscreenTxt = document.getElementById('fullscreen_txt');
const fullscreenBt = document.getElementById('fullscreen_bt');

const updateIcon = () => {
    fullscreenTxt.innerHTML = fullscreen
        ? '<i class="fa-solid fa-minimize"></i>'
        : '<i class="fa-solid fa-maximize"></i>';
};

updateIcon();

fullscreenBt.addEventListener('click', (e) => {
    e.preventDefault();
    if (!fullscreen && document.documentElement.requestFullscreen) {
        document.documentElement.requestFullscreen();
        fullscreen = true;
    } else if (fullscreen && document.exitFullscreen) {
        document.exitFullscreen();
        fullscreen = false;
    }
    updateIcon();
});

document.addEventListener('fullscreenchange', () => {
    fullscreen = !!document.fullscreenElement;
    updateIcon();
});

// --- language ---
const language = document.getElementById("language");
language.value = lang;
setLanguage(lang);
language.addEventListener("change", () => setLanguage(language.value));

// --- popup elements ---
const alertPopup = document.getElementById('alertPopup');
const confirmPopup = document.getElementById('confirmPopup');
const promptPopup = document.getElementById('promptPopup');

const alertMessageElement = document.getElementById('alertMessageElement');
const alertOkBtn = document.getElementById('alertOkBtn');

function hidePopups() {
    if (alertPopup) alertPopup.style.display = 'none';
    if (confirmPopup) confirmPopup.style.display = 'none';
    if (promptPopup) promptPopup.style.display = 'none';
}

async function alert_popup(message) {
    hidePopups();
    if (!alertPopup || !alertMessageElement || !alertOkBtn) {
        console.error("Alert popup elements not found!");
        return;
    }
    alertMessageElement.textContent = message;
    alertPopup.style.display = 'flex';
    alertOkBtn.focus();
    const handler = () => { hidePopups(); };
    alertOkBtn.removeEventListener('click', handler);
    alertOkBtn.addEventListener('click', handler, { once: true });
}

async function confirm_popup(message) {
    return new Promise((resolve) => {
        hidePopups();
        const popupElement = document.getElementById('confirmPopup');
        const msgElement = document.getElementById('confirmMessageElement');
        const okButton = document.getElementById('confirmOkBtn');
        const cancelButton = document.getElementById('confirmCancelBtn');
        if (!popupElement || !msgElement || !okButton || !cancelButton) {
            console.error("confirm_popup: elements not found", { popupElement, msgElement, okButton, cancelButton });
            resolve(false);
            return;
        }
        msgElement.textContent = message;
        popupElement.style.display = 'flex';
        okButton.focus();

        const okHandler = () => { cleanup(); resolve(true); };
        const cancelHandler = () => { cleanup(); resolve(false); };
        const cleanup = () => {
            okButton.removeEventListener('click', okHandler);
            cancelButton.removeEventListener('click', cancelHandler);
            hidePopups();
        };
        okButton.removeEventListener('click', okHandler);
        cancelButton.removeEventListener('click', cancelHandler);
        okButton.addEventListener('click', okHandler);
        cancelButton.addEventListener('click', cancelHandler);
    });
}

async function prompt_popup(message, defaultValue = '') {
    return new Promise((resolve) => {
        hidePopups();
        const popupElement = document.getElementById('promptPopup');
        const msgElement = document.getElementById('promptMessageElement');
        const inputElement = document.getElementById('promptInputElement');
        const okButton = document.getElementById('promptOkBtn');
        const cancelButton = document.getElementById('promptCancelBtn');
        if (!popupElement || !msgElement || !inputElement || !okButton || !cancelButton) {
            console.error("prompt_popup: elements not found", { popupElement, msgElement, inputElement, okButton, cancelButton });
            resolve(null);
            return;
        }
        msgElement.textContent = message;
        inputElement.value = defaultValue;
        popupElement.style.display = 'flex';
        inputElement.focus();

        const okHandler = () => { cleanup(); resolve(inputElement.value); };
        const cancelHandler = () => { cleanup(); resolve(null); };
        const enterKeyHandler = (event) => { if (event.key === 'Enter') okHandler(); };
        const cleanup = () => {
            okButton.removeEventListener('click', okHandler);
            cancelButton.removeEventListener('click', cancelHandler);
            inputElement.removeEventListener('keydown', enterKeyHandler);
            hidePopups();
        };
        okButton.removeEventListener('click', okHandler);
        cancelButton.removeEventListener('click', cancelHandler);
        inputElement.removeEventListener('keydown', enterKeyHandler);
        okButton.addEventListener('click', okHandler);
        cancelButton.addEventListener('click', cancelHandler);
        inputElement.addEventListener('keydown', enterKeyHandler);
    });
}

document.getElementById("logo_bt").addEventListener("click", () => {
    location.href = `http://${location.hostname}`;
});

// 1) Socket.IO
const socket = io(`http://${location.host}`, { path: "/socket.io" });
socket.on("camera_image", (data) => {
    const cameraImg = document.getElementById('camera');
    cameraImg.src = "data:image/jpeg;base64," + data;
});

// 2) globals & MobileNet
const MOBILE_NET_INPUT_WIDTH = 224;
const MOBILE_NET_INPUT_HEIGHT = 224;
const CLASS_NAMES = [];
let mobilenet;
let model;
let gatherDataState = -1;
let trainingDataInputs = [];
let trainingDataOutputs = [];
let predict = false;
let capturing = false;
let captureInterval;
let previewing = false;
let predictInterval = null;
let cameraEnabled = false;

const BLANK_IMG = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z/C/HwAF/gL+eCDUMAAAAABJRU5ErkJggg==";

// 상태 메시지는 data-key로 표시해 언어 전환 시 같이 바뀌게 함
function setProgress(key, text) {
    const el = document.getElementById('training-progress');
    if (key) { el.setAttribute('data-key', key); el.innerText = t(key); }
    else { el.removeAttribute('data-key'); el.innerText = text; }
}

async function loadMobileNetFeatureModel() {
    const URL = 'static/model.json';
    const tmp_model = await tf.loadLayersModel(URL);
    const layer = tmp_model.getLayer('global_average_pooling2d_1');
    mobilenet = tf.model({ inputs: tmp_model.inputs, outputs: layer.output });
    tf.tidy(() => {
        mobilenet.predict(tf.zeros([1, MOBILE_NET_INPUT_HEIGHT, MOBILE_NET_INPUT_WIDTH, 3]));
    });
    setProgress('init_done');
}
loadMobileNetFeatureModel();

// 3) class management
function addClass() {
    const className = document.getElementById('class-name').value.trim();
    if (className && !CLASS_NAMES.includes(className)) {
        CLASS_NAMES.push(className);
        const classContainer = document.createElement('div');
        classContainer.className = 'class-container';
        classContainer.id = `class-${className}`;
        const h3 = document.createElement('h3');
        h3.innerText = className;
        classContainer.onclick = () => selectClass(className);
        classContainer.appendChild(h3);
        const imageCollection = document.createElement('div');
        imageCollection.className = 'image-collection';
        classContainer.appendChild(imageCollection);
        const btnGroup = document.createElement('div');
        btnGroup.className = 'class-buttons';

        const downloadButton = document.createElement('button');
        downloadButton.innerHTML = `<i class="fas fa-download"></i> <span data-key="download">${t('download')}</span>`;
        downloadButton.onclick = (e) => {
            e.stopPropagation();
            downloadClassDataset(className);
        };
        btnGroup.appendChild(downloadButton);

        const uploadInput = document.createElement('input');
        uploadInput.type = 'file';
        uploadInput.accept = '.zip';
        uploadInput.style.display = 'none';
        uploadInput.onchange = (e) => { uploadClassDataset(e, className); };
        const uploadLabel = document.createElement('label');
        uploadLabel.innerHTML = `<i class="fas fa-upload"></i> <span data-key="upload">${t('upload')}</span>`;
        uploadLabel.classList.add('upload-button');
        uploadLabel.onclick = () => { uploadInput.click(); };
        btnGroup.appendChild(uploadInput);
        btnGroup.appendChild(uploadLabel);

        const deleteButton = document.createElement('button');
        deleteButton.innerHTML = `<i class="fas fa-trash"></i> <span data-key="delete">${t('delete')}</span>`;
        deleteButton.onclick = async (e) => {
            e.stopPropagation();
            if (await confirm_popup(t('confirm_del_class', className))) {
                classContainer.remove();
                const classIndex = CLASS_NAMES.indexOf(className);
                if (classIndex > -1) {
                    CLASS_NAMES.splice(classIndex, 1);
                    trainingDataInputs = trainingDataInputs.filter((_, i) => trainingDataOutputs[i] !== classIndex);
                    trainingDataOutputs = trainingDataOutputs.filter(output => output !== classIndex);
                    trainingDataOutputs = trainingDataOutputs.map(output => (output > classIndex ? output - 1 : output));
                }
            }
        };
        btnGroup.appendChild(deleteButton);
        classContainer.appendChild(btnGroup);
        document.getElementById('class-list').appendChild(classContainer);
        document.getElementById('class-name').value = '';
    }
}
function selectClass(className) {
    document.querySelectorAll('.class-container').forEach(container => {
        container.classList.remove('selected');
    });
    gatherDataState = CLASS_NAMES.indexOf(className);
    const selectedClassContainer = document.getElementById(`class-${className}`);
    if (selectedClassContainer) {
        selectedClassContainer.classList.add('selected');
    }
}

// 4) capture
async function startCapturingImages() {
    if (gatherDataState === -1) {
        await alert_popup(t('select_class'));
        return;
    }
    capturing = true;
    captureInterval = setInterval(() => {
        if (capturing) captureImage();
    }, 100);
}
function stopCapturingImages() {
    capturing = false;
    clearInterval(captureInterval);
}
function captureImage() {
    const cameraImg = document.getElementById('camera');
    try {
        const imgTensor = tf.tidy(() => {
            return tf.browser.fromPixels(cameraImg)
                .resizeNearestNeighbor([MOBILE_NET_INPUT_HEIGHT, MOBILE_NET_INPUT_WIDTH])
                .toFloat()
                .div(tf.scalar(255));
        });
        addImageToClass(imgTensor, gatherDataState);
    } catch (error) {
        console.error("Error capturing image:", error);
    }
}
function addImageToClass(imgTensor, classIndex) {
    try {
        const features = mobilenet.predict(imgTensor.expandDims()).squeeze();
        trainingDataInputs.push(features);
        trainingDataOutputs.push(classIndex);
        const imageElement = document.createElement('img');
        tf.browser.toPixels(imgTensor).then((pixels) => {
            const canvas = document.createElement('canvas');
            canvas.width = MOBILE_NET_INPUT_WIDTH;
            canvas.height = MOBILE_NET_INPUT_HEIGHT;
            const ctx = canvas.getContext('2d');
            const imageData = new ImageData(pixels, MOBILE_NET_INPUT_WIDTH, MOBILE_NET_INPUT_HEIGHT);
            ctx.putImageData(imageData, 0, 0);
            imageElement.src = canvas.toDataURL();
            imageElement.className = 'thumbnail';
            imageElement.onclick = async () => {
                if (await confirm_popup(t('confirm_del_img'))) {
                    imageElement.remove();
                }
            };
            document.querySelector(`#class-${CLASS_NAMES[classIndex]} .image-collection`).appendChild(imageElement);
        });
    } catch (error) {
        console.error("Error adding image to class:", error);
    }
}

// 5) dataset up/download
async function uploadClassDataset(event, className) {
    const file = event.target.files[0];
    if (file) {
        const zip = await JSZip.loadAsync(file);
        const imageFiles = Object.keys(zip.files).filter(name => name.endsWith('.png'));
        for (const imageName of imageFiles) {
            const imageData = await zip.file(imageName).async('base64');
            const imgElement = document.createElement('img');
            imgElement.src = `data:image/png;base64,${imageData}`;
            imgElement.className = 'thumbnail';
            imgElement.onload = () => {
                if (imgElement.naturalWidth > 0 && imgElement.naturalHeight > 0) {
                    const imgTensor = tf.tidy(() => {
                        return tf.browser.fromPixels(imgElement)
                            .resizeNearestNeighbor([MOBILE_NET_INPUT_HEIGHT, MOBILE_NET_INPUT_WIDTH])
                            .toFloat()
                            .div(tf.scalar(255));
                    });
                    addImageToClass(imgTensor, CLASS_NAMES.indexOf(className));
                } else {
                    console.warn("Skipping corrupted image", imageName);
                }
            };
        }
        await alert_popup(t('upload_done', className));
    }
}
function downloadClassDataset(className) {
    const zip = new JSZip();
    const classFolder = zip.folder(className);
    const imageElements = document.querySelectorAll(`#class-${className} .image-collection img`);
    imageElements.forEach((imgElement, index) => {
        const dataURL = imgElement.src;
        const binary = atob(dataURL.split(',')[1]);
        const array = [];
        for (let i = 0; i < binary.length; i++) {
            array.push(binary.charCodeAt(i));
        }
        classFolder.file(`image_${index}.png`, new Uint8Array(array), { binary: true });
    });
    zip.generateAsync({ type: 'blob' }).then(function (content) {
        const a = document.createElement('a');
        a.href = URL.createObjectURL(content);
        a.download = `${className}_dataset.zip`;
        a.click();
    });
}

// 6) train
async function trainAndPredict() {
    if (trainingDataInputs.length === 0) {
        await alert_popup(t('no_data'));
        return;
    }
    predict = false;
    setProgress('training');
    tf.util.shuffleCombo(trainingDataInputs, trainingDataOutputs);
    let outputsAsTensor = tf.tensor1d(trainingDataOutputs, 'int32');
    let oneHotOutputs = tf.oneHot(outputsAsTensor, CLASS_NAMES.length);
    let inputsAsTensor = tf.stack(trainingDataInputs);
    model = tf.sequential();
    model.add(tf.layers.dense({ inputShape: [1280], units: 128, activation: 'relu' }));
    model.add(tf.layers.dropout({ rate: 0.3 }));
    model.add(tf.layers.dense({ units: CLASS_NAMES.length, activation: 'softmax' }));
    model.compile({
        optimizer: 'adam',
        loss: 'categoricalCrossentropy',
        metrics: ['accuracy']
    });
    model.fit(inputsAsTensor, oneHotOutputs, {
        shuffle: true,
        batchSize: parseInt(document.getElementById('batch-size').value),
        epochs: parseInt(document.getElementById('epochs').value),
        callbacks: { onEpochEnd: logProgress }
    }).then(() => {
        outputsAsTensor.dispose();
        oneHotOutputs.dispose();
        inputsAsTensor.dispose();
        setProgress('train_done');
        predict = true;
    });
}
function logProgress(epoch, logs) {
    setProgress(null, `Epoch: ${epoch}, ${JSON.stringify(logs)}`);
}

async function predictImage() {
    const cameraImg = document.getElementById('camera');
    const img = tf.tidy(() =>
        tf.browser.fromPixels(cameraImg)
            .resizeNearestNeighbor([MOBILE_NET_INPUT_HEIGHT, MOBILE_NET_INPUT_WIDTH])
            .toFloat()
            .div(tf.scalar(255.0))
            .expandDims()
    );
    const features = tf.tidy(() => mobilenet.predict(img).flatten());
    const prediction = tf.tidy(() => model.predict(features.expandDims()));
    const predictionData = await prediction.data();
    const classIndex = prediction.argMax(-1).dataSync()[0];
    const confidence = predictionData[classIndex];
    const className = CLASS_NAMES[classIndex];
    const resultEl = document.getElementById('prediction-result');
    resultEl.removeAttribute('data-key');
    resultEl.innerText = t('prediction', className, (confidence * 100).toFixed(2));
    img.dispose();
    features.dispose();
    prediction.dispose();
}

socket.emit('control_cam', false);
cameraEnabled = false;
setTimeout(() => { document.getElementById('camera').src = BLANK_IMG; }, 2000);

// 7) camera toggle
function toggleCamera() {
    if (cameraEnabled) {
        socket.emit('control_cam', false);
        cameraEnabled = false;
        setTimeout(() => { document.getElementById('camera').src = BLANK_IMG; }, 2000);
    } else {
        socket.emit('control_cam', true);
        cameraEnabled = true;
    }
}

// 8) preview / inference
function setStatus(key) {
    const el = document.getElementById('preview-status');
    el.setAttribute('data-key', key);
    el.innerText = t(key);
}
async function setInferenceMode() {
    if (!model) {
        await alert_popup(t('no_model'));
        return;
    }
    if (!previewing) {
        predictInterval = setInterval(() => predictImage(), 1000);
        previewing = true;
        setStatus('infer_running');
        document.getElementById('prediction-result').style.visibility = 'visible';
    }
}
function setPreviewMode() {
    if (previewing) {
        clearInterval(predictInterval);
        previewing = false;
        setStatus('preview_running');
        document.getElementById('prediction-result').style.visibility = 'hidden';
    }
}

// 9) export / import / convert
async function exportModelAsZip() {
    if (!model) {
        await alert_popup(t('no_model'));
        return;
    }
    const zip = new JSZip();
    try {
        const modelArtifacts = await model.save(tf.io.withSaveHandler(async (artifacts) => artifacts));
        zip.file('model.json', JSON.stringify(modelArtifacts.modelTopology));
        if (modelArtifacts.weightSpecs) {
            zip.file('weightsSpecs.json', JSON.stringify(modelArtifacts.weightSpecs));
        }
        if (modelArtifacts.weightData) {
            zip.file('weights.bin', new Uint8Array(modelArtifacts.weightData));
        }
        zip.file('labels.txt', CLASS_NAMES.join('\n'));
        zip.generateAsync({ type: 'blob' }).then(function (content) {
            const a = document.createElement('a');
            a.href = URL.createObjectURL(content);
            a.download = 'trained-model.zip';
            a.click();
        });
    } catch (error) {
        console.error("export error:", error);
        await alert_popup(t('export_fail'));
    }
}
async function importModel(event) {
    const file = event.target.files[0];
    if (!file) return;
    try {
        const zip = await JSZip.loadAsync(file);
        const modelJson = await zip.file('model.json').async('string');
        const weightDataFile = zip.file('weights.bin');
        if (!weightDataFile) {
            await alert_popup(t('missing_weights'));
            return;
        }
        const weightSpecsFile = zip.file('weightsSpecs.json');
        if (!weightSpecsFile) {
            await alert_popup(t('missing_specs'));
            return;
        }
        const weightData = await weightDataFile.async('arraybuffer');
        const weightSpecs = JSON.parse(await weightSpecsFile.async('string'));
        const modelTopology = JSON.parse(modelJson);
        if (model) model = null;
        const handler = tf.io.fromMemory({ modelTopology, weightSpecs, weightData });
        model = await tf.loadLayersModel(handler);
        const labelsFile = zip.file('labels.txt');
        if (labelsFile) {
            const labelsText = await labelsFile.async('string');
            CLASS_NAMES.splice(0, CLASS_NAMES.length, ...labelsText.split('\n'));
        }
        await alert_popup(t('import_ok'));
        setProgress('model_loaded');
    } catch (error) {
        console.error("import error:", error);
        await alert_popup(t('import_fail'));
    }
}

function convertToH5() {
    exportConvertedModelAsZipAndConvert();
}

const convertToH5_bt = document.getElementById("convertToH5_bt");
const convertToH5_bt_innerHTML = convertToH5_bt.innerHTML;
async function exportConvertedModelAsZipAndConvert() {
    if (!model) {
        await alert_popup(t('no_model'));
        return;
    }
    try {
        convertToH5_bt.innerHTML = `<i class='fa-solid fa-spinner fa-spin'></i>&nbsp; <span data-key="converting">${t('converting')}</span>`;
        const modelArtifacts = await model.save(tf.io.withSaveHandler(async (artifacts) => artifacts));

        const zip = new JSZip();
        zip.file('model.json', JSON.stringify(modelArtifacts.modelTopology));
        if (modelArtifacts.weightSpecs) {
            zip.file('weightsSpecs.json', JSON.stringify(modelArtifacts.weightSpecs));
        }
        if (modelArtifacts.weightData) {
            zip.file('weights.bin', new Uint8Array(modelArtifacts.weightData));
        }
        zip.file('labels.txt', CLASS_NAMES.join('\n'));

        const trainedModelBlob = await zip.generateAsync({ type: 'blob' });
        const formData = new FormData();
        formData.append("tfjs_zip", trainedModelBlob, "trained-model.zip");

        const response = await fetch(`http://${location.host}/convert`, { method: 'POST', body: formData });
        if (!response.ok) {
            const errorMessage = await response.text();
            console.error("convert request failed:", errorMessage);
            await alert_popup(t('convert_req_fail', errorMessage));
            return;
        }
        const resultBlob = await response.blob();
        const downloadUrl = URL.createObjectURL(resultBlob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = 'converted_h5.zip';
        document.body.appendChild(a);
        a.click();
        a.remove();
        URL.revokeObjectURL(downloadUrl);
        await alert_popup(t('convert_ok'));
    } catch (err) {
        console.error('convert error:', err);
        await alert_popup(t('convert_fail'));
    }
    finally {
        convertToH5_bt.innerHTML = convertToH5_bt_innerHTML;
        setLanguage(lang);
    }
}

window.addEventListener('beforeunload', () => {
    fetch(`http://${location.hostname}/classifier?enable=off`)
        .then(response => { if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`); return response.text(); })
        .then(() => { })
        .catch(() => { });
});
