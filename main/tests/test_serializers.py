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


@pytest.mark.django_db
def test_register_serializer_should_pass(user_info):
    serializer = RegisterSerializer(data=user_info)
    assert serializer.is_valid() is True


@pytest.mark.parametrize(
    'data',
    [
        ({'username': None, 'email': None, 'password': None}),
        ({'username': 'John', 'email': 'incorrect.com', 'password': 'MyPass12'}),
        ({'username': 'John', 'email': 'JohnDou@gmail.com', 'password': 'lowPass'}),
     ]
)
@pytest.mark.django_db
def test_register_serializer_should_fail(data):
    serializer = RegisterSerializer(data=data)
    assert serializer.is_valid() is False


@pytest.mark.django_db
def test_duration_serializer_should_pass():
    data = {'duration': 10}
    serializer = SurgeDurationSerializer(data=data)
    assert serializer.is_valid() is True


@pytest.mark.parametrize(
    'duration',
    [
        0,
        1441,
     ]
)
@pytest.mark.django_db
def test_duration_serializer_should_fail(duration):
    data = {'duration': duration}
    serializer = SurgeDurationSerializer(data=data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_threshold_coefficient_serializer_should_pass(threshold):
    serializer = ThresholdCoefficientSerializer(data=threshold)
    assert serializer.is_valid() is True


@pytest.mark.django_db
def test_threshold_coefficient_serializer_should_fail(threshold):
    serializer = ThresholdCoefficientSerializer(data=threshold)
    assert serializer.is_valid() is True
