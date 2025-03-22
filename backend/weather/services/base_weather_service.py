import logging

from weather.models import WeatherData
from weather.services.weather_api_client import WeatherAPIClient
from weather.services.weather_factory import WeatherModelFactory


class BaseWeatherService:
    def __init__(self):
        self.api_client = WeatherAPIClient()
        self.logger = logging.getLogger(__name__)

    def _parse_hour(self, time_str: str) -> int:
        return int(time_str[-5:-3])

    def _already_exists(self, city: str, date: str, hour: int):
        return WeatherData.objects.filter(city=city, timestamp__date=date, timestamp__hour=hour).first()

    def _save_weather(self, city: str, data: dict) -> WeatherData:
        wind = WeatherModelFactory.create_wind(data)
        condition = WeatherModelFactory.create_condition(data)
        return WeatherModelFactory.create_weather(city, data, wind, condition)
