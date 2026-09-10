"""
admin.py - Django admin configuration for the Courses app.

Registers all course-related models in Django's admin panel at /admin/.
This lets superusers manage departments, sessions, semesters, courses, and enrollments
through a web interface without writing any code.

Each @admin.register decorator:
    1. Makes the model visible in the admin panel
    2. The ModelAdmin class customizes how it looks and behaves
"""

from django.contrib import admin
from .models import Department, AcademicSession, Semester, Course, Enrollment


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    # Columns shown in the department list table
    list_display = ["code", "name", "head"]

    # Search bar searches through these fields
    search_fields = ["name", "code"]


@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = ["name", "start_date", "end_date", "is_active"]

    # Sidebar filter — click to see only active/inactive sessions
    list_filter = ["is_active"]


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ["session", "name", "start_date", "end_date", "is_active"]
    list_filter = ["is_active", "name"]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["code", "title", "department", "lecturer", "credit_units", "semester"]

    # Filter by department or semester on the sidebar
    list_filter = ["department", "semester"]

    # Search by course code or title
    search_fields = ["code", "title"]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ["student", "course", "status", "enrolled_at"]
    list_filter = ["status"]

    # Search by student username or course code
    # The double underscore (student__username) traverses the ForeignKey relationship:
    # Enrollment → student (User) → username
    search_fields = ["student__username", "course__code"]
from .models import Lecture

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ["title", "course", "order", "created_at"]
    list_filter = ["course"]