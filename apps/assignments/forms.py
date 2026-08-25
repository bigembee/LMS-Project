"""
forms.py - Forms for the Assignments app.

AssignmentForm  → used by LECTURERS to create/edit assignments
SubmissionForm  → used by STUDENTS to submit their work
GradeForm       → used by LECTURERS to grade submissions
"""

from django import forms
from .models import Assignment, Submission, Grade


class AssignmentForm(forms.ModelForm):
    """
    Form for lecturers to create or edit an assignment.

    USED IN: apps/lecturers/views.py → create_assignment()

    The widgets dict customizes how form fields are rendered in HTML.
    DateTimeInput with type="datetime-local" shows a browser date/time picker
    instead of a plain text input.
    """
    class Meta:
        model = Assignment
        fields = ["course", "title", "description", "file", "max_score", "due_date"]
        widgets = {
            # Renders as: <input type="datetime-local"> — a browser-native date/time picker
            "due_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class SubmissionForm(forms.ModelForm):
    """
    Form for students to submit their work.

    USED IN: apps/assignments/views.py → submit_assignment()

    Only includes "file" and "text_response" — the student, assignment, and status
    fields are set programmatically in the view (not by the student).
    """
    class Meta:
        model = Submission
        # Only these fields are shown in the form — student and assignment are set in the view
        fields = ["file", "text_response"]


class GradeForm(forms.ModelForm):
    """
    Form for lecturers to grade a student's submission.

    USED IN: apps/lecturers/views.py → grade_submission()

    Only includes "score" and "feedback" — the submission and graded_by
    fields are set in the view.
    """
    class Meta:
        model = Grade
        fields = ["score", "feedback"]
