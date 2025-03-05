from .weather_api_client import WeatherAPIClient

class HistoricalWeatherService:
    """Сервіс для отримання історичних погодних даних."""

    def __init__(self):
        self.api_client = WeatherAPIClient()

    def get_history(self, city: str, date: str, hour: int):
        """Отримує історичні погодні дані."""
        params = {"key": self.api_client.api_key, "q": city, "dt": date}
        data = self.api_client.fetch_data("history", params)

        if "forecast" not in data:
            return {"error": "API response does not contain historical data"}

        for forecast_day in data["forecast"]["forecastday"]:
            if forecast_day["date"] == date:
                for hourly_data in forecast_day["hour"]:
                    if int(hourly_data["time"][-5:-3]) == hour:
                        return hourly_data

        return {"error": "Requested date or hour not found in historical data"}
