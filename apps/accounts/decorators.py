"""
decorators.py - Custom decorators for role-based access control.

WHAT ARE DECORATORS?
Decorators are functions that wrap other functions to add extra behavior.
They're applied with the @ symbol above a function definition.

EXAMPLE:
    @student_required           ← This is the decorator
    def my_grades(request):     ← This is the view being decorated
        ...

    What actually happens behind the scenes:
    my_grades = student_required(my_grades)
    Now my_grades is wrapped — before running the real view, it checks the user's role.

FLOW WHEN A DECORATED VIEW IS CALLED:
    1. User visits /students/grades/
    2. Django calls my_grades(request)
    3. But my_grades is wrapped by @student_required
    4. The decorator checks: Is the user logged in? Is their role "student"?
    5. If YES → the real my_grades() runs and returns the grades page
    6. If NOT logged in → redirect to the login page
    7. If wrong role → return 403 Forbidden error

HOW THESE ARE USED:
    In views.py of any app:
        from apps.accounts.decorators import student_required, lecturer_required, admin_required

        @student_required
        def student_dashboard(request):
            ...  # Only students can reach this code

        @lecturer_required
        def grade_assignment(request):
            ...  # Only lecturers can reach this code

        @admin_required
        def manage_users(request):
            ...  # Only admins can reach this code
"""

from functools import wraps                     # wraps preserves the original function's name and docstring
from django.shortcuts import redirect           # Redirects the user to another URL
from django.core.exceptions import PermissionDenied  # Raises a 403 Forbidden error


def role_required(allowed_roles):
    """
    Factory function that creates a decorator for role-based access control.

    This is a THREE-LEVEL function (a "decorator factory"):
        Level 1: role_required(["student"])     → returns a decorator
        Level 2: decorator(view_func)           → returns a wrapper
        Level 3: wrapper(request, ...)          → runs the actual check

    Parameters:
        allowed_roles: A list of role strings, e.g., ["student"] or ["lecturer", "admin"]
    """
    def decorator(view_func):
        # @wraps(view_func) preserves the original function's __name__ and __doc__
        # Without it, every decorated view would appear as "wrapper" in debugging
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Step 1: Check if the user is logged in
            if not request.user.is_authenticated:
                # Not logged in → redirect to the login page
                return redirect("accounts:login")

            # Step 2: Check if the user's role is in the allowed list
            if request.user.role not in allowed_roles:
                # Wrong role → raise 403 Forbidden (Django shows an error page)
                raise PermissionDenied

            # Step 3: All checks passed → run the actual view function
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


# Convenience decorators — shortcuts for common role checks
# Instead of writing @role_required(["student"]) every time, just write @student_required

def student_required(view_func):
    """Only allows users with role='student'. Shortcut for @role_required(["student"])"""
    return role_required(["student"])(view_func)


def lecturer_required(view_func):
    """Only allows users with role='lecturer'. Shortcut for @role_required(["lecturer"])"""
    return role_required(["lecturer"])(view_func)


def admin_required(view_func):
    """Only allows users with role='admin'. Shortcut for @role_required(["admin"])"""
    return role_required(["admin"])(view_func)
