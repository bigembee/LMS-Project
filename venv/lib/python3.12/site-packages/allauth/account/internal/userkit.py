from __future__ import annotations

import unicodedata
from collections.abc import Callable

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.db.models import Q
from django.utils.encoding import force_str

from allauth.account import app_settings
from allauth.utils import import_callable


def user_id_to_str(user: AbstractBaseUser) -> str:
    return user._meta.pk.value_to_string(user)


def str_to_user_id(value: str):
    return get_user_model()._meta.pk.to_python(value)


def user_field(user: AbstractBaseUser, field, *args, commit=False):
    """
    Gets or sets (optional) user model fields. No-op if fields do not exist.
    """
    if not field:
        return
    User = get_user_model()
    try:
        field_meta = User._meta.get_field(field)
        max_length = field_meta.max_length  # type:ignore[union-attr]
    except FieldDoesNotExist:
        if not hasattr(user, field):
            return
        max_length = None
    if args:
        # Setter
        v = args[0]
        if v:
            v = v[0:max_length]
        elif v is None and not field_meta.null:  # type:ignore[union-attr]
            v = ""
        setattr(user, field, v)
        if commit:
            user.save(update_fields=[field])
    else:
        # Getter
        return getattr(user, field)


def did_user_login(user: AbstractBaseUser | None) -> bool:
    return user is not None and user.last_login is not None


_user_display_callable = None


def default_user_display(user: AbstractBaseUser) -> str:
    ret = ""
    if app_settings.USER_MODEL_USERNAME_FIELD:
        ret = getattr(user, app_settings.USER_MODEL_USERNAME_FIELD)
    return ret or force_str(user) or force_str(user._meta.verbose_name)


def user_display(user: AbstractBaseUser) -> str:
    global _user_display_callable
    if not _user_display_callable:
        f = getattr(settings, "ACCOUNT_USER_DISPLAY", default_user_display)
        _user_display_callable = import_callable(f)
    return _user_display_callable(user)


def user_username(user: AbstractBaseUser, *args, commit=False):
    if args and not app_settings.PRESERVE_USERNAME_CASING and args[0]:
        args = tuple([args[0].lower()])
    return user_field(user, app_settings.USER_MODEL_USERNAME_FIELD, *args)


def user_email(user: AbstractBaseUser, *args, commit=False):
    if args and args[0]:
        args = tuple([args[0].lower()])
    ret = user_field(user, app_settings.USER_MODEL_EMAIL_FIELD, *args, commit=commit)
    if ret:
        ret = ret.lower()
    return ret


def filter_users_by_username(*username) -> models.QuerySet[AbstractBaseUser]:
    """Return matching users according to the DB collation rules."""
    if app_settings.PRESERVE_USERNAME_CASING:
        qlist = [
            Q(**{f"{app_settings.USER_MODEL_USERNAME_FIELD}__iexact": u})
            for u in username
        ]
        q = qlist[0]
        for q2 in qlist[1:]:
            q = q | q2
        ret = get_user_model()._default_manager.filter(q)
    else:
        ret = get_user_model()._default_manager.filter(
            **{
                f"{app_settings.USER_MODEL_USERNAME_FIELD}__in": [
                    u.lower() for u in username
                ]
            }
        )
    return ret


def get_user_by_username(username: str) -> AbstractBaseUser | None:
    """Returns the user in a DB collation safe manner."""
    users = filter_users_by_username(username)
    ci_users = [
        user
        for user in users
        if (stored_username := user_username(user)) is not None
        and stored_username.lower() == username.lower()
    ]
    return ci_users[0] if len(ci_users) == 1 else None


def unicode_ci_compare(s1: str, s2: str) -> bool:
    """
    Perform case-insensitive comparison of two identifiers, using the
    recommended algorithm from Unicode Technical Report 36, section
    2.11.2(B)(2).
    """
    norm_s1 = unicodedata.normalize("NFKC", s1).casefold()
    norm_s2 = unicodedata.normalize("NFKC", s2).casefold()
    return norm_s1 == norm_s2


def filter_users_by_email(
    email: str,
    *,
    is_active: bool | None = None,
    prefer_verified: bool = False,
    for_login: bool = False,
) -> list:
    """Return list of users by email address

    Typically one, at most just a few in length.  First we look through
    EmailAddress table, than customisable User model table. Add results
    together avoiding SQL joins and deduplicate.

    `prefer_verified`: When looking up users by email, there can be cases where
    users with verified email addresses are preferable above users who did not
    verify their email address. The password reset is such a use case -- if
    there is a user with a verified email than that user should be returned, not
    one of the other users.
    """
    from allauth.account.models import EmailAddress

    compare: Callable[[str, str], bool]
    compare = (lambda a, b: a.lower() == b.lower()) if for_login else unicode_ci_compare

    User = get_user_model()
    email = email.lower()
    mails = list(EmailAddress.objects.filter(email=email).select_related("user"))
    mails = [e for e in mails if compare(e.email, email)]
    is_verified = False
    if prefer_verified:
        verified_mails = list(filter(lambda e: e.verified, mails))
        if verified_mails:
            mails = verified_mails
            is_verified = True
    users = []
    for e in mails:
        users.append(e.user)
    if app_settings.USER_MODEL_EMAIL_FIELD and not is_verified:
        q_dict = {app_settings.USER_MODEL_EMAIL_FIELD: email}
        user_qs = User.objects.filter(**q_dict)
        for user in user_qs.iterator(2000):
            user_email = getattr(user, app_settings.USER_MODEL_EMAIL_FIELD)
            if compare(user_email, email):
                users.append(user)
    if is_active is not None:
        users = [u for u in set(users) if u.is_active == is_active]
    return list(set(users))
