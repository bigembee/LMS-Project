"""
views.py - Views for the Assignments app.

These are SHARED views — accessible by any authenticated user.
Role-specific assignment views are in the role apps:
    - Students viewing/submitting assignments → apps/students/views.py
    - Lecturers creating/grading assignments  → apps/lecturers/views.py

THESE VIEWS HANDLE:
    - Listing assignments (filtered by the user's enrolled/taught courses)
    - Viewing assignment details
    - Submitting an assignment (student action)
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def assignment_list(request):
    """
    List all assignments relevant to the current user.

    For students: show assignments from their enrolled courses
    For lecturers: show assignments from their taught courses

    URL: /assignments/

    TODO: Implement filtering based on user role:
        if request.user.is_student:
            # Get courses the student is enrolled in, then their assignments
            enrolled_courses = request.user.enrollments.filter(status="enrolled").values_list("course", flat=True)
            assignments = Assignment.objects.filter(course__in=enrolled_courses)
        elif request.user.is_lecturer:
            assignments = Assignment.objects.filter(course__lecturer=request.user)
    """
    return render(request, "assignments/assignment_list.html")


@login_required
def assignment_detail(request, pk):
    """
    View details of a single assignment.

    URL: /assignments/5/ (pk=5)

    Shows: title, description, due date, attached file, submission status
    For students: also shows submission form if not yet submitted
    For lecturers: shows submission count and link to grade

    TODO: Implement — use get_object_or_404(Assignment, pk=pk)
    """
    return render(request, "assignments/assignment_detail.html")


@login_required
def submit_assignment(request, pk):
    """
    Handle assignment submission by a student.

    URL: /assignments/5/submit/

    GET: Show the submission form
    POST: Save the uploaded file and create a Submission object

    TODO: Implement:
        assignment = get_object_or_404(Assignment, pk=pk)
        if request.method == "POST":
            form = SubmissionForm(request.POST, request.FILES)  # request.FILES for file uploads
            if form.is_valid():
                submission = form.save(commit=False)    # Create object but don't save to DB yet
                submission.student = request.user        # Set the student to the current user
                submission.assignment = assignment       # Set which assignment this is for
                submission.save()                        # Now save to the database
                return redirect("students:my_assignments")
    """
    return render(request, "assignments/submit.html")
