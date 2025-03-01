from django.contrib import admin
from .models import WeatherData


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'temperature', 'humidity', 'wind_speed', 'pressure', 'rainfall')
    list_filter = ('timestamp', 'temperature', 'humidity', 'pressure')
    search_fields = ('timestamp', 'temperature')
