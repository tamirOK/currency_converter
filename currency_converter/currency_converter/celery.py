from django.conf import settings

from celery import Celery

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'currency_converter.settings')

app = Celery('currency_converter')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
