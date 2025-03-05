from .weather_api_client import WeatherAPIClient

class ForecastWeatherService:
    """Сервіс для отримання прогнозу погоди."""

    def __init__(self):
        self.api_client = WeatherAPIClient()

    def get_forecast(self, city: str, date: str, hour: int):
        """Отримує прогноз погоди для міста на конкретну дату та годину."""
        params = {"key": self.api_client.api_key, "q": city, "days": 3, "aqi": "no", "alerts": "no"}
        data = self.api_client.fetch_data("forecast", params)

        if "forecast" not in data:
            return {"error": "API response does not contain forecast data"}

        for forecast_day in data["forecast"]["forecastday"]:
            if forecast_day["date"] == date:
                for hourly_data in forecast_day["hour"]:
                    if int(hourly_data["time"][-5:-3]) == hour:
                        return hourly_data

        return {"error": "Requested date or hour not found in forecast data"}
