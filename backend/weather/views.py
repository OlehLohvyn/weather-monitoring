"""API views for listing and creating weather data entries."""

from rest_framework import viewsets
from .models import WeatherData
from .serializers import WeatherDataSerializer


class WeatherDataViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WeatherDataSerializer

    def get_queryset(self):
        queryset = WeatherData.objects.select_related("wind", "condition").all()

        city = self.request.query_params.get("city")
        if city:
            queryset = queryset.filter(city__iexact=city)

        return queryset.order_by("-timestamp")