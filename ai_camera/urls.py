from django.urls import path
from .views import CameraView, CameraListView


urlpatterns = [
    path('', CameraListView.as_view(), name="ai_camera_index"),
    path('camera/<int:pk>/', CameraView.as_view(), name='camera'),
]
