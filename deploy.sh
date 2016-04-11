#!/usr/bin/sh

python manage.py migrate
echo "import auth_init" | python manage.py shell
# cat create_user.sh | python manage.py shell
# python manage.py runserver
