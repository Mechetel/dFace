from django.db.models import signals
from django.dispatch import receiver
from .constants import input_shape, lfw_trained_model, mtcnn
from django.db import models
from ndarraydjango.fields import NDArrayField
from PIL import Image
import numpy as np
import cv2
import os


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
    image  = models.FileField(upload_to ='images/', null=True)
    image_nd_array = NDArrayField(shape=(96, 96, 3), dtype=np.float32, null=True)

    def __str__(self):
        return self.name

@receiver(signals.post_save, sender=Person)
def create_person(sender, instance, **kwargs):
    image = np.asarray(Image.open(instance.image))
    image = cv2.resize(image, tuple(reversed(input_shape[:-1])), interpolation=cv2.INTER_AREA)
    image = np.array(image, dtype='float32') / 255
    image = np.expand_dims(image, axis=0)

    predicted_image_data = lfw_trained_model.predict(image)
    instance.image_nd_array = predicted_image_data
