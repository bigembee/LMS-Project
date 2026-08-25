#!/usr/bin/env python
"""
manage.py - Django's command-line utility for administrative tasks.

This is the ENTRY POINT for your Django project. You run commands through this file like:
    python manage.py runserver      → starts the development server
    python manage.py makemigrations → creates database migration files from model changes
    python manage.py migrate        → applies migrations to the actual database
    python manage.py createsuperuser → creates an admin user
    python manage.py shell          → opens a Python shell with Django loaded

HOW IT WORKS:
1. It tells Django where to find settings (lms/settings.py)
2. It passes your terminal command (like "runserver") to Django's command handler
3. Django then executes whatever command you typed
"""

import os   # os module lets us interact with the operating system (environment variables, file paths)
import sys  # sys module gives access to command-line arguments (sys.argv)


def main():
    # Tell Django which settings file to use. "lms.settings" means lms/settings.py
    # setdefault() only sets it if it's not already set — so environment can override this
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lms.settings")

    try:
        # Import Django's command-line handler
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # If Django isn't installed, show a helpful error message
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # sys.argv is a list like: ["manage.py", "runserver", "8000"]
    # This passes those arguments to Django so it knows what command to run
    execute_from_command_line(sys.argv)


# This block runs only when you execute this file directly (python manage.py ...)
# It does NOT run when this file is imported as a module
if __name__ == "__main__":
    main()
