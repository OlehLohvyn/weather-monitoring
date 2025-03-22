"""Celery tasks for retrieving and displaying current weather data."""

import datetime
from datetime import datetime

from celery import shared_task

# from .models import WeatherData
from .services.current_weather_service import CurrentWeatherService


@shared_task
def ask_weather_question():
    """
    Celery task that prints a weather-related question with a timestamp.

    This task is used as a placeholder or for demonstration/debugging purposes.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] What is the air temperature now?")


@shared_task
def get_current_weather_data():
    """
    Celery task that fetches the current weather data for Boryspil.

    Uses the CurrentWeatherService to get and print the weather.
    """
    service = CurrentWeatherService()
    weather = service.get_weather("Boryspil")
    print(f"In Boryspil now {weather}")
