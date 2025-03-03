import unittest
from unittest.mock import patch
from ..services.weather_api import WeatherAPIClient


class TestWeatherAPIClient(unittest.TestCase):

    def setUp(self):
        """Ініціалізація клієнта перед кожним тестом"""
        self.client = WeatherAPIClient()

    @patch("weather.services.weather_api.requests.get")
    def test_get_current_weather_success(self, mock_get):
        """Тестуємо успішний запит поточної погоди"""

        # Фейковий API-відповідь
        mock_response = {
            "location": {"name": "Kyiv", "country": "Ukraine", "lat": 50.45, "lon": 30.52},
            "current": {
                "temp_c": 10.0, "feelslike_c": 8.0, "humidity": 60, "pressure_mb": 1012,
                "wind_kph": 15.0, "wind_dir": "NW",  # Додано `wind_dir`
                "wind_degree": 270,  # Додано `wind_degree`
                "cloud": 20, "vis_km": 10.0, "precip_mm": 0.0, "uv": 5.0,
                "condition": {"text": "Clear", "icon": "//cdn.weatherapi.com/weather/64x64/day/113.png"}
            }
        }

        # Налаштовуємо mock, щоб повертати нашу фейкову відповідь
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        # Викликаємо метод
        result = self.client.get_current_weather("Kyiv")

        # Перевіряємо, чи повернуто правильні дані
        self.assertEqual(result["city"], "Kyiv")
        self.assertEqual(result["country"], "Ukraine")
        self.assertEqual(result["temperature"], 10.0)
        self.assertEqual(result["weather_condition"], "Clear")
        self.assertEqual(result["wind_direction"], "NW")  # Тестуємо wind_dir
        self.assertEqual(result["wind_degree"], 270)  # Тестуємо wind_degree


if __name__ == "__main__":
    unittest.main()
