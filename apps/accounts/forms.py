"""
forms.py - Django forms for the Accounts app.

WHAT ARE FORMS?
Forms handle user input — they:
    1. Generate HTML form fields (input, select, textarea, etc.)
    2. Validate submitted data (is the email valid? is the username taken?)
    3. Save data to the database (or return errors if validation fails)

TWO TYPES OF FORMS:
    forms.Form        → Manual form — you define every field yourself
    forms.ModelForm   → Auto-generated from a model — fields match model columns

HOW FORMS ARE USED IN VIEWS:
    GET request (loading the page):
        form = RegistrationForm()                    # Create empty form
        return render(request, "register.html", {"form": form})

    POST request (submitting the form):
        form = RegistrationForm(request.POST)        # Fill form with submitted data
        if form.is_valid():                          # Run all validation
            user = form.save()                       # Save to database
            return redirect("success_page")
        # If invalid, form now contains error messages — re-render the template

HOW FORMS ARE USED IN TEMPLATES:
    <form method="post">
        {% csrf_token %}           ← Required for security (prevents CSRF attacks)
        {{ form.as_p }}            ← Renders all form fields as <p> tags
        <button type="submit">Submit</button>
    </form>
"""

from django import forms                                            # Base form classes
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # Built-in auth forms
from .models import User                                             # Our custom User model


class RegistrationForm(UserCreationForm):
    """
    Form for new user registration.

    Extends UserCreationForm which provides:
        - password1 field (the password)
        - password2 field (confirm password — must match password1)
        - Password validation (length, complexity, etc. — from settings.py)

    We add our custom fields via Meta.fields.

    USED IN: views.register_view()
    """
    class Meta:
        model = User  # This form creates/edits User objects

        # Which fields to show in the form, in this order
        # password1 and password2 are provided by UserCreationForm automatically
        fields = ["username", "email", "first_name", "last_name", "role", "password1", "password2"]


class LoginForm(AuthenticationForm):
    """
    Form for user login.

    Extends Django's AuthenticationForm which provides:
        - username field
        - password field
        - Validates credentials against the database
        - Returns the authenticated user via form.get_user()

    We use "pass" because the built-in form already does everything we need.
    You can customize it later (e.g., add "remember me" checkbox, change field widgets).

    USED IN: views.login_view()
    """
    pass


class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating user profile information.

    ModelForm automatically creates form fields that match the model's database columns.
    We list only the fields the user should be able to edit — NOT username, role, or password.

    USED IN: views.profile_view()
    """
    class Meta:
        model = User  # This form edits User objects

        # Only allow editing these fields — role and username are NOT editable through this form
        fields = ["first_name", "last_name", "email", "phone", "date_of_birth", "profile_picture"]
