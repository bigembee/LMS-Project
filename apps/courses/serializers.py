"""
serializers.py - DRF serializers for the Courses app.

These convert Course models to/from JSON for the REST API.

EXAMPLE:
    GET /api/courses/
    [
        {
            "id": 1,
            "code": "CSC 201",
            "title": "Introduction to Python",
            "department": 3,
            "credit_units": 3,
            "semester": 1,
            "lecturer": 7,
            "max_students": 100,
            "enrolled_count": 45
        },
        ...
    ]

NOTE on "__all__":
    fields = "__all__" means "include every field from the model".
    This is convenient but be careful — it includes everything, even fields
    you might not want exposed (like internal IDs or timestamps).
    For production, explicitly list the fields you want.
"""

from rest_framework import serializers
from .models import Department, AcademicSession, Semester, Course, Enrollment


class DepartmentSerializer(serializers.ModelSerializer):
    """Converts Department objects to/from JSON."""
    class Meta:
        model = Department
        fields = "__all__"  # Include all fields: id, name, code, description, head, created_at


class AcademicSessionSerializer(serializers.ModelSerializer):
    """Converts AcademicSession objects to/from JSON."""
    class Meta:
        model = AcademicSession
        fields = "__all__"


class SemesterSerializer(serializers.ModelSerializer):
    """Converts Semester objects to/from JSON."""
    class Meta:
        model = Semester
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """
    Converts Course objects to/from JSON.

    enrolled_count is a @property on the model (not a database field),
    so we must explicitly declare it as a ReadOnlyField for it to appear in the JSON output.
    """
    # ReadOnlyField: reads the value from the model's @property method
    # It's computed, not stored in the DB, so it can only be read — not written
    enrolled_count = serializers.ReadOnlyField()

    class Meta:
        model = Course
        fields = "__all__"


class EnrollmentSerializer(serializers.ModelSerializer):
    """Converts Enrollment objects to/from JSON."""
    class Meta:
        model = Enrollment
        fields = "__all__"
