"""
settings.py - The BRAIN of your Django project.

Every Django project has a settings file. It controls EVERYTHING:
- Which database to use
- Which apps are installed
- Where to find templates and static files
- Security settings, authentication, etc.

FLOW: manage.py → looks for DJANGO_SETTINGS_MODULE → loads this file → Django starts

The config() function (from python-decouple) reads values from the .env file.
This keeps secrets like passwords out of your code.
"""

import os                       # For interacting with the operating system
from pathlib import Path        # Modern way to handle file paths in Python
from decouple import config     # Reads values from .env file (pip install python-decouple)

# =============================================================================
# BASE DIRECTORY
# =============================================================================
# __file__ = this file (settings.py)
# .resolve() = get the absolute path (no shortcuts like ../)
# .parent = go up one folder (to lms/)
# .parent = go up again (to the project root: LMS Project/)
# So BASE_DIR = "C:/Users/embee/LMS Project/"
# We use this everywhere to build paths relative to the project root
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# SECURITY SETTINGS
# =============================================================================
# SECRET_KEY: A long random string used for:
#   - Signing session cookies (so hackers can't forge them)
#   - CSRF protection tokens
#   - Password reset tokens
# config() reads from .env file first, falls back to the default if not found
SECRET_KEY = config("SECRET_KEY", default="django-insecure-change-me-in-production")

# DEBUG = True: Shows detailed error pages with code tracebacks in the browser
# DEBUG = False: Shows generic error pages (for production — don't leak code to users!)
# cast=bool converts the string "True"/"False" from .env into actual Python boolean
DEBUG = config("DEBUG", default=True, cast=bool)

# Which hostnames/domains this Django site can serve
# Prevents "Host header" attacks where someone fakes the domain name
# The lambda splits "localhost,127.0.0.1" into ["localhost", "127.0.0.1"]
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="localhost,127.0.0.1",
    cast=lambda v: [s.strip() for s in v.split(",")]
)

# =============================================================================
# INSTALLED APPS
# =============================================================================
# Every feature in Django is an "app". This list tells Django which apps to load.
# Order matters for some things (like template resolution).
INSTALLED_APPS = [
    # --- Django's built-in apps ---
    "django.contrib.admin",         # The admin panel at /admin/ — auto-generated CRUD interface
    "django.contrib.auth",          # Authentication system (users, groups, permissions)
    "django.contrib.contenttypes",  # Tracks all models in the project (used by auth & admin)
    "django.contrib.sessions",      # Stores session data (keeps users logged in across requests)
    "django.contrib.messages",      # Flash messages ("Success!", "Error!") shown once then disappear
    "django.contrib.staticfiles",   # Manages static files (CSS, JS, images) during development

    # --- Third-party apps (installed via pip) ---
    "rest_framework",               # Django REST Framework — builds the REST API
    "corsheaders",                  # Handles Cross-Origin requests (needed if React is on a different port)
    "django_filters",               # Adds ?field=value filtering to API endpoints

    # --- Our custom apps (in the apps/ folder) ---
    # Each app is a self-contained feature module. Django finds them via their apps.py file.
    "apps.accounts",        # Authentication & Users: login, register, profiles, roles
    "apps.courses",         # Course Management: departments, semesters, courses, enrollment
    "apps.assignments",     # Assignments: create, submit, grade
    "apps.students",        # Student-specific: dashboard, timetable, GPA
    "apps.lecturers",       # Lecturer-specific: dashboard, manage courses, grade work
    "apps.administration",  # Admin-specific: manage everything, analytics
    "apps.communication",   # Communication: announcements, notifications, messaging
    "apps.core",            # Shared utilities: permissions, audit logs, file validation
]

