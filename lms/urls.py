"""
urls.py (ROOT) - The URL ROUTER for the entire project.

HOW DJANGO HANDLES A REQUEST:
1. User visits: http://localhost:8000/students/dashboard/
2. Django loads ROOT_URLCONF (this file, defined in settings.py)
3. Django goes through urlpatterns top to bottom, looking for a match
4. "students/" matches → Django strips "students/" and passes "dashboard/" to apps/students/urls.py
5. apps/students/urls.py finds "dashboard/" → calls the dashboard view function
6. The view function returns an HTML response to the user

The include() function delegates URL matching to another app's urls.py file.
This is how each app "owns" its own URLs — team members work independently.

URL STRUCTURE:
    /admin/            → Django's built-in admin panel
    /accounts/...      → Login, register, profile, password reset
    /students/...      → Student dashboard, courses, grades, GPA
    /lecturers/...     → Lecturer dashboard, assignments, grading
    /administration/...→ Admin dashboard, manage everything
    /courses/...       → Course listing, course details
    /assignments/...   → Assignment listing, submission
    /communication/... → Announcements, notifications, messages
    /api/...           → REST API endpoints (JSON responses for React/mobile)
"""

from django.contrib import admin                    # Django's admin site
from django.urls import path, include               # path() maps URLs to views, include() delegates to other urls.py
from django.conf import settings                    # Access to settings.py variables
from django.conf.urls.static import static          # Helper to serve uploaded files in development

# The main URL routing table. Django checks these patterns in ORDER from top to bottom.
urlpatterns = [
    # Django's built-in admin panel — auto-generates CRUD pages for all registered models
    # Access it at: http://localhost:8000/admin/
    # Create an admin user first: python manage.py createsuperuser
    path("admin/", admin.site.urls),

    # include() says: "For any URL starting with 'accounts/', let apps/accounts/urls.py handle the rest"
    # Example: /accounts/login/ → accounts/urls.py looks for "login/" → calls login_view
    path("accounts/", include("apps.accounts.urls")),

    # Student-specific pages. Only users with role="student" can access these.
    # Example: /students/dashboard/ → students/urls.py → dashboard view
    path("students/", include("apps.students.urls")),

    # Lecturer-specific pages. Only users with role="lecturer" can access these.
    # Example: /lecturers/courses/ → lecturers/urls.py → my_courses view
    path("lecturers/", include("apps.lecturers.urls")),

    # Admin-specific pages. Only users with role="admin" can access these.
    # Example: /administration/analytics/ → administration/urls.py → analytics view
    path("administration/", include("apps.administration.urls")),

    # Course pages accessible by all authenticated users.
    # Example: /courses/ → courses/urls.py → course_list view
    path("courses/", include("apps.courses.urls")),

    # Assignment pages accessible by all authenticated users.
    # Example: /assignments/5/submit/ → assignments/urls.py → submit_assignment view
    path("assignments/", include("apps.assignments.urls")),

    # Communication: announcements, notifications, messaging
    # Example: /communication/messages/ → communication/urls.py → inbox view
    path("communication/", include("apps.communication.urls")),

    # REST API endpoints — returns JSON instead of HTML (for React frontend or mobile apps)
    # Example: /api/courses/ → returns JSON list of courses
    path("api/", include("api.urls")),
]

# In development (DEBUG=True), serve user-uploaded files (media/) through Django
# In production, the web server (Nginx) handles this instead
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
