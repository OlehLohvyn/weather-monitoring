"""Tests for the _prepare_request method of WeatherAPIClient.

These tests check if request parameters are properly formatted
before being sent to the external weather API.
"""


import pytest
from weather.services.exceptions import WeatherAPIError
from weather.services.weather_api_client import WeatherAPIClient


def test_prepare_request_valid():
    """Test _prepare_request with valid endpoint and parameters."""
    client = WeatherAPIClient()
    url, params = client._prepare_request("current", {"q": "Kyiv"})

    assert "current" in url
    assert "key" in params
    assert params["q"] == "Kyiv"

def test_prepare_request_invalid_endpoint():
    """Test _prepare_request with invalid endpoint. Expect WeatherAPIError."""
    client = WeatherAPIClient()
    with pytest.raises(WeatherAPIError, match="Invalid or missing API endpoint"):
        client._prepare_request("invalid", {"q": "Kyiv"})

def test_prepare_request_missing_q_param():
    """Test _prepare_request with missing required 'q' parameter. Expect WeatherAPIError."""
    client = WeatherAPIClient()
    with pytest.raises(WeatherAPIError, match="Missing required parameter"):
        client._prepare_request("current", {})

