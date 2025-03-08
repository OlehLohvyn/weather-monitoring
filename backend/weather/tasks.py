from celery import shared_task
from .services.current_weather_service import CurrentWeatherService
from django.conf import settings
from datetime import datetime

@shared_task
def fetch_and_store_weather():
    """ Отримує поточну погоду і зберігає її в базу кожну годину. """
    service = CurrentWeatherService()
    city = settings.DEFAULT_CITY  # Візьми місто із settings.py або .env

    weather = service.get_weather(city)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if isinstance(weather, dict) and "error" in weather:
        print(f"[{now}] ❌ Помилка отримання погоди: {weather['error']}")
    else:
        print(f"[{now}] ✅ Погода для {city} успішно збережена: {weather.temperature}°C")
