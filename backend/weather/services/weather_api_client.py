import logging

import requests
from django.conf import settings
from weather.services.exceptions import WeatherAPIError

logger = logging.getLogger(__name__)


class WeatherAPIClient:
    """Client for interacting with WeatherAPI."""

    BASE_URLS = {
        "current": "https://api.weatherapi.com/v1/current.json",
        "forecast": "https://api.weatherapi.com/v1/forecast.json",
        "history": "https://api.weatherapi.com/v1/history.json",
    }

    def __init__(self):
        self.api_key = settings.WEATHER_API_KEY

    def fetch_data(self, endpoint: str, params: dict) -> dict:
        """Public method to fetch data from WeatherAPI."""
        url, full_params = self._prepare_request(endpoint, params)

        try:
            response = requests.get(url, params=full_params, timeout=5)
            response.raise_for_status()
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            msg = f"Request failed: {str(e)}"
            logger.error(f"Request to WeatherAPI failed: {msg}")
            raise WeatherAPIError(msg) from e

    def _prepare_request(self, endpoint: str, params: dict) -> tuple[str, dict]:
        """Validate and build URL + params for the request."""
        if not endpoint or endpoint not in self.BASE_URLS:
            msg = "Invalid or missing API endpoint"
            logger.warning(f"WeatherAPI error: {msg}")
            raise WeatherAPIError(msg)

        if not params or "q" not in params:
            msg = "Missing required parameter(s): q"
            logger.warning(f"WeatherAPI error: {msg}")
            raise WeatherAPIError(msg)

        url = self.BASE_URLS[endpoint]
        full_params = {"key": self.api_key, **params}
        return url, full_params

    def _handle_response(self, response: requests.Response) -> dict:
        """Validate and parse JSON response."""
        data = response.json()
        if "error" in data:
            msg = data["error"].get("message", "Unknown API error")
            logger.warning(f"WeatherAPI error: {msg}")
            raise WeatherAPIError(msg)
        return data
