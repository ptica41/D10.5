import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsproject.settings')

app = Celery('newsproject')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_every_30_seconds': {
        'task': 'newsapp.tasks.recieve_mail',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        # 'args': (),
    },
}