"""
admin.py - Admin configuration for the Lecturers app.

Registers LecturerProfile in Django's admin panel so superusers
can manage lecturer details (staff ID, department, title, etc.)
"""

from django.contrib import admin
from .models import LecturerProfile


@admin.register(LecturerProfile)
class LecturerProfileAdmin(admin.ModelAdmin):
    list_display = ["staff_id", "user", "department", "title"]
    list_filter = ["department"]
    # user__first_name: traverses LecturerProfile → User → first_name
    search_fields = ["staff_id", "user__first_name", "user__last_name"]
