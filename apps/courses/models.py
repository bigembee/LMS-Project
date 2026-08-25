"""
models.py - Database models for the Courses app.

THIS IS THE DATA BACKBONE OF THE LMS.
These models define the academic structure that everything else builds on.

DATABASE RELATIONSHIPS (how tables connect):

    Department  ←──── Course (each course belongs to one department)
                ←──── StudentProfile (each student belongs to one department)
                ←──── LecturerProfile (each lecturer belongs to one department)

    AcademicSession ←── Semester (each session has semesters: first, second)

    Semester ←──── Course (each course is offered in a specific semester)

    Course  ←──── Enrollment (students enroll in courses)
            ←──── Assignment (assignments belong to a course)
            ←──── Announcement (course-specific announcements)

    User (lecturer) ←── Course (a lecturer teaches courses)
    User (student)  ←── Enrollment (a student enrolls in courses)

RELATIONSHIP TYPES IN DJANGO:
    ForeignKey     → Many-to-One: Many courses belong to ONE department
    OneToOneField  → One-to-One: Each user has ONE student profile
    ManyToManyField → Many-to-Many: (not used here, but would be like students ↔ courses without Enrollment)
"""

from django.db import models            # All Django model fields
from django.conf import settings        # Access to settings.py — we use settings.AUTH_USER_MODEL


class Department(models.Model):
    """
    Academic department — e.g., Computer Science, Mathematics, English.

    DATABASE TABLE: courses_department
    COLUMNS: id, name, code, description, head_id, created_at
    """
    # CharField: short text. unique=True means no two departments can have the same name.
    name = models.CharField(max_length=200, unique=True)

    # A short code like "CSC", "MTH", "ENG" — unique across all departments
    code = models.CharField(max_length=10, unique=True)

    # TextField: long text with no max length (unlike CharField). blank=True makes it optional.
    description = models.TextField(blank=True)

    # ForeignKey: creates a Many-to-One relationship with User
    # One user can head one department. One department has one head.
    # settings.AUTH_USER_MODEL = "accounts.User" (from settings.py)
    # on_delete=models.SET_NULL: if the head user is deleted, set this field to NULL (don't delete the department!)
    # null=True: allows the database column to be empty
    # blank=True: allows the form field to be empty
    # related_name="headed_department": from a User object, access this with user.headed_department
    head = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="headed_department",
    )

    # DateTimeField with auto_now_add=True: automatically set to the current date/time when created
    # This field is NOT editable — it's set once and never changes
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # String representation: "CSC - Computer Science"
        return f"{self.code} - {self.name}"


class AcademicSession(models.Model):
    """
    An academic year — e.g., "2025/2026 Academic Session".

    Only ONE session should have is_active=True at any time.
    The active session is the "current" school year.

    DATABASE TABLE: courses_academicsession
    COLUMNS: id, name, start_date, end_date, is_active
    """
    name = models.CharField(max_length=50)            # e.g., "2025/2026"
    start_date = models.DateField()                    # When the session starts
    end_date = models.DateField()                      # When the session ends
    is_active = models.BooleanField(default=False)     # Is this the current session?

    class Meta:
        # Default ordering: newest sessions first (the "-" means descending)
        ordering = ["-start_date"]

    def __str__(self):
        return self.name


class Semester(models.Model):
    """
    A semester within an academic session — e.g., "First Semester of 2025/2026".

    Each academic session typically has two semesters.
    Only ONE semester should have is_active=True at any time.

    DATABASE TABLE: courses_semester
    COLUMNS: id, session_id, name, start_date, end_date, is_active
    """
    # TextChoices limits the semester name to "first" or "second"
    class SemesterChoice(models.TextChoices):
        FIRST = "first", "First Semester"
        SECOND = "second", "Second Semester"

    # ForeignKey to AcademicSession: each semester belongs to one session
    # on_delete=models.CASCADE: if the session is deleted, delete its semesters too
    # related_name="semesters": from an AcademicSession object, access semesters with session.semesters.all()
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name="semesters")

    # Which semester this is (first or second)
    name = models.CharField(max_length=10, choices=SemesterChoice.choices)

    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    class Meta:
        # unique_together: no duplicate combinations of session + name
        # You can't have TWO "first" semesters in the same session
        unique_together = ["session", "name"]

    def __str__(self):
        # get_name_display() returns the human-readable label ("First Semester")
        # instead of the stored value ("first")
        return f"{self.session.name} - {self.get_name_display()}"


