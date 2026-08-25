"""
urls.py - URL patterns for the Administration app.

ALL URLs are prefixed with /administration/ (set in lms/urls.py).

FULL URL MAP:
    /administration/dashboard/      → Admin dashboard with analytics
    /administration/students/       → Manage student accounts
    /administration/lecturers/      → Manage lecturer accounts
    /administration/departments/    → Manage departments
    /administration/courses/        → Manage courses
    /administration/enrollments/    → Manage student enrollments
    /administration/sessions/       → Manage academic sessions/semesters
    /administration/analytics/      → View system reports and analytics
"""

from django.urls import path
from . import views

app_name = "administration"  # Namespace: "administration:dashboard", etc.

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("students/", views.manage_students, name="manage_students"),
    path("lecturers/", views.manage_lecturers, name="manage_lecturers"),
    path("departments/", views.manage_departments, name="manage_departments"),
    path("courses/", views.manage_courses, name="manage_courses"),
    path("enrollments/", views.manage_enrollments, name="manage_enrollments"),
    path("sessions/", views.manage_sessions, name="manage_sessions"),
    path("analytics/", views.analytics, name="analytics"),
]
