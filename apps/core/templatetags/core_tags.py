"""
core_tags.py - Custom template tags and filters.

WHAT ARE TEMPLATE TAGS?
    Template tags extend Django's template language with custom functionality.
    They let you add Python logic that's available in ANY template.

TWO TYPES:
    1. Template TAGS: {% my_tag %} — do something (like include content)
    2. Template FILTERS: {{ value|my_filter }} — transform a value

HOW TO USE:
    1. Load the template tags at the top of your template:
        {% load core_tags %}

    2. Use the filter in your template:
        {% if user|has_role:"student" %}
            <p>Welcome, student!</p>
        {% endif %}

        {% if user|has_role:"lecturer" %}
            <a href="{% url 'lecturers:create_assignment' %}">Create Assignment</a>
        {% endif %}

WHY USE CUSTOM TEMPLATE TAGS?
    Without them, you'd need to pass role-checking logic from EVERY view.
    With them, the template can check roles directly — no extra view code needed.

REGISTRATION:
    register = template.Library() creates a "library" of custom tags
    @register.filter registers a function as a template filter
    The file must be in a "templatetags" directory inside an app
    The app must be in INSTALLED_APPS
"""

from django import template

# Create a template tag library — this is required for Django to find our custom tags
register = template.Library()


@register.filter  # Register this function as a template filter
def has_role(user, role):
    """
    Check if a user has a specific role.

    Usage in templates:
        {% load core_tags %}
        {% if user|has_role:"student" %}
            ... student-only content ...
        {% endif %}

    Parameters:
        user: the User object (automatically passed as the value before |)
        role: the role string to check (passed as the argument after :)

    Returns:
        True if the user is authenticated and has the specified role, False otherwise

    Template syntax breakdown:
        {{ user|has_role:"student" }}
           ^^^^  ^^^^^^^^  ^^^^^^^
           value  filter    argument
    """
    return user.is_authenticated and user.role == role
