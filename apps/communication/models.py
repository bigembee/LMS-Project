"""
models.py - Database models for the Communication app.

THREE TYPES OF COMMUNICATION:

1. ANNOUNCEMENTS: One-to-many broadcast messages
    - Posted by lecturers or admins
    - Can target: all users, students only, lecturers only, or a specific course
    - Examples: "Exam timetable released", "CSC 201 class cancelled tomorrow"

2. NOTIFICATIONS: System-generated personal alerts
    - Created automatically when things happen (e.g., assignment graded, new announcement)
    - Each notification goes to ONE specific user
    - Has a "read" status and optional link to the relevant page
    - Examples: "Your CSC 201 assignment has been graded", "New announcement in MTH 101"

3. MESSAGES: Direct messaging between users
    - One-to-one private messages
    - Like email: sender, recipient, subject, body
    - Examples: Student asks lecturer a question about an assignment

RELATIONSHIPS:
    User ←── Announcement.author (who posted it)
    User ←── Notification.recipient (who receives it)
    User ←── Message.sender (who sent it)
    User ←── Message.recipient (who receives it)
    Course ←── Announcement.course (optional, for course-specific announcements)
"""

from django.db import models
from django.conf import settings


class Announcement(models.Model):
    """
    A broadcast message visible to a group of users.

    DATABASE TABLE: communication_announcement
    """
    # Audience choices — who should see this announcement
    class Audience(models.TextChoices):
        ALL = "all", "All Users"            # Everyone in the system
        STUDENTS = "students", "Students Only"  # Only students
        LECTURERS = "lecturers", "Lecturers Only"  # Only lecturers
        COURSE = "course", "Course Specific"  # Only students enrolled in a specific course

    title = models.CharField(max_length=200)     # Announcement title/headline
    content = models.TextField()                  # The full announcement body

    # Who posted this announcement
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="announcements")

    # Who should see it
    audience = models.CharField(max_length=10, choices=Audience.choices, default=Audience.ALL)

    # If audience is "course", which specific course is this for?
    # null=True: this field can be empty in the database (it's only needed for course-specific announcements)
    course = models.ForeignKey(
        "courses.Course", on_delete=models.CASCADE,
        null=True, blank=True, related_name="announcements",
    )

    # Pinned announcements appear at the top of the list
    is_pinned = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Ordering: pinned first, then newest first
        # "-is_pinned" puts True (pinned) before False (not pinned)
        # "-created_at" puts newest dates first
        ordering = ["-is_pinned", "-created_at"]

    def __str__(self):
        return self.title


class Notification(models.Model):
    """
    A personal notification for a specific user.

    These are typically created programmatically (in signals or views),
    not through a form. When something important happens, the system
    creates a notification for the affected user.

    DATABASE TABLE: communication_notification

    HOW TO CREATE NOTIFICATIONS (in other apps' views or signals):
        Notification.objects.create(
            recipient=student_user,
            title="Assignment Graded",
            message="Your CSC 201 project has been graded. You scored 85/100.",
            link="/students/grades/"
        )
    """
    # Who receives this notification
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")

    title = models.CharField(max_length=200)       # Short title: "Assignment Graded"
    message = models.TextField()                    # Detailed message
    is_read = models.BooleanField(default=False)   # Has the user seen this? Starts as unread.

    # Optional link to the relevant page — clicking the notification takes the user there
    link = models.CharField(max_length=500, blank=True)  # e.g., "/students/grades/"

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]  # Newest notifications first

    def __str__(self):
        return f"{self.recipient} - {self.title}"


class Message(models.Model):
    """
    A direct message between two users.

    DATABASE TABLE: communication_message

    FLOW:
        1. User A composes a message (fill in recipient, subject, body)
        2. Message is saved with sender=User A, recipient=User B
        3. User B sees it in their inbox (/communication/messages/)
        4. When User B opens it, is_read is set to True
    """
    # Who sent this message
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")

    # Who receives this message
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_messages")

    subject = models.CharField(max_length=200)     # Message subject line
    body = models.TextField()                       # The message content
    is_read = models.BooleanField(default=False)   # Has the recipient read it?
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]  # Newest messages first

    def __str__(self):
        return f"{self.sender} -> {self.recipient}: {self.subject}"
