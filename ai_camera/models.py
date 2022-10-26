from .constants import (
        lfw_trained_model,
        openface_model,
        pinface_trained_model,
        mtcnn,
        input_shape
    )
from django.db import models
from ndarraydjango.fields import NDArrayField
from PIL import Image as PIL_Image
from .Image import Image
from .Shape import Shape
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
    career                  = models.TextField(max_length=15, null=True, choices=PERSON_CHOISES)
    image                   = models.FileField(upload_to ='images/', null=True)
    # image_original_nd_array = NDArrayField(shape=(128), dtype=np.float32, null=True)
    # image_pinfase_nd_array  = NDArrayField(shape=(128), dtype=np.float32, null=True)
    image_lfw_nd_array      = NDArrayField(shape=(128), dtype=np.float32, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        image = Image(np.asarray(PIL_Image.open(self.image))) # already RGB, so no need cv2.cvtColor
        image.resize(Shape(96, 96))
        image.normalize()

        # self.image_original_nd_array = openface_model.encode(image)
        # self.image_pinfase_nd_array  = pinface_trained_model.encode(image)
        self.image_lfw_nd_array      = lfw_trained_model.encode(image)
        super(Person, self).save(*args, **kwargs)
