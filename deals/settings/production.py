from os import environ

from .common import *


DEBUG = False
SECRET_KEY = environ['DJANGO_SECRET_KEY']
ALLOWED_HOSTS = environ['DJANGO_ALLOWED_HOSTS'].split(',')
ADMIN_URL = environ['DJANGO_ADMIN_URL']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = environ['DJANGO_EMAIL_HOST']
EMAIL_USE_TLS = environ['DJANGO_EMAIL_USE_TLS']
EMAIL_PORT = environ['DJANGO_EMAIL_PORT']
EMAIL_HOST_USER = environ['DJANGO_EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = environ['DJANGO_EMAIL_HOST_PASSWORD']
