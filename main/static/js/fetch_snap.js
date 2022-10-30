export function generate_table(persons) {
  var text = "<table class=\'table\'>\
        <thead>\
          <tr>\
            <th scope='col'>#</th>\
            <th scope='col'>Person Name</th>\
            <th scope='col'>Image</th>\
          </tr>\
        </thead>\
        <tbody class='table-group-divider'>";

  persons.forEach((person) => {
    text += "<tr>\
              <th>" + person.index + "</th>\
              <td>" + person.name + "</td>\
              <td><img width='96' height='96' src='" + person.image + "'></td>\
            </tr>"
  });

  text += "</tbody></table>";
  return text;
}


export function edit_persons_data(persons) {
  persons.forEach((person, index, array) => {
    let person_image_src = "data:image/jpeg;base64," + person.base64_data;
    delete person.base64_data;
    person.index = index + 1;
    person.image = person_image_src;
  });

  return persons
}

export function fetch_snapshot(img, snapshot, formData, _url, personsTable) {
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
      if (personsTable) {
        let { image, persons } = data
        let edited_persons_data = edit_persons_data(persons)
        console.log(edited_persons_data);

        img.src = "data:image/jpeg;base64," + image;
        snapshot.appendChild(img);

        personsTable.innerHTML = generate_table(persons);
      } else {
        img.src = "data:image/jpeg;base64," + data;
        snapshot.appendChild(img);
      }
    },
    error: function (e) {
      console.log(e);
    },
  });
}


export function predictImage(img, snapshot, path_to_fetch, personsTable) {
  fetch(img.src, {
    mode: "no-cors",
  })
    .then((res) => res.blob())
    .then((blob) => {
      const file = new File([blob], "capture.jpeg");
      var formData = new FormData();
      formData.append("image", file);
      fetch_snapshot(img, snapshot, formData, path_to_fetch, personsTable);
    });
}
