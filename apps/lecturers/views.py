"""
views.py - Lecturer-facing views.

ALL views in this file are protected by @lecturer_required — only users with
role="lecturer" can access them.

WHAT LECTURERS CAN DO:
    - See their dashboard with an overview of their courses and pending work
    - View the courses they're assigned to teach
    - Manage individual courses (view enrolled students, post materials)
    - Create new assignments for their courses
    - View all submissions for an assignment
    - Grade individual submissions

DATA FLOW:
    Lecturer → creates Assignment (linked to their Course)
    Student → creates Submission (linked to the Assignment)
    Lecturer → creates Grade (linked to the Submission)
"""

from django.shortcuts import render
from apps.accounts.decorators import lecturer_required  # Only lecturers can access these views


@lecturer_required
def dashboard(request):
    """
    Lecturer's main dashboard.

    Shows: courses taught, pending submissions to grade, recent activity

    URL: /lecturers/dashboard/

    TODO: Implement:
        courses = Course.objects.filter(lecturer=request.user)
        # Count submissions waiting to be graded across all their courses
        pending_count = Submission.objects.filter(
            assignment__course__lecturer=request.user, status="submitted"
        ).count()
    """
    return render(request, "lecturers/dashboard.html")


@lecturer_required
def my_courses(request):
    """
    List all courses this lecturer is assigned to teach.

    URL: /lecturers/courses/

    TODO: Implement:
        # request.user.courses_taught is available because Course model has:
        # lecturer = ForeignKey(User, related_name="courses_taught")
        courses = request.user.courses_taught.select_related("department", "semester")
    """
    return render(request, "lecturers/my_courses.html")


@lecturer_required
def manage_course(request, pk):
    """
    Manage a specific course — view enrolled students, assignments, etc.

    URL: /lecturers/courses/5/manage/ (pk=5)

    The "pk" comes from the URL: path("courses/<int:pk>/manage/", ...)

    TODO: Verify the lecturer owns this course:
        course = get_object_or_404(Course, pk=pk, lecturer=request.user)
        # Adding lecturer=request.user ensures a lecturer can only manage THEIR courses
    """
    return render(request, "lecturers/manage_course.html")


@lecturer_required
def create_assignment(request):
    """
    Create a new assignment for one of the lecturer's courses.

    URL: /lecturers/assignments/create/

    GET: Show the assignment creation form
    POST: Validate and save the new assignment

    TODO: Implement:
        if request.method == "POST":
            form = AssignmentForm(request.POST, request.FILES)
            if form.is_valid():
                assignment = form.save(commit=False)      # Don't save to DB yet
                assignment.created_by = request.user       # Set the creator to current lecturer
                assignment.save()                          # Now save
                messages.success(request, "Assignment created!")
                return redirect("lecturers:my_courses")
        else:
            form = AssignmentForm()
            # Limit the "course" dropdown to only courses this lecturer teaches
            form.fields["course"].queryset = Course.objects.filter(lecturer=request.user)
    """
    return render(request, "lecturers/create_assignment.html")


@lecturer_required
def view_submissions(request, assignment_id):
    """
    View all student submissions for a specific assignment.

    URL: /lecturers/assignments/5/submissions/ (assignment_id=5)

    Shows a table of all students who submitted, their status (graded/ungraded),
    and links to grade each one.

    TODO: Implement:
        assignment = get_object_or_404(Assignment, pk=assignment_id, created_by=request.user)
        submissions = assignment.submissions.select_related("student", "grade")
    """
    return render(request, "lecturers/view_submissions.html")


@lecturer_required
def grade_submission(request, submission_id):
    """
    Grade a specific student submission.

    URL: /lecturers/submissions/5/grade/ (submission_id=5)

    GET: Show the submission details + grading form
    POST: Save the grade and feedback

    TODO: Implement:
        submission = get_object_or_404(Submission, pk=submission_id)
        if request.method == "POST":
            form = GradeForm(request.POST)
            if form.is_valid():
                grade = form.save(commit=False)
                grade.submission = submission
                grade.graded_by = request.user
                grade.save()
                submission.status = "graded"    # Update submission status
                submission.save()
    """
    return render(request, "lecturers/grade_submission.html")


@lecturer_required
def post_announcement(request):
    """
    Post an announcement to a course or globally.

    URL: /lecturers/announcements/create/

    TODO: Implement using AnnouncementForm from apps/communication/forms.py
    """
    return render(request, "lecturers/post_announcement.html")
