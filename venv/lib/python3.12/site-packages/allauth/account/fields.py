from __future__ import annotations

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import RegexValidator
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.urls import NoReverseMatch, reverse
from django.utils.functional import lazy
from django.utils.safestring import SafeString, mark_safe
from django.utils.translation import gettext_lazy as _

from allauth.account import app_settings
from allauth.account.adapter import get_adapter


class EmailField(forms.EmailField):
    def __init__(self, *args, **kwargs) -> None:
        kwargs.setdefault("label", _("Email"))
        kwargs.setdefault(
            "widget",
            forms.TextInput(
                attrs={
                    "type": "email",
                    "autocomplete": "email",
                    "placeholder": _("Email address"),
                }
            ),
        )
        super().__init__(*args, **kwargs)

    def clean(self, value):
        return super().clean(value).lower()


class PasswordField(forms.CharField):
    def __init__(self, *args, **kwargs) -> None:
        render_value = kwargs.pop(
            "render_value", app_settings.PASSWORD_INPUT_RENDER_VALUE
        )
        kwargs.setdefault("strip", False)
        kwargs["widget"] = forms.PasswordInput(
            render_value=render_value,
            attrs={"placeholder": kwargs.get("label")},
        )
        autocomplete = kwargs.pop("autocomplete", None)
        if autocomplete is not None:
            kwargs["widget"].attrs["autocomplete"] = autocomplete
        show_reset_help = kwargs.pop("show_reset_help", False)
        if show_reset_help:
            # Lazily evaluation needed to avoid hitting ``reverse()`` at import
            # time.
            kwargs.setdefault("help_text", lazy(self._get_help_text, str, SafeString)())
        super().__init__(*args, **kwargs)

    @staticmethod
    def _get_help_text() -> SafeString:
        try:
            return mark_safe(  # nosec
                render_to_string(
                    f"account/password_reset_help_text.{app_settings.TEMPLATE_EXTENSION}"
                )
            )
        except TemplateDoesNotExist:
            pass

        try:
            reset_url = reverse("account_reset_password")
        except NoReverseMatch:
            return mark_safe("")  # nosec
        else:
            forgot_txt = _("Forgot your password?")
            return mark_safe(f'<a href="{reset_url}">{forgot_txt}</a>')  # nosec


class SetPasswordField(PasswordField):
    user: AbstractBaseUser | None

    def __init__(self, *args, **kwargs) -> None:
        kwargs["autocomplete"] = "new-password"
        kwargs.setdefault(
            "help_text", password_validation.password_validators_help_text_html()
        )
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self, value):
        value = super().clean(value)
        value = get_adapter().clean_password(value, user=self.user)
        return value


class PhoneField(forms.CharField):
    e164_validator = RegexValidator(
        regex=r"^\+[1-9]\d{5,14}$",
        message=_("Enter a phone number including country code (e.g. +1 for the US)."),
        code="invalid_phone",
    )

    def __init__(self, *args, **kwargs) -> None:
        widget = forms.TextInput(
            attrs={"placeholder": _("Phone"), "autocomplete": "tel", "type": "tel"}
        )
        kwargs.setdefault("validators", [self.e164_validator])
        kwargs.setdefault("widget", widget)
        kwargs.setdefault("label", _("Phone"))
        super().__init__(*args, **kwargs)

    def clean(self, value):
        value = super().clean(value)
        if value:
            value = value.replace(" ", "").replace("-", "")
            value = get_adapter().clean_phone(value)
        return value
