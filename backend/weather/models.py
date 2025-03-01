from django.db import models


class WeatherData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    humidity = models.FloatField()
    wind_speed = models.FloatField()
    pressure = models.FloatField()
    rainfall = models.FloatField()

    def __str__(self):
        return f"{self.timestamp} - Temp: {self.temperature}°C"
