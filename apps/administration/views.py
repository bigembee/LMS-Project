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

from django.shortcuts import redirect, render
from apps.accounts.decorators import admin_required
from apps.accounts.models import User
from apps.courses.models import Course,Department,Enrollment,AcademicSession,Semester   # Only admins can access these views
from django.db.models import Count, Avg  # For analytics queries
from apps.assignments.models import Grade  # For analytics queries
from apps.courses.forms import CourseForm, DepartmentForm, AcademicSessionForm,SemesterForm
from django.shortcuts import get_object_or_404


@admin_required
def dashboard(request):
    total_students = User.objects.filter(role="student").count()
    total_lecturers = User.objects.filter(role="lecturer").count()
    total_courses = Course.objects.count()
    active_session = AcademicSession.objects.filter(is_active=True).first()

    context = {
        "total_students": total_students,
        "total_lecturers": total_lecturers,
        "total_courses": total_courses,
        "active_session": active_session,
    }
    return render(request, "administration/dashboard.html", context)


@admin_required
def manage_students(request):
    students = User.objects.filter(role="student").select_related("student_profile")
    context = {"students": students}
    return render(request, "administration/manage_students.html", context)


@admin_required
def manage_lecturers(request):
    lecturers = User.objects.filter(role="lecturer").select_related("lecturer_profile")
    context = {"lecturers": lecturers}
    return render(request, "administration/manage_lecturers.html", context)


@admin_required
def manage_departments(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("administration:manage_departments")
    else:
        form = DepartmentForm()

    departments = Department.objects.select_related("head")
    context = {"departments": departments, "form": form}
    return render(request, "administration/manage_departments.html", context)


@admin_required
def edit_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect("administration:manage_departments")
    else:
        form = DepartmentForm(instance=department)

    context = {"form": form, "department": department}
    return render(request, "administration/edit_department.html", context)


@admin_required
def delete_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    if request.method == "POST":
        department.delete()
        return redirect("administration:manage_departments")
    context = {"department": department}
    return render(request, "administration/delete_department.html", context)

@admin_required
def manage_courses(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("administration:manage_courses")
    else:
        form = CourseForm()

    courses = Course.objects.select_related("department", "lecturer", "semester")
    context = {"courses": courses, "form": form}
    return render(request, "administration/manage_courses.html", context)


@admin_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect("administration:manage_courses")
    else:
        form = CourseForm(instance=course)

    context = {"form": form, "course": course}
    return render(request, "administration/edit_course.html", context)


@admin_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        course.delete()
        return redirect("administration:manage_courses")
    context = {"course": course}
    return render(request, "administration/delete_course.html", context)

@admin_required
def manage_enrollments(request):
    enrollments = Enrollment.objects.select_related("student", "course")
    context = {"enrollments": enrollments}
    return render(request, "administration/manage_enrollments.html", context)


@admin_required
def manage_sessions(request):
    if request.method == "POST":
        form = AcademicSessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("administration:manage_sessions")
    else:
        form = AcademicSessionForm()

    sessions = AcademicSession.objects.prefetch_related("semesters")
    context = {"sessions": sessions, "form": form}
    return render(request, "administration/manage_sessions.html", context)


@admin_required
def edit_session(request, session_id):
    session = get_object_or_404(AcademicSession, id=session_id)
    if request.method == "POST":
        form = AcademicSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect("administration:manage_sessions")
    else:
        form = AcademicSessionForm(instance=session)

    context = {"form": form, "session": session}
    return render(request, "administration/edit_session.html", context)


@admin_required
def delete_session(request, session_id):
    session = get_object_or_404(AcademicSession, id=session_id)
    if request.method == "POST":
        session.delete()
        return redirect("administration:manage_sessions")
    context = {"session": session}
    return render(request, "administration/delete_session.html", context)

@admin_required
def add_semester(request):
    if request.method == "POST":
        form = SemesterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("administration:manage_sessions")
    else:
        form = SemesterForm()

    context = {"form": form}
    return render(request, "administration/add_semester.html", context)


@admin_required
def edit_semester(request, semester_id):
    semester = get_object_or_404(Semester, id=semester_id)
    if request.method == "POST":
        form = SemesterForm(request.POST, instance=semester)
        if form.is_valid():
            form.save()
            return redirect("administration:manage_sessions")
    else:
        form = SemesterForm(instance=semester)

    context = {"form": form, "semester": semester}
    return render(request, "administration/edit_semester.html", context)


@admin_required
def delete_semester(request, semester_id):
    semester = get_object_or_404(Semester, id=semester_id)
    if request.method == "POST":
        semester.delete()
        return redirect("administration:manage_sessions")
    context = {"semester": semester}
    return render(request, "administration/delete_semester.html", context)

@admin_required
def analytics(request):
    students_per_department = Department.objects.annotate(
        student_count=Count("studentprofile")
    )
    courses_per_department = Department.objects.annotate(
        course_count=Count("courses")
    )
    enrollment_status_counts = Enrollment.objects.values("status").annotate(
        total=Count("id")
    )
    average_score_per_course = Course.objects.annotate(
        avg_score=Avg("assignments__submissions__grade__score")
    )

    context = {
        "students_per_department": students_per_department,
        "courses_per_department": courses_per_department,
        "enrollment_status_counts": enrollment_status_counts,
        "average_score_per_course": average_score_per_course,
    }
    return render(request, "administration/analytics.html", context)

