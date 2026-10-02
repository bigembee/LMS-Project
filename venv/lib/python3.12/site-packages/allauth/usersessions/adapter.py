from __future__ import annotations

from django.utils.module_loading import import_string

from allauth.core.internal.adapter import BaseAdapter
from allauth.usersessions import app_settings


class DefaultUserSessionsAdapter(BaseAdapter):
    """The adapter class allows you to override various functionality of the
    ``allauth.usersessions`` app.  To do so, point
    ``settings.USERSESSIONS_ADAPTER`` to your own class that derives from
    ``DefaultUserSessionsAdapter`` and override the behavior by altering the
    implementation of the methods according to your own needs.
    """

    def end_sessions(self, sessions) -> None:
        for session in sessions:
            session.end()


def get_adapter() -> DefaultUserSessionsAdapter:
    return import_string(app_settings.ADAPTER)()
