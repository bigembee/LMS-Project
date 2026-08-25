"""
urls.py - REST API URL configuration.

WHAT IS A REST API?
    REST (Representational State Transfer) API serves data as JSON instead of HTML.
    It's used by:
        - React/Vue/Angular frontends (JavaScript apps)
        - Mobile apps (Android/iOS)
        - Other services that need to read/write LMS data

    While the regular views return HTML pages, the API returns JSON data:
        HTML view:  GET /courses/         → returns an HTML page with courses
        API view:   GET /api/courses/     → returns JSON: [{"id": 1, "code": "CSC 201", ...}]

DRF ROUTER:
    DefaultRouter automatically creates URL patterns for ViewSets:
        router.register("courses", CourseViewSet)
    This creates:
        GET    /api/courses/       → list all courses
        POST   /api/courses/       → create a new course
        GET    /api/courses/5/     → get course with id=5
        PUT    /api/courses/5/     → update course with id=5
        DELETE /api/courses/5/     → delete course with id=5

    All 5 URLs from ONE line of code!

HOW TO ADD NEW API ENDPOINTS:
    1. Create a ViewSet in the app's views.py (or a separate api_views.py)
    2. Import it here
    3. Register it with the router

EXAMPLE:
    from apps.courses.views import CourseViewSet
    router.register("courses", CourseViewSet, basename="course")
    # This creates: /api/courses/ and /api/courses/<pk>/
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter  # Auto-generates URL patterns for ViewSets

# Create a router instance — it will hold all our API URL patterns
router = DefaultRouter()

# Register ViewSets here as features are built:
# router.register("users", UserViewSet)           # /api/users/
# router.register("courses", CourseViewSet)        # /api/courses/
# router.register("assignments", AssignmentViewSet) # /api/assignments/
# router.register("enrollments", EnrollmentViewSet) # /api/enrollments/

app_name = "api"  # Namespace: "api:course-list", "api:course-detail", etc.

urlpatterns = [
    # Include all router-generated URLs
    path("", include(router.urls)),

    # DRF's built-in login/logout views for the browsable API
    # When you visit /api/ in your browser, DRF shows a nice interface
    # This adds a "Log in" button to that interface
    path("auth/", include("rest_framework.urls")),
]
