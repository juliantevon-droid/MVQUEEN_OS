from __future__ import annotations

import os
import threading
import time
from typing import Any

import requests

TOKEN_ENDPOINT_TEMPLATE = "https://{shop}/admin/oauth/access_token"


class ShopifyClientCredentialsError(RuntimeError):
    """Raised when Shopify cannot issue an app access token."""


class ShopifyClientCredentials:
    """Small server-side token provider for an app acting on its own store.

    Shopify client-credentials tokens expire after 24 hours. The provider keeps
    the token only in process memory and refreshes it before expiry. Secrets
    remain environment-only.
    """

    def __init__(
        self,
        *,
        store_domain: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        timeout_seconds: float | None = None,
    ) -> None:
        self.store_domain = (store_domain or os.getenv("SHOPIFY_STORE_DOMAIN", "")).strip()
        self.client_id = client_id or os.getenv("SHOPIFY_API_KEY", "")
        self.client_secret = client_secret or os.getenv("SHOPIFY_API_SECRET", "")
        self.timeout_seconds = timeout_seconds or float(os.getenv("SHOPIFY_TIMEOUT_SECONDS", "30"))
        self._access_token: str | None = None
        self._expires_at = 0.0
        self._lock = threading.Lock()

    def get_access_token(self) -> str:
        now = time.time()
        if self._access_token and now < self._expires_at - 300:
            return self._access_token

        with self._lock:
            now = time.time()
            if self._access_token and now < self._expires_at - 300:
                return self._access_token
            return self._request_token()

    def _request_token(self) -> str:
        if not self.store_domain:
            raise ShopifyClientCredentialsError("SHOPIFY_STORE_DOMAIN is required")
        if not self.client_id:
            raise ShopifyClientCredentialsError("SHOPIFY_API_KEY is required")
        if not self.client_secret:
            raise ShopifyClientCredentialsError("SHOPIFY_API_SECRET is required")

        response = requests.post(
            TOKEN_ENDPOINT_TEMPLATE.format(shop=self.store_domain),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
            timeout=self.timeout_seconds,
        )

        if not response.ok:
            raise ShopifyClientCredentialsError(
                f"Shopify token request failed with HTTP {response.status_code}"
            )

        body: dict[str, Any] = response.json()
        token = body.get("access_token")
        expires_in = int(body.get("expires_in", 0) or 0)

        if not token or expires_in <= 0:
            raise ShopifyClientCredentialsError("Shopify returned an invalid access-token response")

        self._access_token = token
        self._expires_at = time.time() + expires_in
        return token

    def status(self) -> dict[str, Any]:
        return {
            "configured": bool(self.store_domain and self.client_id and self.client_secret),
            "authenticated": bool(self._access_token and time.time() < self._expires_at),
            "token_expires_at": self._expires_at or None,
        }


_provider = ShopifyClientCredentials()


def get_authenticated_client(*, dry_run: bool = True):
    from shopify_graphql_client import get_client

    return get_client(
        dry_run=dry_run,
        access_token=_provider.get_access_token(),
    )


def auth_status() -> dict[str, Any]:
    return _provider.status()
