import unittest
from unittest.mock import patch
from ..services.weather_api_client import WeatherAPIClient


class TestWeatherAPIClient(unittest.TestCase):

    @patch("weather.services.weather_api_client.requests.get")
    def test_fetch_current_weather(self, mock_get):
        """Test fetching current weather data"""

        # Expected API response
        mock_response = {
            "location": {"name": "Kyiv", "country": "Ukraine"},
            "current": {
                "temp_c": 15.5,
                "condition": {"text": "Clear"},
                "wind_kph": 10.2,
                "humidity": 60
            }
        }

        # Configure mock request
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        # Create an instance of the API client
        api_client = WeatherAPIClient()

        # Call the method being tested
        result = api_client.fetch_data("current", {"q": "Kyiv"})

        # Verify that `requests.get` was called with the correct arguments
        mock_get.assert_called_once()

        # Get the actual parameters passed to the request
        actual_params = mock_get.call_args.kwargs["params"]
        expected_params = {"q": "Kyiv", "key": api_client.api_key}

        # Verify that the passed parameters contain the correct values (order doesn't matter)
        self.assertDictEqual(actual_params, expected_params)


if __name__ == "__main__":
    unittest.main()
