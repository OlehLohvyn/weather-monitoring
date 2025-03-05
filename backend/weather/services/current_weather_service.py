from ..models import WeatherData, WindData, WeatherCondition
from .weather_api_client import WeatherAPIClient

class CurrentWeatherService:
    """Сервіс для отримання поточної погоди."""

    def __init__(self):
        self.api_client = WeatherAPIClient()

    def get_weather(self, city: str):
        """Отримує поточну погоду та зберігає її в базу."""
        params = {"key": self.api_client.api_key, "q": city, "aqi": "no"}
        data = self.api_client.fetch_data("current", params)

        if "current" not in data:
            return {"error": "Failed to fetch current weather"}

        current = data["current"]
        location = data["location"]

        # Створюємо пов’язані моделі
        wind = WindData.objects.create(
            wind_speed=current["wind_kph"],
            wind_gust=current.get("gust_kph", None),
            wind_direction=current["wind_dir"],
            wind_degree=current["wind_degree"]
        )

        condition = WeatherCondition.objects.create(
            weather_condition=current["condition"]["text"],
            weather_icon=f"https:{current['condition']['icon']}",
            cloudiness=current["cloud"],
            visibility=current["vis_km"],
            uv_index=current["uv"]
        )

        # Зберігаємо основну модель WeatherData
        weather = WeatherData.objects.create(
            city=location["name"],
            country=location["country"],
            lat=location["lat"],
            lon=location["lon"],
            temperature=current["temp_c"],
            feels_like=current["feelslike_c"],
            humidity=current["humidity"],
            pressure=current["pressure_mb"],
            precipitation=current["precip_mm"],
            wind=wind,
            condition=condition
        )

        return weather
