from django.db import models


class WeatherData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=100, null=False, blank=False)
    country = models.CharField(max_length=100, null=False, blank=False)
    lat = models.FloatField(null=False, blank=False)
    lon = models.FloatField(null=False, blank=False)

    temperature = models.FloatField(help_text="Temperature (°C)", null=False, blank=False)
    feels_like = models.FloatField(help_text="Feels-like temperature (°C)", null=True, blank=True)
    humidity = models.IntegerField(help_text="Relative humidity (%)", null=True, blank=True)
    pressure = models.FloatField(help_text="Atmospheric pressure (mbar)", null=False, blank=False)
    precipitation = models.FloatField(help_text="Precipitation amount (mm)", null=True, blank=True, default=0.0)
    dew_point = models.FloatField(help_text="Dew point (°C)", null=True, blank=True)

    wind = models.OneToOneField('WindData', on_delete=models.CASCADE, related_name='weather_data', null=False,
                                                                                                        blank=False)
    condition = models.OneToOneField('WeatherCondition', on_delete=models.CASCADE, related_name='weather_data',
                                                                                                null=False, blank=False)

    def __str__(self):
        return f"{self.timestamp} - {self.city}: {self.temperature}°C"


class WindData(models.Model):
    wind_speed = models.FloatField(help_text="Wind speed (km/h)", null=False, blank=False)
    wind_gust = models.FloatField(help_text="Wind gusts (km/h)", null=True, blank=True)
    wind_direction = models.CharField(max_length=10, help_text="Wind direction (ENE, N, SW, etc.)", null=False,
                                                                                                            blank=False)
    wind_degree = models.IntegerField(help_text="Wind direction in degrees (0° - North, 90° - East)", null=True,
                                                                                                            blank=True)

    def __str__(self):
        return f"Wind: {self.wind_speed} km/h, {self.wind_direction}"


class WeatherCondition(models.Model):
    weather_condition = models.CharField(max_length=100, help_text="Weather description (Clear, Rain, Fog, etc.)",
                                                                                             null=False, blank=False)
    weather_icon = models.URLField(help_text="URL of the weather condition icon", null=True, blank=True)
    cloudiness = models.IntegerField(help_text="Cloud cover (%)", null=True, blank=True)
    visibility = models.FloatField(help_text="Visibility (km)", null=False, blank=False)
    uv_index = models.FloatField(help_text="UV index (sun exposure risk)", null=True, blank=True)

    def __str__(self):
        return f"Condition: {self.weather_condition}, Cloudiness: {self.cloudiness}%"
