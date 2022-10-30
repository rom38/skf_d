import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'models_tutor.settings')

app = Celery('models_tutor')
app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'print_every_5_seconds': {
        'task': 'mc_donalds.tasks.printer',
        'schedule': 5,
        'args': (5,),
    },
    'clear_board_every_minute': {
        'task': 'mc_donalds.tasks.clear_old',
        'schedule': crontab(minute='*/2'),
    },
}
