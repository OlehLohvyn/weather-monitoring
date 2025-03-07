import unittest
import json
import os
import copy
from unittest.mock import patch, MagicMock
from django.test import TestCase
from ..services.historical_weather_service import HistoricalWeatherService
from ..models import WeatherData, WindData, WeatherCondition


class TestHistoricalWeatherService(TestCase):

    @classmethod
    def setUpClass(cls):
        """Load mock data once for all tests."""
        super().setUpClass()
        file_path = os.path.join(os.path.dirname(__file__), "data", "mock_historical_weather_response.json")

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                cls.mock_response = json.load(file)
            print(f"[setUpClass] Mock data loaded: {len(cls.mock_response)} keys")
        except FileNotFoundError:
            cls.mock_response = {}
            print("[setUpClass] Warning: mock_historical_weather_response.json not found!")

    def setUp(self):
        """Initialize HistoricalWeatherService before each test."""
        print("[setUp] Initializing HistoricalWeatherService...")
        self.service = HistoricalWeatherService()

    @patch("weather.services.historical_weather_service.WeatherAPIClient")
    def test_service_initialization(self, mock_api_client):
        """Test that HistoricalWeatherService initializes WeatherAPIClient correctly."""
        print("[test_service_initialization] Running test...")
        service = HistoricalWeatherService()
        self.assertIsNotNone(service.api_client)
        mock_api_client.assert_called_once()

    @patch("weather.services.weather_api_client.WeatherAPIClient.fetch_data")
    def test_get_history_success(self, mock_fetch_data):
        """Test that get_history() correctly retrieves and saves historical weather data."""

        # Use deepcopy to ensure mock_response is not modified between tests
        mock_fetch_data.return_value = copy.deepcopy(self.mock_response)
        city = "London"
        date = "2025-03-06"
        hour = 23

        # Call the method
        weather = self.service.get_history(city, date, hour)

        # Verify that fetch_data was called with correct parameters
        mock_fetch_data.assert_called_once_with("history", {"key": self.service.api_client.api_key, "q": city, "dt": date})

        # Ensure WeatherData object was created
        self.assertIsInstance(weather, WeatherData)

        # Verify that saved values match mock response
        forecast_data = self.mock_response["forecast"]["forecastday"][0]["hour"][hour]

        self.assertEqual(weather.city, city)
        self.assertEqual(weather.temperature, forecast_data["temp_c"])
        self.assertEqual(weather.feels_like, forecast_data["feelslike_c"])
        self.assertEqual(weather.humidity, forecast_data["humidity"])
        self.assertEqual(weather.pressure, forecast_data["pressure_mb"])
        self.assertEqual(weather.precipitation, forecast_data["precip_mm"])

        # Ensure WindData and WeatherCondition objects were created and linked correctly
        self.assertIsInstance(weather.wind, WindData)
        self.assertIsInstance(weather.condition, WeatherCondition)

        self.assertEqual(weather.wind.wind_speed, forecast_data["wind_kph"])
        self.assertEqual(weather.wind.wind_gust, forecast_data.get("gust_kph"))
        self.assertEqual(weather.wind.wind_direction, forecast_data["wind_dir"])
        self.assertEqual(weather.wind.wind_degree, forecast_data.get("wind_degree"))

        self.assertEqual(weather.condition.weather_condition, forecast_data["condition"]["text"])
        self.assertEqual(weather.condition.weather_icon, f"https:{forecast_data['condition']['icon']}")
        self.assertEqual(weather.condition.cloudiness, forecast_data["cloud"])
        self.assertEqual(weather.condition.visibility, forecast_data["vis_km"])
        self.assertEqual(weather.condition.uv_index, forecast_data["uv"])

        print("[test_get_history_success] Historical weather data saved and verified successfully.")


    @patch("weather.models.WeatherData.objects.filter")
    def test_get_history_data_already_exists(self, mock_filter):
        """Test that get_history() returns existing data without API call."""

        # Create a mock existing record
        mock_existing_data = MagicMock(spec=WeatherData)
        mock_filter.return_value.first.return_value = mock_existing_data

        city = "London"
        date = "2025-03-06"
        hour = 23
        # Call the method
        result = self.service.get_history(city, date, hour)

        # Ensure API was not called
        mock_filter.assert_called_once_with(city=city, timestamp__date=date, timestamp__hour=hour)

        # Ensure the existing record is returned
        self.assertEqual(result, mock_existing_data)

        print("[test_get_history_data_already_exists] Existing data returned successfully.")

    @patch("weather.services.weather_api_client.WeatherAPIClient.fetch_data")
    def test_get_history_no_forecast_data(self, mock_fetch_data):
        """Test handling when 'forecast' block is missing in API response."""

        # Mock API response without 'forecast' key
        mock_fetch_data.return_value = {}

        city = "London"
        date = "2025-03-06"
        hour = 23

        # Call the method
        result = self.service.get_history(city, date, hour)

        # Ensure API was called
        mock_fetch_data.assert_called_once_with("history", {"key": self.service.api_client.api_key, "q": city, "dt": date})

        # Ensure the correct error is returned
        self.assertEqual(result, {"error": "API response does not contain historical data"})

        print("[test_get_history_no_forecast_data] Handled missing 'forecast' block correctly.")

    @patch("weather.services.weather_api_client.WeatherAPIClient.fetch_data")
    def test_get_history_requested_date_not_found(self, mock_fetch_data):
        """Test handling when requested date is not found in API response."""

        # Modify mock response to exclude requested date
        mock_response = copy.deepcopy(self.mock_response)
        mock_response["forecast"]["forecastday"][0]["date"] = "2024-02-28"  # Different date

        mock_fetch_data.return_value = mock_response

        city = "London"
        date = "2025-03-06"
        hour = 23

        # Call the method
        result = self.service.get_history(city, date, hour)

        # Ensure API was called
        mock_fetch_data.assert_called_once_with("history", {"key": self.service.api_client.api_key, "q": city, "dt": date})

        # Ensure the correct error is returned
        self.assertEqual(result, {"error": "Requested date or hour not found in historical data"})

        print("[test_get_history_requested_date_not_found] Handled missing date correctly.")

    @patch("weather.services.weather_api_client.WeatherAPIClient.fetch_data")
    def test_get_history_requested_hour_not_found(self, mock_fetch_data):
        """Test handling when requested hour is not found in API response."""

        # Modify mock response to exclude requested hour
        mock_response = copy.deepcopy(self.mock_response)
        mock_response["forecast"]["forecastday"][0]["hour"] = [
            {
                "time": "2024-03-01 14:00",  # Only hour 14 is present, hour 15 is missing
                "temp_c": 10.0,
                "humidity": 70,
                "pressure_mb": 1015
            }
        ]

        mock_fetch_data.return_value = mock_response

        city = "London"
        date = "2025-03-06"
        hour = 23

        # Call the method
        result = self.service.get_history(city, date, hour)

        # Ensure API was called
        mock_fetch_data.assert_called_once_with("history", {"key": self.service.api_client.api_key, "q": city, "dt": date})

        # Ensure the correct error is returned
        self.assertEqual(result, {"error": "Requested date or hour not found in historical data"})

        print("[test_get_history_requested_hour_not_found] Handled missing hour correctly.")


