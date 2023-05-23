#!/usr/bin/env bash
python manage.py makemigrations --noinput
python manage.py migrate --run-syncdb

python ./manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('$ADMIN_USERNAME', '$ADMIN_EMAIL', '$ADMIN_PASSWORD')"

# python ./manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'test@admin.es', 'admin')"

# gunicorn DjangoAPI.wsgi:application --bind 0.0.0.0:8540 --timeout 0 --log-level info

daphne -b 0.0.0.0 -p 8540 -t 0 DjangoAPI.asgi:application