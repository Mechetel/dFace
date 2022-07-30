from django.db import models

class Camera(models.Model):
    name = models.CharField(max_length=10)
    url = models.CharField(max_length=100, default="")
    description = models.TextField(default="")

    def __str__(self):
        return self.name


