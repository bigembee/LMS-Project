from __future__ import annotations

from django.urls import include, path
from django.utils.module_loading import import_string


def default_urlpatterns(provider):
    login_view = import_string(f"{provider.get_package()}.views.oauth2_login")
    callback_view = import_string(f"{provider.get_package()}.views.oauth2_callback")

    urlpatterns = [
        path("login/", login_view, name=f"{provider.id}_login"),
        path("login/callback/", callback_view, name=f"{provider.id}_callback"),
    ]

    return [path(f"{provider.get_slug()}/", include(urlpatterns))]
