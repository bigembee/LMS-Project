"""
apps.py - App configuration for the Administration app.

This app provides the admin-facing experience — the school administrator's control panel.
Admins can manage EVERYTHING:
    - Students and lecturers (create, edit, deactivate accounts)
    - Departments and courses
    - Enrollments (add/remove students from courses)
    - Academic sessions and semesters
    - System analytics (how many students, grades distribution, etc.)

NOTE: This is DIFFERENT from Django's built-in admin panel (/admin/).
    - Django's admin (/admin/) = developer tool for database management
    - Our admin dashboard (/administration/) = school admin's user-friendly control panel
"""

from django.apps import AppConfig


class AdministrationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.administration"
    verbose_name = "Administration"
