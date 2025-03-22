from weather.services.base_weather_service import BaseWeatherService
from weather.services.weather_factory import WeatherModelFactory


class CurrentWeatherService(BaseWeatherService):
    """Service for getting current weather."""

    def get_weather(self, city: str):
        params = {"key": self.api_client.api_key, "q": city, "aqi": "no"}
        data = self.api_client.fetch_data("current", params)

        if "current" not in data or "location" not in data:
            self.logger.error(f"Missing 'current' or 'location' in API response for city: {city}")
            return {"error": "Failed to fetch current weather"}

        current = data["current"]
        location = data["location"]

        # Валідація критичних полів
        for field in ["temp_c", "pressure_mb", "wind_kph", "vis_km"]:
            if field not in current or current[field] is None:
                self.logger.error(f"Missing critical field '{field}' for city: {city}")
                return {"error": f"Missing field: {field}"}

        wind = WeatherModelFactory.create_wind(current)
        condition = WeatherModelFactory.create_condition(current)

        weather = WeatherModelFactory.create_weather(
            city=location.get("name", "Unknown"),
            data={**location, **current},
            wind=wind,
            condition=condition
        )

        return weather
