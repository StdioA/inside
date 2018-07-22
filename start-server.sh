#!/usr/bin/sh
python manage.py collectstatic --no-input
python manage.py migrate
python manage auth_init
python manage.py runserver 0.0.0.0:8000
