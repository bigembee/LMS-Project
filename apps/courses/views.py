"""
views.py - Views for the Courses app.

These are SHARED views — accessible by all authenticated users (students, lecturers, admins).
Role-specific course views are in their respective apps:
    - Students registering for courses → apps/students/views.py
    - Lecturers managing their courses → apps/lecturers/views.py
    - Admins managing all courses      → apps/administration/views.py

THESE VIEWS HANDLE:
    - Browsing the course catalog (all users)
    - Viewing course details (all users)
"""

from django.shortcuts import render                           # Renders HTML templates
from django.contrib.auth.decorators import login_required     # Requires login to access


@login_required  # User must be logged in — if not, redirects to LOGIN_URL (settings.py)
def course_list(request):
    """
    Display a list of all courses, with search and filtering.

    URL: /courses/
    TEMPLATE: courses/course_list.html

    TODO: Implement this:
        courses = Course.objects.select_related("department", "lecturer", "semester")
        # select_related() fetches related objects in ONE query instead of N+1 queries
        # Without it: 1 query for courses + 1 query per course for department + 1 for lecturer...
        # With it: 1 single JOIN query — much faster!
        return render(request, "courses/course_list.html", {"courses": courses})
    """
    return render(request, "courses/course_list.html")


@login_required
def course_detail(request, pk):
    """
    Display details for a single course.

    URL: /courses/5/ (where 5 is the course's primary key/id)
    TEMPLATE: courses/course_detail.html

    The "pk" parameter comes from the URL pattern: path("<int:pk>/", ...)
    <int:pk> means: capture an integer from the URL and pass it as "pk"

    TODO: Implement this:
        course = get_object_or_404(Course, pk=pk)
        # get_object_or_404(): Find the course with this pk.
        # If it doesn't exist, show a 404 page instead of crashing.
        return render(request, "courses/course_detail.html", {"course": course})
    """
    return render(request, "courses/course_detail.html")
