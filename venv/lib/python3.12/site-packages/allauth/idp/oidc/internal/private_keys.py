from __future__ import annotations

import math
from typing import TYPE_CHECKING, Literal

from django.utils import timezone


if TYPE_CHECKING:
    from allauth.idp.oidc.models import PrivateKey


def filter_keys(
    keys: list[PrivateKey],
    *,
    did_activate: Literal[True] | None = None,
    is_active: Literal[True] | None = None,
) -> list[PrivateKey]:
    now = timezone.now()
    return [
        key
        for key in keys
        # Activated
        if (not did_activate or key.not_before is None or key.not_before <= now)
        # Not expired
        and (not is_active or key.expires_at is None or key.expires_at > now)
    ]


def pick_signing_key(keys: list[PrivateKey]) -> PrivateKey | None:
    """
    Returns the key that should sign new tokens: the most recently issued one.
    Introducing a newer key is therefore what rotates signing away from older
    keys.  A key without an ``issued_at`` (e.g. the legacy
    ``IDP_OIDC_PRIVATE_KEY``) is treated as oldest, so any dated key takes
    precedence.
    """
    if not keys:
        return None
    return max(keys, key=_signing_priority)


def _signing_priority(key: PrivateKey) -> float:
    ts = key.issued_at or key.not_before
    return ts.timestamp() if ts is not None else -math.inf
