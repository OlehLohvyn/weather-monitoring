from django.contrib import admin
from .models import WeatherData


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp', 'city', 'country', 'temperature', 'feels_like',
        'humidity', 'pressure', 'wind_speed', 'wind_gust',
        'wind_direction', 'wind_degree', 'cloudiness',
        'visibility', 'precipitation', 'uv_index', 'dew_point',
        'weather_condition'
    )

    list_filter = ('city', 'timestamp', 'temperature', 'humidity', 'wind_speed', 'cloudiness', 'uv_index')
    search_fields = ('city', 'country', 'weather_condition')
    ordering = ('-timestamp',)
