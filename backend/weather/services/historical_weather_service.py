import logging

from weather.models import WeatherCondition, WeatherData, WindData
from weather.services.weather_api_client import WeatherAPIClient


class HistoricalWeatherService:
    """Service for retrieving and storing historical weather data."""

    def __init__(self):
        self.api_client = WeatherAPIClient()
        self.logger = logging.getLogger(__name__)  # Logger for tracking errors and info

    def get_history(self, city: str, date: str, hour: int):
        """Retrieves historical weather data and stores it in the database."""

        # Validate hour format
        if not isinstance(hour, int) or hour < 0 or hour > 23:
            self.logger.error(f"Invalid hour format received: {hour}")
            return {"error": "Invalid hour format"}

        try:
            # Check if data already exists
            existing_record = WeatherData.objects.filter(city=city, timestamp__date=date, timestamp__hour=hour).first()
            if existing_record:
                self.logger.info(f"Historical weather data already exists for {city}, {date} {hour}:00")
                return existing_record

            # Fetch data from the API
            params = {"key": self.api_client.api_key, "q": city, "dt": date}
            data = self.api_client.fetch_data("history", params)

            if "forecast" not in data:
                self.logger.error(f"API response does not contain historical data for {city} on {date}.")
                return {"error": "API response does not contain historical data"}

            # Search for the requested date and hour in the API response
            for forecast_day in data["forecast"]["forecastday"]:
                if forecast_day["date"] == date:
                    for hourly_data in forecast_day["hour"]:
                        if int(hourly_data["time"][-5:-3]) == hour:
                            return self._save_to_db(city, hourly_data)

            self.logger.warning(f"Requested date or hour not found in historical data for {city}, {date}, {hour}:00.")
            return {"error": "Requested date or hour not found in historical data"}

        except (ConnectionError, TimeoutError) as e:
            self.logger.error(f"API request failed: {e}")
            return {"error": "Failed to fetch historical weather data"}

    def _save_to_db(self, city: str, data: dict):
        """Stores retrieved historical weather data in the database."""

        # Create WindData entry
        wind = WindData.objects.create(
            wind_speed=data.get("wind_kph"),
            wind_gust=data.get("gust_kph"),
            wind_direction=data.get("wind_dir"),
            wind_degree=data.get("wind_degree")
        )

        # Create WeatherCondition entry
        condition = WeatherCondition.objects.create(
            weather_condition=data.get("condition", {}).get("text"),
            weather_icon=f"https:{data.get('condition', {}).get('icon')}" if data.get("condition") else None,
            cloudiness=data.get("cloud"),
            visibility=data.get("vis_km"),
            uv_index=data.get("uv")
        )

        # Create WeatherData entry (historical record)
        weather = WeatherData.objects.create(
            city=city,
            country=data.get("country", "Unknown"),
            lat=data.get("lat", 0.0),
            lon=data.get("lon", 0.0),
            temperature=data.get("temp_c"),
            feels_like=data.get("feelslike_c"),
            humidity=data.get("humidity"),
            pressure=data.get("pressure_mb"),
            precipitation=data.get("precip_mm"),
            dew_point=data.get("dewpoint_c"),
            wind=wind,
            condition=condition
        )

        self.logger.info(f"Saved historical weather data for {city}, {data.get('time')}")
        return weather
