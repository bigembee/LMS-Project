"""
apps.py - App configuration for the Accounts app.

Every Django app has an apps.py file. It tells Django:
    - The app's name (must match the path in INSTALLED_APPS in settings.py)
    - Any startup code to run when the app loads

This file is auto-discovered by Django when the app is listed in INSTALLED_APPS.
"""

from django.apps import AppConfig  # Base class for app configuration


class AccountsConfig(AppConfig):
    # The type of auto-generated primary key (id field) for models in this app
    default_auto_field = "django.db.models.BigAutoField"

    # The Python path to this app — must match what's in settings.py INSTALLED_APPS
    # "apps.accounts" means the app is at apps/accounts/
    name = "apps.accounts"

    # Human-readable name shown in Django's admin panel
    verbose_name = "Accounts"

    def ready(self):
        """
        Called once when Django starts up and this app is fully loaded.
        We use it to import signals so they get registered.

        Signals are like event listeners — "when X happens, do Y".
        For example: "when a new User is saved, create their profile automatically".
        They MUST be imported somewhere to work, and ready() is the right place.

        The # noqa: F401 comment tells linters "yes, this import looks unused, but it's intentional"
        """
        import apps.accounts.signals  # noqa: F401