class Course(models.Model):
    """
    A course offered in the LMS — e.g., "CSC 201 - Introduction to Python".

    This is the central model that ties everything together:
        - Belongs to a Department
        - Offered in a Semester
        - Taught by a Lecturer (User)
        - Students enroll in it (via Enrollment)
        - Has Assignments

    DATABASE TABLE: courses_course
    COLUMNS: id, code, title, description, department_id, credit_units,
             semester_id, lecturer_id, max_students, created_at, updated_at
    """
    code = models.CharField(max_length=20, unique=True)      # e.g., "CSC 201" — unique across all courses
    title = models.CharField(max_length=200)                  # e.g., "Introduction to Python"
    description = models.TextField(blank=True)                # Detailed course description (optional)

    # ForeignKey: this course belongs to one department
    # on_delete=CASCADE: if the department is deleted, delete its courses too
    # related_name="courses": access from department: department.courses.all()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="courses")

    # How many credit units this course is worth (used for GPA calculation)
    # PositiveIntegerField: only allows 0 or positive numbers
    credit_units = models.PositiveIntegerField(default=3)

    # Which semester this course is offered in
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="courses")

    # Which lecturer teaches this course
    # SET_NULL: if the lecturer is deleted, the course stays but lecturer becomes NULL
    lecturer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="courses_taught",
    )

    max_students = models.PositiveIntegerField(default=100)   # Maximum students allowed to enroll

    # auto_now_add=True: set once when created, never changes
    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now=True: updates to current time every time the object is saved
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.title}"

    @property
    def enrolled_count(self):
        """
        Count how many students are currently enrolled in this course.

        self.enrollments = all Enrollment objects for this course
        (available because Enrollment has related_name="enrollments")

        .filter(status="enrolled") = only count active enrollments (not dropped/completed)
        .count() = returns the count as an integer (more efficient than len())
        """
        return self.enrollments.filter(status="enrolled").count()

    @property
    def is_full(self):
        """Check if the course has reached its maximum student capacity."""
        return self.enrolled_count >= self.max_students


class Enrollment(models.Model):
    """
    Links a student to a course — represents "this student is taking this course".

    This is a JOIN TABLE (also called a "through table" or "association table").
    Instead of a ManyToManyField, we use an explicit model so we can add extra fields:
        - status (enrolled, dropped, completed)
        - enrolled_at, dropped_at (timestamps)

    DATABASE TABLE: courses_enrollment
    COLUMNS: id, student_id, course_id, status, enrolled_at, dropped_at
    """
    class Status(models.TextChoices):
        ENROLLED = "enrolled", "Enrolled"       # Currently taking the course
        DROPPED = "dropped", "Dropped"          # Student dropped the course
        COMPLETED = "completed", "Completed"    # Student finished the course

    # ForeignKey to User: which student is enrolled
    # related_name="enrollments": from a user → user.enrollments.all()
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enrollments",
    )

    # ForeignKey to Course: which course they're enrolled in
    # related_name="enrollments": from a course → course.enrollments.all()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ENROLLED)
    enrolled_at = models.DateTimeField(auto_now_add=True)       # When they enrolled
    dropped_at = models.DateTimeField(null=True, blank=True)    # When they dropped (if they did)

    class Meta:
        # A student can only enroll in a course ONCE
        # Trying to create a duplicate will raise an IntegrityError
        unique_together = ["student", "course"]

    def __str__(self):
        return f"{self.student} - {self.course.code}"
