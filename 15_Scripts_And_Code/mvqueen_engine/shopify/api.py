"""Safe Shopify Admin API client foundation.

Live writes are opt-in. Credentials are read from environment variables and
never stored in source control.
"""
from __future__ import annotations

import os
from typing import Any
import requests


class ShopifyAPIError(RuntimeError):
    """Raised when Shopify returns an unsuccessful response."""


class ShopifyClient:
    def __init__(self, shop_domain: str | None = None, token: str | None = None,
                 api_version: str | None = None, timeout: int = 30, dry_run: bool = True):
        self.shop_domain = (shop_domain or os.getenv("SHOPIFY_SHOP_DOMAIN", "")).strip()
        self.token = token or os.getenv("SHOPIFY_ADMIN_API_TOKEN", "")
        self.api_version = api_version or os.getenv("SHOPIFY_API_VERSION", "2025-01")
        self.timeout = timeout
        self.dry_run = dry_run
        if not self.shop_domain:
            raise ValueError("SHOPIFY_SHOP_DOMAIN is required")
        self.base_url = f"https://{self.shop_domain}/admin/api/{self.api_version}"
        self.session = requests.Session()
        self.session.headers.update({
            "X-Shopify-Access-Token": self.token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def request(self, method: str, path: str, *, payload: dict[str, Any] | None = None,
                allow_write: bool = False) -> dict[str, Any]:
        if method.upper() in {"POST", "PUT", "PATCH", "DELETE"} and (self.dry_run or not allow_write):
            return {"dry_run": True, "method": method.upper(), "path": path, "payload": payload or {}}
        response = self.session.request(method, f"{self.base_url}{path}", json=payload,
                                        timeout=self.timeout)
        if not response.ok:
            raise ShopifyAPIError(f"Shopify {response.status_code}: {response.text[:500]}")
        return response.json() if response.content else {}

    def get(self, path: str) -> dict[str, Any]:
        return self.request("GET", path)

    def write(self, method: str, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self.request(method, path, payload=payload, allow_write=True)
