from django.urls import path
from .views import (
            CameraListView,
            rtc_stream,
<<<<<<< HEAD

            api,
            )
=======
            ip_camera_view,
            playback,
            playback_view,
            image_loader
        )
>>>>>>> bc4fedf (feat: major improvement)


urlpatterns = [
    path('', CameraListView.as_view(), name="ai_camera"),
    path('camera/<int:cam_id>/', ip_camera_view, name='camera'),
    path('camera/<int:cam_id>/playback', playback, name='playback'),
    path('camera/<int:cam_id>/playback/<int:play_id>/', playback_view, name='playback_view'),
    path('webrtc_camera/', rtc_stream, name='webrtc_camera'),
    path('image_loader/', image_loader, name='image_loader'),
]
