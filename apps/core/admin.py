"""
admin.py - Admin configuration for the Core app.

Registers the AuditLog model in Django's admin panel.
AuditLog entries are READ-ONLY in the admin — admins can view them but not edit them.
This is important because audit logs should be immutable (unchangeable) for integrity.
"""

from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    # Columns shown in the audit log list
    list_display = ["user", "action", "model_name", "timestamp"]

    # Sidebar filters — filter by action type or which model was affected
    list_filter = ["action", "model_name"]

    # Search by username or details text
    search_fields = ["user__username", "details"]

    # ALL fields are read-only — audit logs should never be edited
    # This prevents accidental (or intentional) tampering with the audit trail
    readonly_fields = ["user", "action", "model_name", "object_id", "details", "ip_address", "timestamp"]
