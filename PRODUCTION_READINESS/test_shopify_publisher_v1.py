"""Tests for the controlled Shopify publisher V1."""
from __future__ import annotations

import unittest

from SHOPIFY_PUBLISHER_V1 import ShopifyPublisherError, build_product_payload, publish_to_shopify


class FakeClient:
    def __init__(self, result=True):
        self.result = result
        self.calls = []

    def update_product(self, product_id, payload):
        self.calls.append((product_id, payload))
        return self.result


def record():
    return {
        "identity": {"product_id": "123"},
        "category": {"product_type": "dress"},
        "copy": {"title": "Midnight Satin", "description": "A polished evening silhouette."},
        "merchandising": {"tags": ["MVQueen", "Evening"]},
    }


class ShopifyPublisherV1Tests(unittest.TestCase):
    def test_payload_is_narrow_and_preserves_protected_scope(self):
        payload = build_product_payload(record())
        self.assertEqual(payload["id"], "123")
        self.assertEqual(payload["vendor"], "MVQueen")
        self.assertNotIn("handle", payload)
        self.assertNotIn("variants", payload)
        self.assertNotIn("inventory", payload)
        self.assertNotIn("price", payload)
        self.assertNotIn("sku", payload)

    def test_success_calls_transport_once(self):
        client = FakeClient(True)
        result = publish_to_shopify(record(), client)
        self.assertEqual(len(client.calls), 1)
        self.assertEqual(result["status"], "SUCCESS")
        self.assertEqual(client.calls[0][0], "123")

    def test_transport_failure_is_not_success(self):
        client = FakeClient(False)
        with self.assertRaises(ShopifyPublisherError):
            publish_to_shopify(record(), client)
        self.assertEqual(len(client.calls), 1)

    def test_missing_product_id_blocks_transport(self):
        client = FakeClient(True)
        bad = record()
        bad["identity"].pop("product_id")
        with self.assertRaises(ShopifyPublisherError):
            publish_to_shopify(bad, client)
        self.assertEqual(client.calls, [])


if __name__ == "__main__":
    unittest.main()
