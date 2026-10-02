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








##"""
##models.py - Database models for the Accounts app.
##
##WHAT ARE MODELS?
##Models are Python classes that define your database tables. Each model = one table.
##Each attribute = one column in that table.
##
##Django's ORM (Object-Relational Mapper) converts these classes into SQL automatically:
##    - "python manage.py makemigrations" → creates migration files (SQL blueprints)
##    - "python manage.py migrate"        → runs those migrations to create/update the actual tables
##
##WHAT THIS FILE DEFINES:
##    - User: A custom user model that extends Django's built-in user with LMS-specific fields.
##      Every person in the system (students, lecturers, admins) is a User.
##
##WHY A CUSTOM USER MODEL?
##    Django's built-in User model only has: username, email, password, first_name, last_name.
##    We need extra fields: role (student/lecturer/admin), phone, profile picture, etc.
##    We extend AbstractUser which gives us ALL the built-in fields PLUS our custom ones.
##
##RELATIONSHIPS TO OTHER MODELS:
##    → StudentProfile (apps/students/models.py) — one-to-one, extra student info
##    → LecturerProfile (apps/lecturers/models.py) — one-to-one, extra lecturer info
##    → Course (apps/courses/models.py) — a lecturer teaches courses (ForeignKey)
##    → Enrollment (apps/courses/models.py) — a student enrolls in courses
##    → Submission (apps/assignments/models.py) — a student submits assignments
##    → Announcement/Message (apps/communication/models.py) — users send/receive messages
##"""
##
##from django.contrib.auth.models import AbstractUser  # Django's user model with auth built in
##from django.db import models                          # Django's ORM — all field types come from here
##
##class Core(models.Model):
##    first_name = models.CharField(max_length=255)
##    last_name = models.CharField(max_length=255)
##    slug = models.SlugField()
##    email = models.EmailField(unique=True)
##    phone = models.CharField(max_length=255)
##    birth_date = models.DateField(null=True)
##    password = models.CharField(max_length=22, min_length=8)
##    #encrypted_key = models.IntegerField()
##    #passwords should not be more than 8 
##    department = models.CharField(max_length=255)
##    sex = models.CharField(max_length=255)
##    year_of_admission = models.IntegerField()
##    membership = models.CharField(max_length=1, choices=ROLE)
##    USERNAME_FIELD = 'email'
##    REQUIRED_FIELD=['username']
##
##
##    def __str__(self):
##        return self.email
##
##
#class User(AbstractUser):
#    """
#    Custom User model for the LMS. Extends Django's AbstractUser.
#
#    INHERITED FIELDS from AbstractUser (you get these for FREE, no need to define them):
#        - username: unique login name
#        - password: hashed password (Django NEVER stores plain text passwords)
#        - email: email address
#        - first_name, last_name: the user's real name
#        - is_active: can this user log in? (True/False)
#        - is_staff: can this user access the Django admin panel?
#        - is_superuser: does this user have ALL permissions?
#        - date_joined: when the account was created
#        - last_login: when they last logged in
#
#    CUSTOM FIELDS (defined below):
#        - role: what type of user they are (student, lecturer, admin)
#        - phone: phone number
#        - profile_picture: uploaded photo
#        - date_of_birth: birthday
#    """
##    STUDENT = "student"
##    LECTURER = "lecturer"
##    ADMIN = "admin"
##    ROLE_CHOICES = [
##        (STUDENT, "Student"),
##        (LECTURER, "Lecturer"),
##        (ADMIN, "Admin"),
##    ]
## 
##    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=STUDENT)
##    phone = models.CharField(max_length=20, blank=True)
##    profile_picture = models.ImageField(
##        upload_to="profile_pictures/", null=True, blank=True
##    )
##    date_of_birth = models.DateField(null=True, blank=True)
## 
##    @property
##    def is_student(self):
##        return self.role == self.STUDENT
## 
##    @property
##    def is_lecturer(self):
##        return self.role == self.LECTURER
## 
##    @property
##    def is_admin_role(self):
##        return self.role == self.ADMIN
## 
##    def __str__(self):
##        return f"{self.username} ({self.get_role_display()})"
#
#
#    # TextChoices creates a set of allowed values for the role field.
#    # This creates a dropdown in forms and validates that only these values are saved.
#    # The database stores the first value ("student"), forms display the second ("Student").
#class Role(models.TextChoices):
#    STUDENT = "student", "Student"      # DB stores "student", display shows "Student"
#    LECTURER = "lecturer", "Lecturer"   # DB stores "lecturer", display shows "Lecturer"
#    ADMIN = "admin", "Admin"            # DB stores "admin", display shows "Admin"
#
#    # CharField = a short text column in the database
#    # max_length=10: maximum 10 characters (enough for "lecturer")
#    # choices=Role.choices: only allow values from the Role enum above
#    # default=Role.STUDENT: new users are students by default
#    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)
#
#    # blank=True: this field is optional in forms (user can leave it empty)
#    phone = models.CharField(max_length=20, blank=True)
#
#    # ImageField: like FileField but validates that the upload is an image
#    # upload_to="profiles/": saves files to media/profiles/ folder
#    # null=True: the database column can be NULL (empty)
#    # blank=True: the field is optional in forms
#    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
#
#    # DateField: stores a date (year-month-day), no time
#    date_of_birth = models.DateField(blank=True, null=True)
#
#    class Meta:
#        # Default ordering when you query User.objects.all()
#        # Users will be sorted by last_name first, then first_name
#        ordering = ["last_name", "first_name"]
#
#    def __str__(self):
#        """
#        String representation of the user. Called when you:
#            - Print a user object: print(user)
#            - Display a user in the admin panel
#            - Show a user in a template: {{ user }}
#            - Display a user in a dropdown (ForeignKey fields)
#
#        get_full_name() returns "first_name last_name" (inherited from AbstractUser)
#        """
#        return f"{self.get_full_name()} ({self.role})"
#
#    # @property turns a method into an attribute — you call user.is_student, not user.is_student()
#    # These are convenience shortcuts used throughout the codebase.
#    @property
#    def is_student(self):
#        """Check if this user is a student. Usage: if user.is_student: ..."""
#        return self.role == self.Role.STUDENT
#
#    @property
#    def is_lecturer(self):
#        """Check if this user is a lecturer. Usage: if user.is_lecturer: ..."""
#        return self.role == self.Role.LECTURER
#
#    @property
#    def is_admin_user(self):
#        """
#        Check if this user is an admin.
#        Named is_admin_user (not is_admin) to avoid conflicting with Django's is_staff.
#        """
#        return self.role == self.Role.ADMIN
#
##
##
##
##    
##    
##    
#class Profile(models.Model):
#    user = models.OneToOneField(
#        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile"
#    )
#    slug = models.SlugField(unique=True, blank=True)
#    phone = models.CharField(max_length=30, blank=True)
#    birth_date = models.DateField(null=True, blank=True)
#    department = models.CharField(max_length=255, blank=True)
#    sex = models.CharField(max_length=10, blank=True)
#    year_of_admission = models.PositiveIntegerField(null=True, blank=True)
#
#    def save(self, *args, **kwargs):
#        if not self.slug:
#            self.slug = slugify(f"{self.user.username}-{self.user_id}")
#        super().save(*args, **kwargs)
#
#    def __str__(self):
#        return self.user.get_full_name() or self.user.username
#
#
#
#
#
##
##from django.conf import settings
##from django.contrib.auth.models import AbstractUser
##from django.db import models
##from django.db.models.signals import post_save
##from django.dispatch import receiver
##from django.utils.text import slugify
##
##
### ---------------------------------------------------------------------------
### USER (login account shared by everyone)
### ---------------------------------------------------------------------------
##class User(AbstractUser):
##    """
##    Custom User model for the LMS. Extends Django's AbstractUser.
##
##    INHERITED FIELDS from AbstractUser (you get these for FREE, no need to define them):
##        - username: unique login name
##        - password: hashed password (Django NEVER stores plain text passwords)
##        - email: email address
##        - first_name, last_name: the user's real name
##        - is_active: can this user log in? (True/False)
##        - is_staff: can this user access the Django admin panel?
##        - is_superuser: does this user have ALL permissions?
##        - date_joined: when the account was created
##        - last_login: when they last logged in
##
##    CUSTOM FIELDS (defined below):
##        - role: what type of user they are (student, lecturer, admin)
##        - phone: phone number
##        - profile_picture: uploaded photo
##        - date_of_birth: birthday
##        - sex: male / female (optional)
##
##    ROLE PROFILES:
##        Each role has its own profile model (Student, Lecturer, AdminProfile)
##        linked to the user. A profile is created automatically when the user
##        is created. Access it with: user.student, user.lecturer, user.adminprofile
##    """
##
##    STUDENT = "student"
##    LECTURER = "lecturer"
##    ADMIN = "admin"
##    ROLE_CHOICES = [
##        (STUDENT, "Student"),
##        (LECTURER, "Lecturer"),
##        (ADMIN, "Admin"),
##    ]
##
##    SEX_CHOICES = [
##        ("M", "Male"),
##        ("F", "Female"),
##    ]
##
##    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=STUDENT)
##    phone = models.CharField(max_length=20, blank=True)
##    profile_picture = models.ImageField(
##        upload_to="profile_pictures/", null=True, blank=True
##    )
##    date_of_birth = models.DateField(null=True, blank=True)
##    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True)
##
##    def save(self, *args, **kwargs):
##        # Superusers created with `createsuperuser` are always admins.
##        if self.is_superuser:
##            self.role = self.ADMIN
##        super().save(*args, **kwargs)
##
##    @property
##    def is_student(self):
##        return self.role == self.STUDENT
##
##    @property
##    def is_lecturer(self):
##        return self.role == self.LECTURER
##
##    @property
##    def is_admin_role(self):
##        return self.role == self.ADMIN
##
##    def __str__(self):
##        return f"{self.username} ({self.get_role_display()})"
##
##
### ---------------------------------------------------------------------------
### ROLE PROFILES
### ---------------------------------------------------------------------------
##class BaseProfile(models.Model):
##    """
##    Abstract base shared by every role profile (no table is created for it).
##    Holds the link to the User plus fields every role has.
##    """
##
##    user = models.OneToOneField(
##        settings.AUTH_USER_MODEL,
##        on_delete=models.CASCADE,
##        related_name="%(class)s",  # user.student / user.lecturer / user.adminprofile
##    )
##    slug = models.SlugField(unique=True, blank=True)
##    department = models.CharField(max_length=255, blank=True)
##    created_at = models.DateTimeField(auto_now_add=True)
##    updated_at = models.DateTimeField(auto_now=True)
##
##    class Meta:
##        abstract = True
##
##    def save(self, *args, **kwargs):
##        if not self.slug:
##            self.slug = slugify(f"{self.user.username}-{self.user_id}")
##        super().save(*args, **kwargs)
##
##    def __str__(self):
##        return self.user.get_full_name() or self.user.username
##
##
##class Student(BaseProfile):
##    """Extra details that only students have."""
##
##    year_of_admission = models.PositiveIntegerField(null=True, blank=True)
##
##
##class Lecturer(BaseProfile):
##    """Extra details that only lecturers have."""
##
##    staff_id = models.CharField(max_length=30, unique=True, null=True, blank=True)
##    title = models.CharField(max_length=30, blank=True)  # e.g. Dr., Prof.
##    office = models.CharField(max_length=100, blank=True)
##
##
##class AdminProfile(BaseProfile):
##    """Extra details that only administrators have."""
##
##    staff_id = models.CharField(max_length=30, unique=True, null=True, blank=True)
##    position = models.CharField(max_length=100, blank=True)  # e.g. Registrar
##
##
### ---------------------------------------------------------------------------
### AUTO-CREATE THE MATCHING PROFILE WHEN A USER IS CREATED
### ---------------------------------------------------------------------------
##PROFILE_BY_ROLE = {
##    User.STUDENT: Student,
##    User.LECTURER: Lecturer,
##    User.ADMIN: AdminProfile,
##}
##
##
##@receiver(post_save, sender=User)
##def create_role_profile(sender, instance, created, **kwargs):
##    if created:
##        PROFILE_BY_ROLE[instance.role].objects.get_or_create(user=instance)