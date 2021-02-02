import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Yektanet.settings')
app = Celery('Yektanet')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
