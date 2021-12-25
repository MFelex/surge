import os
from celery import Celery
from celery.schedules import crontab


# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'surge.settings')

app = Celery('surge')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs
app.autodiscover_tasks()

# Prevent from converting task times into UTC
app.conf.enable_utc = False

app.conf.beat_schedule = {
    "trigger-redis-cron-job": {
        "task": "cron_job",
        "schedule": crontab(minute="*/1")
    }
}
