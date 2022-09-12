from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import generic
<<<<<<< HEAD
from aiortc import (
            RTCSessionDescription,
            RTCPeerConnection
            )
from ninja import (
        NinjaAPI,
        Schema
        )

from .video_camera import VideoCamera, gen
from .video_transform_track import VideoTransformTrack
from .models import Camera
import asyncio


class Offer(Schema):
    sdp: str
    type: str
    video_transform: str = None

api = NinjaAPI()
pcs = set()

=======
from django.http import HttpResponse
from .models import Camera, PlaybackVideo
import os


>>>>>>> bc4fedf (feat: major improvement)
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CameraListView(generic.ListView):
    model = Camera
    template_name = 'ai_camera/index.html'


@login_required(login_url='/login/')
def ip_camera_view(request, cam_id):
    camera = Camera.objects.get(id = cam_id)
    context = { 'camera': camera }
    return render(request, 'ai_camera/ip_camera.html', context)


@login_required(login_url='/login/')
def playback(request, cam_id):
    camera = Camera.objects.get(id = cam_id)

    if request.method == "POST":
        PlaybackVideo.objects.filter(camera_id=camera).delete()
        os.system("cd main/media/ && \
                rm -rf * && \
                hikload --server " + camera.ip_cam_adress + \
                " --user " + camera.ip_cam_user + \
                " --password " + camera.ip_cam_password + \
                " --allrecordings --downloads video")

        directory = "main/media/video/"
        for filename in os.listdir(directory):
            os.rename(filename, str(cam_id) + "_" + filename)

        for filename in os.listdir(directory):
            if filename.endswith('.mp4'):
                PlaybackVideo(
                        camera_id=camera,
                        headline=filename,
                        video="video/" + str(camera.id) + "_"+ filename
                    ).save()

    playbacks = PlaybackVideo.objects.filter(camera_id=camera)

    context = {
            'playbacks': playbacks,
            'camera': camera
        }
    return render(request, 'ai_camera/playback.html', context)


@login_required(login_url='/login/')
def playback_view(request, cam_id, play_id):
    camera = Camera.objects.get(id = cam_id)
    playback = PlaybackVideo.objects.filter(camera_id=camera).get(id=play_id)
    context = {
            'playback': playback,
            'camera': camera
        }
    return render(request, 'ai_camera/playback_view.html', context)


@login_required(login_url='/login/')
def rtc_stream(request):
    return render(request, 'ai_camera/rtc_stream.html')


<<<<<<< HEAD
@api.post("offer")
async def offer(request, params: Offer):
    offer = RTCSessionDescription(sdp=params.sdp, type=params.type)
=======
@login_required(login_url='/login/')
def image_loader(request):
    return render(request, 'ai_camera/image_loader.html')
>>>>>>> bc4fedf (feat: major improvement)


<<<<<<< HEAD
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
=======
# @csrf_exempt
# @require_POST
# def predict_image(request):
#     image = request.FILES.get('image')
#     result = predict(image)
#     return HttpResponse(result, content_type='image/jpeg')
>>>>>>> bc4fedf (feat: major improvement)
