from celery import shared_task
from datetime import datetime, timedelta
import datetime

from .models import WeatherData
from .services.current_weather_service import CurrentWeatherService


@shared_task
def ask_weather_question():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] Яка зараз температура повітря?")


@shared_task
def get_current_weather_data():
    service = CurrentWeatherService()  # Створюємо екземпляр класу
    weather = service.get_weather("Boryspil")  # Викликаємо метод у екземпляра
    print(f"In Boryspil now {weather}")


