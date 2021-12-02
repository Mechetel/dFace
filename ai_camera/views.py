from django.shortcuts import render


def index(request):
    return render(request, 'ai_camera/index.html')
