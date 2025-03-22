"""Factory class for creating weather models from API input."""

from weather.models import WeatherCondition, WeatherData, WindData


class WeatherModelFactory:
    """Factory for creating instances of weather-related models."""
    @staticmethod
    def create_wind(data: dict) -> WindData:
        """
        Create a WindData instance from API data.

        Args:
            data (dict): A dictionary containing wind information.

        Returns:
            WindData: A saved WindData instance.
        """
        return WindData.objects.create(
            wind_speed=data.get("wind_kph"),
            wind_gust=data.get("gust_kph"),
            wind_direction=data.get("wind_dir"),
            wind_degree=data.get("wind_degree")
        )

    @staticmethod
    def create_condition(data: dict) -> WeatherCondition:
        """
        Create a WeatherCondition instance from API data.

        Args:
            data (dict): A dictionary containing weather condition information.

        Returns:
            WeatherCondition: A saved WeatherCondition instance.
        """
        condition_data = data.get("condition", {})
        return WeatherCondition.objects.create(
            weather_condition=condition_data.get("text", "Unknown"),
            weather_icon=f"https:{condition_data.get('icon', '')}" if condition_data else None,
            cloudiness=data.get("cloud"),
            visibility=data.get("vis_km"),
            uv_index=data.get("uv")
        )

    @staticmethod
    def create_weather(city: str, data: dict, wind: WindData, condition: WeatherCondition) -> WeatherData:
        """
        Create a WeatherData instance from full weather information.

        Args:
            city (str): Name of the city.
            data (dict): A dictionary containing weather data.
            wind (WindData): Related WindData instance.
            condition (WeatherCondition): Related WeatherCondition instance.

        Returns:
            WeatherData: A saved WeatherData instance.
        """
        return WeatherData.objects.create(
            city=city,
            country=data.get("country", "Unknown"),
            lat=data.get("lat", 0.0),
            lon=data.get("lon", 0.0),
            temperature=data.get("temp_c"),
            feels_like=data.get("feelslike_c"),
            humidity=data.get("humidity"),
            pressure=data.get("pressure_mb"),
            precipitation=data.get("precip_mm"),
            dew_point=data.get("dewpoint_c") if "dewpoint_c" in data else None,
            wind=wind,
            condition=condition
        )
