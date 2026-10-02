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
from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator


class Department(models.Model):
    """
    Academic department — e.g., Computer Science, Mathematics, English.
    """
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)

    # Points to LecturerProfile (different app) so we get title/specialization directly
    head = models.ForeignKey(
        "lecturers.LecturerProfile",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="headed_departments",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class AcademicSession(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return self.name


class Semester(models.Model):
    class SemesterChoice(models.TextChoices):
        FIRST = "first", "First Semester"
        SECOND = "second", "Second Semester"

    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name="semesters")
    name = models.CharField(max_length=10, choices=SemesterChoice.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ["session", "name"]

    def __str__(self):
        return f"{self.session.name} - {self.get_name_display()}"


class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="courses")
    credit_units = models.PositiveIntegerField(default=3)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="courses")
    lecturer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="courses_taught",
    )
    max_students = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.title}"

    @property
    def enrolled_count(self):
        return self.enrollments.filter(status="enrolled").count()

    @property
    def is_full(self):
        return self.enrolled_count >= self.max_students


class Module(models.Model):
    """A structured unit within a course, e.g. 'Week 1: Introduction'."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.course.code} - {self.name}"


class CourseMaterial(models.Model):
    """A file or link attached to a Module (PDF, slides, video file, external link)."""
    MATERIAL_TYPES = (
        ("pdf", "PDF"),
        ("doc", "Document"),
        ("slide", "Presentation Slide"),
        ("video", "Video Lecture"),
        ("link", "External Link"),
    )
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="materials")
    title = models.CharField(max_length=255)
    material_type = models.CharField(max_length=10, choices=MATERIAL_TYPES)
    file = models.FileField(
        upload_to="course_materials/",
        blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=["pdf", "doc", "docx", "ppt", "pptx", "mp4"])],
    )
    external_url = models.URLField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Lecture(models.Model):
    """A simple standalone video lecture directly under a course (not tied to a Module)."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lectures")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_url = models.URLField(blank=True, help_text="Link to lecture video (e.g. YouTube, Vimeo)")
    order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "created_at"]

    def __str__(self):
        return f"{self.course.code} - {self.title}"


class Enrollment(models.Model):
    class Status(models.TextChoices):
        ENROLLED = "enrolled", "Enrolled"
        DROPPED = "dropped", "Dropped"
        COMPLETED = "completed", "Completed"

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ENROLLED)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    dropped_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ["student", "course"]

    def __str__(self):
        return f"{self.student} - {self.course.code}"
