import pytest


@pytest.fixture()
def lat_lon():
    return {
        'lat': 51.123456789,
        'lon': 35.123456789,
    }


@pytest.fixture()
def user_info():
    return {
        'username': 'John',
        'email': 'JohnDou@gmail.com',
        'password': 'MyPass12',
    }


@pytest.fixture()
def threshold():
    return {
        'request_count': 1000,
        'coefficient': 1.05,
    }
