"""
apps.py - App configuration for the Assignments app.

This app manages the assignment lifecycle:
    1. Lecturer creates an Assignment for a Course
    2. Students submit their work (Submission)
    3. Lecturer grades the submission (Grade)

MODELS IN THIS APP:
    - Assignment: The task itself (title, description, due date, max score)
    - Submission: A student's submitted work (file upload, text response)
    - Grade: The score and feedback for a submission
"""

from django.apps import AppConfig


class AssignmentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.assignments"
    verbose_name = "Assignments"
