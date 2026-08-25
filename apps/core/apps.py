"""
apps.py - App configuration for the Core app.

The Core app provides SHARED utilities used by ALL other apps:
    - AuditLog model: tracks who did what and when
    - TimeStampedModel: abstract base model with created_at/updated_at
    - Permission classes: DRF permissions for the REST API (IsStudent, IsLecturer, etc.)
    - Middleware: audit logging for every request
    - Utility functions: file validation (size, type)
    - Template tags: custom filters for templates (role checking)

Think of this as the "toolbox" — other apps import from here but Core doesn't
import from them.
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
    verbose_name = "Core"
