"""
forms.py - Forms for the Communication app.

AnnouncementForm → used by lecturers and admins to post announcements
MessageForm      → used by any user to compose a direct message
"""

from django import forms
from .models import Announcement, Message


class AnnouncementForm(forms.ModelForm):
    """
    Form for creating/editing announcements.

    USED IN:
        - apps/lecturers/views.py → post_announcement()
        - apps/administration/views.py (admin can also post announcements)

    The "author" field is NOT in the form — it's set in the view to request.user.
    """
    class Meta:
        model = Announcement
        fields = ["title", "content", "audience", "course", "is_pinned"]


class MessageForm(forms.ModelForm):
    """
    Form for composing a direct message.

    USED IN: apps/communication/views.py → compose_message()

    The "sender" field is NOT in the form — it's set in the view to request.user.
    """
    class Meta:
        model = Message
        # Only recipient, subject, and body are shown in the form
        # sender is set programmatically in the view
        fields = ["recipient", "subject", "body"]
