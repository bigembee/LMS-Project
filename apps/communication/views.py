"""
views.py - Views for the Communication app.

These views are accessible by ALL authenticated users (students, lecturers, admins).

FEATURES:
    - Announcements: view system-wide and course-specific announcements
    - Notifications: view personal notifications, mark as read
    - Messages: inbox, compose, read messages
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def announcement_list(request):
    """
    List announcements relevant to the current user.

    URL: /communication/announcements/

    Announcements should be filtered by audience:
        - "all" → visible to everyone
        - "students" → visible only if user.role == "student"
        - "lecturers" → visible only if user.role == "lecturer"
        - "course" → visible only if user is enrolled in that course

    TODO: Implement filtering:
        from django.db.models import Q
        # Q objects allow complex OR queries
        announcements = Announcement.objects.filter(
            Q(audience="all") |
            Q(audience=request.user.role) |
            Q(audience="course", course__enrollments__student=request.user)
        ).distinct()
        # .distinct() removes duplicates that can occur with OR queries across joins
    """
    return render(request, "communication/announcement_list.html")


@login_required
def announcement_detail(request, pk):
    """
    View a single announcement.

    URL: /communication/announcements/5/ (pk=5)
    """
    return render(request, "communication/announcement_detail.html")


@login_required
def notification_list(request):
    """
    View the current user's notifications.

    URL: /communication/notifications/

    TODO: Implement:
        # Only show notifications for the CURRENT user (not other users' notifications)
        notifications = request.user.notifications.all()
        # request.user.notifications works because of related_name="notifications" on the model

        # Optionally mark all as read when they view the page:
        request.user.notifications.filter(is_read=False).update(is_read=True)
    """
    return render(request, "communication/notification_list.html")


@login_required
def inbox(request):
    """
    Message inbox — shows all messages received by the current user.

    URL: /communication/messages/

    TODO: Implement:
        messages = request.user.received_messages.select_related("sender")
        # request.user.received_messages works because of related_name="received_messages"
    """
    return render(request, "communication/inbox.html")


@login_required
def compose_message(request):
    """
    Compose and send a new message.

    URL: /communication/messages/compose/

    GET: Show the compose form
    POST: Save the message and redirect to inbox

    TODO: Implement:
        if request.method == "POST":
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.sender = request.user    # Set the sender to the current user
                message.save()
                return redirect("communication:inbox")
    """
    return render(request, "communication/compose.html")


@login_required
def message_detail(request, pk):
    """
    Read a specific message.

    URL: /communication/messages/5/ (pk=5)

    When the recipient opens a message, mark it as read.

    TODO: Implement:
        message = get_object_or_404(Message, pk=pk)
        # Security check: only the sender or recipient should see this message
        if request.user not in [message.sender, message.recipient]:
            raise PermissionDenied
        # Mark as read if the current user is the recipient
        if request.user == message.recipient and not message.is_read:
            message.is_read = True
            message.save()
    """
    return render(request, "communication/message_detail.html")
