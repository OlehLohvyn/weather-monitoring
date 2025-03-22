from django.contrib import admin
from weather.models import WeatherCondition, WeatherData, WindData


class WeatherDataAdmin(admin.ModelAdmin):
    """Custom admin configuration for the WeatherData model."""

    list_display = (
        'timestamp', 'city', 'country', 'lat', 'lon',
        'temperature', 'feels_like', 'humidity', 'pressure',
        'wind_speed', 'wind_gust', 'wind_direction', 'wind_degree',
        'cloudiness', 'visibility', 'precipitation', 'uv_index',
        'weather_condition'
    )

    list_filter = (
        'city', 'country', 'temperature', 'humidity', 'pressure',
        'wind__wind_speed', 'wind__wind_direction', 'wind__wind_degree',
        'condition__cloudiness', 'condition__uv_index', 'condition__weather_condition'
    )

    def wind_speed(self, obj):
        """Return wind speed from related WindData, if available."""
        return obj.wind.wind_speed if obj.wind else None

    def wind_gust(self, obj):
        """Return wind gust from related WindData, if available."""
        return obj.wind.wind_gust if obj.wind else None

    def wind_direction(self, obj):
        """Return wind direction from related WindData, if available."""
        return obj.wind.wind_direction if obj.wind else None

    def wind_degree(self, obj):
        """Return wind degree from related WindData, if available."""
        return obj.wind.wind_degree if obj.wind else None

    def cloudiness(self, obj):
        """Return cloudiness from related WeatherCondition, if available."""
        return obj.condition.cloudiness if obj.condition else None

    def visibility(self, obj):
        """Return visibility from related WeatherCondition, if available."""
        return obj.condition.visibility if obj.condition else None

    def uv_index(self, obj):
        """Return UV index from related WeatherCondition, if available."""
        return obj.condition.uv_index if obj.condition else None

    def weather_condition(self, obj):
        """Return weather condition description from related WeatherCondition, if available."""
        return obj.condition.weather_condition if obj.condition else None

    wind_speed.admin_order_field = 'wind__wind_speed'
    wind_gust.admin_order_field = 'wind__wind_gust'
    wind_direction.admin_order_field = 'wind__wind_direction'
    wind_degree.admin_order_field = 'wind__wind_degree'
    cloudiness.admin_order_field = 'condition__cloudiness'
    visibility.admin_order_field = 'condition__visibility'
    uv_index.admin_order_field = 'condition__uv_index'
    weather_condition.admin_order_field = 'condition__weather_condition'


# Weather
admin.site.register(WeatherData, WeatherDataAdmin)
admin.site.register(WindData)
admin.site.register(WeatherCondition)
