from django.db.models import signals
from django.dispatch import receiver
from ndarraydjango.fields import NDArrayField
from facenet_pytorch import MTCNN
from .cnn_model import create_models
from django.db import models
from PIL import Image
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

    def save(self, *args, **kwargs):
        image = np.asarray(Image.open(self.image)) # already RGB, so no need cv2.cvtColor
        # image = cv2.cvtColor(cv2.imread(self.image.url), cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, tuple(reversed(input_shape[:-1])), interpolation=cv2.INTER_AREA)
        image = np.array(image, dtype='float32') / 255

        predicted_image_data = lfw_trained_model.predict(image) # error
        ## ValueError: Input 0 of layer "model_3" is incompatible with the layer: expected shape=(None, 96, 96, 3), found shape=(32, 96, 3)

        self.image_nd_array.save(predicted_image_data, save=False)
        super().save(*args, **kwargs)
