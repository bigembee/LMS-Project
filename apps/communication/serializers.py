"""
serializers.py - DRF serializers for the Communication app.

These convert Announcement/Notification/Message objects to/from JSON for the REST API.
"""

from rest_framework import serializers
from .models import Announcement, Notification, Message


class AnnouncementSerializer(serializers.ModelSerializer):
    """API representation of an Announcement."""
    class Meta:
        model = Announcement
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    """API representation of a Notification."""
    class Meta:
        model = Notification
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    """API representation of a Message."""
    class Meta:
        model = Message
        fields = "__all__"
