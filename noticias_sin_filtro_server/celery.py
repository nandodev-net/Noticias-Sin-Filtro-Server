"""
    Configurations file for celery
"""
import os

# Third party imports
from celery import Celery

# Set settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "noticias_sin_filtro_server.settings")

# Create celery app
app = Celery("noticias_sin_filtro_server")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
