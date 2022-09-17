import { fetch_snapshot } from "./fetch_snap.js";

var btnCapture = document.getElementById("btn-capture");
var snapshot = document.getElementById("snapshot");

function captureSnapshot(ip_cam_adress) {
  var img = new Image();

  img.src =
    "http://" +
    ip_cam_adress +
    "/ISAPI/Streaming/channels/102/picture?t=" +
    new Date().getTime();
  img.width = 640;
  img.height = 480;

  snapshot.innerHTML = "";
  snapshot.appendChild(img);

  fetch_snapshot(img, snapshot);
}
