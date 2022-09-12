from django.db import models

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


class Person(models.Model):
    name  = models.TextField(max_length=50, null=False)

    PERSON_CHOISES = [
        ("staff", "staff"),
        ("student", "student"),
    ]
    career = models.TextField(max_length=15, null=True, choices=PERSON_CHOISES)
    image  = models.FileField(null=False, upload_to ='images/')


