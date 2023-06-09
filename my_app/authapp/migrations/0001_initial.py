# Generated by Django 4.2 on 2023-05-13 10:17

import authapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True, validators=[authapp.models.validate_username], verbose_name='')),
                ('email', models.EmailField(max_length=254, unique=True, validators=[authapp.models.validate_email], verbose_name='')),
                ('password1', models.CharField(verbose_name='')),
                ('password2', models.CharField(verbose_name='')),
            ],
        ),
    ]
