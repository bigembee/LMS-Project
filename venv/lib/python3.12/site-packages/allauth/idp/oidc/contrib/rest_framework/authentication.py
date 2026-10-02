from __future__ import annotations

from django.http import HttpRequest

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import PermissionDenied

from allauth.idp.oidc.internal.oauthlib.server import get_server
from allauth.idp.oidc.internal.oauthlib.utils import (
    extract_params,
    get_validator_context,
)
from allauth.idp.oidc.internal.resources import is_resources_subset


class TokenAuthentication(BaseAuthentication):
    """
    Use the OIDC access token to authenticate the request.
    """

    def authenticate(self, request: HttpRequest):
        server = get_server()
        orequest = extract_params(request)
        valid, orequest = server.verify_request(*orequest, scopes=[])
        if not valid:
            return None
        access_token = get_validator_context().access_token
        if access_token:
            resources = access_token.get_resources()
            if not is_resources_subset(
                [request.build_absolute_uri(request.path)], resources
            ):
                raise PermissionDenied("Invalid target resource.")

        return orequest.user, access_token
