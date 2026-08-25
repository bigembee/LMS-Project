"""
admin.py - Admin configuration for the Students app.

Registers StudentProfile in the Django admin panel.
Admins can view and manage student profiles (student ID, department, level, etc.)
"""

from django.contrib import admin
from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    # Columns shown in the student profile list
    list_display = ["student_id", "user", "department", "level"]

    # Sidebar filters — filter students by department or level
    list_filter = ["department", "level"]

    # Search bar — search by student ID, first name, or last name
    # user__first_name traverses: StudentProfile → User → first_name
    search_fields = ["student_id", "user__first_name", "user__last_name"]