# =============================================================================
# MIDDLEWARE
# =============================================================================
# Middleware are "layers" that every HTTP request/response passes through.
# Think of them as security checkpoints at an airport — each one checks something.
#
# REQUEST FLOW:  Browser → Middleware (top to bottom) → View → Response
# RESPONSE FLOW: View → Middleware (bottom to top) → Browser
MIDDLEWARE = [
    # Security headers (HTTPS redirect, XSS protection, etc.)
    "django.middleware.security.SecurityMiddleware",

    # Serves static files efficiently in production (CSS, JS)
    "whitenoise.middleware.WhiteNoiseMiddleware",

    # Manages user sessions — reads/writes session cookies on every request
    "django.contrib.sessions.middleware.SessionMiddleware",

    # Adds CORS headers so React (on port 3000) can call Django (on port 8000)
    "corsheaders.middleware.CorsMiddleware",

    # Handles common operations: URL normalization, content-length header
    "django.middleware.common.CommonMiddleware",

    # CSRF protection — prevents cross-site request forgery attacks
    # Requires {% csrf_token %} in every POST form
    "django.middleware.csrf.CsrfViewMiddleware",

    # Attaches the logged-in user to request.user on every request
    # Without this, request.user would always be AnonymousUser
    "django.contrib.auth.middleware.AuthenticationMiddleware",

    # Makes flash messages available in templates via {% if messages %}
    "django.contrib.messages.middleware.MessageMiddleware",

    # Prevents your site from being embedded in an iframe (clickjacking protection)
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# =============================================================================
# URL CONFIGURATION
# =============================================================================
# Tells Django which file contains the root URL patterns.
# When a request comes in, Django starts looking for matching URLs in this file.
# "lms.urls" means lms/urls.py
ROOT_URLCONF = "lms.urls"

# =============================================================================
# TEMPLATES
# =============================================================================
# Templates are HTML files with special Django tags like {% if %}, {{ variable }}, etc.
# This tells Django where to find them and how to render them.
TEMPLATES = [
    {
        # Use Django's built-in template engine (there are others like Jinja2)
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        # DIRS: Extra folders to look for templates (besides each app's templates/ folder)
        # BASE_DIR / "templates" = the project-level templates/ folder (for base.html, navbar, etc.)
        "DIRS": [BASE_DIR / "templates"],

        # APP_DIRS: Also look in each app's templates/ folder
        # e.g., apps/accounts/templates/accounts/login.html
        "APP_DIRS": True,

        "OPTIONS": {
            # Context processors inject variables into EVERY template automatically
            "context_processors": [
                "django.template.context_processors.debug",     # Adds "debug" variable
                "django.template.context_processors.request",   # Adds "request" variable
                "django.contrib.auth.context_processors.auth",  # Adds "user" and "perms" variables
                "django.contrib.messages.context_processors.messages",  # Adds "messages" variable
            ],
        },
    },
]

# =============================================================================
# WSGI / ASGI
# =============================================================================
# WSGI = Web Server Gateway Interface — the standard for Python web apps
# This tells production servers (like Gunicorn) how to connect to our Django app
WSGI_APPLICATION = "lms.wsgi.application"

# =============================================================================
# DATABASE
# =============================================================================
# Configures which database Django connects to.
# By default: SQLite (a single file, perfect for development)
# In production: Switch to PostgreSQL by changing DB_ENGINE in .env
#
# Django's ORM (Object-Relational Mapper) translates Python code into SQL,
# so you write Python classes (models) and Django creates the database tables.
DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE", default="django.db.backends.sqlite3"),  # Database type
        "NAME": config("DB_NAME", default=str(BASE_DIR / "db.sqlite3")),     # Database name/path
        "USER": config("DB_USER", default=""),           # DB username (empty for SQLite)
        "PASSWORD": config("DB_PASSWORD", default=""),   # DB password (empty for SQLite)
        "HOST": config("DB_HOST", default=""),           # DB server address (empty = localhost)
        "PORT": config("DB_PORT", default=""),           # DB port (empty = default port)
    }
}

