"""
apps.py - App configuration for the Communication app.

This app handles all communication features:
    - Announcements: broadcast messages (system-wide, role-specific, or course-specific)
    - Notifications: personal alerts (assignment due, grade posted, etc.)
    - Messages: direct messaging between users (student ↔ lecturer)
"""

from django.apps import AppConfig


class CommunicationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.communication"
    verbose_name = "Communication"
