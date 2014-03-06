"""
Production Django settings for grapher project.

Changes to the main settings.py file
"""

from settings import *

DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'dev.ceit.uq.edu.au', 'tools.ceit.uq.edu.au', 'uqmarkup.ceit.uq.edu.au']
ADMINS = (
    ('Andrew Dekker', 'uqadekke@uq.edu.au'),
)
MANAGERS = (
    ('Andrew Dekker', 'uqadekke@uq.edu.au'),
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
SESSION_ENGINE = 'django.contrib.sessions.backends.file'
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
#         'LOCATION': '127.0.0.1:11211' # can also be a list of locations
#    }
#}
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATIC_URL = '/xygrapher_static/'
