"""
admin.py - Admin configuration for the Communication app.

Registers Announcement, Notification, and Message in Django's admin panel.
"""

from django.contrib import admin
from .models import Announcement, Notification, Message


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "audience", "is_pinned", "created_at"]
    list_filter = ["audience", "is_pinned"]
    search_fields = ["title", "content"]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["recipient", "title", "is_read", "created_at"]
    list_filter = ["is_read"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["sender", "recipient", "subject", "is_read", "created_at"]
    list_filter = ["is_read"]
