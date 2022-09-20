import { fetch_snapshot, predictImage } from "./fetch_snap.js";

var img = new Image();

var btnPredict = document.getElementById("btn-predict");
var snapshot = document.getElementById("snapshot");

btnPredict.addEventListener("click", function () {
  predictImage(img, snapshot, "../../predict/");
  btnPredict.disabled = true;
});

window.captureSnapshot = function captureSnapshot(
  ip_cam_adress,
  ip_cam_user,
  ip_cam_password
) {
  img.width = 640;
  img.height = 480;

  var formData = new FormData();
  formData.append("ip_cam_adress", ip_cam_adress);
  formData.append("ip_cam_user", ip_cam_user);
  formData.append("ip_cam_password", ip_cam_password);

  fetch_snapshot(img, snapshot, formData, "../../get_picture_from_ip/");
  btnPredict.disabled = false;
};


