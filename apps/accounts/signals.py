"""
signals.py - Event handlers (signals) for the Accounts app.

WHAT ARE SIGNALS?
Signals are Django's way of allowing certain senders to notify receivers when actions happen.
Think of them as "event listeners" or "hooks":
    - "When event X happens, automatically do Y"

COMMON SIGNALS:
    post_save   → fires AFTER a model instance is saved to the database
    pre_save    → fires BEFORE a model instance is saved
    post_delete → fires AFTER a model instance is deleted
    pre_delete  → fires BEFORE a model instance is deleted

HOW THEY WORK:
    1. Something happens (e.g., a new User is saved to the database)
    2. Django sends a signal (post_save)
    3. Any function connected to that signal (via @receiver) runs automatically

WHY USE SIGNALS?
    They keep your code decoupled. Instead of putting "create profile" logic
    inside the User model or view, the signal handles it separately.
    If you later add a new app that needs to react to user creation,
    you add a new signal handler — no need to change existing code.

IMPORTANT:
    This file must be IMPORTED for signals to work.
    That's why apps.py has: import apps.accounts.signals
    If you forget to import it, the signals will NEVER fire!

EXAMPLE (uncomment and customize when ready to implement):

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        # "created" is True when a NEW user is made (not when an existing one is updated)
        if created and instance.is_student:
            from apps.students.models import StudentProfile
            StudentProfile.objects.create(user=instance)
        elif created and instance.is_lecturer:
            from apps.lecturers.models import LecturerProfile
            LecturerProfile.objects.create(user=instance)
"""

from django.db.models.signals import post_save  # Signal sent after a model's save() method
from django.dispatch import receiver             # Decorator to connect a function to a signal
from .models import User                         # Our User model — the signal sender
