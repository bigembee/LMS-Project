from __future__ import annotations

from typing import Any

from allauth.core.internal import jwkkit
from allauth.core.internal.deferred import jwt
from allauth.idp.oidc.adapter import get_adapter
from allauth.idp.oidc.models import Token


def decode_jwt_token(
    value: str, *, client_id: str | None = None, verify_exp: bool, verify_iss: bool
) -> dict[str, Any] | None:
    if not value:
        return None
    try:
        headers = jwt.get_unverified_header(value)

        if "kid" not in headers:
            return None

        adapter = get_adapter()
        for key in adapter.list_private_keys(is_active=True):
            jwk_dict, private_key = jwkkit.load_jwk_from_pem(key.pem)
            if jwk_dict["kid"] == headers["kid"]:
                break
        else:
            return None

        issuer: str | None = None
        audience: str | None = None
        if client_id:
            audience = client_id
        if verify_iss:
            issuer = adapter.get_issuer()
        return jwt.decode(
            value,
            key=private_key.public_key(),
            algorithms=["RS256"],
            options={
                "verify_signature": True,
                "verify_iss": verify_iss,
                "verify_aud": client_id is not None,
                "verify_exp": verify_exp,
            },
            audience=audience,
            issuer=issuer,
        )
    except jwt.PyJWTError:
        return None


def is_jwt_token(token: str) -> bool:
    # Same check as done by the `JWTToken` class of `oauthlib`
    # count == "2" should be sufficient as currently only JWS as AccessTokens is supported,
    # but count == "4" allows also for JWE, if that is added in the future.
    # This is more of a "loose" check, but as those JWT that aren't detected using this check
    # will be rejected by the verify_request anyways, we can use the same logic here.
    return (
        isinstance(token, str) and token.startswith("ey") and token.count(".") in (2, 4)
    )


def determine_token_type(
    token: str, token_type_hint: str | None
) -> tuple[list[Token.Type] | None, list[Token.Type] | None]:
    """
    https://datatracker.ietf.org/doc/html/rfc7009#section-2.1
    > token_type_hint  OPTIONAL.  A hint about the type of the token
    >   submitted for revocation.  Clients MAY pass this parameter in
    >   order to help the authorization server to optimize the token
    >   lookup.  If the server is unable to locate the token using
    >   the given hint, it MUST extend its search across all of its
    >   supported token types.  An authorization server MAY ignore
    >   this parameter, particularly if it is able to detect the
    >   token type automatically.  This specification defines two
    >   such values:

    >   * access_token: An access token as defined in [RFC6749],
    >     Section 1.4

    >   * refresh_token: A refresh token as defined in [RFC6749],
    >     Section 1.5

    >   Specific implementations, profiles, and extensions of this
    >   specification MAY define other values for this parameter
    >   using the registry defined in Section 4.1.2.

    Returns a tuple of (token_types_to_try, token_type_for_error_response)
    """

    # This allows us to still handle JWT tokens when the configured access token format has been changed
    if is_jwt_token(token):
        payload = decode_jwt_token(token, verify_exp=True, verify_iss=True)
        if payload:
            return (
                (
                    [Token.Type.ACCESS_TOKEN]
                    if payload.get("token_use") == "access"
                    else None
                ),
                None,
            )
        # In theory, an opaque token could start with "ey...", so continue.
    default = ([Token.Type.ACCESS_TOKEN, Token.Type.REFRESH_TOKEN], None)
    if not isinstance(token_type_hint, str):
        return default
    return {
        "access_token": ([Token.Type.ACCESS_TOKEN], [Token.Type.REFRESH_TOKEN]),
        "refresh_token": ([Token.Type.REFRESH_TOKEN], [Token.Type.ACCESS_TOKEN]),
    }.get(token_type_hint, default)
