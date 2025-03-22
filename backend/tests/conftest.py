import pytest
from tests.utils.fixtures_loader import load_fixture


@pytest.fixture
def mock_current_weather_response_json():
    """Fixture: returns mock data for current weather response."""
    return load_fixture("mock_current_weather_response.json")


@pytest.fixture
def mock_forecast_weather_response():
    """Fixture: returns mock data for forecast weather response."""
    return load_fixture("mock_forecast_weather_response.json")


@pytest.fixture
def mock_historical_weather_response():
    """Fixture: returns mock data for historical weather response."""
    return load_fixture("mock_historical_weather_response.json")
