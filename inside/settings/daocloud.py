from . import *
import os

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.environ["MYSQL_PORT_3306_TCP_ADDR"],
        'PORT': os.environ["MYSQL_PORT_3306_TCP_PORT"],
        'NAME': os.environ["MYSQL_INSTANCE_NAME"],
        'USER': os.environ["MYSQL_USERNAME"],
        'PASSWORD': os.environ["MYSQL_PASSWORD"],
    }
}
