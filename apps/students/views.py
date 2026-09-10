"""
views.py - Student-facing views.

ALL views in this file are protected by @student_required — only users with
role="student" can access them. If a lecturer tries to visit /students/dashboard/,
they'll get a 403 Forbidden error.

DECORATOR CHAIN:
    @student_required checks:
        1. Is the user logged in? (if not → redirect to login)
        2. Is their role "student"? (if not → 403 Forbidden)
        3. If both pass → run the view function

DATA THESE VIEWS NEED:
    These views don't own the data — they READ from other apps:
        - Enrolled courses  → Enrollment model (apps/courses/models.py)
        - Assignments       → Assignment model (apps/assignments/models.py)
        - Grades            → Grade model (apps/assignments/models.py)
        - Student info      → StudentProfile model (this app's models.py)

FLOW EXAMPLE (student views their grades):
    1. Student visits /students/grades/
    2. Django routes to this file's my_grades() function
    3. @student_required checks the user's role
    4. The view queries the database for the student's grades
    5. The view renders the template with the grade data
    6. HTML is returned to the browser
"""

from django.shortcuts import render

# Import the decorator from the accounts app — it checks that the user is a student
from apps.accounts.decorators import student_required


@student_required
def dashboard(request):
    """
    Student's main dashboard — the landing page after login.

    Shows an overview:
        - Number of enrolled courses
        - Upcoming assignments (due soon)
        - Recent grades
        - Notifications

    URL: /students/dashboard/
    TEMPLATE: students/dashboard.html

    TODO: Implement — query enrolled courses, upcoming assignments, recent grades
    """
    return render(request, "students/dashboard.html")


@student_required
def my_courses(request):
    """
    List courses the student is currently enrolled in.

    URL: /students/courses/

    TODO: Query enrolled courses:
        enrollments = Enrollment.objects.filter(student=request.user, status="enrolled")
            .select_related("course", "course__lecturer", "course__department")
    """
    return render(request, "students/my_courses.html")


@student_required
def register_course(request):
    """
    Course registration page — browse available courses and enroll.

    URL: /students/courses/register/

    GET: Show available courses (not already enrolled, not full)
    POST: Create an Enrollment record linking the student to the selected course

    TODO: Implement course registration logic:
        - Show courses for the student's department/level
        - Check if the course is full (course.is_full)
        - Check if already enrolled (unique_together constraint)
        - Create Enrollment object on success
    """
    return render(request, "students/register_course.html")


@student_required
def schedule(request):
    """
    Display the student's weekly course timetable.

    URL: /students/timetable/

    TODO: This requires a Timetable/Schedule model (Phase 2)
    or can be computed from enrolled courses + time slots
    """
    return render(request, "students/schedule.html")


@student_required
def my_assignments(request):
    """
    List all assignments from the student's enrolled courses.

    URL: /students/assignments/

    TODO: Implement:
        # Get IDs of courses the student is enrolled in
        enrolled_course_ids = request.user.enrollments.filter(
            status="enrolled"
        ).values_list("course_id", flat=True)
        # values_list("course_id", flat=True) returns [1, 5, 12] instead of [(1,), (5,), (12,)]

        # Get all assignments from those courses
        assignments = Assignment.objects.filter(course_id__in=enrolled_course_ids)
    """
    return render(request, "students/my_assignments.html")


@student_required
def my_grades(request):
    """
    View the student's grades and results for all submitted assignments.

    URL: /students/grades/

    TODO: Implement:
        submissions = Submission.objects.filter(student=request.user, status="graded")
            .select_related("grade", "assignment", "assignment__course")
    """
    return render(request, "students/my_grades.html")


@student_required
def gpa(request):
    """
    Calculate and display the student's GPA.

    URL: /students/gpa/

    Uses the utility functions in utils.py to:
        1. Get all graded submissions for the student
        2. Convert scores to letter grades (A, B, C, D, E, F)
        3. Convert letter grades to grade points (5.0, 4.0, 3.0, etc.)
        4. Calculate weighted GPA using credit units

    TODO: Implement using calculate_gpa() and score_to_grade() from utils.py
    """
    return render(request, "students/gpa.html")

@student_required
def notes(request):
    """
    Display the student's notes.

    URL: /students/notes/
    """
    return render(request, "students/notes.html")

@student_required
def maps(request):
    """
    Display the schools map and how to locate classes.

    URL: /students/maps/
    """
    return render(request, "students/maps.html")

