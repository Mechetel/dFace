from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import (
                                User,
                                Group
                                )
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators import gzip
from django.utils.decorators import method_decorator
from django.http import (
                 StreamingHttpResponse,
                 JsonResponse,
                 FileResponse
                 )
from django.shortcuts import render
from django.views import generic
from aiortc import (
            RTCSessionDescription,
            RTCPeerConnection
            )
from ninja import NinjaAPI

from .video_camera import VideoCamera, gen
from .video_transform_track import VideoTransformTrack
from .models import Camera
from .schemas import Offer
import os
import json
import asyncio

api = NinjaAPI()
pcs = set()

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CameraListView(generic.ListView):
    model = Camera
    template_name = 'ai_camera/index.html'

@gzip.gzip_page
@method_decorator(login_required(login_url='/login/'), name='dispatch')
def cv_camera(request):
    return StreamingHttpResponse(gen(VideoCamera()),
                    content_type='multipart/x-mixed-replace; boundary=frame')

# camera = Camera.objects.get(id = id)

# def image_process(request):
#     return render(request, 'image.html')

def rtc_stream(request):
    return render(request, 'ai_camera/stream.html')


@csrf_exempt
@api.post("offer/")
async def offer(request):
    json_data = json.loads(request.body)
    rtc_session_description = RTCSessionDescription(sdp=json_data['sdp'], type=json_data['type'])

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
                VideoTransformTrack(track, transform=json_data['video_transform'])
            )

    # handle rtc_session_description
    await pc.setRemoteDescription(rtc_session_description)

    # send answer
    answer = await pc.createAnswer()
    await pc.setRemoteDescription(rtc_session_description)
    await pc.setLocalDescription(answer)

    return JsonResponse({"sdp": pc.localDescription.sdp, "type": pc.localDescription.type})
