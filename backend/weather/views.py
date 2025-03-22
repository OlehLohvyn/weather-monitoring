"""API views for listing and creating weather data entries."""

from rest_framework import generics

from .models import WeatherData
from .serializers import WeatherDataSerializer


class WeatherDataListCreate(generics.ListCreateAPIView):
    """API view for retrieving a list of weather data or creating new entries."""

    queryset = WeatherData.objects.all().order_by('-timestamp')
    serializer_class = WeatherDataSerializer
