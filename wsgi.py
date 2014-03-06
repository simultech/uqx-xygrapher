import os
import sys

APP_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(APP_BASE_DIR)

os.environ["DJANGO_SETTINGS_MODULE"] = "grapher.settings_production"

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()