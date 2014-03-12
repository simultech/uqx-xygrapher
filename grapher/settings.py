"""
Django settings for grapher project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't2$-^drf7(u3b&yfl(lcq$zimas*0h#6di4ly@(wr43w1@l36)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'dev.ceit.uq.edu.au', 'tools.ceit.uq.edu.au', 'uqmarkup.ceit.uq.edu.au']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'xygrapher'
)

# Configuration for XYGrapher

XYGRAPHER_CONFIG_XAXIS = 'My X Axis'
XYGRAPHER_CONFIG_YAXIS = 'My Y Axis'
XYGRAPHER_MIN_X_VALUE = 0
XYGRAPHER_MIN_Y_VALUE = 0
XYGRAPHER_MAX_X_VALUE = 30
XYGRAPHER_MAX_Y_VALUE = 50
XYGRAPHER_SHOWLINES = 'true'
XYGRAPHER_MONGO_COLLECTION = 'xygrapher'
XYGRAPHER_REQUIRES_GRADE = 'false'
XYGRAPHER_MULTIPLE_ATTEMPTS = 'false'
XYGRAPHER_SUBMIT_BUTTON = 'Submit My Values'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'grapher.middleware.http.Http403Middleware'
)

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
#         'LOCATION': '127.0.0.1:11211' # can also be a list of locations
#    }
#}

#SESSION_COOKIE_DOMAIN = 'uqmarkup.ceit.uq.edu.au'
SESSION_COOKIE_DOMAIN = 'tools.ceit.uq.edu.au'
SESSION_ENGINE = 'django.contrib.sessions.backends.file'

ROOT_URLCONF = 'grapher.urls'

WSGI_APPLICATION = 'grapher.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# Templates

TEMPLATES_DIRS = [os.path.join(BASE_DIR,'templates')]