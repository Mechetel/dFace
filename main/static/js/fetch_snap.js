export function fetch_snapshot(img, snapshot, formData, _url) {
  $.ajax({
    type: "POST",
    enctype: "multipart/form-data",
    url: _url,
    data: formData,
    mode: "no-cors",
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
}


export function predictImage(img, snapshot, path_to_fetch) {
  fetch(img.src, {
    mode: "no-cors",
  })
    .then((res) => res.blob())
    .then((blob) => {
      const file = new File([blob], "capture.jpeg");
      var formData = new FormData();
      formData.append("image", file);
      fetch_snapshot(img, snapshot, formData, path_to_fetch);
    });
}

