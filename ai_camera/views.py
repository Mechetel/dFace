from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.views import generic
from django.core.files import File
from django.http import HttpResponse
from .models import Camera, PlaybackVideo, Person
from hikvisionapi import Client
from .RecognizeAlgorithm import RecognizeAlgorithm
from .constants import (
        lfw_trained_model,
        openface_model,
        pinface_trained_model
    )
from .utils import to_base64
import numpy as np
import base64
import json
import cv2
import os


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
        os.system("cd Downloads/" + str(cam_id) + " &&  ls | grep -v '\-conv.mp4$' | xargs rm")
        os.system("cd Downloads && \
                hikload --server " + camera.ip_cam_adress   + \
                " --user "         + camera.ip_cam_user     + \
                " --password "     + camera.ip_cam_password + \
                " --downloads "    + str(cam_id)            + \
                " && cd "          + str(cam_id)            + \
                " && for i in *-101.mp4; do name=`echo \"$i\" | cut -d'.' -f1`; echo \"$name\"; ffmpeg -n -i \"$i\" \"${name}-conv.mp4\"; done")

        downloads_dir = f'Downloads'
        for directory in os.listdir(downloads_dir):
            if not os.path.isdir(f'{downloads_dir}/{directory}'):
                continue
            cam_id = directory
            camera = Camera.objects.get(id = cam_id)
            for filename in os.listdir(f'{downloads_dir}/{directory}'):
                if filename.endswith("-conv.mp4"):
                    path = f'{downloads_dir}/{directory}/{filename}'
                    try:
                        playback_exist = PlaybackVideo.objects.get(filename = filename)
                    except PlaybackVideo.DoesNotExist:
                        playback_exist = None
                    if not playback_exist:
                        playback = PlaybackVideo(camera_id = camera, filename = filename)
                        with open(path, 'rb') as f:
                            data = File(f)
                            playback.video.save(filename, data, True)


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


@login_required(login_url='/login/')
def image_loader(request):
    return render(request, 'ai_camera/image_loader.html')


@csrf_exempt
@require_POST
def load_pin_dataset(request):
    dataset_dir = f'datasets/pin_faces'
    for directory in os.listdir(dataset_dir):
        if not os.path.isdir(f'{dataset_dir}/{directory}'):
            continue
        person_name = directory
        for filename in os.listdir(f'{dataset_dir}/{directory}'):
            if filename.endswith(".jpg"):
                path = f'{dataset_dir}/{directory}/{filename}'
                try:
                    person_exist = Person.objects.get(name = person_name)
                except Person.DoesNotExist:
                    person_exist = None

                if not person_exist:
                    person = Person(name=person_name.title())
                    with open(path, 'rb') as f:
                        data = File(f)
                        person.image.save(filename, data, True)

    return HttpResponse(request)

@csrf_exempt
@require_POST
def get_picture_from_ip(request):
    ip_cam_adress   = request.POST.get('ip_cam_adress')
    ip_cam_user     = request.POST.get('ip_cam_user')
    ip_cam_password = request.POST.get('ip_cam_password')
    cam             = Client('http://' + ip_cam_adress, ip_cam_user, ip_cam_password)
    image           = cam.Streaming.channels[102].picture(method='get', type='opaque_data')
    image = cv2.imdecode(np.fromstring(image.content, np.uint8), cv2.IMREAD_UNCHANGED)
    result = to_base64(image)

    return HttpResponse(result, content_type='image/jpeg')

@csrf_exempt
@require_POST
def predict_image(request):
    image = request.FILES.get('image')
    image = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    persons = Person.objects.all()
    result = RecognizeAlgorithm.recognize(image, persons, lfw_trained_model)
    # image = RecognizeAlgorithm.recognize(image, persons, openface_model)
    # image = RecognizeAlgorithm.recognize(image, persons, pinface_trained_model)

    return HttpResponse(json.dumps(result), content_type="application/json")
