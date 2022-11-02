import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import cv2
import numpy as np
import time
import asyncio

from av import VideoFrame
from aiortc import RTCPeerConnection, RTCSessionDescription, MediaStreamTrack

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware

from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from django.core.wsgi import get_wsgi_application
from django.conf import settings
from importlib.util import find_spec

from ai_camera.RecognizeAlgorithm import RecognizeAlgorithm
from ai_camera.constants import (
        lfw_trained_model,
        openface_model,
        pinface_trained_model
    )

from pydantic import BaseModel
class Offer(BaseModel):
    sdp: str
    type: str
    video_transform: str = None

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dFace.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django_app = get_wsgi_application()

# Import a model
# And always import your models after you export settings
# and you get Django WSGI app
from ai_camera.models import Person

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pcs = set()
app.mount("/static", StaticFiles(directory="aiortc_be/static"), name="static")
templates = Jinja2Templates(directory="aiortc_be/templates")

class VideoTransformTrack(MediaStreamTrack):
    kind = "video"

    def __init__(self, track, transform):
        super().__init__()
        self.track = track
        self.transform = transform
        self.model = lfw_trained_model
        self.persons = Person.objects.all()
        self.persons_array = RecognizeAlgorithm.persons_to_dict_array(self.persons)

    async def recv(self):
        frame = await self.track.recv()

        if self.transform == "recognize":
            img = frame.to_ndarray(format="bgr24")

            (image_height, image_widht, _) = np.shape(img)
            image_scale_params = RecognizeAlgorithm.scaling_image(image_height, image_widht)
            recognized_image = RecognizeAlgorithm.predict_image(img, self.persons_array, self.model, image_scale_params)

            new_frame = VideoFrame.from_ndarray(img, format="bgr24")
            new_frame.pts = frame.pts
            new_frame.time_base = frame.time_base
            return new_frame
        else:
            return frame


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/offer")
async def offer(params: Offer):
    offer = RTCSessionDescription(sdp=params.sdp, type=params.type)

    pc = RTCPeerConnection()
    pcs.add(pc)

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    @pc.on("track")
    def on_track(track):
        if track.kind == "video":
            pc.addTrack(
                VideoTransformTrack(track, transform=params.video_transform)
            )

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}

@app.on_event("shutdown")
async def on_shutdown():
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()
