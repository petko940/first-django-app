# Generated by Django 4.2 on 2023-05-03 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0004_city_icon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='clouds',
        ),
    ]
