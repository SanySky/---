"""
Django settings for megano project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
import sys
from pathlib import Path
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", )

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DJANGO_DEBUG", "1") == "1"

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sites",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django_cleanup.apps.CleanupConfig',
    'taggit',
    'banners.apps.BannersConfig',
    'accounts.apps.AccountsConfig',
    'shop.apps.ProductsConfig',
    'comparison.apps.ComparisonConfig',
    'discounts.apps.DiscountsConfig',
    'orders.apps.OrdersConfig',
    'payments.apps.PaymentsConfig',
    'django_redis',
]

MIDDLEWARE = [
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
]

if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]

    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

    INTERNAL_IPS = [
        '127.0.0.1',
    ]
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS.append("10.0.2.2")
    INTERNAL_IPS.extend(
        [ip[: ip.rfind(".")] + ".1" for ip in ips]
    )

ROOT_URLCONF = "megano.urls"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'shop.context_processors.categories',
                'shop.context_processors.info_cart',
            ],
        },
    },
]

WSGI_APPLICATION = "megano.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": str(os.getenv("DB_ENGINE")),
        "NAME": str(os.getenv("DB_NAME")),
        "USER": str(os.getenv("DB_USER")),
        "PASSWORD": str(os.getenv("DB_PASS")),
        "HOST": str(os.getenv("DB_HOST")),
        "PORT": str(os.getenv("DB_PORT")),
    }
}

if os.getenv('DATABASE') == 'postgres':
    INSTALLED_APPS += ['django.contrib.postgres',]

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/


TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

if sys.argv[1] == 'runserver':
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = 'media/'

MEDIA_ROOT = BASE_DIR / 'media'

LOCALE_PATHS = [BASE_DIR / 'locale']

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DEFAULT_CACHE_TIME = 24 * 60 * 60

AUTH_USER_MODEL = 'accounts.User'

LANGUAGE_CODE = 'ru'

LANGUAGES = [
    ('en', gettext_lazy('English')),
    ('ru', gettext_lazy('Russian')),
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True


DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Celery and Redis sittings

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = DEFAULT_CACHE_TIME
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

CACHES = {
    "default": {
        'BACKEND': str(os.getenv('CACHES_BACKEND')),
        'LOCATION': str(os.getenv('CACHES_LOCATION')),
    }
}

STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')

SITE_ID=1

LOGOUT_REDIRECT_URL = '/accounts/login/'
