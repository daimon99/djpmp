"""
Django settings for tjccconfig project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import datetime
import os

from . import config
from . import loggings

VERSION = "1.0.0"

LOGGING = loggings.LOGGING

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.TJHB_DEBUG

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'djpmp',

    # 'simpleui',
    'formadmin',

    'django_dj_plugin',
    'django_bestzhlocale',

    # 'admin_auto_filters',  # https://pypi.org/project/django-admin-autocomplete-filter/

    'openauth',
    'kronos',

    'django_extensions',
    'django_filters',

    'rest_framework',
    'rest_framework.authtoken',

    'corsheaders',

    'custadmin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    'whitenoise.runserver_nostatic',

    'django.contrib.staticfiles',
    'debug_toolbar',

    'mptt',
]

MIDDLEWARE = [
    'django_middleware_global_request.middleware.GlobalRequestMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'config.urls'
# FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'config.context_processors.footer',
            ],
            'debug': True
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': config.DATABASE_URL
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True

USE_L10N = True
USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = ','
NUMBER_GROUPING = 3
from django.conf.locale.zh_Hans import formats

formats.NUMBER_GROUPING = 3

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
# 如果使用 simpleui 主题，尽量不要使用下面的 这个 static storage
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_URL = '/static/'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'EXCEPTION_HANDLER': 'config.exception_handler.exception_handler',
}

JWT_AUTH = {
    # 'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.auth.jwt_response_payload_handler',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=60 * 60 * 24)
}

# https://pypi.org/project/django-cors-headers/
CORS_ORIGIN_ALLOW_ALL = True

# CORS_ORIGIN_WHITELIST = (
#     'http://localhost',
#     'http://127.0.0.1',
# )

# debug tool bar settings
INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]

import django.test.runner


# 单元测试不创建测试数据库
class MyTestRunner(django.test.runner.DiscoverRunner):
    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass


TEST_RUNNER = 'config.settings.MyTestRunner'

FOOTER = "Copyright &copy; 2002-2019 北京太极华保科技股份有限公司 版权所有 (京ICP备09058794号)"
MEDIA_URL = '/upload/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
FILE_UPLOAD_PERMISSIONS = 0o644
# https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-USE_X_FORWARDED_HOST
# https://docs.djangoproject.com/en/3.0/ref/settings/#secure-proxy-ssl-header
# https://gist.github.com/davewongillies/6897161
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/cache_djpmp',
    }
}

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://db138c4cb8f94f43ba7dd5d3d54fe529@sentry.taijihuabao.com/9",
    integrations=[DjangoIntegration()]
)

# Use telegraf to monitor your app health.
TELEGRAF_HOST = 'telegraf'
TELEGRAF_PORT = 8094
TELEGRAF_TAGS = {}

# celery
CELERY_BROKER_URL = config.CELERY_BROKER_URL

# django-openauth
OPENAUTH_JWT_SECRET = config.OPENAUTH_JWT_SECRET
QYWX_LOGIN_URL = config.QYWX_LOGIN_URL
