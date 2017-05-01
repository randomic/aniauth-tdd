from django.contrib.messages import constants as messages

from .common import *

ALLOWED_HOSTS = SECRETS.get('allowed_hosts', ['localhost'])

DEBUG = True
MESSAGE_LEVEL = messages.DEBUG if DEBUG else messages.INFO

CSRF_COOKIE_SECURE = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_DOMAIN = next(iter(ALLOWED_HOSTS))

DEFAULT_FROM_EMAIL = 'noreply@' + EMAIL_DOMAIN

SERVER_EMAIL = 'root@' + EMAIL_DOMAIN

MEDIA_ROOT = str(DATA_DIR.joinpath('media_root'))

SESSION_COOKIE_SECURE = False

STATIC_ROOT = str(DATA_DIR.joinpath('static_root'))
