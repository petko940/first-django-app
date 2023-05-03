from django.urls import path
from weather import views

urlpatterns = [
    path('weather', views.weather, name='weather'),
    path('delete_city/<city_id>/', views.delete_city, name='delete_city'),
]
