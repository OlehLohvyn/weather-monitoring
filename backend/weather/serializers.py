"""Serializers for converting WeatherData model instances to and from JSON."""

from rest_framework import serializers
from .models import WeatherData


class WeatherDataSerializer(serializers.ModelSerializer):
    """Serializer for WeatherData model."""

    class Meta:
        model = WeatherData
        fields = '__all__'
