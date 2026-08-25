"""
models.py - Student-specific models.

StudentProfile stores extra information specific to students that doesn't belong
in the general User model. Not all users are students, so student-specific fields
(student ID, level, admission date) go here instead of in the User model.

RELATIONSHIP:
    User (accounts app) ←→ StudentProfile (one-to-one)

    A User with role="student" has ONE StudentProfile.
    Access: user.student_profile (thanks to related_name)
    Access reverse: profile.user

HOW IT'S CREATED:
    Option 1: Manually in views when a student registers
    Option 2: Automatically via a signal in apps/accounts/signals.py
              (when a User with role="student" is created, auto-create the profile)
"""

from django.db import models
from django.conf import settings  # For settings.AUTH_USER_MODEL → "accounts.User"


class StudentProfile(models.Model):
    """
    Extra profile information for students.

    DATABASE TABLE: students_studentprofile
    COLUMNS: id, user_id, student_id, department_id, level, admission_date
    """
    # OneToOneField: each User has exactly ONE StudentProfile, and vice versa
    # This is different from ForeignKey (which allows many profiles per user)
    # on_delete=CASCADE: if the User is deleted, delete their profile too
    # related_name="student_profile": access from user → user.student_profile
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile")

    # The student's matric/registration number — unique across all students
    student_id = models.CharField(max_length=20, unique=True)

    # Which department the student belongs to
    # String "courses.Department" avoids circular imports
    department = models.ForeignKey("courses.Department", on_delete=models.SET_NULL, null=True)

    # Academic level: 100 (year 1), 200 (year 2), 300 (year 3), etc.
    level = models.PositiveIntegerField(default=100)

    # When the student was admitted to the school
    admission_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student_id} - {self.user.get_full_name()}"
