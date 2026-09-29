"""Deferred (lazy) imports for heavyweight optional dependencies.

Importing ``jwt`` and ``cryptography`` at boot costs ~8MB of RSS, yet many
deployments configure providers in settings without ever verifying a token
(Celery workers, admin-only services, ...). Rather than sprinkling function
local ``import jwt`` statements around the codebase -- which is easy to
regress, since a single stray top-level ``import jwt`` silently negates the
saving -- modules import these proxies once, at the top, and use them exactly
as they would the real module::

    from allauth.core.internal.deferred import jwt

    def verify(token, key):
        return jwt.decode(token, key, algorithms=["RS256"])

The underlying module (and any submodule accessed through it) is not imported
until the first attribute access, which happens the first time a token is
actually processed -- well after boot.
"""

from __future__ import annotations

import importlib
import importlib.util
from types import ModuleType
from typing import TYPE_CHECKING, Any


class LazyModule:
    """A stand-in for a module that imports the real thing on first use.

    Attribute access resolves against the real module once loaded. Missing
    attributes that name an importable submodule (e.g.
    ``cryptography.hazmat``) resolve to a nested :class:`LazyModule`, so deep
    chains such as ``cryptography.hazmat.primitives.serialization`` stay lazy
    all the way down.
    """

    def __init__(self, name: str) -> None:
        object.__setattr__(self, "_lazy_name", name)
        object.__setattr__(self, "_lazy_module", None)

    def _resolve(self) -> ModuleType:
        module = object.__getattribute__(self, "_lazy_module")
        if module is None:
            module = importlib.import_module(
                object.__getattribute__(self, "_lazy_name")
            )
            object.__setattr__(self, "_lazy_module", module)
        return module

    def __getattr__(self, attr: str) -> Any:
        # __getattr__ only fires for names not found the normal way, so it
        # never shadows _resolve/_lazy_* which live in the instance/class dict.
        module = self._resolve()
        try:
            return getattr(module, attr)
        except AttributeError:
            name = object.__getattribute__(self, "_lazy_name")
            full = f"{name}.{attr}"
            if importlib.util.find_spec(full) is not None:
                return LazyModule(full)
            raise

    def __repr__(self) -> str:
        name = object.__getattribute__(self, "_lazy_name")
        loaded = object.__getattribute__(self, "_lazy_module") is not None
        state = "loaded" if loaded else "deferred"
        return f"<LazyModule {name!r} ({state})>"


if TYPE_CHECKING:
    # Type checkers bind these names to the real modules, so call sites get
    # the actual signatures -- and can annotate with e.g.
    # ``cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey`` -- while
    # importing nothing at runtime. Submodules are spelled out because an
    # ``import cryptography`` alone does not make them resolvable.
    import cryptography.hazmat.backends
    import cryptography.hazmat.primitives.asymmetric.rsa
    import cryptography.hazmat.primitives.ciphers
    import cryptography.hazmat.primitives.serialization
    import cryptography.x509
    import jwt
    import jwt.algorithms
    import jwt.exceptions
else:
    jwt = LazyModule("jwt")
    cryptography = LazyModule("cryptography")
