"""
apps.py - App configuration for the Students app.

This app provides the student-facing experience:
    - Student dashboard (overview of courses, assignments, grades)
    - Course registration/dropping
    - Timetable view
    - Assignment listing and submission
    - Grade viewing
    - GPA calculation

NOTE: This app doesn't define the core data models (courses, assignments, etc.)
— it READS from them. The data lives in the courses and assignments apps.
This app defines student-specific views and the StudentProfile model.
"""

from django.apps import AppConfig


class StudentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.students"
    verbose_name = "Students"
