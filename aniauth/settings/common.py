# Settings for ANIAuth
import json
import os
from pathlib import Path

from django.contrib.messages import constants as messages

# Utilities
PROJECT_PACKAGE = Path(__file__).resolve().parent.parent

# The full path to the repository root.
BASE_DIR = PROJECT_PACKAGE.parent

data_dir_key = 'ANIAUTH_DATA_DIR'
DATA_DIR = Path(os.environ[data_dir_key]) if data_dir_key in os.environ else BASE_DIR.parent


with DATA_DIR.joinpath('conf', 'secrets.json').open() as handle:
    SECRETS = json.load(handle)


# Django settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR.joinpath('db.sqlite3')),
    }
}

INSTALLED_APPS = [
    'aniauth',
    'logintokens',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LANGUAGE_CODE = 'en-gb'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "simple": {"format": "[%(name)s] %(levelname)s: %(message)s"},
        "full": {"format": "%(asctime)s [%(name)s] %(levelname)s: %(message)s"},
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s',
        },
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
    },
    "loggers": {
        "django.request": {
            "handlers": [],
            "level": "ERROR",
            "propagate": False,
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = LOGIN_REDIRECT_URL

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'logintokens.backends.EmailOnlyAuthenticationBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

MEDIA_URL = '/media/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'aniauth.urls'

ADMINS = [tuple(admin) for admin in SECRETS.get('admins', [])]

SECRET_KEY = str(SECRETS['secret_key'])

SECURE_BROWSER_XSS_FILTER = True

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")

SESSION_COOKIE_HTTPONLY = True

SILENCED_SYSTEM_CHECKS = [
    'security.W004',
    'security.W008',  # SSL redirect is handled by load balancer
]


STATIC_URL = '/static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.ERROR: 'danger',
}

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = True

X_FRAME_OPTIONS = 'DENY'
