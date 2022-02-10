from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic
from django.contrib.auth.models import User, Group
from .models import Camera


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CameraListView(generic.ListView):
    model = Camera
    template_name = 'ai_camera/index.html'

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CameraView(generic.DetailView):
    model = Camera
    template_name = 'ai_camera/camera.html'
