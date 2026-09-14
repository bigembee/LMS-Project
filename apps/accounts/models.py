"""
models.py - Database models for the Accounts app.

WHAT ARE MODELS?
Models are Python classes that define your database tables. Each model = one table.
Each attribute = one column in that table.

Django's ORM (Object-Relational Mapper) converts these classes into SQL automatically:
    - "python manage.py makemigrations" → creates migration files (SQL blueprints)
    - "python manage.py migrate"        → runs those migrations to create/update the actual tables

WHAT THIS FILE DEFINES:
    - User: A custom user model that extends Django's built-in user with LMS-specific fields.
      Every person in the system (students, lecturers, admins) is a User.

WHY A CUSTOM USER MODEL?
    Django's built-in User model only has: username, email, password, first_name, last_name.
    We need extra fields: role (student/lecturer/admin), phone, profile picture, etc.
    We extend AbstractUser which gives us ALL the built-in fields PLUS our custom ones.

RELATIONSHIPS TO OTHER MODELS:
    → StudentProfile (apps/students/models.py) — one-to-one, extra student info
    → LecturerProfile (apps/lecturers/models.py) — one-to-one, extra lecturer info
    → Course (apps/courses/models.py) — a lecturer teaches courses (ForeignKey)
    → Enrollment (apps/courses/models.py) — a student enrolls in courses
    → Submission (apps/assignments/models.py) — a student submits assignments
    → Announcement/Message (apps/communication/models.py) — users send/receive messages
"""

from django.contrib.auth.models import AbstractUser  # Django's user model with auth built in
from django.db import models                          # Django's ORM — all field types come from here


class User(AbstractUser):
    """
    Custom User model for the LMS. Extends Django's AbstractUser.

    INHERITED FIELDS from AbstractUser (you get these for FREE, no need to define them):
        - username: unique login name
        - password: hashed password (Django NEVER stores plain text passwords)
        - email: email address
        - first_name, last_name: the user's real name
        - is_active: can this user log in? (True/False)
        - is_staff: can this user access the Django admin panel?
        - is_superuser: does this user have ALL permissions?
        - date_joined: when the account was created
        - last_login: when they last logged in

    CUSTOM FIELDS (defined below):
        - role: what type of user they are (student, lecturer, admin)
        - phone: phone number
        - profile_picture: uploaded photo
        - date_of_birth: birthday
    """

    # TextChoices creates a set of allowed values for the role field.
    # This creates a dropdown in forms and validates that only these values are saved.
    # The database stores the first value ("student"), forms display the second ("Student").
    class Role(models.TextChoices):
        STUDENT = "student", "Student"      # DB stores "student", display shows "Student"
        LECTURER = "lecturer", "Lecturer"   # DB stores "lecturer", display shows "Lecturer"
        ADMIN = "admin", "Admin"            # DB stores "admin", display shows "Admin"

    # CharField = a short text column in the database
    # max_length=10: maximum 10 characters (enough for "lecturer")
    # choices=Role.choices: only allow values from the Role enum above
    # default=Role.STUDENT: new users are students by default
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)

    # blank=True: this field is optional in forms (user can leave it empty)
    phone = models.CharField(max_length=20, blank=True)

    # ImageField: like FileField but validates that the upload is an image
    # upload_to="profiles/": saves files to media/profiles/ folder
    # null=True: the database column can be NULL (empty)
    # blank=True: the field is optional in forms
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)

    # DateField: stores a date (year-month-day), no time
    date_of_birth = models.DateField(blank=True, null=True)

    class Meta:
        # Default ordering when you query User.objects.all()
        # Users will be sorted by last_name first, then first_name
        ordering = ["last_name", "first_name"]

    def __str__(self):
        """
        String representation of the user. Called when you:
            - Print a user object: print(user)
            - Display a user in the admin panel
            - Show a user in a template: {{ user }}
            - Display a user in a dropdown (ForeignKey fields)

        get_full_name() returns "first_name last_name" (inherited from AbstractUser)
        """
        return f"{self.get_full_name()} ({self.role})"

    # @property turns a method into an attribute — you call user.is_student, not user.is_student()
    # These are convenience shortcuts used throughout the codebase.
    @property
    def is_student(self):
        """Check if this user is a student. Usage: if user.is_student: ..."""
        return self.role == self.Role.STUDENT

    @property
    def is_lecturer(self):
        """Check if this user is a lecturer. Usage: if user.is_lecturer: ..."""
        return self.role == self.Role.LECTURER

    @property
    def is_admin_user(self):
        """
        Check if this user is an admin.
        Named is_admin_user (not is_admin) to avoid conflicting with Django's is_staff.
        """
        return self.role == self.Role.ADMIN



class Student(models.Model):
    MEMBERSHIP_FRESHMAN = 'F'
    MEMBERSHIP_BACHELOR_OF_SCIENCE = 'BSC'
    MEMBERSHIP_POST_GRADUATE_DIPLOMA ='PGD'
    MEMBERSHIP_MASTER_OF_SCIENCE= 'MSC'
    MEMBERSHIP_MASTER_OF_PHILOSOPHY ='MPHIL'
    MEMBERSHIP_DOCTOR_OF_PHILOSOPHY = 'PHD'
    
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_FRESHMAN, 'Freshman'),
        (MEMBERSHIP_BACHELOR_OF_SCIENCE, 'Bachelor of Science'),
        (MEMBERSHIP_POST_GRADUATE_DIPLOMA, 'Post Graduate Diploma'),
        (MEMBERSHIP_MASTER_OF_SCIENCE, 'Master of Science'),
        (MEMBERSHIP_MASTER_OF_PHILOSOPHY, 'Master of Philosophy'),
        (MEMBERSHIP_DOCTOR_OF_PHILOSOPHY, 'Doctor of Philosophy'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    slug = models.SlugField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    password = models.CharField(max_length=128)
    encrypted_key = models.IntegerField()
    #passwords should not be more than 10 
    membership = models.CharField(max_length=5, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_FRESHMAN)
    
    
