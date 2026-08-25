"""
apps.py - App configuration for the Lecturers app.

This app provides the lecturer-facing experience:
    - Lecturer dashboard
    - View and manage their assigned courses
    - Create assignments for their courses
    - View student submissions
    - Grade submissions and give feedback
    - Post course announcements

Like the students app, this doesn't own the core data models — it provides
lecturer-specific views that READ/WRITE to models in courses, assignments, and communication apps.
"""

from django.apps import AppConfig


class LecturersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.lecturers"
    verbose_name = "Lecturers"
