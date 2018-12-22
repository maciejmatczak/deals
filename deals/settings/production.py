from os import environ

from .common import *


DEBUG = False
SECRET_KEY = environ['DJANGO_SECRET_KEY']
ALLOWED_HOSTS = environ['DJANGO_ALLOWED_HOSTS'].split(',')
ADMIN_URL = environ['DJANGO_ADMIN_URL']
