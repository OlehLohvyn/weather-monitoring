import json
import os
import unittest
from unittest.mock import patch

import requests
from weather.services.weather_api_client import WeatherAPIClient


class TestWeatherAPIClient(unittest.TestCase):

    @patch("weather.services.weather_api_client.requests.get")
    def test_fetch_current_weather(self, mock_get):
        """Test fetching current weather data"""

        # Load mock data from a JSON file
        file_path = os.path.join(os.path.dirname(__file__), "data", "mock_weather_response.json")
        with open(file_path, "r") as file:
            mock_response = json.load(file)

        # Configure mock request
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        # Create an instance of the client
        api_client = WeatherAPIClient()

        # Call the method under test
        result = api_client.fetch_data("current", {"q": "Kyiv"})

        # Verify that the response matches the expected result
        self.assertEqual(result, mock_response)

    @patch("weather.services.weather_api_client.requests.get")
    def test_fetch_forecast_weather(self, mock_get):
        """Test fetching forecast weather data"""

        # Load mock data from a JSON file
        file_path = os.path.join(os.path.dirname(__file__), "data", "mock_weather_response.json")
        with open(file_path, "r") as file:
            mock_response = json.load(file)

        # Configure mock request
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        # Create an instance of the client
        api_client = WeatherAPIClient()

        # Call the method under test
        result = api_client.fetch_data("forecast", {"q": "Kyiv"})

        # Verify that the response matches the expected result
        self.assertEqual(result, mock_response)

    @patch("weather.services.weather_api_client.requests.get")
    def test_fetch_history_weather(self, mock_get):
        """Test fetching history weather data"""

        # Load mock data from a JSON file
        file_path = os.path.join(os.path.dirname(__file__), "data", "mock_weather_response.json")
        with open(file_path, "r") as file:
            mock_response = json.load(file)

        # Configure mock request
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        # Create an instance of the client
        api_client = WeatherAPIClient()

        # Call the method under test
        result = api_client.fetch_data("history", {"q": "Kyiv"})

        # Verify that the response matches the expected result
        self.assertEqual(result, mock_response)


class TestWeatherAPIClientErrorHandling(unittest.TestCase):

    @patch("weather.services.weather_api_client.requests.get")
    def test_api_returns_500(self, mock_get):
        """Test handling of API returning status code 500"""
        mock_get.return_value.status_code = 500
        mock_get.return_value.json.return_value = {"error": {"message": "Internal Server Error"}}

        api_client = WeatherAPIClient()
        result = api_client.fetch_data("current", {"q": "Kyiv"})

        self.assertIn("error", result)
        self.assertEqual(result["error"], "Internal Server Error")

    @patch("weather.services.weather_api_client.requests.get")
    def test_api_returns_invalid_json(self, mock_get):
        """Test handling of API returning invalid JSON"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.side_effect = requests.exceptions.JSONDecodeError("Invalid JSON", "", 0)

        api_client = WeatherAPIClient()
        result = api_client.fetch_data("current", {"q": "Kyiv"})

        self.assertIn("error", result)
        self.assertTrue("Request failed" in result["error"])  # Ensure the error message is properly set

    @patch("weather.services.weather_api_client.requests.get")
    def test_api_returns_404(self, mock_get):
        """Test handling of API returning status code 404 (city not found)"""
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {"error": {"message": "No matching location found"}}

        api_client = WeatherAPIClient()
        result = api_client.fetch_data("current", {"q": "UnknownCity"})

        self.assertIn("error", result)
        self.assertEqual(result["error"], "No matching location found")


class TestWeatherAPIClientValidation(unittest.TestCase):
    def test_invalid_endpoint(self):
        """Test handling of an invalid API endpoint"""
        api_client = WeatherAPIClient()
        result = api_client.fetch_data("invalid_endpoint", {"q": "Kyiv"})
        self.assertEqual(result["error"], "Invalid or missing API endpoint")

    def test_none_params(self):
        """Test handling of None as parameters"""
        api_client = WeatherAPIClient()
        result = api_client.fetch_data("current", None)
        self.assertEqual(result["error"], "Missing required parameter(s): q")

    def test_missing_required_param(self):
        """Test missing required parameter should return an error"""
        api_client = WeatherAPIClient()
        result = api_client.fetch_data("current", {})
        self.assertEqual(result["error"], "Missing required parameter(s): q")


class TestWeatherAPIClientTimeout(unittest.TestCase):

    @patch("weather.services.weather_api_client.requests.get")
    def test_fetch_data_timeout(self, mock_get):
        """Test handling of request timeout"""

        # Mock the request to simulate a timeout exception
        mock_get.side_effect = requests.exceptions.Timeout

        # Create an instance of the API client
        api_client = WeatherAPIClient()

        # Call the method with test parameters
        result = api_client.fetch_data("current", {"q": "Kyiv"})

        # Ensure the method returns an appropriate error message
        self.assertIn("error", result)
        self.assertTrue(result["error"].startswith("Request failed"))

        # Verify that the request was attempted exactly once
        mock_get.assert_called_once()


if __name__ == "__main__":
    unittest.main()

