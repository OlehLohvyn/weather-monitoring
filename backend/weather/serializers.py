from rest_framework import serializers
from .models import WeatherData, WindData, WeatherCondition


class WindDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WindData
        fields = [
            "wind_speed",
            "wind_direction",
            "wind_gust",
            "wind_degree"
        ]


class WeatherConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherCondition
        fields = [
            "weather_condition",
            "weather_icon",
            "cloudiness",
            "visibility",
            "uv_index"
        ]


class WeatherDataSerializer(serializers.ModelSerializer):
    wind = WindDataSerializer(read_only=True)
    condition = WeatherConditionSerializer(read_only=True)

    class Meta:
        model = WeatherData
        fields = [
            "id",
            "timestamp",
            "city",
            "country",
            "lat",
            "lon",
            "temperature",
            "feels_like",
            "humidity",
            "pressure",
            "precipitation",
            "dew_point",
            "wind",
            "condition"
        ]
