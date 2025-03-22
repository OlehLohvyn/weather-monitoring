from unittest.mock import Mock, patch

import pytest
from requests import RequestException
from tests.conftest import mock_current_weather_response_json
from weather.services.exceptions import WeatherAPIError
from weather.services.weather_api_client import WeatherAPIClient


# Tests prepare_request
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


# Tests handle_response
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



# Tests fetch_data
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
