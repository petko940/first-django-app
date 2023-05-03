# Generated by Django 4.2 on 2023-05-02 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('temperature', models.IntegerField(null=True)),
                ('feels_like', models.IntegerField(null=True)),
                ('humidity', models.FloatField(null=True)),
                ('wind_speed', models.FloatField(null=True)),
                ('clouds', models.FloatField(null=True)),
            ],
        ),
    ]
