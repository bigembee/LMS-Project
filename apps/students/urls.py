"""
urls.py - URL patterns for the Students app.

ALL these URLs are prefixed with /students/ (set in lms/urls.py).
So "dashboard/" here becomes /students/dashboard/ in the full URL.

FULL URL MAP:
    /students/dashboard/          → Student dashboard (home page after login)
    /students/courses/            → List enrolled courses
    /students/courses/register/   → Browse and register for new courses
    /students/timetable/          → View weekly timetable
    /students/assignments/        → View all assignments
    /students/grades/             → View grades and results
    /students/gpa/                → View GPA calculation
"""

from django.urls import path
from . import views

# Namespace: use "students:dashboard", "students:my_courses", etc. in templates and redirects
app_name = "students"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("courses/", views.my_courses, name="my_courses"),
    path("courses/register/", views.register_course, name="register_course"),
    path("timetable/", views.timetable, name="timetable"),
    path("assignments/", views.my_assignments, name="my_assignments"),
    path("grades/", views.my_grades, name="my_grades"),
    path("gpa/", views.gpa, name="gpa"),
]
