from django.shortcuts import render
from django.contrib.auth.models import User, Group


def index(request):
    user_is_member = request.user.groups.filter(name="camera_staff").exists()
    return render(request, 'ai_camera/index.html')
