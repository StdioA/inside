#!/usr/bin/sh
python manage.py collectstatic --no-input
python manage.py migrate
echo "import auth_init; auth_init.init(); exit()" | python manage.py shell
python manage.py runserver 0.0.0.0:8000
