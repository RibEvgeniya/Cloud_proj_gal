from django.db import models
from django.contrib.auth.models import User

from . import storage
from .storage import S3Storage


class PhotoFolder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255,
                            unique=True)

    def __str__(self):
        return self.name


def user_directory_path(instance, filename):
    username = instance.folder.user.username
    return f'user_{username}/{filename}'




from django.utils.deconstruct import deconstructible


@deconstructible
class MyS3BotoStorage(S3Storage):
    def deconstruct(self):
        path, args, kwargs = super().deconstruct()
        return path, args, kwargs

class Photo(models.Model):
    folder = models.ForeignKey(PhotoFolder, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to=user_directory_path, storage=MyS3BotoStorage)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title or self.image.name






