"""
views.py - Admin-facing views.

ALL views are protected by @admin_required — only users with role="admin" can access them.

THE ADMIN CAN:
    - See system-wide analytics on the dashboard
    - CRUD (Create, Read, Update, Delete) students and lecturers
    - Manage departments and courses
    - Manage enrollments (add/remove students from courses)
    - Manage academic sessions and semesters

These views work with models from OTHER apps:
    - User (accounts)
    - Course, Department, Enrollment, AcademicSession, Semester (courses)
    - StudentProfile (students), LecturerProfile (lecturers)
"""

from django.shortcuts import render
from apps.accounts.decorators import admin_required  # Only admins can access these views


@admin_required
def dashboard(request):
    """
    Admin dashboard — system overview with key statistics.

    URL: /administration/dashboard/

    TODO: Implement with analytics:
        total_students = User.objects.filter(role="student").count()
        total_lecturers = User.objects.filter(role="lecturer").count()
        total_courses = Course.objects.count()
        active_session = AcademicSession.objects.filter(is_active=True).first()
    """
    return render(request, "administration/dashboard.html")


@admin_required
def manage_students(request):
    """
    List, search, create, edit, and deactivate student accounts.

    URL: /administration/students/

    TODO: Implement CRUD for students:
        - GET: list all students with search/filter
        - POST: create new student or update existing one
        students = User.objects.filter(role="student").select_related("student_profile")
    """
    return render(request, "administration/manage_students.html")


@admin_required
def manage_lecturers(request):
    """
    List, search, create, edit, and deactivate lecturer accounts.

    URL: /administration/lecturers/

    TODO: Similar to manage_students but for lecturers
    """
    return render(request, "administration/manage_lecturers.html")


@admin_required
def manage_departments(request):
    """
    CRUD operations for departments.

    URL: /administration/departments/

    TODO: Implement:
        departments = Department.objects.all()
        Use DepartmentForm from apps/courses/forms.py for create/edit
    """
    return render(request, "administration/manage_departments.html")


@admin_required
def manage_courses(request):
    """
    CRUD operations for courses.

    URL: /administration/courses/

    TODO: Implement:
        courses = Course.objects.select_related("department", "lecturer", "semester")
        Use CourseForm from apps/courses/forms.py for create/edit
    """
    return render(request, "administration/manage_courses.html")


@admin_required
def manage_enrollments(request):
    """
    Manage student enrollments — add/remove students from courses.

    URL: /administration/enrollments/

    TODO: Implement:
        enrollments = Enrollment.objects.select_related("student", "course")
    """
    return render(request, "administration/manage_enrollments.html")


@admin_required
def manage_sessions(request):
    """
    Manage academic sessions and semesters.

    URL: /administration/sessions/

    The admin creates sessions (e.g., "2025/2026") and semesters within them.
    Only one session and one semester should be active at a time.

    TODO: Implement:
        sessions = AcademicSession.objects.prefetch_related("semesters")
        # prefetch_related() loads related semesters in a separate query
        # More efficient than select_related() for reverse ForeignKey (one-to-many)
    """
    return render(request, "administration/manage_sessions.html")


@admin_required
def analytics(request):
    """
    System analytics and reports.

    URL: /administration/analytics/

    TODO: Implement with aggregated data:
        - Students per department
        - Average GPA per course
        - Enrollment trends over time
        - Assignment submission rates
        - Grade distributions

    Django's aggregation functions:
        from django.db.models import Count, Avg
        students_per_dept = Department.objects.annotate(student_count=Count("studentprofile"))
        avg_scores = Grade.objects.aggregate(average=Avg("score"))
    """
    return render(request, "administration/analytics.html")
