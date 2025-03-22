@echo off
set PYTHONPATH=.
set DJANGO_SETTINGS_MODULE=app.settings
pylint --load-plugins=pylint_django .
