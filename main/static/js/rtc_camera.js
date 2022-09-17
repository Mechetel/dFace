import { fetch_snapshot } from "./fetch_snap.js";

// The buttons to start & stop stream and to capture the image
var btnStart = document.getElementById("btn-start");
var btnStop = document.getElementById("btn-stop");
var btnCapture = document.getElementById("btn-capture");
var btnPredict = document.getElementById("btn-predict");
var checkboxPredict = document.getElementById("checkboxPredict");

// The stream & capture
var stream = document.getElementById("stream");
var canvas = document.getElementById("canvas");
var snapshot = document.getElementById("snapshot");

// The video stream
var cameraStream = null;

// Attach listeners
btnStart.addEventListener("click", startStreaming);
btnStop.addEventListener("click", stopStreaming);
btnCapture.addEventListener("click", captureSnapshot);
checkboxPredict.addEventListener("change", btnEnabling);

function btnEnabling() {
  if (!btnStop.disabled || !btnCapture.disabled) {
    btnPredict.disabled = checkboxPredict.checked ? true : false;
  } else {
    btnPredict.disabled = true;
  }
}

// Start Streaming
function startStreaming() {
  btnStart.disabled = true;
  btnStop.disabled = false;
  btnCapture.disabled = false;
  btnEnabling();

  var mediaSupport = "mediaDevices" in navigator;

  if (mediaSupport && null == cameraStream) {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then(function (mediaStream) {
        cameraStream = mediaStream;
        stream.srcObject = mediaStream;

        stream.play();
      })
      .catch(function (err) {
        console.log("Unable to access camera: " + err);
      });
  } else {
    alert("Your browser does not support media devices.");

    return;
  }
}

// Stop Streaming
function stopStreaming() {
  btnStart.disabled = false;
  btnStop.disabled = true;
  btnCapture.disabled = true;
  btnPredict.disabled = true;

  if (null != cameraStream) {
    var track = cameraStream.getTracks()[0];

    track.stop();
    stream.load();

    cameraStream = null;
  }
}

function captureSnapshot() {
  if (null != cameraStream) {
    canvas
      .getContext("2d")
      .drawImage(stream, 0, 0, stream.width, stream.height);
    var img = new Image();

    img.src = canvas.toDataURL("image/jpeg");
    img.width = stream.width;
    img.height = stream.height;

    snapshot.innerHTML = "";
    snapshot.appendChild(img);

    if (checkboxPredict.checked) {
      fetch_snapshot(img, snapshot);
    }
  }
}
