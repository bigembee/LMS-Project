from __future__ import annotations

import re
from re import Pattern
from urllib.parse import ParseResult, parse_qsl, urlparse

from django.core.exceptions import ValidationError
from django.forms import URLField
from django.utils.translation import gettext_lazy as _

from allauth.idp.oidc import app_settings
from allauth.idp.oidc.internal import cimd
from allauth.idp.oidc.models import Client


def is_loopback(parsed_uri: ParseResult) -> bool:
    return parsed_uri.scheme == "http" and parsed_uri.hostname in (
        "127.0.0.1",
        "::1",
    )


def _validate_uri_wildcard_format(uri: str, allow_uri_wildcards: bool) -> None:
    if not allow_uri_wildcards:
        if "*" in uri:
            raise ValidationError(
                _("Wildcards are not allowed unless 'Allow URI wildcards' is enabled.")
            )
    elif uri.count("*") > 1:
        raise ValidationError(
            _(
                "URI '{}' contains more than one wildcard (*). Only one wildcard per URI is allowed."
            ).format(uri)
        )
    else:
        try:
            parsed = urlparse(uri)
        except ValueError as e:
            # it's possible for this to happen with wildcards in ports
            raise ValidationError(_(f"Invalid URI: {e}"))

        if "*" in parsed.scheme or "*" in parsed.path or "*" in parsed.query:
            raise ValidationError(
                _("Wildcards are only allowed in the hostname portion of the URI.")
            )


def _wildcard_to_regex(wildcard: str) -> Pattern[str]:
    pattern = re.escape(wildcard).replace(r"\*", r"[^.]+")
    return re.compile(f"^{pattern}$")


def _is_scheme_hostname_allowed(
    parsed_uri: ParseResult, parsed_allowed_uri: ParseResult, allow_uri_wildcards: bool
) -> bool:
    if parsed_allowed_uri.scheme != parsed_uri.scheme:
        return False

    if (
        allow_uri_wildcards
        and parsed_allowed_uri.hostname
        and "*" in parsed_allowed_uri.hostname
    ):
        allowed_hostname_pattern = _wildcard_to_regex(parsed_allowed_uri.hostname)

        if not parsed_uri.hostname or not allowed_hostname_pattern.match(
            parsed_uri.hostname
        ):
            return False
    else:
        if parsed_allowed_uri.hostname != parsed_uri.hostname:
            return False

    return True


def is_parsed_redirect_uri_allowed(
    parsed_uri: ParseResult, allowed_uri: str, allow_uri_wildcards: bool
) -> bool:
    parsed_allowed_uri = urlparse(allowed_uri)

    if not _is_scheme_hostname_allowed(
        parsed_uri, parsed_allowed_uri, allow_uri_wildcards
    ):
        return False

    if parsed_allowed_uri.path != parsed_uri.path:
        return False

    if not is_loopback(parsed_allowed_uri):
        if parsed_allowed_uri.port != parsed_uri.port:
            return False

    if not set(parse_qsl(parsed_allowed_uri.query)).issubset(
        set(parse_qsl(parsed_uri.query))
    ):
        return False

    return True


def is_redirect_uri_allowed(
    uri: str, allowed_uris: list[str], allow_uri_wildcards: bool
) -> bool:
    parsed_uri = urlparse(uri)
    return any(
        is_parsed_redirect_uri_allowed(parsed_uri, allowed_uri, allow_uri_wildcards)
        for allowed_uri in allowed_uris
    )


def is_origin_allowed(
    origin: str, allowed_origins: list[str], allow_uri_wildcards: bool
) -> bool:
    parsed_origin = urlparse(origin)

    for allowed_origin in allowed_origins:
        parsed_allowed_origin = urlparse(allowed_origin)
        if (
            not _is_scheme_hostname_allowed(
                parsed_origin, parsed_allowed_origin, allow_uri_wildcards
            )
            or parsed_origin.username != parsed_allowed_origin.username
            or parsed_origin.password != parsed_allowed_origin.password
            or parsed_origin.port != parsed_allowed_origin.port
        ):
            continue
        else:
            return True

    return False


def is_post_logout_redirect_uri_allowed(
    client: Client, post_logout_redirect_uri: str, parsed_uri: ParseResult
) -> bool:
    registered_uris = client.get_post_logout_redirect_uris()
    if registered_uris:
        # Logout redirect URIs were explicitly set, so only accept those.
        return is_redirect_uri_allowed(
            post_logout_redirect_uri, registered_uris, client.allow_uri_wildcards
        )
    # No explicit redirect URIs configured. Let's at least check the netloc
    # against redirect_uris. But, we can only do so for proper http(s) urls,
    # as app uris like 'org.allauth.app://logout' don't have that.
    if parsed_uri.scheme in ("http", "https"):
        return is_origin_allowed(
            post_logout_redirect_uri,
            client.get_redirect_uris(),
            client.allow_uri_wildcards,
        )
    else:
        # Our caller did already perform scheme validation, meaning,
        # scheme 'org.allauth.app' would pass, and 'com.evil.app' would not.
        return True


def get_used_schemes(client: Client) -> set[str]:
    schemes = set()
    for uri in client.get_redirect_uris() + client.get_post_logout_redirect_uris():
        parsed = urlparse(uri)
        if parsed.scheme:
            schemes.add(parsed.scheme)
    return schemes


def clean_post_logout_redirect_uri(
    post_logout_redirect_uri: str | None, client: Client | None
) -> str | None:
    """
    This URI SHOULD use the https scheme and MAY contain port, path, and
    query parameter components; however, it MAY use the http scheme, provided
    that the Client Type is confidential, as defined in Section 2.1 of OAuth 2.0
    [RFC6749], and provided the OP allows the use of http RP URIs. The URI MAY
    use an alternate scheme, such as one that is intended to identify a callback
    into a native application. The value MUST have been previously registered
    with the OP, either using the post_logout_redirect_uris Registration
    parameter or via another mechanism. An id_token_hint is also RECOMMENDED
    when this parameter is included.
    """
    if not client:
        # Without a client we have no way of validating this part:
        # "...The value MUST have been previously registered...".
        return None
    if not post_logout_redirect_uri:
        return None
    allowed_schemes = {"https"}
    allowed_schemes.update(get_used_schemes(client))
    if client.type == Client.Type.CONFIDENTIAL:
        allowed_schemes.add("http")
    parsed = urlparse(post_logout_redirect_uri)
    if not parsed.scheme or parsed.scheme not in allowed_schemes:
        raise ValidationError(URLField.default_error_messages["invalid"])
    if parsed.scheme in ("http", "https"):
        URLField().clean(post_logout_redirect_uri)
    if not is_post_logout_redirect_uri_allowed(
        client, post_logout_redirect_uri, parsed
    ):
        raise ValidationError(URLField.default_error_messages["invalid"])
    return post_logout_redirect_uri


def lookup_client(client_id: str) -> Client | None:
    client = Client.objects.filter(id=client_id).first()
    if not app_settings.CIMD_ENABLED:
        return client
    return cimd.lookup_client(client_id, client)


def lookup_public_client(client_id: str) -> Client | None:
    client = lookup_client(client_id)
    if not client:
        return None
    if client.type != Client.Type.PUBLIC:
        return None
    return client
