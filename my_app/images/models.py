from django.db import models

from authapp.models import Register


# Create your models here.
class Image(models.Model):
    image_name = models.CharField(max_length=50, null=True)
    image_data = models.BinaryField(null=True, blank=True)

    user = models.ForeignKey(Register, on_delete=models.CASCADE, null=True)


class ProfileImageUpdate(models.Model):
    image_data = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(Register, on_delete=models.CASCADE, null=True)
