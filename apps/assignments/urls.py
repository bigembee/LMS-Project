"""
urls.py - URL patterns for the Assignments app.

URL: /assignments/           → list all assignments
URL: /assignments/5/         → view assignment details (pk=5)
URL: /assignments/5/submit/  → submit work for assignment (pk=5)
"""

from django.urls import path
from . import views

app_name = "assignments"  # Namespace: "assignments:assignment_list", "assignments:submit", etc.

urlpatterns = [
    # /assignments/ → list all assignments relevant to the logged-in user
    path("", views.assignment_list, name="assignment_list"),

    # /assignments/5/ → view details for assignment with id=5
    path("<int:pk>/", views.assignment_detail, name="assignment_detail"),

    # /assignments/5/submit/ → submit work for assignment with id=5
    path("<int:pk>/submit/", views.submit_assignment, name="submit"),
]
