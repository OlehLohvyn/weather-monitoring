"""App configuration for the Weather application."""

from django.apps import AppConfig


class WeatherConfig(AppConfig):
    """Configuration class for the Weather app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weather'
