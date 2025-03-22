"""Tests for the _handle_response method of WeatherAPIClient.

These tests ensure that the response data is correctly handled,
including valid JSON parsing and error cases.
"""


from unittest.mock import Mock

import pytest
from weather.services.exceptions import WeatherAPIError
from weather.services.weather_api_client import WeatherAPIClient


def test_handle_response_valid(mock_current_weather_response_json):
    """Test _handle_response with a valid mock response containing weather data."""
    client = WeatherAPIClient()

    mock_response = Mock()
    mock_response.json.return_value = mock_current_weather_response_json

    data = client._handle_response(mock_response)

    assert "location" in data
    assert "current" in data
    assert isinstance(data["current"]["temp_c"], (int, float))

def test_handle_response_with_error():
    """Test _handle_response with an error in the response. Expect WeatherAPIError."""
    client = WeatherAPIClient()

    mock_response = Mock()
    mock_response.json.return_value = {
        "error": {"message": "Invalid API key"}
    }

    with pytest.raises(WeatherAPIError, match="Invalid API key"):
        client._handle_response(mock_response)



