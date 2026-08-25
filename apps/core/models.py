"""
models.py - Core models shared across the project.

AuditLog: Tracks all important actions in the system for security and accountability.
TimeStampedModel: An abstract base model that other models can inherit from.

WHAT IS AN ABSTRACT MODEL?
    A model with "class Meta: abstract = True" does NOT create a database table.
    Instead, other models inherit from it to get its fields.

    Example:
        class TimeStampedModel(models.Model):
            created_at = ...
            updated_at = ...
            class Meta:
                abstract = True

        class Announcement(TimeStampedModel):
            title = ...
            # Now Announcement automatically has created_at and updated_at fields
            # WITHOUT a separate TimeStampedModel table in the database
"""

from django.db import models
from django.conf import settings


class AuditLog(models.Model):
    """
    Records important user actions for security and accountability.

    Examples of logged actions:
        - "User john_doe logged in"
        - "User admin1 deleted student #45"
        - "User lecturer1 graded submission #102"

    WHY AUDIT LOGS?
        - Track who changed what and when
        - Debug issues ("who deleted this course?")
        - Security monitoring ("failed login attempts")
        - Compliance requirements

    DATABASE TABLE: core_auditlog

    HOW TO CREATE AN AUDIT LOG ENTRY (from any view):
        AuditLog.objects.create(
            user=request.user,
            action="graded_submission",
            model_name="Submission",
            object_id=submission.id,
            details=f"Graded submission for {submission.assignment.title} - Score: {score}",
            ip_address=request.META.get("REMOTE_ADDR")
        )
    """
    # Who performed the action. SET_NULL because we want to keep the log even if the user is deleted.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    # What action was performed — a short identifier like "login", "create_course", "grade_submission"
    action = models.CharField(max_length=50)

    # Which model/table was affected — e.g., "Course", "Submission", "User"
    model_name = models.CharField(max_length=100)

    # The ID of the specific object that was affected — e.g., Course #5
    object_id = models.PositiveIntegerField(null=True)

    # Free-text details about what happened
    details = models.TextField(blank=True)

    # The IP address of the user when they performed the action
    # GenericIPAddressField: stores both IPv4 (192.168.1.1) and IPv6 addresses
    ip_address = models.GenericIPAddressField(null=True)

    # When the action happened — auto-set to current time
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]  # Newest logs first

    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name} - {self.timestamp}"


class TimeStampedModel(models.Model):
    """
    Abstract base model that adds created_at and updated_at fields.

    OTHER MODELS CAN INHERIT FROM THIS to get timestamps without defining them each time.
    "abstract = True" means this model does NOT create its own database table.

    USAGE:
        class MyModel(TimeStampedModel):
            name = models.CharField(max_length=100)
            # MyModel now automatically has id, name, created_at, updated_at
    """
    created_at = models.DateTimeField(auto_now_add=True)  # Set once when the object is first created
    updated_at = models.DateTimeField(auto_now=True)      # Updated every time .save() is called

    class Meta:
        abstract = True  # CRITICAL: this prevents Django from creating a database table for this model
