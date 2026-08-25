"""
serializers.py - DRF serializers for the Assignments app.

These convert Assignment/Submission/Grade objects to/from JSON for the REST API.
"""

from rest_framework import serializers
from .models import Assignment, Submission, Grade


class AssignmentSerializer(serializers.ModelSerializer):
    """API representation of an Assignment."""
    class Meta:
        model = Assignment
        fields = "__all__"


class SubmissionSerializer(serializers.ModelSerializer):
    """API representation of a Submission."""
    class Meta:
        model = Submission
        fields = "__all__"


class GradeSerializer(serializers.ModelSerializer):
    """
    API representation of a Grade.

    The "percentage" field is a @property on the model (computed, not stored in DB),
    so we add it as a ReadOnlyField to include it in the JSON response.
    """
    percentage = serializers.ReadOnlyField()

    class Meta:
        model = Grade
        fields = "__all__"
