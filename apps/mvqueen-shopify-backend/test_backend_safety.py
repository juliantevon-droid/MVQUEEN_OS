from __future__ import annotations

import base64
import hashlib
import hmac
import os
import tempfile
import unittest
from pathlib import Path

from audit import AuditLog
from catalog_service import preview_products
from internal_auth import require_internal_api_key
from webhook_security import DeliveryDeduplicator, verify_shopify_hmac


class WebhookSecurityTests(unittest.TestCase):
    def test_valid_hmac(self) -> None:
        secret = "test-secret"
        body = b'{"id":123}'
        digest = hmac.new(secret.encode(), body, hashlib.sha256).digest()
        signature = base64.b64encode(digest).decode()
        self.assertTrue(verify_shopify_hmac(body, signature, secret))

    def test_invalid_hmac(self) -> None:
        self.assertFalse(verify_shopify_hmac(b"body", "invalid", "secret"))

    def test_delivery_deduplication(self) -> None:
        guard = DeliveryDeduplicator()
        self.assertFalse(guard.seen("delivery-1"))
        self.assertTrue(guard.seen("delivery-1"))
        self.assertFalse(guard.seen("delivery-2"))


class AuditLogTests(unittest.TestCase):
    def test_persistent_event_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "audit.sqlite3"
            log = AuditLog(path)
            log.record(
                "test_event",
                actor="test",
                shop_domain="example.myshopify.com",
                dry_run=True,
                details={"safe": True},
            )
            events = log.recent()
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0]["event_type"], "test_event")
            self.assertEqual(events[0]["dry_run"], 1)


class CatalogPreviewTests(unittest.TestCase):
    def test_preview_reads_one_bounded_page(self) -> None:
        class FakeClient:
            def __init__(self):
                self.calls = 0
                self.variables = {}

            def execute(self, query, variables=None, **kwargs):
                self.calls += 1
                self.variables = variables or {}
                return {"data": {"products": {"nodes": [{"id": "1", "title": "Test"}], "pageInfo": {"hasNextPage": True}}}}

        client = FakeClient()
        result = preview_products(client, first=50)
        self.assertEqual(client.calls, 1)
        self.assertEqual(client.variables["first"], 50)
        self.assertEqual(result["count_returned"], 1)


class InternalAuthTests(unittest.TestCase):
    def test_development_allows_missing_key(self) -> None:
        old_env = os.environ.pop("MVQUEEN_INTERNAL_API_KEY", None)
        old_mode = os.environ.get("MVQUEEN_ENV")
        os.environ["MVQUEEN_ENV"] = "development"
        try:
            require_internal_api_key(None)
        finally:
            if old_env is not None:
                os.environ["MVQUEEN_INTERNAL_API_KEY"] = old_env
            else:
                os.environ.pop("MVQUEEN_INTERNAL_API_KEY", None)
            if old_mode is not None:
                os.environ["MVQUEEN_ENV"] = old_mode
            else:
                os.environ.pop("MVQUEEN_ENV", None)

    def test_configured_key_rejects_wrong_key(self) -> None:
        from fastapi import HTTPException
        old_env = os.environ.get("MVQUEEN_INTERNAL_API_KEY")
        os.environ["MVQUEEN_INTERNAL_API_KEY"] = "expected"
        try:
            with self.assertRaises(HTTPException):
                require_internal_api_key("wrong")
        finally:
            if old_env is None:
                os.environ.pop("MVQUEEN_INTERNAL_API_KEY", None)
            else:
                os.environ["MVQUEEN_INTERNAL_API_KEY"] = old_env


if __name__ == "__main__":
    unittest.main()
