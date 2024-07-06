import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rent_bike.settings')

app = Celery('rent_bike')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()