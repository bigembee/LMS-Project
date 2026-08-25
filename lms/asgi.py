"""
asgi.py - Asynchronous Server Gateway Interface configuration.

ASGI is the newer version of WSGI that supports:
    - Regular HTTP requests (like WSGI)
    - WebSockets (real-time two-way communication, e.g., live chat)
    - Background tasks

You'd use this if you add real-time features like live notifications or chat.
For now, WSGI (wsgi.py) is sufficient for this project.

HOW IT'S USED:
    Production with async: daphne lms.asgi:application
    Or: uvicorn lms.asgi:application
"""

import os
from django.core.asgi import get_asgi_application

# Tell Django which settings file to use
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lms.settings")

# Create the ASGI application object
application = get_asgi_application()
