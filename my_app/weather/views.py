import requests
from django.contrib.gis.geoip2 import GeoIP2
from django.shortcuts import render, redirect

from authapp.models import Register
from authapp.views import check_if_someone_logged
from weather.models import City


# Create your views here.
def update_weather_data(city_obj):
    city = city_obj.name.capitalize()

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=c584d18750dd25c4a8c4e7c84d98d9d7'
    response = requests.get(url).json()

    temperature = response['main']['temp'] - 273.15
    feels_like = response['main']['feels_like'] - 273.15
    humidity = response['main']['humidity']
    wind_speed = response['wind']['speed']
    weather_type = response['weather'][0]['main']
    icon = response['weather'][0]['icon']

    city_obj.temperature = temperature
    city_obj.feels_like = feels_like
    city_obj.humidity = humidity
    city_obj.wind_speed = wind_speed
    city_obj.type = weather_type
    city_obj.icon = icon

    city_obj.save()


def weather(request):
    try:
        user = Register.objects.get(id=request.session.get('user_id'))
        is_logged = check_if_someone_logged(request)
    except:
        return redirect('home')

    # City.objects.all().delete()
    if request.method == 'POST':
        try:
            city = request.POST.get('city')
            city = city.capitalize()

            city_obj, created = City.objects.get_or_create(name=city)
            update_weather_data(city_obj)
        except:
            context = {'error': 'Write valid city',
                       'is_logged': is_logged,
                       'user': user
                       }
            return render(request, 'weather.html', context)

    cities = City.objects.all()
    if cities:
        for city_obj in cities:
            update_weather_data(city_obj)

    context = {'cities': cities,
               'is_logged': is_logged,
               'user': user
               }
    return render(request, 'weather.html', context)


def delete_city(request, city_id):
    city = City.objects.get(id=city_id)
    city.delete()

    return redirect('weather')
