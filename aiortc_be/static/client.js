var pc = null;
var iceConnectionLog = document.getElementById('ice-connection-state'),
    iceGatheringLog = document.getElementById('ice-gathering-state'),
    signalingLog = document.getElementById('signaling-state');

function createPeerConnection() {
  var config = { sdpSemantics: "unified-plan" };
  pc = new RTCPeerConnection(config);

  // register some listeners to help debugging
  pc.addEventListener('icegatheringstatechange', function() {
      iceGatheringLog.textContent += ' -> ' + pc.iceGatheringState;
  }, false);
  iceGatheringLog.textContent = pc.iceGatheringState;

  pc.addEventListener('iceconnectionstatechange', function() {
      iceConnectionLog.textContent += ' -> ' + pc.iceConnectionState;
  }, false);
  iceConnectionLog.textContent = pc.iceConnectionState;

  pc.addEventListener('signalingstatechange', function() {
      signalingLog.textContent += ' -> ' + pc.signalingState;
  }, false);
  signalingLog.textContent = pc.signalingState;

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

      document.getElementById('offer-sdp').textContent = offer.sdp;  //debugging to html

      return fetch("/offer", {
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
      document.getElementById('answer-sdp').textContent = answer.sdp;  //debugging to html

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

  setTimeout(function () {
    pc.close();
  }, 500);

  document.getElementById("start").style.display = "inline-block";
}
