from weather.models import WindData, WeatherCondition, WeatherData


class WeatherModelFactory:
    @staticmethod
    def create_wind(data: dict) -> WindData:
        return WindData.objects.create(
            wind_speed=data.get("wind_kph"),
            wind_gust=data.get("gust_kph"),
            wind_direction=data.get("wind_dir"),
            wind_degree=data.get("wind_degree")
        )

    @staticmethod
    def create_condition(data: dict) -> WeatherCondition:
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
