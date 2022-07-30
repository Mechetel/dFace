var pc = null;

function createPeerConnection() {
  var config = { sdpSemantics: "unified-plan" };
  config.iceServers = [{ urls: ["stun:stun.l.google.com:19301"] }];

  pc = new RTCPeerConnection(config);
  pc.addEventListener("track", function (evt) {
    if (evt.track.kind == "video")
      document.getElementById("video").srcObject = evt.streams[0];
  });

  return pc;
}

function negotiate() {
  return pc
    .createOffer()
    .then((offer) => {
      pc.setLocalDescription(offer);
    })
    .then(() => {
      return new Promise(function (resolve) {
        if (pc.iceGatheringState === "complete") {
          resolve();
        } else {
          function checkState() {
            if (pc.iceGatheringState === "complete") {
              pc.removeEventListener("icegatheringstatechange", checkState);
              resolve();
            }
          }
          pc.addEventListener("icegatheringstatechange", checkState);
        }
      });
    })
    .then(() => {
      var offer = pc.localDescription;

      return fetch("/ai_camera/api/offer/", {
        body: JSON.stringify({
          sdp: offer.sdp,
          type: offer.type,
          video_transform: document.getElementById("video-transform").value,
        }),
        headers: {
          "Content-Type": "application/json",
        },
        method: "POST",
      });
    })
    .then((response) => {
      return response.json();
    })
    .then((answer) => {
      return pc.setRemoteDescription(answer);
    })
    .catch((e) => {
      alert(e);
    });
}

function start() {
  document.getElementById("start").style.display = "none";
  pc = createPeerConnection();
  var constraints = { video: false };

  var resolution = document.getElementById("video-resolution").value;
  if (resolution) {
    resolution = resolution.split("x");
    constraints.video = {
      width: parseInt(resolution[0], 0),
      height: parseInt(resolution[1], 0),
    };
  } else {
    constraints.video = true;
  }

  if (constraints.video) {
    document.getElementById("media").style.display = "block";
  }

  navigator.mediaDevices.getUserMedia(constraints).then(
    function (stream) {
      stream.getTracks().forEach(function (track) {
        pc.addTrack(track, stream);
      });
      return negotiate();
    },
    function (err) {
      alert("Could not acquire media: " + err);
    }
  );

  document.getElementById("stop").style.display = "inline-block";
}

function stop() {
  document.getElementById("stop").style.display = "none";
  document.getElementById("media").style.display = "none";

  pc.getSenders().forEach(function (sender) {
    sender.track.stop();
  });

  // pc.getTransceivers().forEach(function(transceiver) {
  //   transceiver.stop();
  // });

  setTimeout(function () {
    pc.close();
  }, 500);

  document.getElementById("start").style.display = "inline-block";
}
