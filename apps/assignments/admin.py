"""
admin.py - Django admin configuration for the Assignments app.

Registers Assignment, Submission, and Grade models in the admin panel.
"""

from django.contrib import admin
from .models import Assignment, Submission, Grade


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    # Columns in the assignment list table
    list_display = ["title", "course", "due_date", "max_score", "created_by"]

    # Sidebar filters
    list_filter = ["course", "due_date"]

    # Search bar searches these fields
    search_fields = ["title", "course__code"]  # course__code traverses: Assignment → Course → code


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ["student", "assignment", "status", "submitted_at"]
    list_filter = ["status"]


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ["submission", "score", "graded_by", "graded_at"]
