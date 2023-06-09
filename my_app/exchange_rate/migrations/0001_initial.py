# Generated by Django 4.2 on 2023-05-13 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeRateHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_currency', models.CharField(max_length=3)),
                ('target_currency', models.CharField(max_length=3)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='authapp.register')),
            ],
        ),
    ]
