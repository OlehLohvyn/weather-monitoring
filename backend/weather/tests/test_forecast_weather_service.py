import unittest
import json
import os
import copy
from unittest.mock import patch, MagicMock
from django.test import TestCase
from ..services.forecast_weather_service import ForecastWeatherService
from ..models import WeatherData, WindData, WeatherCondition


class TestForecastWeatherService(TestCase):
    """Tests for core functionality of ForecastWeatherService."""

    @classmethod
    def setUpClass(cls):
        """Load mock data once for all tests."""
        super().setUpClass()
        file_path = os.path.join(os.path.dirname(__file__), "data", "mock_forecast_weather_response.json")

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                cls.mock_response = json.load(file)
            print(f"[setUpClass] Mock data loaded: {len(cls.mock_response)} keys")
        except FileNotFoundError:
            cls.mock_response = {}
            print("[setUpClass] Warning: mock_forecast_weather_response.json not found!")

    def setUp(self):
        """Initialize ForecastWeatherService before each test."""
        print("[setUp] Initializing ForecastWeatherService...")
        self.service = ForecastWeatherService()

    @patch("weather.services.forecast_weather_service.WeatherAPIClient")
    def test_service_initialization(self, mock_api_client):
        """Test that ForecastWeatherService initializes WeatherAPIClient correctly."""
        print("[test_service_initialization] Running test...")
        service = ForecastWeatherService()
        self.assertIsNotNone(service.api_client)
        mock_api_client.assert_called_once()

    @patch("weather.services.weather_api_client.WeatherAPIClient.fetch_data")
    def test_get_forecast_success(self, mock_fetch_data):
        """Test that get_forecast() correctly retrieves and saves forecast weather data."""

        mock_fetch_data.return_value = copy.deepcopy(self.mock_response)
        city = "London"
        date = "2025-03-08"
        hour = 23  # Оновлений час з мок-даних

        # Call the method
        weather = self.service.get_forecast(city, date, hour)

        # Ensure WeatherData is created
        self.assertIsInstance(weather, WeatherData)

        # Verify that saved values match mock response
        forecast_data = self.mock_response["forecast"]["forecastday"][0]["hour"][-1]  # Остання година дня

        self.assertEqual(weather.city, city)
        self.assertEqual(weather.temperature, forecast_data["temp_c"])
        self.assertEqual(weather.feels_like, forecast_data["feelslike_c"])
        self.assertEqual(weather.humidity, forecast_data["humidity"])
        self.assertEqual(weather.pressure, forecast_data["pressure_mb"])
        self.assertEqual(weather.precipitation, forecast_data["precip_mm"])

        print("[test_get_forecast_success] Forecast weather data saved and verified successfully.")

    @patch("weather.models.WeatherData.objects.filter")
    def test_get_forecast_data_already_exists(self, mock_filter):
        """Test that get_forecast() returns existing data without API call."""

        mock_existing_data = MagicMock(spec=WeatherData)
        mock_filter.return_value.first.return_value = mock_existing_data

        city = "London"
        date = "2025-03-08"
        hour = 23

        # Call the method
        result = self.service.get_forecast(city, date, hour)

        # Ensure API was not called
        mock_filter.assert_called_once_with(city=city, timestamp__date=date, timestamp__hour=hour)

        # Ensure the existing record is returned
        self.assertEqual(result, mock_existing_data)

        print("[test_get_forecast_data_already_exists] Existing forecast data returned successfully.")

    @patch("weather.services.weather_api_client.WeatherAPIClient.fetch_data")
    def test_get_forecast_no_forecast_data(self, mock_fetch_data):
        """Test handling when 'forecast' block is missing in API response."""

        mock_fetch_data.return_value = {}

        city = "London"
        date = "2025-03-08"
        hour = 23

        # Call the method
        result = self.service.get_forecast(city, date, hour)

        # Ensure API was called
        mock_fetch_data.assert_called_once()

        # Ensure the correct error is returned
        self.assertEqual(result, {"error": "API response does not contain forecast data"})

        print("[test_get_forecast_no_forecast_data] Handled missing 'forecast' block correctly.")

    @patch("weather.services.weather_api_client.WeatherAPIClient.fetch_data")
    def test_get_forecast_requested_date_not_found(self, mock_fetch_data):
        """Test handling when requested date is not found in API response."""

        mock_response = copy.deepcopy(self.mock_response)
        mock_response["forecast"]["forecastday"][0]["date"] = "2025-03-07"  # Інша дата

        mock_fetch_data.return_value = mock_response

        city = "London"
        date = "2025-03-08"
        hour = 23

        # Call the method
        result = self.service.get_forecast(city, date, hour)

        # Ensure API was called
        mock_fetch_data.assert_called_once()

        # Ensure the correct error is returned
        self.assertEqual(result, {"error": "Requested date or hour not found in forecast data"})

        print("[test_get_forecast_requested_date_not_found] Handled missing date correctly.")

    @patch("weather.services.weather_api_client.WeatherAPIClient.fetch_data")
    def test_get_forecast_requested_hour_not_found(self, mock_fetch_data):
        """Test handling when requested hour is not found in API response."""

        mock_response = copy.deepcopy(self.mock_response)
        mock_response["forecast"]["forecastday"][0]["hour"] = [
            {
                "time": "2025-03-08 22:00",  # Only hour 22 is present, hour 23 is missing
                "temp_c": 10.0,
                "humidity": 70,
                "pressure_mb": 1015
            }
        ]

        mock_fetch_data.return_value = mock_response

        city = "London"
        date = "2025-03-08"
        hour = 23  # Requested hour not in response

        # Call the method
        result = self.service.get_forecast(city, date, hour)

        # Ensure API was called
        mock_fetch_data.assert_called_once()

        # Ensure the correct error is returned
        self.assertEqual(result, {"error": "Requested date or hour not found in forecast data"})

        print("[test_get_forecast_requested_hour_not_found] Handled missing hour correctly.")


if __name__ == "__main__":
    unittest.main()
