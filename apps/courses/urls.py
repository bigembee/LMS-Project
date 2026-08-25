"""
urls.py - URL patterns for the Courses app.

URL: /courses/       → course_list (browse all courses)
URL: /courses/5/     → course_detail (view course with id=5)

The <int:pk> syntax is a URL "converter":
    <int:pk> means: capture digits from the URL, convert to integer, pass as "pk" argument
    So /courses/5/ passes pk=5 to the view function

FULL URL CHAIN:
    Browser: /courses/5/
    → lms/urls.py matches "courses/" → passes "5/" to this file
    → this file matches "<int:pk>/" → captures pk=5 → calls course_detail(request, pk=5)
"""

from django.urls import path
from . import views

# Namespace: use "courses:course_list" and "courses:course_detail" in templates and redirects
app_name = "courses"

urlpatterns = [
    # /courses/ → shows the full course catalog
    path("", views.course_list, name="course_list"),

    # /courses/5/ → shows details for course with primary key (id) = 5
    path("<int:pk>/", views.course_detail, name="course_detail"),
]
