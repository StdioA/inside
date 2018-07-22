#!/usr/bin/env sh
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py auth_init

echo "Starting Gunicorn."
exec gunicorn inside.wsgi:application \
    --name inside_app \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --log-level=info \
    --log-file=gunicorn.log \
    --access-logfile=- \
    "$@"
