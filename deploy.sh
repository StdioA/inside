#!/usr/bin/sh

python manage.py migrate
# echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'myemail@example.com', 'password')" | python manage.py shell
cat create_user.sh | python manage.py shell
python manage.py runserver
