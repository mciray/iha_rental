from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
from datetime import timedelta


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rental.settings')

app = Celery('rental')

app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.enable_utc = False

app.conf.update(timezone='Europe/Istanbul')

app.conf.beat_schedule = {
    'control_is_car_valid': {
        'task': 'rent_app.tasks.has_iha_rented',
        'schedule': timedelta(minutes=20),
    },

    'send_mail_to_valid_cars': {
        'task': 'rent_app.tasks.iha_is_valid',
        'schedule': timedelta(hours=6),
    },
    'my-scheduled-task-every-15-minutes': {
        'task': 'rent_app.views.is_valid_rental_view',
        'schedule': timedelta(minutes=15),
    },
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')