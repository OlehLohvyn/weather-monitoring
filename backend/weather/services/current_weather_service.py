from ..models import WeatherData, WindData, WeatherCondition
from .weather_api_client import WeatherAPIClient


import logging


class CurrentWeatherService:
    """Сервіс для отримання поточної погоди."""

    def __init__(self):
        self.api_client = WeatherAPIClient()
        self.logger = logging.getLogger(__name__)

    def get_weather(self, city: str):
        """Retrieves current weather and saves it to the database."""
        params = {"key": self.api_client.api_key, "q": city, "aqi": "no"}
        data = self.api_client.fetch_data("current", params)

        if "current" not in data or "location" not in data:
            self.logger.error(f"Missing 'current' or 'location' in API response for city: {city}")
            return {"error": "Failed to fetch current weather"}

        current = data.get("current", {})
        location = data.get("location", {})

        # Ensure critical values exist
        required_fields = ["temp_c", "pressure_mb", "wind_kph", "vis_km"]
        for field in required_fields:
            if field not in current or current[field] is None:
                self.logger.error(f"Critical weather data missing: {field} for city: {city}")
                return {"error": f"Missing critical weather data: {field}"}

        # Create related models
        wind = WindData.objects.create(
            wind_speed=current["wind_kph"],
            wind_gust=current.get("gust_kph"),
            wind_direction=current.get("wind_dir"),
            wind_degree=current.get("wind_degree")
        )

        condition = WeatherCondition.objects.create(
            weather_condition=current.get("condition", {}).get("text", "Unknown"),
            weather_icon=f"https:{current.get('condition', {}).get('icon', '')}" if current.get("condition") else None,
            cloudiness=current.get("cloud"),
            visibility=current["vis_km"],  # This is required, so no .get()
            uv_index=current.get("uv")
        )

        # Save the main WeatherData model
        weather = WeatherData.objects.create(
            city=location.get("name", "Unknown"),
            country=location.get("country", "Unknown"),
            lat=location.get("lat", 0.0),
            lon=location.get("lon", 0.0),
            temperature=current["temp_c"],  # Required
            feels_like=current.get("feelslike_c"),
            humidity=current.get("humidity"),
            pressure=current["pressure_mb"],  # Required
            precipitation=current.get("precip_mm"),
            wind=wind,
            condition=condition
        )

        return weather
