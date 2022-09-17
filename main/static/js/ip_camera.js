import { fetch_snapshot } from "./fetch_snap.js";


var snapshot = document.getElementById("snapshot");
window.captureSnapshot = function captureSnapshot(ip_cam_adress, ip_cam_user, ip_cam_password) {
  var img = new Image();
  img.width = 640;
  img.height = 480;

  var formData = new FormData();
  formData.append("ip_cam_adress",   ip_cam_adress);
  formData.append("ip_cam_user",     ip_cam_user);
  formData.append("ip_cam_password", ip_cam_password);

  fetch_snapshot(img, snapshot, formData, "../../get_picture_from_ip/");
};
