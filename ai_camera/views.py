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
from .utils import detect, recognize

import numpy as np
import base64
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
        PlaybackVideo.objects.filter(camera_id=camera).delete()
        os.system("rm -r Downloads && mkdir Downloads && cd Downloads && \
                hikload --server " + camera.ip_cam_adress + \
                " --user "         + camera.ip_cam_user + \
                " --password "     + camera.ip_cam_password + \
                " --downloads "    + str(cam_id) + \
                " && ls -la"       + str(cam_id))

        directory = "Downloads/" + str(cam_id)
        for filename in os.listdir(directory):
            print(filename)
            PlaybackVideo(
                    camera_id=camera,
                    headline=filename,
                    video=filename
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
                person = Person(name=person_name)
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

    retval, buffer = cv2.imencode('.jpg', image)
    data = base64.b64encode(buffer.tobytes())
    result = data.decode()

    return HttpResponse(result, content_type='image/jpeg')

@csrf_exempt
@require_POST
def predict_image(request):
    image = request.FILES.get('image')
    image = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    #image = recognize(image)
    image = detect(image) 

    retval, buffer = cv2.imencode('.jpg', image)
    data = base64.b64encode(buffer.tobytes())
    result = data.decode()

    return HttpResponse(result, content_type='image/jpeg')
