from pathlib import Path
from os import environ
from dotenv import load_dotenv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR.joinpath('settings.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'main.apps.MainConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework_simplejwt',
]

INSTALLED_APPS += [
    'health_check',  # required
    'health_check.db',  # stock Django health checkers
    'health_check.contrib.migrations',
    'health_check.contrib.redis',
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

ROOT_URLCONF = 'surge.urls'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'surge.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': environ.get('DB_SQL_HOST'),
        'PORT': environ.get('DB_SQL_PORT'),
        'NAME': environ.get('DB_DEFAULT_SQL_NAME'),
        'USER': environ.get('DB_SQL_USER'),
        'PASSWORD': environ.get('DB_SQL_PASS'),
    },
}


# Cache
CACHE_KEY_PREFIX = 'SURGE'
REDIS_HOST = environ.get('REDIS_HOST')
REDIS_PORT = environ.get('REDIS_PORT')
REDIS_USER = environ.get('REDIS_USER')
REDIS_PASS = environ.get('REDIS_PASS')
REDIS_URL = f"redis://{environ.get('REDIS_FULL_HOST')}"

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': environ.get('REDIS_FULL_HOST'),
        'KEY_PREFIX': CACHE_KEY_PREFIX,
        'KEY_FUNCTION': 'utils.functions.cache_key_maker',  # use to remove `version` from keys
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'USERNAME': REDIS_USER,
            'PASSWORD': REDIS_PASS,
        },
    }
}


# Broker Configuration
CELERY_BROKER_HOST = environ.get('CELERY_BROKER_HOST')
CELERY_BROKER_PORT = environ.get('CELERY_BROKER_PORT')
CELERY_BROKER_USER = environ.get('CELERY_BROKER_USER')
CELERY_BROKER_PASS = environ.get('CELERY_BROKER_PASS')
CELERY_TASK_DEFAULT_QUEUE = 'surge'
CELERY_BROKER_URL = f'redis://{CELERY_BROKER_HOST}:{CELERY_BROKER_PORT}'

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Global Config
DISTRICT_COUNT = int(environ.get('DISTRICT_COUNT', 22))

# ThirdParty
NOMINATIM_URL = environ.get('NOMINATIM_URL', 'http://nominatim.openstreetmap.org/reverse')
