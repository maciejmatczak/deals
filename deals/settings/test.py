from .common import *


SECRET_KEY = 'secret!'
DEBUG = True
ALLOWED_HOSTS = []
ADMIN_URL = 'admin/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
