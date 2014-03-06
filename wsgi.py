import os
import sys

APP_BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Add the app's directory to the PYTHONPATH
sys.path.append(APP_BASE_DIR)
sys.path.append(os.path.join(APP_BASE_DIR, 'grapher'))
sys.path.append('/var/www/html/xygrapher/src/uqx-xygrapher')
sys.path.append('/var/www/html/xygrapher/src/uqx-xygrapher/xygrapher')


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "grapher.settings")

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()