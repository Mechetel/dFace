from django.urls import path
from .views import CameraListView, ip_camera_view, video_feed


urlpatterns = [
    path('', CameraListView.as_view(), name="ai_camera_index"),
    path('camera/<int:id>/', ip_camera_view, name='camera'),
    path('video_feed', video_feed, name='video_feed'),
]
