from __future__ import annotations

import base64
import hashlib
import hmac
import os
from collections import deque
from threading import Lock
from time import time


class WebhookSecurityError(ValueError):
    pass


def verify_shopify_hmac(raw_body: bytes, provided_hmac: str | None, secret: str | None = None) -> bool:
    """Verify Shopify's Base64 HMAC using the raw request body."""
    if not provided_hmac:
        return False
    secret = secret or os.getenv("SHOPIFY_API_SECRET", "")
    if not secret:
        raise WebhookSecurityError("SHOPIFY_API_SECRET is required for webhook verification")

    digest = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).digest()
    expected = base64.b64encode(digest).decode("ascii")
    return hmac.compare_digest(expected, provided_hmac)


class DeliveryDeduplicator:
    """Small in-memory guard against duplicate webhook delivery IDs.

    Production deployments should replace this with shared persistent storage
    so multiple workers cannot process the same delivery concurrently.
    """

    def __init__(self, max_items: int = 5000, ttl_seconds: int = 86400) -> None:
        self.max_items = max_items
        self.ttl_seconds = ttl_seconds
        self._seen: dict[str, float] = {}
        self._order: deque[str] = deque()
        self._lock = Lock()

    def seen(self, delivery_id: str | None) -> bool:
        if not delivery_id:
            return False
        now = time()
        with self._lock:
            while self._order and (now - self._seen.get(self._order[0], now)) > self.ttl_seconds:
                old = self._order.popleft()
                self._seen.pop(old, None)
            if delivery_id in self._seen:
                return True
            self._seen[delivery_id] = now
            self._order.append(delivery_id)
            while len(self._order) > self.max_items:
                old = self._order.popleft()
                self._seen.pop(old, None)
        return False
