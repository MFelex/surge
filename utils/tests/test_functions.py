import pytest
import fakeredis
from utils.functions import *


def test_find_districts_in_address_should_pass():
    address = 'منطقه ۵ شهر تهران'
    district = find_district_in_address(address)
    assert district == 5


def test_find_districts_in_address_should_fail():
    address = 'منطقه شهر تهران'
    with pytest.raises(Exception):
        find_district_in_address(address)


def test_find_address_by_lat_lon_should_pass(requests_mock):
    lat = 35.69439
    lon = 51.42151
    response = {
        'place_id': 51159347,
        'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright',
        'osm_type': 'node',
        'osm_id': 4430539193,
        'lat': '35.69439',
        'lon': '51.42151',
        'display_name': 'موبایل, جمهوری اسلامی, فردوسی, منطقه ۱۲ شهر تهران, شهرداری منطقه شش ناحیه یک, شهر تهران'
                        ', بخش مرکزی شهرستان تهران, شهرستان تهران, استان تهران, چاپ گلستانیان, ایران',
        'address': {
            'shop': 'موبایل',
            'road': 'جمهوری اسلامی',
            'neighbourhood': 'فردوسی',
            'suburb': 'منطقه ۱۲ شهر تهران',
            'borough': 'شهرداری منطقه شش ناحیه یک',
            'city': 'شهر تهران',
            'district': 'بخش مرکزی شهرستان تهران',
            'county': 'شهرستان تهران',
            'province': 'استان تهران',
            'postcode': 'چاپ گلستانیان',
            'country': 'ایران',
            'country_code': 'ir'
        },
        'boundingbox': [
            '35.69434',
            '35.69444',
            '51.42146',
            '51.42156'
        ]
    }
    requests_mock.get(settings.NOMINATIM_URL, status_code=200, json=response)
    address = find_address_by_lat_lon(lat=lat, lon=lon)
    assert address == response['address']['suburb']


def test_redis_surge_duration_should_pass(mocker):
    mocker.patch('utils.functions.redis_connector', return_value=fakeredis.FakeStrictRedis())
    duration = get_redis_surge_duration()
    assert duration == settings.DEFAULT_DURATION


def test_redis_requests_should_pass(mocker):
    district = 5
    mocker.patch('utils.functions.redis_connector', return_value=fakeredis.FakeStrictRedis())
    amount = redis_requests(district)
    assert amount == 1


@pytest.mark.django_db
def test_amount_from_db_should_pass(requests_db):
    amount = get_amount_from_db(district=5, duration=10)
    assert amount == requests_db.requested_count


def test_district_requests_should_pass(mocker):
    mocker.patch('utils.functions.redis_requests', return_value=25)
    mocker.patch('utils.functions.get_redis_surge_duration', return_value=10)
    mocker.patch('utils.functions.get_amount_from_db', return_value=75)
    amount = district_requests(district=5)
    assert amount == 100


@pytest.mark.django_db(transaction=True)
def test_find_coefficient_should_pass(coefficient_db):
    coefficient = find_coefficient(coefficient_db.request_count)
    assert coefficient == coefficient_db.coefficient
