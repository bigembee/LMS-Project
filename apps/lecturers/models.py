"""
models.py - Lecturer-specific models.

LecturerProfile stores extra information specific to lecturers that doesn't belong
in the general User model — staff ID, academic title, specialization, etc.

RELATIONSHIP:
    User (accounts app) ←→ LecturerProfile (one-to-one)
    Access from user: user.lecturer_profile
    Access from profile: profile.user
"""

from django.db import models
from django.conf import settings


class LecturerProfile(models.Model):
    """
    Extra profile information for lecturers.

    DATABASE TABLE: lecturers_lecturerprofile
    COLUMNS: id, user_id, staff_id, department_id, title, specialization
    """
    # OneToOneField: each User has exactly ONE LecturerProfile
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lecturer_profile")

    # Staff ID number — unique identifier for the lecturer
    staff_id = models.CharField(max_length=20, unique=True)

    # Which department the lecturer belongs to
    department = models.ForeignKey("courses.Department", on_delete=models.SET_NULL, null=True)

    # Academic title: "Prof.", "Dr.", "Mr.", "Mrs.", etc.
    title = models.CharField(max_length=50, blank=True)

    # Area of expertise: "Artificial Intelligence", "Database Systems", etc.
    specialization = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.title} {self.user.get_full_name()}"