class TestHistoricalWeatherServiceEdgeCases(TestCase):
    """Edge cases for HistoricalWeatherService."""

    @classmethod
    def setUpClass(cls):
        """Load mock data once for all tests."""
        super().setUpClass()
        file_path = os.path.join(os.path.dirname(__file__), "data", "mock_historical_weather_response.json")

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                cls.mock_response = json.load(file)
            print(f"[setUpClass] Mock data loaded: {len(cls.mock_response)} keys")
        except FileNotFoundError:
            cls.mock_response = {}
            print("[setUpClass] Warning: mock_historical_weather_response.json not found!")

    def setUp(self):
        """Initialize HistoricalWeatherService before each test."""
        print("[setUp] Initializing HistoricalWeatherService...")
        self.service = HistoricalWeatherService()

    @patch("weather.services.weather_api_client.WeatherAPIClient.fetch_data")
    def test_get_history_correct_api_call(self, mock_fetch_data):
        """Test that fetch_data() is called with the correct parameters."""

        city = "London"
        date = "2025-03-06"
        expected_params = {"key": self.service.api_client.api_key, "q": city, "dt": date}

        # Mock API response
        mock_fetch_data.return_value = copy.deepcopy(self.mock_response)

        # Call the method
        self.service.get_history(city, date, 15)

        # Verify the API call was made with the correct parameters
        mock_fetch_data.assert_called_once_with("history", expected_params)

        print("[test_get_history_correct_api_call] API called with correct parameters.")

    @patch("weather.services.weather_api_client.WeatherAPIClient.fetch_data")
    def test_get_history_api_exception(self, mock_fetch_data):
        """Test that get_history() correctly handles API errors like ConnectionError and Timeout."""

        city = "London"
        date = "2025-03-06"
        hour = 23

        # Simulate an API exception
        mock_fetch_data.side_effect = ConnectionError("API request failed")

        # Call the method
        result = self.service.get_history(city, date, hour)

        # Ensure the correct error is returned
        self.assertEqual(result, {"error": "Failed to fetch historical weather data"})

        print("[test_get_history_api_exception] API exception handled correctly.")

    def test_get_history_invalid_hour_format(self):
        """Test that get_history() returns an error for invalid hour values."""

        city = "London"
        date = "2025-03-06"
        invalid_hours = [-1, 25, "abc"]

        for hour in invalid_hours:
            with self.subTest(hour=hour):
                result = self.service.get_history(city, date, hour)
                self.assertEqual(result, {"error": "Invalid hour format"})

        print("[test_get_history_invalid_hour_format] Invalid hour values handled correctly.")

    @patch("weather.services.weather_api_client.WeatherAPIClient.fetch_data")
    def test_get_history_partial_data(self, mock_fetch_data):
        """Test that get_history() correctly saves data even when some optional fields are missing."""

        # Modify mock response to exclude optional fields
        mock_response = copy.deepcopy(self.mock_response)
        forecast_hour = mock_response["forecast"]["forecastday"][0]["hour"][0]

        # Remove optional fields
        forecast_hour.pop("gust_kph", None)
        forecast_hour.pop("uv", None)

        mock_fetch_data.return_value = mock_response

        city = "London"
        date = "2025-03-06"
        hour = int(forecast_hour["time"][-5:-3])

        # Call the method
        weather = self.service.get_history(city, date, hour)

        # Ensure WeatherData is created
        self.assertIsInstance(weather, WeatherData)

        # Ensure WindData and WeatherCondition exist
        self.assertIsInstance(weather.wind, WindData)
        self.assertIsInstance(weather.condition, WeatherCondition)

        # Ensure missing optional fields default to None
        self.assertIsNone(weather.wind.wind_gust)
        self.assertIsNone(weather.condition.uv_index)

        print("[test_get_history_partial_data] Handled missing optional fields correctly.")



