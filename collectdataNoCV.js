// connect to websocket server
const socket = new WebSocket("ws://localhost:8765");

// open connection
socket.addEventListener("open", (event) => {
    console.log("Connected to server! Port 8765");
});

// listen for messages from server
socket.addEventListener("message", (event) => {
    console.log("Message from server: ", event.data);
});

socket.addEventListener("error", (event) => {
    console.log("Error!", event);
});

socket.addEventListener("close", (event) => {
    console.log("Connection closed.");
});

function determineQuadrant(gaze) {
    // returns: if LEFT -1, if RIGHT 1, if DOWN -3, if UP 3, if FORWARD 2 if BACKWARD -2
    if (gaze.x <= (1 / 3)) {
        if (gaze.y >= 0.5) {
            console.log("RIGHT");
            return 1;
        }
        else {
            console.log("LEFT");
            return -1;
        }
    }
    else if (gaze.x >= (2 / 3)) {
        if (gaze.y >= 0.5) {
            console.log("DOWN");
            return -3;
        }
        else {
            console.log("UP");
            return 3;
        }
    }
    else {
        if (gaze.y >= 0.5) {
            console.log("BACKWARD");
            return -2;
        }
        else {
            console.log("FORWARD");
            return 2;
        }
    }
}

// test
let endCalibration = false; // default state is calibration
let gaze = null;

webgazer.setGazeListener((data, elapsedTime) => {
    if (data) {
        // dividing the raw coordinates (in pixels) by window.innerWidth and window.innerHeight normalizes these coordinates
        // this way, we can test on a variety of screen and viewport sizes.
        gaze = { x: data.x / window.innerWidth, y: data.y / window.innerHeight, t: elapsedTime };
    }
}).begin();

const endCalibrationButton = document.getElementById("endcalibration");

endCalibrationButton.addEventListener("click", (event) => {
    if (!endCalibration) {
        endCalibration = true;
        endCalibrationButton.textContent = "End Data Collection";
    }
    else {
        endCalibration = false;
        endCalibrationButton.textContent = "End Calibration";
    }
})

// webgazer collects data way too frequently, so we'll poll every 2 seconds (2000 ms)
setInterval(() => {
    if (gaze && socket.readyState === WebSocket.OPEN && endCalibration) {
        console.log(gaze);
        socket.send(determineQuadrant(gaze)); // sends to server
    }
}, 2000);