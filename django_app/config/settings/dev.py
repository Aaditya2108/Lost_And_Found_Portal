from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

# We can use SQLite for local dev or hook it up directly to Postgres
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
