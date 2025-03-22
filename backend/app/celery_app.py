"""Celery application configuration for Django project."""

import os
from celery import Celery

# Set Django settings as the configuration source for Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

# Create Celery application
app = Celery("app")

# Load Celery settings from Django's settings module (keys starting with CELERY_)
app.config_from_object("django.conf:settings", namespace="CELERY")

# Automatically discover tasks in all installed Django apps
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """
    A simple debug task to print the request information.

    Args:
        self: The task instance.

    Returns:
        None
    """
    print(f'Request: {self.request!r}')
