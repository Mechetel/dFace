export function fetch_snapshot(img, snapshot) {
  fetch(img.src)
    .then((res) => res.blob())
    .then((blob) => {
      const file = new File([blob], "capture.jpeg");
      var formData = new FormData();
      formData.append("image", file);
      $.ajax({
        type: "POST",
        enctype: "multipart/form-data",
        url: "../predict/",
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        beforeSend: function () {
          img.src = "";
          snapshot.innerHTML = "";
          snapshot.appendChild(img);
        },
        success: function (data) {
          img.src = "data:image/jpeg;base64," + data;
          snapshot.appendChild(img);
        },
        error: function (e) {
          console.log(e);
        },
      });
    });
}
