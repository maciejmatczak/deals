from .common import *
from os import environ


SECRET_KEY = 'secret!'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
ADMIN_URL = 'admin/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

if EMAIL_BACKEND == 'django.core.mail.backends.smtp.EmailBackend':
    EMAIL_HOST = environ['DJANGO_EMAIL_HOST']
    EMAIL_USE_TLS = environ['DJANGO_EMAIL_USE_TLS']
    EMAIL_PORT = environ['DJANGO_EMAIL_PORT']
    EMAIL_HOST_USER = environ['DJANGO_EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = environ['DJANGO_EMAIL_HOST_PASSWORD']
