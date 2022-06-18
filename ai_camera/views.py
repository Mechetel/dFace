from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic
from django.contrib.auth.models import User, Group
from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from .models import Camera
from ai_camera.camera import VideoCamera, IPWebCamera
from django.views.decorators import gzip


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CameraListView(generic.ListView):
    model = Camera
    template_name = 'ai_camera/index.html'

@gzip.gzip_page
@method_decorator(login_required(login_url='/login/'), name='dispatch')
def ip_camera_view(request, id):
    camera = Camera.objects.get(id = id)
    response = StreamingHttpResponse(gen(IPWebCamera(camera.url)),
                    content_type='multipart/x-mixed-replace; boundary=frame')

    return render(request, 'ai_camera/camera.html', response)

@gzip.gzip_page
def video_feed(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    print("==============")
    print('rtsp://' + ip + '/0')
    print("==============")

    return StreamingHttpResponse(gen(VideoCamera()),
                    content_type='multipart/x-mixed-replace; boundary=frame')

