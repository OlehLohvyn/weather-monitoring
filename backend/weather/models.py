from django.db import models


class WeatherData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)  # Time of data retrieval

    # Location
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    lat = models.FloatField()  # Latitude
    lon = models.FloatField()  # Longitude

    # Core weather parameters
    temperature = models.FloatField(help_text="Temperature (°C)")
    feels_like = models.FloatField(help_text="Feels-like temperature (°C)")
    humidity = models.IntegerField(help_text="Relative humidity (%)")
    pressure = models.FloatField(help_text="Atmospheric pressure (mbar)")

    # Wind
    wind_speed = models.FloatField(help_text="Wind speed (km/h)")
    wind_gust = models.FloatField(help_text="Wind gusts (km/h)", null=True, blank=True)
    wind_direction = models.CharField(max_length=10, help_text="Wind direction (ENE, N, SW, etc.)")
    wind_degree = models.IntegerField(help_text="Wind direction in degrees (0° - North, 90° - East)")

    # Cloudiness and visibility
    cloudiness = models.IntegerField(help_text="Cloud cover (%)")
    visibility = models.FloatField(help_text="Visibility (km)")

    # Precipitation
    precipitation = models.FloatField(help_text="Precipitation amount (mm)", default=0.0)

    # Additional meteorological parameters
    uv_index = models.FloatField(help_text="UV index (sun exposure risk)")
    dew_point = models.FloatField(help_text="Dew point (°C)")

    # Weather condition
    weather_condition = models.CharField(max_length=100,
                                         help_text="Description of current weather conditions (Clear, Rain, Fog, etc.)")
    weather_icon = models.URLField(help_text="URL of the weather condition icon")

    def __str__(self):
        return f"{self.timestamp} - {self.city}: {self.weather_condition}, {self.temperature}°C"
