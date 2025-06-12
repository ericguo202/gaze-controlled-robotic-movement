const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const statusEl = document.getElementById('status');
let isAppInit = false;
let lastTime = 0; // will be necessary to delay
const dataArr = [];

async function initCamera() {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
    return new Promise(r => video.onloadedmetadata = r);
}

const CASCADES = {
    face: { local: 'opencv/faces.xml', remote: 'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml' },
    eyes: { local: 'opencv/eyes.xml', remote: 'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_eye_tree_eyeglasses.xml' }
};

async function loadClassifier(name, file) {
    const { local, remote } = CASCADES[name];
    let buf;
    try {
        buf = await (await fetch(local)).arrayBuffer();
    }
    catch {
        buf = await (await fetch(remote)).arrayBuffer();
    }
    cv.FS_createDataFile('/', file, new Uint8Array(buf), true, false, false);
    const cc = new cv.CascadeClassifier();
    if (!cc.load(file)) throw new Error(`${name} cascade failed`);
    return cc;
}

let faceCascade, eyeCascade, src, gray;
const MISS = 6, seen = { L: MISS, R: MISS };

function processFrame(timestamp) {
    console.log(`Current timestamp: ${timestamp}`); // timestamp automatically passed in 
    if (video.readyState < 2) {
        requestAnimationFrame(processFrame);
        return;
    }
    if (timestamp - lastTime < 100) { // interval is 500
        requestAnimationFrame(processFrame);
        return;
    }

    lastTime = timestamp; // updates the last time this function runs fully.

    // % of zoom (e.g. 1.5 = 150% zoom, 2 = 200% zoom)
    const zoomFactor = 2;

    // Source video dimensions
    const vw = video.videoWidth;
    const vh = video.videoHeight;

    // Calculate zoom crop box
    const sw = vw / zoomFactor;
    const sh = vh / zoomFactor;
    const sx = (vw - sw) / 2;
    const sy = (vh - sh) / 2;


    ctx.drawImage(video, sx, sy, sw, sh, 0, 0, canvas.width, canvas.height);
    src.data.set(ctx.getImageData(0, 0, src.cols, src.rows).data);
    cv.cvtColor(src, gray, cv.COLOR_RGBA2GRAY);
    cv.equalizeHist(gray, gray);

    const faces = new cv.RectVector(), eyes = new cv.RectVector();
    faceCascade.detectMultiScale(gray, faces, 1.2, 3, 0, new cv.Size(80, 80));

    const hit = { L: false, R: false };
    for (let i = 0; i < faces.size(); ++i) {
        const f = faces.get(i), roi = gray.roi(f);
        eyeCascade.detectMultiScale(roi, eyes, 1.15, 3, 0, new cv.Size(20, 20));
        for (let j = 0; j < eyes.size(); ++j) {
            const e = eyes.get(j), cx = f.x + e.x + e.width / 2;
            const side = cx < f.x + f.width / 2 ? 'L' : 'R';
            hit[side] = true;
            cv.rectangle(src,
                new cv.Point(f.x + e.x, f.y + e.y),
                new cv.Point(f.x + e.x + e.width, f.y + e.y + e.height),
                side === 'L' ? [0, 255, 0, 255] : [0, 0, 255, 255], 2);
        }
        roi.delete();
    }

    ['L', 'R'].forEach(s => { hit[s] ? seen[s] = MISS : seen[s] > 0 && seen[s]--; });

    const leftOpen = seen.L > 0;
    const rightOpen = seen.R > 0;

    // determines if left and right open or closed
    if (leftOpen && rightOpen) {
        console.log('NONE CLOSED');
        statusEl.textContent = 'NONE CLOSED';
        dataArr.push(0);
    }
    else if (!leftOpen && !rightOpen) {
        console.log('BOTH CLOSED');
        statusEl.textContent = 'BOTH CLOSED';
        dataArr.push(5);
    }
    else {
        if (!leftOpen) {
            console.log('LEFT CLOSED');
            statusEl.textContent = 'LEFT CLOSED';
            dataArr.push(4);
        }
        else {
            console.log('RIGHT CLOSED');
            statusEl.textContent = 'RIGHT CLOSED';
            dataArr.push(-4);
        }
    }

    cv.imshow('canvas', src);
    faces.delete();
    eyes.delete();
    requestAnimationFrame(processFrame);
}

async function initApp() {
    try {
        statusEl.textContent = 'Starting camera…';
        await initCamera();

        statusEl.textContent = 'Loading classifiers…';
        [faceCascade, eyeCascade] = await Promise.all([
            loadClassifier('face', 'face.xml'),
            loadClassifier('eyes', 'eyes.xml')
        ]);

        src = new cv.Mat(video.videoHeight, video.videoWidth, cv.CV_8UC4);
        gray = new cv.Mat(video.videoHeight, video.videoWidth, cv.CV_8UC1);

        isAppInit = true;
        console.log("App init");
        statusEl.textContent = 'Detecting eyes…';
        requestAnimationFrame(processFrame);
    } catch (err) {
        console.error(err);
        statusEl.textContent = '🚫 ' + err.message;
    }
}