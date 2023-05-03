from django.db import models


# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=100)
    temperature = models.IntegerField(null=True)
    feels_like = models.IntegerField(null=True)
    humidity = models.FloatField(null=True)
    wind_speed = models.FloatField(null=True)
    type = models.TextField(null=True)
    icon = models.ImageField(null=True)
