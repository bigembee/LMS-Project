"""
models.py - Models for the Administration app.

Currently empty because the admin dashboard doesn't need its own models.
It manages models from OTHER apps:
    - User (accounts app)
    - Course, Department, Enrollment, AcademicSession, Semester (courses app)

If you need admin-specific models in the future (e.g., SystemSettings, AuditReport),
define them here.
"""

from django.db import models
