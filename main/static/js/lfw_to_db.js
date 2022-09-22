var btnLfw = document.getElementById("lfw_to_db");
btnLfw.addEventListener("click", lfw_download);

function lfw_download() {
  $.ajax({
    type: "POST",
    url: "load_flw_dataset/",
    mode: "no-cors",
    processData: false,
    contentType: false,
    cache: false,
    success: function () {
    },
    error: function (e) {
      console.log(e);
    },
  });
}
