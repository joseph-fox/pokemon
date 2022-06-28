import os

from celery import Celery
from django.conf import settings


if os.environ['ENV'] == settings.PROD:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'pokemon.config.prod')

if os.environ['ENV'] == settings.DEV:
    # It is dev
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'pokemon.config.dev')

celery_app = Celery('service_worker')
celery_app.config_from_object(settings, namespace='CELERY')
celery_app.autodiscover_tasks()
