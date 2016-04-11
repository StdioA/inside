#!/usr/bin/sh
python manage.py collectstatic --no-input
python manage.py migrate
echo "import auth_init" | python manage.py shell
python manage.py runserver 0.0.0.0:8000
