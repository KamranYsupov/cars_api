import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('cars_api')
app.config_from_object('django.conf:settings', namespace='CELERY')
