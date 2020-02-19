from .common import *


SECRET_KEY = 'secret!'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
ADMIN_URL = 'admin/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
