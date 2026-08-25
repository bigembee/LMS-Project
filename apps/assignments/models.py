"""
models.py - Database models for the Assignments app.

DATA FLOW FOR ASSIGNMENTS:
    1. Lecturer creates an Assignment → linked to a Course
    2. Student creates a Submission → linked to the Assignment and the Student
    3. Lecturer creates a Grade → linked to the Submission

RELATIONSHIPS:
    Course (courses app) ←── Assignment (one course has many assignments)
    Assignment ←── Submission (one assignment has many submissions, one per student)
    Submission ←── Grade (one submission has one grade, via OneToOneField)
    User (lecturer) ←── Assignment.created_by (who created the assignment)
    User (student) ←── Submission.student (who submitted the work)
    User (lecturer) ←── Grade.graded_by (who graded the submission)

DATABASE TABLES:
    assignments_assignment   → stores assignment info
    assignments_submission   → stores student submissions
    assignments_grade        → stores grades/scores
"""

from django.db import models
from django.conf import settings  # For settings.AUTH_USER_MODEL


class Assignment(models.Model):
    """
    An assignment created by a lecturer for a specific course.

    Example: "CSC 201 - Python Project: Build a Calculator"

    DATABASE TABLE: assignments_assignment
    """
    # ForeignKey to Course: this assignment belongs to one course
    # The string "courses.Course" is used instead of importing Course directly
    # This avoids circular import issues when two apps reference each other's models
    # related_name="assignments": from a course → course.assignments.all()
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE, related_name="assignments")

    title = models.CharField(max_length=200)  # e.g., "Python Project: Build a Calculator"
    description = models.TextField()           # Detailed instructions for the assignment

    # FileField: allows file upload. The file is saved to media/assignments/briefs/
    # This could be a PDF with the assignment instructions
    file = models.FileField(upload_to="assignments/briefs/", blank=True, null=True)

    max_score = models.PositiveIntegerField(default=100)  # Maximum possible score (e.g., 100 points)

    # DateTimeField: stores both date AND time (unlike DateField which is date only)
    due_date = models.DateTimeField()  # When the assignment is due

    # Who created this assignment (must be a lecturer)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_assignments",
    )

    created_at = models.DateTimeField(auto_now_add=True)  # Auto-set when created
    updated_at = models.DateTimeField(auto_now=True)      # Auto-updated on every save

    class Meta:
        # Default ordering: most recent due date first (the "-" means descending)
        ordering = ["-due_date"]

    def __str__(self):
        return f"{self.course.code} - {self.title}"


class Submission(models.Model):
    """
    A student's submitted work for an assignment.

    Each student can only submit ONCE per assignment (enforced by unique_together).

    DATABASE TABLE: assignments_submission
    """
    class Status(models.TextChoices):
        SUBMITTED = "submitted", "Submitted"    # Student has submitted, waiting for grading
        GRADED = "graded", "Graded"             # Lecturer has graded it
        RETURNED = "returned", "Returned"       # Lecturer returned it for revision

    # Which assignment this submission is for
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="submissions")

    # Which student submitted this
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="submissions",
    )

    # The actual submitted work — an uploaded file (saved to media/assignments/submissions/)
    file = models.FileField(upload_to="assignments/submissions/")

    # Optional text response (some assignments might accept written answers)
    text_response = models.TextField(blank=True)

    # Current status of the submission
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.SUBMITTED)

    submitted_at = models.DateTimeField(auto_now_add=True)  # When the student submitted
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # A student can only submit ONCE per assignment
        # If they try to submit again, the database raises an IntegrityError
        unique_together = ["assignment", "student"]

    def __str__(self):
        return f"{self.student} - {self.assignment.title}"


class Grade(models.Model):
    """
    A grade/score for a student's submission.

    Uses OneToOneField because each submission can have exactly ONE grade.
    (Unlike ForeignKey which allows many grades per submission)

    DATABASE TABLE: assignments_grade
    """
    # OneToOneField: each submission has exactly one grade, and each grade belongs to one submission
    # related_name="grade": from a submission → submission.grade (not .grade_set.all() like ForeignKey)
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name="grade")

    # DecimalField: for precise numbers (better than FloatField for scores)
    # max_digits=5: total digits (e.g., 100.50 = 5 digits)
    # decimal_places=2: digits after the decimal point
    score = models.DecimalField(max_digits=5, decimal_places=2)

    feedback = models.TextField(blank=True)  # Lecturer's comments/feedback

    # Which lecturer graded this submission
    graded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="grades_given",
    )

    graded_at = models.DateTimeField(auto_now_add=True)  # When it was graded

    def __str__(self):
        return f"{self.submission} - {self.score}"

    @property
    def percentage(self):
        """
        Calculate the score as a percentage of the max possible score.

        Example: score=85, max_score=100 → 85.0%
        Example: score=17, max_score=20  → 85.0%
        """
        if self.submission.assignment.max_score == 0:
            return 0  # Avoid division by zero
        return (self.score / self.submission.assignment.max_score) * 100
