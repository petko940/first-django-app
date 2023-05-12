from django.db import models

from authapp.models import Register


# Create your models here.
class ExchangeRateHistory(models.Model):
    base_currency = models.CharField(max_length=3)
    target_currency = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True,null=True)

    user = models.ForeignKey(Register, on_delete=models.CASCADE, null=True)
