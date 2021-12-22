from celery import shared_task
from django.utils.timezone import datetime, timedelta
from django.conf import settings
from utils.functions import redis_request_key_maker
from main.models import RequestDistrict
from utils.connectors import redis_connector


@shared_task(name='cron_job')
def redis_cron_job():
    request_time = datetime.now().replace(second=0, microsecond=0) - timedelta(minutes=1)
    request_minute = request_time.minute

    for district in range(1, settings.DISTRICT_COUNT+1):
        key = redis_request_key_maker(district, request_minute)
        with redis_connector() as red:
            count = red.get(key)
            red.delete(key)
        if not count:
            continue
        RequestDistrict.objects.create(
            district=district,
            requested_count=count,
            requested_time=request_time,
        )
