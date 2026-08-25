"""
urls.py - URL patterns for the Accounts app.

HOW URL ROUTING WORKS:
    1. A request comes in: /accounts/login/
    2. lms/urls.py matches "accounts/" and passes "login/" to this file
    3. This file matches "login/" and calls views.login_view

THE NAME PARAMETER:
    Each URL has a name (e.g., name="login").
    This lets you reference URLs by name instead of hardcoding paths:
        - In templates: {% url 'accounts:login' %}  →  /accounts/login/
        - In views:     redirect("accounts:login")  →  /accounts/login/
    The format is "app_name:url_name"

    If you ever change the URL path (e.g., "login/" → "sign-in/"),
    all the named references still work — you only change it here, in one place.

APP_NAME:
    app_name = "accounts" creates a namespace.
    Without it, if two apps both have a URL named "login", Django wouldn't know which one you mean.
    With namespaces: "accounts:login" vs "other_app:login" — no ambiguity.
"""

from django.urls import path   # path() connects a URL pattern to a view function
from . import views            # Import all view functions from views.py in the same folder
                               # "." means "current package" (apps/accounts/)

# Namespace for this app — used in templates and redirect() calls
# Example: {% url 'accounts:login' %} → /accounts/login/
app_name = "accounts"

# Each path() maps a URL to a view function:
#   path("url-pattern/", view_function, name="url_name")
urlpatterns = [
    # /accounts/register/ → register_view() → shows/processes registration form
    path("register/", views.register_view, name="register"),

    # /accounts/login/ → login_view() → shows/processes login form
    path("login/", views.login_view, name="login"),

    # /accounts/logout/ → logout_view() → logs user out, redirects to login
    path("logout/", views.logout_view, name="logout"),

    # /accounts/profile/ → profile_view() → shows/edits user profile (requires login)
    path("profile/", views.profile_view, name="profile"),

    # /accounts/password-reset/ → password_reset_view() → password reset flow
    path("password-reset/", views.password_reset_view, name="password_reset"),

    # /accounts/dashboard/ → dashboard_redirect() → redirects to role-specific dashboard
    # This is the landing page after login (LOGIN_REDIRECT_URL in settings.py)
    path("dashboard/", views.dashboard_redirect, name="dashboard_redirect"),
]
