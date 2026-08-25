"""
forms.py - Django forms for the Courses app.

These forms are used by the ADMIN to create and manage academic data:
    - CourseForm → create/edit courses
    - DepartmentForm → create/edit departments
    - AcademicSessionForm → create/edit academic sessions
    - SemesterForm → create/edit semesters

USED IN:
    - apps/administration/views.py (admin creates/edits these)
    - apps/lecturers/views.py (lecturers may edit course descriptions)
"""

from django import forms
from .models import Course, Department, AcademicSession, Semester


class CourseForm(forms.ModelForm):
    """
    Form for creating/editing a Course.
    Django auto-generates form fields from the Course model's fields.

    The "fields" list controls which model fields appear in the form.
    Fields NOT listed (like created_at, updated_at) are excluded — they're auto-set.
    """
    class Meta:
        model = Course
        fields = ["code", "title", "description", "department", "credit_units", "semester", "lecturer", "max_students"]


class DepartmentForm(forms.ModelForm):
    """Form for creating/editing a Department."""
    class Meta:
        model = Department
        fields = ["name", "code", "description", "head"]


class AcademicSessionForm(forms.ModelForm):
    """Form for creating/editing an Academic Session (e.g., 2025/2026)."""
    class Meta:
        model = AcademicSession
        fields = ["name", "start_date", "end_date", "is_active"]


class SemesterForm(forms.ModelForm):
    """Form for creating/editing a Semester within a session."""
    class Meta:
        model = Semester
        fields = ["session", "name", "start_date", "end_date", "is_active"]
