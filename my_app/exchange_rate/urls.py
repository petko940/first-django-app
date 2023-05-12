from django.urls import path

from exchange_rate import views

urlpatterns = [
    path('exchange-rate', views.exchange_rate, name='exchange_rate'),
    path('exchange-delete/<exchange_id>', views.exchange_delete, name='exchange_delete'),
]
