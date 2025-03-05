from django.db import models


class WeatherData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    lat = models.FloatField()
    lon = models.FloatField()

    temperature = models.FloatField(help_text="Temperature (°C)")
    feels_like = models.FloatField(help_text="Feels-like temperature (°C)")
    humidity = models.IntegerField(help_text="Relative humidity (%)")
    pressure = models.FloatField(help_text="Atmospheric pressure (mbar)")
    precipitation = models.FloatField(help_text="Precipitation amount (mm)", default=0.0)
    dew_point = models.FloatField(help_text="Dew point (°C)", null=True, blank=True)

    wind = models.OneToOneField('WindData', on_delete=models.CASCADE, related_name='weather_data')
    condition = models.OneToOneField('WeatherCondition', on_delete=models.CASCADE, related_name='weather_data')

    def __str__(self):
        return f"{self.timestamp} - {self.city}: {self.temperature}°C"


class WindData(models.Model):
    wind_speed = models.FloatField(help_text="Wind speed (km/h)")
    wind_gust = models.FloatField(help_text="Wind gusts (km/h)", null=True, blank=True)
    wind_direction = models.CharField(max_length=10, help_text="Wind direction (ENE, N, SW, etc.)")
    wind_degree = models.IntegerField(help_text="Wind direction in degrees (0° - North, 90° - East)")

    def __str__(self):
        return f"Wind: {self.wind_speed} km/h, {self.wind_direction}"


class WeatherCondition(models.Model):
    weather_condition = models.CharField(max_length=100, help_text="Weather description (Clear, Rain, Fog, etc.)")
    weather_icon = models.URLField(help_text="URL of the weather condition icon")
    cloudiness = models.IntegerField(help_text="Cloud cover (%)")
    visibility = models.FloatField(help_text="Visibility (km)")
    uv_index = models.FloatField(help_text="UV index (sun exposure risk)")

    def __str__(self):
        return f"Condition: {self.weather_condition}, Cloudiness: {self.cloudiness}%"

