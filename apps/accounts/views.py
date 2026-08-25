"""
views.py - Request handlers for the Accounts app.

WHAT ARE VIEWS?
Views are Python functions (or classes) that:
    1. Receive an HTTP request (from the browser)
    2. Do something (query the database, process a form, etc.)
    3. Return an HTTP response (usually an HTML page)

HOW REQUESTS REACH VIEWS:
    Browser → lms/urls.py → "accounts/" matches → apps/accounts/urls.py → "login/" matches → login_view()

THE REQUEST OBJECT:
    Every view receives a "request" object that contains:
        - request.method: "GET" (loading a page) or "POST" (submitting a form)
        - request.user: the currently logged-in user (or AnonymousUser)
        - request.POST: form data submitted via POST
        - request.FILES: uploaded files
        - request.GET: query parameters from the URL (?page=2)

FUNCTIONS USED:
    render()   → loads an HTML template, fills in variables, returns it as a response
    redirect() → sends the browser to a different URL (HTTP 302 redirect)
"""

from django.shortcuts import render, redirect                   # render templates, redirect to URLs
from django.contrib.auth import login, logout                   # Django's login/logout functions
from django.contrib.auth.decorators import login_required       # Decorator: must be logged in to access
from django.contrib import messages                             # Flash messages ("Success!", "Error!")


def register_view(request):
    """
    Handle user registration.

    GET request: Display the empty registration form
    POST request: Process the submitted form, create the user, log them in

    FLOW: User visits /accounts/register/ → sees form → fills it → submits →
          form validates → user created in DB → user logged in → redirect to dashboard

    TODO: Implement this — use RegistrationForm from forms.py
    Example implementation:
        if request.method == "POST":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()           # Creates user in the database
                login(request, user)         # Log them in immediately
                messages.success(request, "Registration successful!")
                return redirect("accounts:dashboard_redirect")
        else:
            form = RegistrationForm()
        return render(request, "accounts/register.html", {"form": form})
    """
    return render(request, "accounts/register.html")


def login_view(request):
    """
    Handle user login.

    GET request: Display the login form
    POST request: Validate credentials, log user in, redirect to dashboard

    FLOW: User visits /accounts/login/ → enters username & password → submits →
          Django checks credentials → if valid, creates a session → redirect to dashboard

    TODO: Implement this — use LoginForm from forms.py or Django's AuthenticationForm
    """
    return render(request, "accounts/login.html")


def logout_view(request):
    """
    Handle user logout.

    logout() clears the user's session data (the cookie that keeps them logged in).
    After logout, redirect them to the login page.

    "accounts:login" is a named URL — it resolves to /accounts/login/
    The format is "app_name:url_name" (defined in urls.py)
    """
    logout(request)                         # Clear the session — user is now logged out
    return redirect("accounts:login")       # Send them to the login page


@login_required  # This decorator checks if the user is logged in. If not, redirects to LOGIN_URL (settings.py)
def profile_view(request):
    """
    Display and update the user's profile.

    GET request: Show the profile page with current user info
    POST request: Update profile with new data

    @login_required ensures only logged-in users can access this.
    If an anonymous user tries to visit /accounts/profile/, they're redirected to /accounts/login/

    TODO: Implement this — use ProfileUpdateForm from forms.py
    """
    return render(request, "accounts/profile.html")


def password_reset_view(request):
    """
    Handle password reset.

    FLOW:
    1. User visits /accounts/password-reset/ and enters their email
    2. Django sends a password reset email with a unique token link
    3. User clicks the link, enters a new password
    4. Password is updated in the database

    TODO: Implement using Django's built-in password reset views
    Django provides these ready-made: PasswordResetView, PasswordResetConfirmView, etc.
    """
    return render(request, "accounts/password_reset.html")


@login_required
def dashboard_redirect(request):
    """
    Smart redirect — sends users to their role-specific dashboard.

    This is called after login. Instead of sending everyone to the same page,
    we check their role and redirect accordingly:
        - Students  → /students/dashboard/
        - Lecturers → /lecturers/dashboard/
        - Admins    → /administration/dashboard/

    FLOW:
        User logs in → LOGIN_REDIRECT_URL sends them to /dashboard/ →
        this view checks request.user.role → redirects to the right dashboard

    "students:dashboard" is a named URL that resolves to /students/dashboard/
    The format is "app_name:url_name" (both defined in the app's urls.py)
    """
    user = request.user  # The currently logged-in user (set by AuthenticationMiddleware)

    if user.is_student:
        return redirect("students:dashboard")           # → /students/dashboard/
    elif user.is_lecturer:
        return redirect("lecturers:dashboard")          # → /lecturers/dashboard/
    elif user.is_admin_user:
        return redirect("administration:dashboard")     # → /administration/dashboard/

    # Fallback — if role is somehow not set, go to the profile page
    return redirect("accounts:profile")
