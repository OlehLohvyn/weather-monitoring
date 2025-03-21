import logging

import requests
from django.conf import settings

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

    def fetch_data(self, endpoint: str, params: dict):
        """Sends a request to WeatherAPI and returns the response."""

        # Validate endpoint
        if not endpoint or endpoint not in self.BASE_URLS:
            return {"error": "Invalid or missing API endpoint"}

        # Validate parameters
        if not params or "q" not in params:
            return {"error": "Missing required parameter(s): q"}

        url = self.BASE_URLS[endpoint]
        params = {"key": self.api_key, **params}  # Add API key

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if "error" in data:
                logger.warning(f"WeatherAPI error: {data['error'].get('message', 'Unknown error')}")
                return {"error": data["error"].get("message", "Unknown API error")}

            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Request to WeatherAPI failed: {str(e)}")
            return {"error": f"Request failed: {str(e)}"}
