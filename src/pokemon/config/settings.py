import os

from envparse import Env
from kombu import Queue

from pokemon.config import secrets

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# This is src/pokemon/config.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Allowed environments.
DEV = 'dev'
PROD = 'prod'

# Unbound envs.
env = Env()

if os.environ.get('ENV') == DEV:
    env = secrets.get_dev_env(os.path.join(BASE_DIR, 'config/envs/.local'))
elif os.environ.get('ENV') in (PROD,):
    env = secrets.get_env()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

SECRET_KEY = env('DJANGO_SECRET_KEY')

# Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',

    # Third party deps.
    'django_extensions',

    # Data layer.
    'pokemon.data',
    'pokemon.data.monsters',

    # Our own packages
    'pokemon.config',
    'pokemon.interfaces.api',
    'pokemon.interfaces.system_jobs',
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

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

# This is /src/pokemon/
_SOURCE_DIR = os.path.dirname(BASE_DIR)

# A list of template directories. They are not packages.
_TEMPLATES = (
    os.path.join(_SOURCE_DIR, 'interfaces/api/templates'),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': _TEMPLATES,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        },
    }
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_URL'),
        'PORT': env('DB_PORT', cast=int),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator'
    },
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.'
                                'PageNumberPagination',
    'PAGE_SIZE': 20
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Import the module for Celery tasks explicitly as it is not registered as a
# Django app.
CELERY_IMPORTS = [
    'pokemon.tasks.monsters.syncs',
]

# Celery broker urls
CELERY_BROKER_URL = env(
    'CELERY_BROKER_URL', default='pyamqp://guest@localhost//')

# Celery task queues
CELERY_TASK_QUEUES = [
    # Task needs to be done ASAP
    Queue('critical_tasks', routing_key='critical'),
]

# Internationalization
LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

# Turn it off to trade for the performance.
# We do not need the translation for now.
USE_I18N = False

# Turn auto localised format off.
USE_L10N = False

# Turn it on, so it always uses the timezone-aware datetime instance.
USE_TZ = True

STATIC_URL = '/static/'

# No auto appending slash.
APPEND_SLASH = True

DEFAULT_LOCALE = 'en-GB'

ROOT_URLCONF = 'pokemon.config.urls'

# WSGI app path.
WSGI_APPLICATION = 'pokemon.config.wsgi.application'

STATICFILES_DIRS = [os.path.join(_SOURCE_DIR, 'static')]

POKEMON_API_BASE_URL = 'https://pokeapi.co/api/v2/'
