"""
Django settings for django_odk project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
import json
import socket
from pathlib import Path
from django.contrib import messages
from django.contrib.messages import constants as message_constants

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Import local parameters from JSON file
with open(os.path.join(BASE_DIR, "config/settings.json")) as f:
    local_settings = json.loads(f.read())

def get_local_setting(setting, mysettings=local_settings):
    try:
        return mysettings[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--d2#^9-@4q3j0ejq@o4-(*#p^tfgc_ma%b9)fn)^vfrd3%yly%'
AUTH_USER_MODEL = 'auth.user'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
USE_HTTPS = False
PROJECT_NAME = get_local_setting('PROJECT_NAME')
AVAILABLE_TXT = 'Available form'
SUBMITTED_TXT = 'Submitted form'
ADMINS = [(item[0], item[1]) for item in get_local_setting('ADMINS')]

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]", "10.12.108.3"]

PROTOCOL = 'https' if USE_HTTPS else "http"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap5',
    'odk',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
# DATABASES = get_local_setting('DATABASES')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Europe/Brussels'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = get_local_setting("STATIC_URL")
STATIC_ROOT = get_local_setting("STATIC_ROOT")
MEDIA_URL = get_local_setting("MEDIA_URL")
MEDIA_ROOT = get_local_setting("MEDIA_ROOT")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = get_local_setting('EMAIL_HOST')
EMAIL_PORT = get_local_setting('EMAIL_PORT')
EMAIL_HOST_USER = get_local_setting('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_local_setting('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = get_local_setting('DEFAULT_FROM_EMAIL')
EMAIL_TO = get_local_setting('EMAIL_TO')

# MESSAGE
MESSAGE_LEVEL = message_constants.DEBUG
MESSAGE_LEVEL = 10  # DEBUG
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info', # bleu
    messages.INFO: 'alert-info', # bleu
    messages.SUCCESS: 'alert-success', # vert
    messages.WARNING: 'alert-warning', # jaune
    messages.ERROR: 'alert-danger', # rouge
}


# LOGGING
LOG_DIR = get_local_setting("LOG_DIR")
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['console'],
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'user_filter': {
            '()': 'config.utils.UserLogFilter',
        }
    },
    'formatters': {
        'standard': {
            'format': '{asctime} [{levelname}] [{name}] [{module}.{funcName} linenr: {lineno}]: {message}',
            'style': '{',
        },
        'with_user': {
            'format': '{asctime} [user:{user}] [{name}] [{module}.{funcName} linenr: {lineno}]: {message}',
            'style': '{',
        },
        'simple': {
            'format': '{message}',
            'style': '{',
        },
    },

    'handlers': {
        # Reports the whole request/response report
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        # Simple error message with user concerned in Subject
        'mail_admins_simple': {
            'level': 'ERROR',
            'class': 'config.utils.MailingAdmins',
            'filters': ['require_debug_false', 'user_filter'],
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'default': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'default.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filters': ['user_filter'],
            'filename': os.path.join(LOG_DIR, 'error.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'with_user',
        },
        'warning': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filters': ['user_filter'],
            'filename': os.path.join(LOG_DIR, 'warning.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'with_user',
        },
        'debugger': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'debug.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'info.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'simple',
        },
    },
    'loggers': {
        'mydebug': {
            'handlers': ['debugger'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'odk': {
            'handlers': ['console', 'warning', 'error', 'mail_admins_simple'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['default'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django.template': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}