from __future__ import annotations

import hmac
import os

from fastapi import HTTPException


def require_internal_api_key(provided_key: str | None) -> None:
    """Protect operational endpoints with a server-side key.

    Development remains usable without a key. Staging/production fail closed
    unless MVQUEEN_INTERNAL_API_KEY is configured.
    """
    expected = os.getenv("MVQUEEN_INTERNAL_API_KEY", "").strip()
    environment = os.getenv("MVQUEEN_ENV", "development").strip().lower()

    if not expected:
        if environment in {"development", "test"}:
            return
        raise HTTPException(status_code=503, detail="Internal API authentication is not configured")

    if not provided_key or not hmac.compare_digest(provided_key, expected):
        raise HTTPException(status_code=401, detail="Unauthorized")
