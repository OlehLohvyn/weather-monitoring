from django.contrib import admin
from .models import WeatherData, WindData, WeatherCondition


class WeatherDataAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp', 'city', 'country', 'lat', 'lon',
        'temperature', 'feels_like', 'humidity', 'pressure',
        'wind_speed', 'wind_gust', 'wind_direction', 'wind_degree',
        'cloudiness', 'visibility', 'precipitation', 'uv_index',
        'weather_condition'
    )

    list_filter = ('city', 'country', 'temperature', 'humidity', 'pressure',
                   'wind__wind_speed', 'wind__wind_direction', 'wind__wind_degree',
                   'condition__cloudiness', 'condition__uv_index', 'condition__weather_condition')

    def wind_speed(self, obj):
        return obj.wind.wind_speed if obj.wind else None

    def wind_gust(self, obj):
        return obj.wind.wind_gust if obj.wind else None

    def wind_direction(self, obj):
        return obj.wind.wind_direction if obj.wind else None

    def wind_degree(self, obj):
        return obj.wind.wind_degree if obj.wind else None

    def cloudiness(self, obj):
        return obj.condition.cloudiness if obj.condition else None

    def visibility(self, obj):
        return obj.condition.visibility if obj.condition else None

    def uv_index(self, obj):
        return obj.condition.uv_index if obj.condition else None

    def weather_condition(self, obj):
        return obj.condition.weather_condition if obj.condition else None

    wind_speed.admin_order_field = 'wind__wind_speed'
    wind_gust.admin_order_field = 'wind__wind_gust'
    wind_direction.admin_order_field = 'wind__wind_direction'
    wind_degree.admin_order_field = 'wind__wind_degree'
    cloudiness.admin_order_field = 'condition__cloudiness'
    visibility.admin_order_field = 'condition__visibility'
    uv_index.admin_order_field = 'condition__uv_index'
    weather_condition.admin_order_field = 'condition__weather_condition'


admin.site.register(WeatherData, WeatherDataAdmin)
admin.site.register(WindData)
admin.site.register(WeatherCondition)
