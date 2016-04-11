#!/usr/bin/sh

python manage.py collectstatic --no-input
# python manage.py migrate
# echo "import auth_init" | python manage.py shell
# cat create_user.sh | python manage.py shell
