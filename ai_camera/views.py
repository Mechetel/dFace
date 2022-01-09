from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic
from django.contrib.auth.models import User, Group
from .models import Camera


class CameraListView(generic.ListView):
    model = Camera
    template_name = 'ai_camera/index.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the username
        user_is_member = self.request.user.groups.filter(name="camera_staff").exists()
        context['user_is_member'] = user_is_member
        return context

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(CameraListView, self).dispatch(request, *args, **kwargs)

class CameraView(generic.DetailView):
    model = Camera
    template_name = 'ai_camera/camera.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the username
        user_is_member = self.request.user.groups.filter(name="camera_staff").exists()
        context['user_is_member'] = user_is_member
        return context

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(CameraView, self).dispatch(request, *args, **kwargs)
