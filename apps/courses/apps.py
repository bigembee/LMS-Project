"""
apps.py - App configuration for the Courses app.

This app manages the core academic data that MULTIPLE other apps depend on:
    - Departments (e.g., Computer Science, Mathematics)
    - Academic Sessions (e.g., 2025/2026)
    - Semesters (e.g., First Semester of 2025/2026)
    - Courses (e.g., CSC 201 - Introduction to Python)
    - Enrollments (linking students to courses)

Other apps reference these models:
    - students app → reads enrollments, courses for the student dashboard
    - lecturers app → reads courses assigned to a lecturer
    - assignments app → assignments belong to a course
    - administration app → manages all of the above
"""

from django.apps import AppConfig


class CoursesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.courses"       # Python path to this app
    verbose_name = "Courses"    # Display name in the Django admin panel
