#!/usr/bin/env bash
python manage.py makemigrations --noinput
python manage.py migrate --run-syncdb

gunicorn DjangoAPI.wsgi:application --bind 0.0.0.0:8000 --timeout 0
