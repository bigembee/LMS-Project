from django.shortcuts import render, redirect
from apps.accounts.decorators import lecturer_required
from django.contrib import messages
from django.utils.dateparse import parse_datetime
from apps.communication.models import Announcement, Message
from apps.assignments.models import Assignment, Submission, Grade
from apps.courses.models import Course
from decimal import Decimal, InvalidOperation



@lecturer_required
def dashboard(request):
    """
    Lecturer's main dashboard view.
    """
    recent_messages = (
    Message.objects
    .filter(recipient=request.user)
    .select_related("sender")
    .order_by("-created_at")[:5]
    )

    unread_messages = Message.objects.filter(
    recipient=request.user,
    is_read=False,
    ).count()
    
    # Fallback mock data matching your exact expected frontend fields
    context = {
        "profile": getattr(request.user, "lecturerprofile", None),
        
        # Stat cards metrics
        "total_courses": 4,
        "total_students": 186,
        "pending_count": 23,
        "unread_messages": unread_messages,
        
        # Ring charts layout data
        "ring_degrees": 140,
        "attendance_rate": 84,
        
        # Core Courses list array
        "courses": [
            {"code": "CSC 201", "title": "Data Structures", "students": 62, "progress": 70, "next_class": "Mon, 10:00"},
            {"code": "CSC 305", "title": "Database Systems", "students": 48, "progress": 55, "next_class": "Tue, 12:00"},
            {"code": "CSC 312", "title": "Web Development", "students": 41, "progress": 82, "next_class": "Wed, 09:00"},
            {"code": "CSC 410", "title": "Machine Learning", "students": 35, "progress": 38, "next_class": "Thu, 14:00"},
        ],
        
        # Submissions waiting block table
        "submissions": [
            {"title": "Assignment 3: Linked Lists", "course": "CSC 201", "submitted": 51, "total": 62, "due": "Oct 04"},
            {"title": "ER Diagram Project", "course": "CSC 305", "submitted": 40, "total": 48, "due": "Oct 06"},
            {"title": "Portfolio Website", "course": "CSC 312", "submitted": 33, "total": 41, "due": "Oct 09"},
        ],
        
        # Course bar chart metrics
        "performance": [
            {"label": "CSC 201", "value": 78},
            {"label": "CSC 305", "value": 64},
            {"label": "CSC 312", "value": 85},
            {"label": "CSC 410", "value": 58},
        ],
        
        # Schedule timetables
        "schedule": [
            {"start": "09:45", "end": "10:30", "title": "Data Structures", "course": "CSC 201", "room": "Hall A"},
            {"start": "12:00", "end": "12:45", "title": "Database Systems", "course": "CSC 305", "room": "Lab 2"},
            {"start": "14:00", "end": "15:30", "title": "Machine Learning", "course": "CSC 410", "room": "Hall C"},
        ],
        
        # Announcement bulletins
        "announcements": [
            {"title": "Midterm test holds next week", "course": "CSC 201", "when": "2h ago"},
            {"title": "Lab session moved to Friday", "course": "CSC 305", "when": "Yesterday"},
        ],
        
        # Unread communication rows
        "recent_messages": recent_messages,
    }
    
    return render(request, "lecturers/dashboard.html", context)


@lecturer_required
def my_courses(request):
    courses = request.user.courses_taught.select_related(
        "department",
        "semester",
    )

    return render(
        request,
        "lecturers/my_courses.html",
        {"courses": courses},
    )


@lecturer_required
def manage_course(request, pk):
    try:
        course = (
            Course.objects
            .select_related("department", "semester")
            .prefetch_related(
                "enrollments__student",
                "modules__materials",
                "lectures",
                "assignments",
                "announcements",
            )
            .get(pk=pk, lecturer=request.user)
        )
    except Course.DoesNotExist:
        messages.error(
            request,
            "The course does not exist or is not assigned to you."
        )
        return redirect("lecturers:my_courses")

    context = {
    "course": course,
    "enrollments": course.enrollments.all(),
    "modules": course.modules.all(),
    "lectures": course.lectures.all(),
    "assignments": course.assignments.all(),
    "announcements": course.announcements.all(),
    "material_count": sum(
        module.materials.count()
        for module in course.modules.all()
    ),
    }

    return render(
        request,
        "lecturers/manage_course.html",
        context,
    )


@lecturer_required
def create_assignment(request):
    courses = Course.objects.filter(
        lecturer=request.user
    ).select_related("department", "semester")

    if request.method == "POST":
        course_id = request.POST.get("course")
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        max_score = request.POST.get("max_score")
        due_date = request.POST.get("due_date")
        due_time = request.POST.get("due_time")
        assignment_file = request.FILES.get("file")

        if not course_id or not title or not description or not max_score or not due_date or not due_time:
            messages.error(request, "Please fill in all required fields.")
            return render(
                request,
                "lecturers/create_assignment.html",
                {"courses": courses},
            )

        try:
            course = courses.get(pk=course_id)
        except Course.DoesNotExist:
            messages.error(request, "Invalid course selected.")
            return render(
                request,
                "lecturers/create_assignment.html",
                {"courses": courses},
            )

        try:
            max_score = int(max_score)

            if max_score <= 0:
                raise ValueError

        except (TypeError, ValueError):
            messages.error(request, "Maximum score must be a positive number.")
            return render(
                request,
                "lecturers/create_assignment.html",
                {"courses": courses},
            )

        due_datetime = parse_datetime(f"{due_date}T{due_time}")

        if due_datetime is None:
            messages.error(request, "Please enter a valid due date and time.")
            return render(
                request,
                "lecturers/create_assignment.html",
                {"courses": courses},
            )

        Assignment.objects.create(
            course=course,
            title=title,
            description=description,
            file=assignment_file,
            max_score=max_score,
            due_date=due_datetime,
            created_by=request.user,
        )

        messages.success(request, "Assignment created successfully.")

        return redirect("lecturers:create_assignment")

    return render(
        request,
        "lecturers/create_assignment.html",
        {"courses": courses},
    )


