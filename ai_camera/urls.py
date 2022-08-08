from django.urls import path
from .views import (
            CameraListView,
            cv_camera,
            rtc_stream,

            api, offer,
            )


urlpatterns = [
    path('', CameraListView.as_view(), name="ai_camera_index"),
    # path('camera/<int:id>/', ip_camera_view, name='camera'),
    path('cv_camera/', cv_camera, name='cv_camera'),
    path('webrtc_camera/', rtc_stream, name='webrtc_camera'),
    path('api/', api.urls, name='offer'),
]
