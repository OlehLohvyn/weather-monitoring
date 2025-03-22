"""Tests for the _handle_response method of WeatherAPIClient.

These tests ensure that the response data is correctly handled,
including valid JSON parsing and error cases.
"""


from unittest.mock import Mock, patch

import pytest
from requests import RequestException
from weather.services.exceptions import WeatherAPIError
from weather.services.weather_api_client import WeatherAPIClient


@patch("weather.services.weather_api_client.requests.get")
def test_fetch_data_success(mock_get, mock_current_weather_response_json):
    """Test fetch_data with valid response. Expect correct weather data returned."""
    # 1. Mocking the API response
    mock_response = Mock()
    mock_response.json.return_value = mock_current_weather_response_json
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    client = WeatherAPIClient()
    params = {"q": "Kyiv"}

    # 2. Call the method
    result = client.fetch_data("current", params)

    # 3. Checking the result
    assert "current" in result
    assert result["location"]["name"].lower() == "kyiv"


@patch("weather.services.weather_api_client.requests.get")
def test_fetch_data_http_error(mock_get):
    """Test fetch_data when a RequestException occurs. Expect WeatherAPIError."""
    # We mock RequestException itself
    mock_get.side_effect = RequestException("Connection error")

    client = WeatherAPIClient()
    params = {"q": "Kyiv"}

    with pytest.raises(WeatherAPIError, match="Request failed: Connection error"):
        client.fetch_data("current", params)


@patch("weather.services.weather_api_client.requests.get")
def test_fetch_data_error_in_json(mock_get):
    """Test fetch_data when API returns an error in JSON. Expect WeatherAPIError."""
    # 1. We mock the response with the "error" field
    mock_response = Mock()
    mock_response.json.return_value = {
        "error": {"message": "Invalid API key"}
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    client = WeatherAPIClient()
    params = {"q": "Kyiv"}

    with pytest.raises(WeatherAPIError, match="Invalid API key"):
        client.fetch_data("current", params)
