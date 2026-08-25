"""
urls.py - URL patterns for the Communication app.

ALL URLs are prefixed with /communication/ (set in lms/urls.py).

FULL URL MAP:
    /communication/announcements/       → List announcements
    /communication/announcements/5/     → View announcement details
    /communication/notifications/       → View personal notifications
    /communication/messages/            → Message inbox
    /communication/messages/compose/    → Compose a new message
    /communication/messages/5/          → Read a specific message
"""

from django.urls import path
from . import views

app_name = "communication"  # Namespace: "communication:inbox", "communication:compose", etc.

urlpatterns = [
    # Announcements
    path("announcements/", views.announcement_list, name="announcement_list"),
    path("announcements/<int:pk>/", views.announcement_detail, name="announcement_detail"),

    # Notifications
    path("notifications/", views.notification_list, name="notification_list"),

    # Messages
    path("messages/", views.inbox, name="inbox"),
    path("messages/compose/", views.compose_message, name="compose"),
    path("messages/<int:pk>/", views.message_detail, name="message_detail"),
]
