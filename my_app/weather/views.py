import time

import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from authapp.models import Register
from authapp.views import check_if_someone_logged
from weather.models import City


# Create your views here.
def update_weather_data(city_obj, user):
    city = city_obj.name.capitalize()

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=4efda915428f625a249c2eb84797631e'
    response = requests.get(url).json()

    if response['cod'] != '404':
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
    except:  # NOQA
        return redirect('home')

    error_message = request.GET.get('error')  # Get the error message from the query parameters

    if request.method == 'POST':
        city = request.POST.get('city')
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=c584d18750dd25c4a8c4e7c84d98d9d7'
        response = requests.get(url).json()

        if not city:
            error_message = 'Invalid city!'
        elif response['cod'] == '404':
            error_message = 'Invalid city!'
        # if response['cod'] != '404':
        else:
            city = city.capitalize()

            existing_city = City.objects.filter(name=city, user=user).first()
            if existing_city:
                city_obj = existing_city
            else:
                city_obj = City.objects.create(name=city, user=user)

            update_weather_data(city_obj, user)

    cities = City.objects.filter(user=user)
    if cities:
        for city_obj in cities:
            update_weather_data(city_obj, user)

    context = {'cities': cities,
               'is_logged': is_logged,
               'user': user,
               'error_message': error_message,
               }

    return render(request, 'weather.html', context)


def delete_city(request, city_id):
    city = City.objects.get(id=city_id)
    city.delete()

    return redirect('weather')
