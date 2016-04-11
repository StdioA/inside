#!/usr/bin/sh

python manage.py migrate
cat auth_init.py | python manage.py shell
# python manage.py runserver