# =============================================================================
# PASSWORD VALIDATION
# =============================================================================
# Rules that passwords must follow when users register or change passwords.
# Django checks these automatically in forms and the admin panel.
AUTH_PASSWORD_VALIDATORS = [
    # Password can't be too similar to username, email, first/last name
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    # Password must be at least 8 characters long
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    # Password can't be in a list of 20,000 common passwords ("password123", etc.)
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    # Password can't be entirely numeric ("12345678")
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =============================================================================
# CUSTOM USER MODEL
# =============================================================================
# CRITICAL: This tells Django to use OUR custom User model (in apps/accounts/models.py)
# instead of Django's default User model.
# Our User model adds: role (student/lecturer/admin), phone, profile_picture, etc.
# This MUST be set BEFORE running the first migration!
AUTH_USER_MODEL = "accounts.User"

# =============================================================================
# INTERNATIONALIZATION
# =============================================================================
LANGUAGE_CODE = "en-us"     # Default language
TIME_ZONE = "UTC"           # Default timezone (change to your timezone, e.g., "Africa/Lagos")
USE_I18N = True             # Enable Django's translation system
USE_TZ = True               # Store datetimes in UTC in the database (best practice)

# =============================================================================
# STATIC FILES (CSS, JavaScript, Images)
# =============================================================================
# Static files = files that don't change per user (CSS, JS, logos)
# These are served differently in development vs production.

# URL prefix for static files in HTML: <link href="/static/css/main.css">
STATIC_URL = "static/"

# Extra folders where Django looks for static files (besides each app's static/ folder)
STATICFILES_DIRS = [BASE_DIR / "static"]  # Our project-level static/ folder

# Where "python manage.py collectstatic" copies ALL static files for production
STATIC_ROOT = BASE_DIR / "staticfiles"

# =============================================================================
# MEDIA FILES (User Uploads)
# =============================================================================
# Media files = files uploaded by users (profile pics, assignment PDFs)
# These are different from static files — they're dynamic and user-specific.

# URL prefix for uploaded files: <img src="/media/profiles/photo.jpg">
MEDIA_URL = "media/"

# Folder on disk where uploaded files are saved
MEDIA_ROOT = BASE_DIR / "media"

# =============================================================================
# DEFAULT PRIMARY KEY TYPE
# =============================================================================
# When Django creates a model, it auto-adds an "id" field as the primary key.
# BigAutoField = auto-incrementing integer that can go up to 9.2 quintillion
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =============================================================================
# AUTHENTICATION URLS
# =============================================================================
# LOGIN_URL: Where to redirect unauthenticated users who try to access @login_required pages
LOGIN_URL = "/accounts/login/"

# LOGIN_REDIRECT_URL: Where to send users after successful login (if no "next" parameter)
LOGIN_REDIRECT_URL = "/dashboard/"

# LOGOUT_REDIRECT_URL: Where to send users after they log out
LOGOUT_REDIRECT_URL = "/"

# =============================================================================
# DJANGO REST FRAMEWORK (DRF) CONFIGURATION
# =============================================================================
# These settings apply to ALL API endpoints by default.
# Individual views can override any of these.
REST_FRAMEWORK = {
    # How the API identifies who is making the request
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # SessionAuthentication: Uses browser cookies (for when you browse the API in a browser)
        "rest_framework.authentication.SessionAuthentication",
        # JWTAuthentication: Uses tokens in the Authorization header (for React/mobile apps)
        # Client sends: Authorization: Bearer <token>
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],

    # Who is ALLOWED to access API endpoints (applied to every view by default)
    "DEFAULT_PERMISSION_CLASSES": [
        # IsAuthenticated: Only logged-in users can access the API
        # Anonymous users get a 401 Unauthorized response
        "rest_framework.permissions.IsAuthenticated",
    ],

    # How list endpoints can be filtered, searched, and sorted
    "DEFAULT_FILTER_BACKENDS": [
        # DjangoFilterBackend: Filter by exact field values → /api/courses/?department=1
        "django_filters.rest_framework.DjangoFilterBackend",
        # SearchFilter: Full-text search → /api/courses/?search=mathematics
        "rest_framework.filters.SearchFilter",
        # OrderingFilter: Sort results → /api/courses/?ordering=-created_at
        "rest_framework.filters.OrderingFilter",
    ],

    # Pagination: Don't return ALL records at once — split into pages
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,  # 20 items per page → /api/courses/?page=2
}

# =============================================================================
# EMAIL CONFIGURATION
# =============================================================================
# Read from .env file. Console backend prints emails to terminal during development.
EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
