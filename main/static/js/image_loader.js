import { generate_table, edit_persons_data } from "./fetch_snap.js";

var image    = new Image();
image.height = 480;
image.width  = 640;

var pred_image    = new Image();
pred_image.height = 480;
pred_image.width  = 640;

var formFile        = document.getElementById("formFile");
var btnPredict      = document.getElementById("btn-predict");
var downloadedImage = document.getElementById("downloadedImage");
var predictedImage  = document.getElementById("predictedImage");

var personsTable    = document.getElementById("predTable");

formFile.addEventListener("change", function() {
  const file = formFile.files[0];
  if (file) {
    var reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      image.src = reader.result;
    }
  }
  downloadedImage.innerHTML = "";
  downloadedImage.appendChild(image);

  btnPredict.disabled = false;
});


btnPredict.addEventListener("click", function() {
  fetch(image.src, {
    mode: "no-cors",
  })
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
        mode: "no-cors",
        processData: false,
        contentType: false,
        cache: false,
        success: function (data) {
          let { image, persons } = data
          let edited_persons_data = edit_persons_data(persons)
          console.log(edited_persons_data);

          pred_image.src = "data:image/jpeg;base64," + image;
          predictedImage.appendChild(pred_image);

          personsTable.innerHTML = generate_table(persons);
        },
        error: function (e) {
          console.log(e);
        },
      });
    });
});
