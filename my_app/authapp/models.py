from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Model


# Create your models here.
# def validate_username(value, user_instance=None):
#     if user_instance:
#         queryset = Register.objects.filter(username=value).exclude(id=user_instance.id)
#     else:
#         queryset = Register.objects.filter(username=value)
#     if queryset.exists():
#         raise ValidationError("This username is already taken.")
#
#
# def validate_email(value, user_instance=None):
#     if user_instance:
#         queryset = Register.objects.filter(email=value).exclude(id=user_instance.id)
#     else:
#         queryset = Register.objects.filter(email=value)
#     if queryset.exists():
#         raise ValidationError("This email is already taken.")


# -----working
def validate_username(value):
    if Register.objects.filter(username=value).exists():
        raise ValidationError("This username is already taken.")


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
