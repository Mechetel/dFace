from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="ai_camera_index"),
]