@lecturer_required
def view_submissions(request, assignment_id):
    try:
        assignment = (
            Assignment.objects
            .select_related("course")
            .prefetch_related(
                "submissions__student",
                "submissions__grade",
            )
            .get(
                pk=assignment_id,
                course__lecturer=request.user,
            )
        )
    except Assignment.DoesNotExist:
        messages.error(
            request,
            "The assignment does not exist or is not assigned to you."
        )
        return redirect("lecturers:my_courses")

    submissions = assignment.submissions.select_related(
        "student",
        "grade",
    ).order_by("-submitted_at")

    graded_count = submissions.filter(
        status=Submission.Status.GRADED
    ).count()

    pending_count = submissions.filter(
        status=Submission.Status.SUBMITTED
    ).count()

    returned_count = submissions.filter(
        status=Submission.Status.RETURNED
    ).count()

    context = {
        "assignment": assignment,
        "submissions": submissions,
        "total_submissions": submissions.count(),
        "graded_count": graded_count,
        "pending_count": pending_count,
        "returned_count": returned_count,
    }

    return render(
        request,
        "lecturers/view_submissions.html",
        context,
    )


@lecturer_required
def grade_submission(request, submission_id):
    try:
        submission = (
            Submission.objects
            .select_related(
                "student",
                "assignment",
                "assignment__course",
                "grade",
            )
            .get(
                pk=submission_id,
                assignment__course__lecturer=request.user,
            )
        )
    except Submission.DoesNotExist:
        messages.error(
            request,
            "The submission does not exist or is not assigned to you."
        )
        return redirect("lecturers:my_courses")

    if request.method == "POST":
        score = request.POST.get("score", "").strip()
        feedback = request.POST.get("feedback", "").strip()

        try:
            score = Decimal(score)
        except (TypeError, InvalidOperation):
            messages.error(
                request,
                "Please enter a valid score."
            )
            return render(
                request,
                "lecturers/grade_submission.html",
                {"submission": submission},
            )

        if score < 0:
            messages.error(
                request,
                "Score cannot be negative."
            )
            return render(
                request,
                "lecturers/grade_submission.html",
                {"submission": submission},
            )

        if score > submission.assignment.max_score:
            messages.error(
                request,
                f"Score cannot be greater than "
                f"{submission.assignment.max_score}."
            )
            return render(
                request,
                "lecturers/grade_submission.html",
                {"submission": submission},
            )

        grade, created = Grade.objects.update_or_create(
            submission=submission,
            defaults={
                "score": score,
                "feedback": feedback,
                "graded_by": request.user,
            },
        )

        submission.status = Submission.Status.GRADED
        submission.save(update_fields=["status", "updated_at"])

        messages.success(
            request,
            "Submission graded successfully."
        )

        return redirect(
            "lecturers:view_submissions",
            assignment_id=submission.assignment.id,
        )

    return render(
        request,
        "lecturers/grade_submission.html",
        {"submission": submission},
    )

@lecturer_required
def post_announcement(request):
    courses = Course.objects.filter(
        lecturer=request.user
    ).select_related(
        "department",
        "semester",
    )

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        audience = request.POST.get("audience", "all")
        course_id = request.POST.get("course")
        is_pinned = request.POST.get("is_pinned") == "on"

        # Check required fields
        if not title or not content:
            messages.error(
                request,
                "Please fill in all required fields."
            )
            return render(
                request,
                "lecturers/post_announcement.html",
                {"courses": courses},
            )

        # Check that the selected audience is valid
        valid_audiences = {
            choice[0]
            for choice in Announcement.Audience.choices
        }

        if audience not in valid_audiences:
            messages.error(
                request,
                "Invalid announcement audience selected."
            )
            return render(
                request,
                "lecturers/post_announcement.html",
                {"courses": courses},
            )

        course = None

        # Course is required for course-specific announcements
        if audience == Announcement.Audience.COURSE:
            if not course_id:
                messages.error(
                    request,
                    "Please select a course for a course-specific announcement."
                )
                return render(
                    request,
                    "lecturers/post_announcement.html",
                    {"courses": courses},
                )

            try:
                course = courses.get(pk=course_id)
            except Course.DoesNotExist:
                messages.error(
                    request,
                    "Invalid course selected."
                )
                return render(
                    request,
                    "lecturers/post_announcement.html",
                    {"courses": courses},
                )

        Announcement.objects.create(
            title=title,
            content=content,
            author=request.user,
            audience=audience,
            course=course,
            is_pinned=is_pinned,
        )

        messages.success(
            request,
            "Announcement posted successfully."
        )

        return redirect("lecturers:post_announcement")

    return render(
        request,
        "lecturers/post_announcement.html",
        {"courses": courses},
    )
