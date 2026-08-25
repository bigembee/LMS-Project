"""
admin.py - Django admin panel configuration for the Accounts app.

WHAT IS THE ADMIN PANEL?
Django auto-generates a web-based admin interface at /admin/ that lets you:
    - View, create, edit, and delete database records
    - Search and filter data
    - Manage users and permissions

You access it by:
    1. Creating a superuser: python manage.py createsuperuser
    2. Running the server: python manage.py runserver
    3. Visiting: http://localhost:8000/admin/

HOW IT WORKS:
    - @admin.register(Model) tells Django to show that model in the admin panel
    - The admin class customizes HOW it's displayed (which columns, which filters, etc.)
    - Without registering a model, it won't appear in the admin panel at all

This is SEPARATE from our custom admin dashboard (/administration/).
Django's built-in admin is for developers; our admin dashboard is for school admins.
"""

from django.contrib import admin                                    # Django's admin module
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin    # Default admin for User models
from .models import User                                            # Our custom User model


# @admin.register(User) registers the User model to appear in the admin panel
# It's equivalent to: admin.site.register(User, UserAdmin)
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Customizes how Users appear in the Django admin panel.

    We extend BaseUserAdmin (Django's built-in user admin) because it already handles:
        - Password hashing when creating/editing users
        - Permission management
        - Group management

    We just add our custom fields on top.
    """

    # Columns shown in the user list table at /admin/accounts/user/
    # These are the columns you see when viewing all users
    list_display = ["username", "email", "first_name", "last_name", "role", "is_active"]

    # Sidebar filters on the right side of the user list
    # Click "student" to see only students, "lecturer" for lecturers, etc.
    list_filter = ["role", "is_active", "is_staff"]

    # Fields that the search bar searches through
    # Admin can type "john" and it'll search username, email, first_name, last_name
    search_fields = ["username", "email", "first_name", "last_name"]

    # Add our custom fields to the user edit form
    # BaseUserAdmin.fieldsets contains the default sections (Personal info, Permissions, etc.)
    # We ADD a new section called "LMS Info" with our custom fields
    fieldsets = BaseUserAdmin.fieldsets + (
        ("LMS Info", {"fields": ("role", "phone", "date_of_birth", "profile_picture")}),
    )
