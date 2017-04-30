from django.contrib.messages import constants as messages

from .common import *

ALLOWED_HOSTS = SECRETS.get('allowed_hosts', ['localhost'])

DEBUG = False
MESSAGE_LEVEL = messages.DEBUG if DEBUG else messages.INFO

CSRF_COOKIE_SECURE = True

EMAIL_DOMAIN = next(iter(ALLOWED_HOSTS))

DEFAULT_FROM_EMAIL = 'noreply@' + EMAIL_DOMAIN

SERVER_EMAIL = 'root@{}' + EMAIL_DOMAIN

MEDIA_ROOT = str(DATA_DIR.joinpath('media'))

SESSION_COOKIE_SECURE = True

STATIC_ROOT = str(DATA_DIR.joinpath('static'))
