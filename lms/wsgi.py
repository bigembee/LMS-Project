"""
wsgi.py - Web Server Gateway Interface configuration.

WSGI is the standard interface between Python web apps and web servers.
This file is used by production servers like Gunicorn to run your Django app.

HOW IT'S USED:
    Development: You DON'T use this — "python manage.py runserver" uses its own server
    Production:  gunicorn lms.wsgi:application --bind 0.0.0.0:8000

The "application" variable is what the web server calls to handle each HTTP request.
"""

import os
from django.core.wsgi import get_wsgi_application

# Tell Django which settings file to use
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lms.settings")

# Create the WSGI application object — this is what Gunicorn calls for every request
application = get_wsgi_application()
