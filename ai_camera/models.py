from django.db.models import signals
from django.dispatch import receiver
from ndarraydjango.fields import NDArrayField
from facenet_pytorch import MTCNN
from .cnn_model import create_models
from django.db import models
import numpy as np
import torch
import cv2
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

device = 'cuda' if torch.cuda.is_available() else 'cpu'
mtcnn = MTCNN(keep_all=True, device=device)
input_shape = (96, 96, 3) # height, width, channels
(_, lfw_trained_model, _) = create_models()


class Camera(models.Model):
    name            = models.CharField(max_length=20, null=False)
    ip_cam_adress   = models.CharField(max_length=20, null=True)
    ip_cam_user     = models.CharField(max_length=10, null=True)
    ip_cam_password = models.CharField(max_length=30, null=True)
    description     = models.TextField(max_length=100, null=True)

    def __str__(self):
        return self.name

class PlaybackVideo(models.Model):
    camera_id = models.ForeignKey(Camera, on_delete=models.CASCADE)
    headline  = models.TextField(max_length=50, null=False)
    video     = models.FileField(upload_to ='videos/')

    def __str__(self):
        return "cam " + self.camera_id + ": " + self.headline

class Person(models.Model):
    name  = models.TextField(max_length=50, null=False)

    PERSON_CHOISES = [
        ("staff", "staff"),
        ("student", "student"),
    ]
    career = models.TextField(max_length=15, null=True, choices=PERSON_CHOISES)
    image  = models.FileField(upload_to ='images/', null=False)
    image_nd_array = NDArrayField(shape=(96, 96, 3), dtype=np.float32, null=True)

    def __str__(self):
        return self.name

@receiver(signals.post_save, sender=Person)
def create_person(sender, instance, created, **kwargs):
    image = cv2.imread(instance.image.url)
    print(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    print(np.shape(image))
    faces, _ = mtcnn.detect(image)

    for face in faces:
        x1, y1, x2, y2 = [int(p) for p in face]
        face_data = image[y1:y2, x1:x2]
        face_data = cv2.resize(face_data, tuple(reversed(input_shape[:-1])), interpolation=cv2.INTER_AREA)
        face_data = np.array(face_data, dtype='float32') / 255.0
        predicted_image_data = lfw_trained_model.predict(face_data)

    instance.image_nd_array = predicted_image_data
