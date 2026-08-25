"""
permissions.py - DRF (Django REST Framework) permission classes.

WHAT ARE DRF PERMISSIONS?
    Permissions control WHO can access API endpoints.
    They're the API equivalent of the @student_required decorators in decorators.py.

    - Decorators → protect HTML views (templates)
    - Permissions → protect API views (JSON responses)

HOW THEY WORK:
    1. A request comes in to an API endpoint
    2. DRF calls has_permission() on each permission class
    3. If ANY permission returns False, the request is denied (403 Forbidden)

HOW TO USE IN API VIEWS:
    from apps.core.permissions import IsStudent, IsLecturer

    class StudentGradesView(APIView):
        permission_classes = [IsStudent]  # Only students can access this endpoint

        def get(self, request):
            ...

    class CourseManagementView(APIView):
        permission_classes = [IsLecturerOrAdmin]  # Lecturers AND admins can access

        def get(self, request):
            ...

COMPARISON:
    decorators.py → @student_required → for HTML views → returns 403 page
    permissions.py → IsStudent → for API views → returns {"detail": "Permission denied"} JSON
"""

from rest_framework.permissions import BasePermission  # Base class for custom permissions


class IsStudent(BasePermission):
    """Only allows access if the user is authenticated AND has role='student'."""
    def has_permission(self, request, view):
        # Both conditions must be True:
        # 1. User is logged in (not AnonymousUser)
        # 2. User's role is "student"
        return request.user.is_authenticated and request.user.role == "student"


class IsLecturer(BasePermission):
    """Only allows access if the user is authenticated AND has role='lecturer'."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "lecturer"


class IsAdmin(BasePermission):
    """Only allows access if the user is authenticated AND has role='admin'."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


class IsLecturerOrAdmin(BasePermission):
    """Allows access for both lecturers AND admins."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["lecturer", "admin"]
