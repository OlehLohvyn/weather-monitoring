from rest_framework import generics
from .models import WeatherData
from .serializers import WeatherDataSerializer


class WeatherDataListCreate(generics.ListCreateAPIView):
    queryset = WeatherData.objects.all().order_by('-timestamp')
    serializer_class = WeatherDataSerializer


