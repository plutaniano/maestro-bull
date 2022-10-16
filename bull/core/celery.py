import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bull.core.settings")
CeleryApp = Celery("maestro")
CeleryApp.config_from_object("bull.core.settings:CELERY")
CeleryApp.autodiscover_tasks()
