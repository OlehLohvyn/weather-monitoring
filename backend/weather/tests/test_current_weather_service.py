import copy
import json
import os
import unittest
from unittest.mock import patch

from django.test import TestCase
from weather.models import WeatherCondition, WeatherData, WindData
from weather.services.current_weather_service import CurrentWeatherService


class TestCurrentWeatherService(TestCase):

    @classmethod
    def setUpClass(cls):
        """Load mock data once for all tests."""
        super().setUpClass()
        file_path = os.path.join(os.path.dirname(__file__), "data", "mock_weather_response.json")

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                cls.mock_response = json.load(file)
            print(f"[setUpClass] Mock data loaded: {len(cls.mock_response)} keys")  # Console output
        except FileNotFoundError:
            cls.mock_response = {}
            print("[setUpClass] Warning: mock_weather_response.json not found!")

    def setUp(self):
        """Initialize CurrentWeatherService before each test."""
        print("[setUp] Initializing CurrentWeatherService...")
        self.service = CurrentWeatherService()

    @patch("weather.services.current_weather_service.WeatherAPIClient")
    def test_service_initialization(self, mock_api_client):
        """Test that CurrentWeatherService initializes WeatherAPIClient."""
        print("[test_service_initialization] Running test...")
        service = CurrentWeatherService()
        self.assertIsNotNone(service.api_client)
        mock_api_client.assert_called_once()

    @patch("weather.services.weather_api_client.WeatherAPIClient.fetch_data")
    @patch("weather.models.WeatherData.objects.create")
    @patch("weather.models.WindData.objects.create")
    @patch("weather.models.WeatherCondition.objects.create")
    def test_get_weather_success(self, mock_weather_condition_create, mock_wind_data_create,
                                 mock_weather_data_create, mock_fetch_data):
        """Test successful retrieval of weather data."""

        # 1. Use a deep copy of the mock response to avoid data modification issues
        mock_fetch_data.return_value = copy.deepcopy(self.mock_response)
        city = "Kyiv"

        # 2. Call the method
        result = self.service.get_weather(city)

        # 3. Verify that fetch_data was called with the correct parameters
        mock_fetch_data.assert_called_once_with("current", {"key": self.service.api_client.api_key, "q": city, "aqi": "no"})

        # 4. Verify the creation of WindData and WeatherCondition models
        mock_wind_data_create.assert_called_once_with(
            wind_speed=self.mock_response["current"]["wind_kph"],
            wind_gust=self.mock_response["current"].get("gust_kph", None),
            wind_direction=self.mock_response["current"]["wind_dir"],
            wind_degree=self.mock_response["current"]["wind_degree"]
        )

        mock_weather_condition_create.assert_called_once_with(
            weather_condition=self.mock_response["current"]["condition"]["text"],
            weather_icon=f"https:{self.mock_response['current']['condition']['icon']}",
            cloudiness=self.mock_response["current"]["cloud"],
            visibility=self.mock_response["current"]["vis_km"],
            uv_index=self.mock_response["current"]["uv"]
        )

        # 5. Verify the creation of the WeatherData model
        mock_weather_data_create.assert_called_once_with(
            city=self.mock_response["location"]["name"],
            country=self.mock_response["location"]["country"],
            lat=self.mock_response["location"]["lat"],
            lon=self.mock_response["location"]["lon"],
            temperature=self.mock_response["current"]["temp_c"],
            feels_like=self.mock_response["current"]["feelslike_c"],
            humidity=self.mock_response["current"]["humidity"],
            pressure=self.mock_response["current"]["pressure_mb"],
            precipitation=self.mock_response["current"]["precip_mm"],
            wind=mock_wind_data_create.return_value,
            condition=mock_weather_condition_create.return_value
        )

        # 6. Ensure that the method returns the expected WeatherData object
        self.assertEqual(result, mock_weather_data_create.return_value)

    @patch("weather.services.weather_api_client.WeatherAPIClient.fetch_data")
    @patch("weather.models.WeatherData.objects.create")
    def test_get_weather_missing_critical_fields(self, mock_weather_data_create, mock_fetch_data):
        """Test handling of missing critical fields in API response."""

        # Create a deep copy of mock response without critical fields
        incomplete_response = copy.deepcopy(self.mock_response)
        incomplete_response["current"].pop("temp_c", None)  # Remove temperature
        incomplete_response["current"].pop("pressure_mb", None)  # Remove pressure
        incomplete_response["current"].pop("wind_kph", None)  # Remove wind speed
        incomplete_response["current"].pop("vis_km", None)  # Remove visibility

        mock_fetch_data.return_value = incomplete_response
        city = "Kyiv"

        # Call the method
        result = self.service.get_weather(city)

        # Verify that fetch_data was called with the correct parameters
        mock_fetch_data.assert_called_once_with("current",
                                                {"key": self.service.api_client.api_key, "q": city, "aqi": "no"})

        # Ensure that no data is saved if critical fields are missing
        mock_weather_data_create.assert_not_called()

        # Check that the method returns an error
        self.assertEqual(result, {"error": "Missing critical weather data: temp_c"})

    @patch("weather.services.weather_api_client.WeatherAPIClient.fetch_data")
    def test_get_weather_data_saved_correctly(self, mock_fetch_data):
        """Test that all retrieved weather data is correctly saved to the database."""

        mock_response = copy.deepcopy(self.mock_response)
        mock_fetch_data.return_value = mock_response
        city = "Kyiv"

        weather = self.service.get_weather(city)

        self.assertIsInstance(weather, WeatherData)

        self.assertEqual(weather.city, mock_response["location"]["name"])
        self.assertEqual(weather.country, mock_response["location"]["country"])
        self.assertEqual(weather.lat, mock_response["location"]["lat"])
        self.assertEqual(weather.lon, mock_response["location"]["lon"])
        self.assertEqual(weather.temperature, mock_response["current"]["temp_c"])
        self.assertEqual(weather.feels_like, mock_response["current"]["feelslike_c"])
        self.assertEqual(weather.humidity, mock_response["current"]["humidity"])
        self.assertEqual(weather.pressure, mock_response["current"]["pressure_mb"])
        self.assertEqual(weather.precipitation, mock_response["current"]["precip_mm"])

        self.assertIsInstance(weather.wind, WindData)
        self.assertIsInstance(weather.condition, WeatherCondition)

        self.assertEqual(weather.wind.wind_speed, mock_response["current"]["wind_kph"])
        self.assertEqual(weather.wind.wind_gust, mock_response["current"].get("gust_kph"))
        self.assertEqual(weather.wind.wind_direction, mock_response["current"]["wind_dir"])
        self.assertEqual(weather.wind.wind_degree, mock_response["current"].get("wind_degree"))

        self.assertEqual(weather.condition.weather_condition, mock_response["current"]["condition"]["text"])
        self.assertEqual(weather.condition.weather_icon, f"https:{mock_response['current']['condition']['icon']}")
        self.assertEqual(weather.condition.cloudiness, mock_response["current"]["cloud"])
        self.assertEqual(weather.condition.visibility, mock_response["current"]["vis_km"])
        self.assertEqual(weather.condition.uv_index, mock_response["current"]["uv"])

        print("[test_get_weather_data_saved_correctly] Weather data saved and verified successfully.")

    @patch("weather.services.weather_api_client.WeatherAPIClient.fetch_data")
    def test_get_weather_correct_api_call(self, mock_fetch_data):
        """Test that fetch_data is called with the correct parameters."""

        city = "Kyiv"
        expected_params = {
            "key": self.service.api_client.api_key,
            "q": city,
            "aqi": "no"
        }

        # Mock API response
        mock_fetch_data.return_value = copy.deepcopy(self.mock_response)

        # Call the method
        self.service.get_weather(city)

        # Verify that fetch_data was called exactly once with the correct parameters
        mock_fetch_data.assert_called_once_with("current", expected_params)

        print("[test_get_weather_correct_api_call] API call parameters verified successfully.")


if __name__ == "__main__":
    unittest.main()