import re

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Model


# Create your models here.
def validate_username(value):
    if Register.objects.filter(username=value).exists():
        raise ValidationError("This username is already taken.")

    if not re.match(r'^[A-Za-z](?=.*[A-Za-z\d])[A-Za-z\d]{4,}$', value):
        raise ValidationError("Invalid username")


def validate_email(value):
    if Register.objects.filter(email=value).exists():
        raise ValidationError("This email is already taken.")


class Register(Model):
    username = models.CharField(validators=[validate_username], verbose_name='', unique=True, max_length=20)
    email = models.EmailField(validators=[validate_email], verbose_name='', unique=True)
    password1 = models.CharField(verbose_name='')
    password2 = models.CharField(verbose_name='')

    def clean(self):
        if self.password1 != self.password2:
            raise ValidationError("Passwords do not match.")

        if len(self.password1) < 6 or len(self.password2) < 6:
            raise ValidationError("Password is too short")