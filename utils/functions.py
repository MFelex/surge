import re
import requests

from rest_framework.exceptions import NotFound
from django.conf import settings
from django.db import connections
from django.utils.timezone import datetime, timedelta

from utils.connectors import redis_connector
from main.models import RequestDistrict, Threshold


def cache_key_maker(key, key_prefix, version):
    return '{key_prefix}:{key}'.format(
        key_prefix=key_prefix,
        key=key
    )


def find_district_in_address(address: str) -> int:
    try:
        re_object = re.search(r'\d+', address)
        district = int(re_object[0])
    except IndexError:
        raise NotFound('Can not detect district')
    else:
        return district


def find_address_by_lat_lon(lat: float, lon: float,) -> str:
    params = {
        'lat': lat,
        'lon': lon,
        'format': 'json',
        'zoom': '14',
    }

    try:
        res = requests.get(url=settings.NOMINATIM_URL, params=params)
        res.raise_for_status()
        jsonify = res.json()
        address = jsonify['address']['suburb']
    except Exception as e:
        raise NotFound('can not find district')
    else:
        return address


def find_district_by_api(lat: float, lon: float) -> int:
    address = find_address_by_lat_lon(lat, lon)
    district = find_district_in_address(address)
    return district


def find_district_by_database(lat: float, lon: float) -> int:
    conn = connections['default']
    cur = conn.cursor()
    cur.execute(f"""
        SELECT gid
        FROM districts
        WHERE ST_DWithin(ST_SetSRID(ST_POINT({lat}, {lon}),4326)::geography, geometry,0)
        """)
    res = cur.fetchone()
    district = res[0] if res else None
    conn.close()
    return district


def redis_request_key_maker(district: int, minute: int) -> str:
    return f'{settings.CACHE_KEY_PREFIX}:DISTRICT:{district}:MINUTE:{minute}'


def redis_surge_duration_key_maker() -> str:
    return f'{settings.CACHE_KEY_PREFIX}:DURATION'


def set_redis_surge_duration(duration: int) -> None:
    key = redis_surge_duration_key_maker()
    with redis_connector() as red:
        red.set(key, duration)


def get_redis_surge_duration() -> int:
    key = redis_surge_duration_key_maker()
    with redis_connector() as red:
        duration = red.get(key)
    duration = int(duration) if duration else settings.DEFAULT_DURATION
    return duration


def redis_requests(district: int) -> int:
    minute = datetime.now().minute
    key = redis_request_key_maker(district, minute)
    with redis_connector() as red:
        amount = red.incr(key, 1)
    return amount


def get_amount_from_db(district: int, duration: int) -> int:
    dt_duration = datetime.now() - timedelta(minutes=duration)
    db_amount = list(RequestDistrict.objects.filter(
        district=district,
        requested_time__gte=dt_duration,
    ).values_list('requested_count', flat=True))

    total_amount = sum(db_amount) if db_amount else 0
    return total_amount


def district_requests(district: int) -> int:
    redis_amount = redis_requests(district)
    duration = get_redis_surge_duration()
    if duration == 1:
        return redis_amount
    db_amount = get_amount_from_db(district, duration)
    return int(redis_amount + db_amount)


def find_coefficient(request_count: int) -> float:
    threshold = Threshold.objects.filter(
        request_count__lte=request_count
    ).order_by(
        'request_count'
    ).first()
    coefficient = threshold.coefficient if threshold else 1
    return coefficient
