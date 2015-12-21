"""
Django settings for sport project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from subprocess import check_output
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


import getpass
username = getpass.getuser()
environment = {
    "production": "production.ini",
    "staging": "staging.ini",
    "development": "development.ini"
}
configfile = os.path.join(BASE_DIR, 'sport', 'settings', environment.get(username, "development.ini"))
config = configparser.RawConfigParser()
config.read(configfile)

CURRENT_ENVIRONMENT = config.get('SETTINGS', 'CURRENT_ENVIRONMENT')

CURRENT_VERSION = "v2.1"

configfile_update = os.path.join(BASE_DIR, 'update.ini')
config_update = configparser.RawConfigParser()
config_update.read(configfile_update)

LAST_UPDATE_DATE = config_update.getfloat('UPDATE', 'date')

LAST_UPDATE_STATUS = config_update.get('UPDATE', 'status')

CURRENT_REVISION = check_output(["git", "rev-parse", "HEAD"]).decode('utf8')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY_VALUE = config.get('SETTINGS', 'SECRET_KEY')
if "{UNDEFINED}" == SECRET_KEY_VALUE:
    SECRET_KEY_VALUE = os.environ.get('SECRET_KEY')
SECRET_KEY = SECRET_KEY_VALUE

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.getboolean('SETTINGS', 'DEBUG')

TEMPLATE_DEBUG = config.getboolean('SETTINGS', 'TEMPLATE_DEBUG')

ALLOWED_HOSTS = ['localhost', '127.0.0.1', config.get('SETTINGS', 'ALLOWED_HOSTS')]


# Application definition
INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'suit_redactor',
    # swd apps
    'exercises',
    'commons',
    'community',
    'home',
    'social',
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

#SESSION_COOKIE_SECURE = config.getboolean('SETTINGS', 'SESSION_COOKIE_SECURE')

#CSRF_COOKIE_SECURE = config.getboolean('SETTINGS', 'CSRF_COOKIE_SECURE')

#CSRF_COOKIE_HTTPONLY = config.getboolean('SETTINGS', 'CSRF_COOKIE_HTTPONLY')

#X_FRAME_OPTIONS = config.get('SETTINGS', 'X_FRAME_OPTIONS')

# Database
DATABASE_DEFAULT_PASSWORD = config.get('SETTINGS', 'DATABASE_DEFAULT_PASSWORD')
if "{UNDEFINED}" == DATABASE_DEFAULT_PASSWORD:
    DATABASE_DEFAULT_PASSWORD = os.environ.get('DATABASE_DEFAULT_PASSWORD')

DATABASE_DEFAULT_USER = config.get('SETTINGS', 'DATABASE_DEFAULT_USER')
if "{UNDEFINED}" == DATABASE_DEFAULT_USER:
    DATABASE_DEFAULT_USER = os.environ.get('DATABASE_DEFAULT_USER')

DATABASES = {
    'default': {
        'ENGINE': config.get('SETTINGS', 'DATABASE_DEFAULT_ENGINE'),
        'NAME': config.get('SETTINGS', 'DATABASE_DEFAULT_NAME'),
        'HOST': config.get('SETTINGS', 'DATABASE_DEFAULT_HOST'),
        'PASSWORD': DATABASE_DEFAULT_PASSWORD,
        'USER': DATABASE_DEFAULT_USER,
    },
}

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
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

SUIT_CONFIG = {
    'ADMIN_NAME': 'SWD Admin'
}

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
STATIC_URL = config.get('SETTINGS', 'STATIC_URL')
STATICFILES_DIRS = (os.path.join(BASE_DIR, config.get('SETTINGS', 'STATICFILES_DIRS')),)
STATIC_ROOT = config.get('SETTINGS', 'STATIC_ROOT')

# Media (user uploads)
MEDIA_URL = config.get('SETTINGS', 'MEDIA_URL')
MEDIA_ROOT = os.path.join(BASE_DIR, config.get('SETTINGS', 'MEDIA_ROOT'))
