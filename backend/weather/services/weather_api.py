import requests
from django.conf import settings
from datetime import datetime, timedelta


import os
import sys
import django


# Adding the project root to Python paths
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Setting the environment variable for Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.app.settings")

# Initializing Django
django.setup()


class WeatherAPIClient:
    """A client for interacting with the WeatherAPI service."""

    BASE_URLS = {
        "current": "https://api.weatherapi.com/v1/current.json",
        "forecast": "https://api.weatherapi.com/v1/forecast.json",
        "history": "https://api.weatherapi.com/v1/history.json",
    }

    def __init__(self):
        self.api_key = settings.WEATHER_API_KEY

    def _fetch_weather_data(self, endpoint: str, params: dict):
        """
        Sends a request to WeatherAPI and returns parsed JSON response.
        """
        url = self.BASE_URLS.get(endpoint)
        if not url:
            return {"error": "Invalid API endpoint"}

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

    def _extract_common_weather_data(self, data: dict):
        """
        Extracts common location information from the API response.
        """
        return {
            "city": data["location"]["name"],
            "country": data["location"]["country"],
            "lat": data["location"]["lat"],
            "lon": data["location"]["lon"],
        }

    def get_current_weather(self, city: str):
        """Fetches real-time weather data for a given city."""
        params = {"key": self.api_key, "q": city, "aqi": "no"}
        data = self._fetch_weather_data("current", params)

        if "current" not in data:
            return {"error": "Failed to fetch current weather", "response": data}

        weather = self._extract_common_weather_data(data)
        current = data["current"]

        weather.update({
            "temperature": current["temp_c"],
            "feels_like": current["feelslike_c"],
            "humidity": current["humidity"],
            "pressure": current["pressure_mb"],
            "wind_speed": current["wind_kph"],
            "wind_gust": current.get("gust_kph", None),
            "wind_direction": current["wind_dir"],
            "wind_degree": current["wind_degree"],
            "cloudiness": current["cloud"],
            "visibility": current["vis_km"],
            "precipitation": current["precip_mm"],
            "uv_index": current["uv"],
            "weather_condition": current["condition"]["text"],
            "weather_icon": f"https:{current['condition']['icon']}",
        })
        return weather

    def get_forecast_weather(self, city: str, date: str, hour: int):
        """Fetches forecast weather for a specific city, date, and hour."""
        today = datetime.utcnow().date()
        max_forecast_date = today + timedelta(days=3)

        if datetime.strptime(date, "%Y-%m-%d").date() > max_forecast_date:
            return {"error": f"Free plan allows only 3-day forecast. Max available date: {max_forecast_date}"}

        params = {"key": self.api_key, "q": city, "days": 3, "aqi": "no", "alerts": "no"}
        data = self._fetch_weather_data("forecast", params)

        if "forecast" not in data:
            return {"error": "API response does not contain forecast data", "response": data}

        for forecast_day in data["forecast"]["forecastday"]:
            if forecast_day["date"] == date:
                for hourly_data in forecast_day["hour"]:
                    if int(hourly_data["time"][-5:-3]) == hour:
                        return {
                            "date": date,
                            "hour": hour,
                            "temperature": hourly_data["temp_c"],
                            "humidity": hourly_data["humidity"],
                            "pressure": hourly_data["pressure_mb"],
                            "wind_speed": hourly_data["wind_kph"],
                            "visibility": hourly_data["vis_km"],
                            "weather_condition": hourly_data["condition"]["text"],
                            "weather_icon": f"https:{hourly_data['condition']['icon']}",
                        }

        return {"error": "Requested date or hour not found in forecast data"}

    def get_historical_weather(self, city: str, date: str, hour: int):
        """Fetches historical weather for a specific city, date, and hour."""
        today = datetime.utcnow().date()
        min_historical_date = today - timedelta(days=7)

        if datetime.strptime(date, "%Y-%m-%d").date() < min_historical_date:
            return {
                "error": f"Free plan allows only last 7 days history. Earliest available date: {min_historical_date}"}

        params = {"key": self.api_key, "q": city, "dt": date}
        data = self._fetch_weather_data("history", params)

        if "forecast" not in data:
            return {"error": "API response does not contain historical data", "response": data}

        for forecast_day in data["forecast"]["forecastday"]:
            if forecast_day["date"] == date:
                for hourly_data in forecast_day["hour"]:
                    if int(hourly_data["time"][-5:-3]) == hour:
                        return {
                            "date": date,
                            "hour": hour,
                            "temperature": hourly_data["temp_c"],
                            "humidity": hourly_data["humidity"],
                            "pressure": hourly_data["pressure_mb"],
                            "wind_speed": hourly_data["wind_kph"],
                            "visibility": hourly_data["vis_km"],
                            "weather_condition": hourly_data["condition"]["text"],
                            "weather_icon": f"https:{hourly_data['condition']['icon']}",
                        }

        return {"error": "Requested date or hour not found in historical data"}