class TestHistoricalWeatherDatabaseIntegrity(TestCase):
    """Tests to verify database integrity after saving historical weather data."""

    @classmethod
    def setUpClass(cls):
        """Load mock data once for all tests."""
        super().setUpClass()
        file_path = os.path.join(os.path.dirname(__file__), "data", "mock_historical_weather_response.json")

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                cls.mock_response = json.load(file)
            print(f"[setUpClass] Mock data loaded: {len(cls.mock_response)} keys")
        except FileNotFoundError:
            cls.mock_response = {}
            print("[setUpClass] Warning: mock_historical_weather_response.json not found!")

    def setUp(self):
        """Initialize HistoricalWeatherService before each test."""
        print("[setUp] Initializing HistoricalWeatherService...")
        self.service = HistoricalWeatherService()

    @patch("weather.services.weather_api_client.WeatherAPIClient.fetch_data")
    def test_get_history_data_saved_correctly(self, mock_fetch_data):
        """Test that all retrieved values (temperature, pressure, humidity, wind direction, etc.) are saved correctly."""

        mock_fetch_data.return_value = copy.deepcopy(self.mock_response)
        city = "London"
        date = "2025-03-06"
        hour = 23

        # Call the method
        weather = self.service.get_history(city, date, hour)

        # Ensure WeatherData is created
        self.assertIsInstance(weather, WeatherData)

        # Retrieve saved data
        saved_weather = WeatherData.objects.get(id=weather.id)

        # Verify saved values match mock response
        forecast_data = self.mock_response["forecast"]["forecastday"][0]["hour"][hour]

        self.assertEqual(saved_weather.city, city)
        self.assertEqual(saved_weather.temperature, forecast_data["temp_c"])
        self.assertEqual(saved_weather.feels_like, forecast_data["feelslike_c"])
        self.assertEqual(saved_weather.humidity, forecast_data["humidity"])
        self.assertEqual(saved_weather.pressure, forecast_data["pressure_mb"])
        self.assertEqual(saved_weather.precipitation, forecast_data["precip_mm"])

        print("[test_get_history_data_saved_correctly] WeatherData saved and verified successfully.")

    @patch("weather.services.weather_api_client.WeatherAPIClient.fetch_data")
    def test_get_history_wind_data_saved(self, mock_fetch_data):
        """Test that WindData is created and correctly linked to WeatherData."""

        mock_fetch_data.return_value = copy.deepcopy(self.mock_response)
        city = "London"
        date = "2025-03-06"
        hour = 23

        # Call the method
        weather = self.service.get_history(city, date, hour)

        # Ensure WindData is created and linked
        self.assertIsInstance(weather.wind, WindData)

        # Retrieve saved wind data
        saved_wind = WindData.objects.get(id=weather.wind.id)
        forecast_data = self.mock_response["forecast"]["forecastday"][0]["hour"][hour]

        self.assertEqual(saved_wind.wind_speed, forecast_data["wind_kph"])
        self.assertEqual(saved_wind.wind_gust, forecast_data.get("gust_kph"))
        self.assertEqual(saved_wind.wind_direction, forecast_data["wind_dir"])
        self.assertEqual(saved_wind.wind_degree, forecast_data.get("wind_degree"))

        print("[test_get_history_wind_data_saved] WindData saved and verified successfully.")

    @patch("weather.services.weather_api_client.WeatherAPIClient.fetch_data")
    def test_get_history_weather_condition_saved(self, mock_fetch_data):
        """Test that WeatherCondition is created and correctly linked to WeatherData."""

        mock_fetch_data.return_value = copy.deepcopy(self.mock_response)
        city = "London"
        date = "2025-03-06"
        hour = 23

        # Call the method
        weather = self.service.get_history(city, date, hour)

        # Ensure WeatherCondition is created and linked
        self.assertIsInstance(weather.condition, WeatherCondition)

        # Retrieve saved weather condition
        saved_condition = WeatherCondition.objects.get(id=weather.condition.id)
        forecast_data = self.mock_response["forecast"]["forecastday"][0]["hour"][hour]

        self.assertEqual(saved_condition.weather_condition, forecast_data["condition"]["text"])
        self.assertEqual(saved_condition.weather_icon, f"https:{forecast_data['condition']['icon']}")
        self.assertEqual(saved_condition.cloudiness, forecast_data["cloud"])
        self.assertEqual(saved_condition.visibility, forecast_data["vis_km"])
        self.assertEqual(saved_condition.uv_index, forecast_data["uv"])

        print("[test_get_history_weather_condition_saved] WeatherCondition saved and verified successfully.")

    @patch("weather.services.weather_api_client.WeatherAPIClient.fetch_data")
    def test_get_history_missing_non_critical_fields(self, mock_fetch_data):
        """Test that missing secondary fields do not prevent the record from being saved."""

        mock_response = copy.deepcopy(self.mock_response)
        forecast_hour = mock_response["forecast"]["forecastday"][0]["hour"][-1]  # Остання година (23:00)

        # Remove non-critical fields
        forecast_hour.pop("gust_kph", None)  # Видаляємо обов'язково
        forecast_hour.pop("uv", None)  # Видаляємо uv

        mock_fetch_data.return_value = mock_response

        city = "London"
        date = "2025-03-06"
        hour = 23

        # Call the method
        weather = self.service.get_history(city, date, hour)

        # Ensure WeatherData is created
        self.assertIsInstance(weather, WeatherData)

        # Ensure WindData and WeatherCondition exist
        self.assertIsInstance(weather.wind, WindData)
        self.assertIsInstance(weather.condition, WeatherCondition)

        # Ensure missing optional fields default to None
        self.assertIsNone(weather.wind.wind_gust, f"[ERROR] wind_gust should be None but got: {weather.wind.wind_gust}")
        self.assertIsNone(weather.condition.uv_index)

        print("[test_get_history_missing_non_critical_fields] Handled missing optional fields correctly.")


if __name__ == "__main__":
    unittest.main()

