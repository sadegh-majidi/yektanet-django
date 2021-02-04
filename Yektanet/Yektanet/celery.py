import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Yektanet.settings')
app = Celery('Yektanet', broker='amqp://localhost')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.timezone = 'UTC'

app.conf.beat_schedule = {
    'save_ad_clicks_last_hour': {
        'task': 'advertiser_management.tasks.count_sum_of_clicks_per_ad_last_hour',
        'schedule': crontab(minute=0),
    },
    'save_ad_views_last_hour': {
        'task': 'advertiser_management.tasks.count_sum_of_views_per_ad_last_hour',
        'schedule': crontab(minute=0),
    },
    'get_ad_clicks_last_day': {
        'task': 'advertiser_management.tasks.get_ad_clicks_last_day',
        'schedule': crontab(minute=2, hour=0),
    },
    'get_ad_views_last_day': {
        'task': 'advertiser_management.tasks.get_ad_views_last_day',
        'schedule': crontab(minute=2, hour=0),
    },
}
