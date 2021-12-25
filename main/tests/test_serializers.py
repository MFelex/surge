# pylint: disable=W0613, C0103

import pytest
from main.serializers import *


def test_factor_serializer_should_pass(lat_lon):
    serializer = FactorSerializer(data=lat_lon)
    serializer.is_valid()
    assert 'lat' in serializer.data
    assert 'lon' in serializer.data


@pytest.mark.parametrize(
    'coordinate',
    [
        ({'lat': None, 'lon': None}),
        ({'lat': None, 'lon': 35.123456789}),
        ({'lat': 51.123456789, 'lon': None}),
        ({'lat': 'text', 'lon': 'text'}),
     ]
)
def test_factor_serializer_should_fail(coordinate):
    serializer = FactorSerializer(data=coordinate)
    assert serializer.is_valid() is False


