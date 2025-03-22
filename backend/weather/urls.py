"""URL configuration for weather-related API endpoints."""

from django.urls import path
from .views import WeatherDataListCreate

urlpatterns = [
    path('weather/', WeatherDataListCreate.as_view(), name='weather-list'),
]
