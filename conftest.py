import pytest


@pytest.fixture()
def lat_lon():
    return {
        'lat': 51.123456789,
        'lon': 35.123456789,
    }
