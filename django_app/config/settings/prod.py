import os
from .base import *

DEBUG = os.environ.get('DJANGO_DEBUG', '') == 'True'
ALLOWED_HOSTS = [os.environ.get('DJANGO_ALLOWED_HOSTS', '*')]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'lostandfound'),
        'USER': os.environ.get('POSTGRES_USER', 'lostfound'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'PORT': os.environ.get('POSTGRES_PORT', 5432),
    }
}
