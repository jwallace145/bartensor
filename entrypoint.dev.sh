#!/bin/bash

/venv/bin/python manage.py migrate
/venv/bin/python manage.py collectstatic
/venv/bin/gunicorn website.wsgi:application --bind 0.0.0.0:8000

exec "$@"
