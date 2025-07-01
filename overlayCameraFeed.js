const deviceId = "123"; // replace this with actual webcam device ID

async function listCameras() {
    try {
        await navigator.mediaDevices.getUserMedia({ video: true });

        const devices = await navigator.mediaDevices.enumerateDevices();
        return devices.filter(devices => devices.kind === "videoinput");
    }
    catch (e) {
        console.log(e);
        return null;
    }
}

async function main() {
    try {
        const cams = await listCameras();

        console.log(cams);

        // destructure
        const [robotMountedCamera] = cams.filter(cam => cam.deviceId === deviceId);

        const robotStream = await navigator.mediaDevices.getUserMedia({
            video: { deviceId: { exact: robotMountedCamera.deviceId }, width: 320, height: 240 }
        });

        document.getElementById("robotVideo").srcObject = robotStream;
    }
    catch (e) {
        console.log(e);
    }
}

main();