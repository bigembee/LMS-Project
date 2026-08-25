"""
urls.py - URL patterns for the Lecturers app.

ALL URLs are prefixed with /lecturers/ (set in lms/urls.py).

FULL URL MAP:
    /lecturers/dashboard/                       → Lecturer dashboard
    /lecturers/courses/                         → List courses they teach
    /lecturers/courses/5/manage/                → Manage a specific course
    /lecturers/assignments/create/              → Create a new assignment
    /lecturers/assignments/5/submissions/       → View all submissions for an assignment
    /lecturers/submissions/5/grade/             → Grade a specific submission
    /lecturers/announcements/create/            → Post a new announcement
"""

from django.urls import path
from . import views

app_name = "lecturers"  # Namespace: "lecturers:dashboard", "lecturers:my_courses", etc.

urlpatterns = [
    # Dashboard — lecturer's home page
    path("dashboard/", views.dashboard, name="dashboard"),

    # List all courses this lecturer teaches
    path("courses/", views.my_courses, name="my_courses"),

    # Manage a specific course (view students, assignments)
    # <int:pk> captures the course ID from the URL
    path("courses/<int:pk>/manage/", views.manage_course, name="manage_course"),

    # Create a new assignment
    path("assignments/create/", views.create_assignment, name="create_assignment"),

    # View all student submissions for a specific assignment
    # <int:assignment_id> captures the assignment ID from the URL
    path("assignments/<int:assignment_id>/submissions/", views.view_submissions, name="view_submissions"),

    # Grade a specific student's submission
    # <int:submission_id> captures the submission ID from the URL
    path("submissions/<int:submission_id>/grade/", views.grade_submission, name="grade_submission"),

    # Post a new announcement
    path("announcements/create/", views.post_announcement, name="post_announcement"),
]
