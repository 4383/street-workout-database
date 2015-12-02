"""
Django settings for sport project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os.path import expanduser

HOME_DIR = expanduser("~")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

RELEASE_DEPENDENCIES_DIR = os.path.join(HOME_DIR, 'www', 'swd')

SITE_DOMAIN = os.environ.get('SWD_DJANGO_SITE_DOMAIN')

CURRENT_VERSION = "v1.0"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SWD_DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'www.the-street-workout-database.ovh', 'the-street-workout-database.ovh']


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'exercises',
    'commons',
    'community',
    'home',
)


if DEBUG:
    INSTALLED_APPS += ('debug_toolbar',)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'sport.urls'

WSGI_APPLICATION = 'sport.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': os.environ.get("SWD_DJANGO_DATABASE_ENGINE"),
        'NAME': os.path.join(BASE_DIR, os.environ.get("SWD_DJANGO_DATABASE_NAME")),
    },
}

if not DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': os.environ.get("SWD_DJANGO_DATABASE_ENGINE"),
            'NAME': os.path.join(RELEASE_DEPENDENCIES_DIR, os.environ.get("SWD_DJANGO_DATABASE_NAME")),
        },
    }


DIRS = [
    os.path.join(BASE_DIR, 'templates'),
    os.path.join(BASE_DIR, 'exercises', 'templates'),
]

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, 'commons', 'templates'),
                 os.path.join(BASE_DIR, 'exercises', 'templates'),
                 os.path.join(BASE_DIR, 'home', 'templates')]

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.template.context_processors.debug',
    'django.template.context_processors.request',
    'django.template.context_processors.i18n',
    'django.template.context_processors.media',
    'django.template.context_processors.static',
    'django.template.context_processors.tz',
    'django.contrib.messages.context_processors.messages')

# Internationalization
LANGUAGE_CODE = 'en-us'

gettext = lambda s: s
LANGUAGES = (
    ('en', gettext('English')),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
if not DEBUG:
    STATIC_URL = 'http://static.{0}/'.format(SITE_DOMAIN)
    STATIC_ROOT = os.path.join(RELEASE_DEPENDENCIES_DIR, 'static')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
if not DEBUG:
    MEDIA_ROOT = os.path.join(RELEASE_DEPENDENCIES_DIR, 'media')
    MEDIA_URL = 'http://media.{0}/'.format(SITE_DOMAIN)
