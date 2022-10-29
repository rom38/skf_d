import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'models_tutor.settings')

app = Celery('models_tutor')
app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.autodiscover_tasks()
