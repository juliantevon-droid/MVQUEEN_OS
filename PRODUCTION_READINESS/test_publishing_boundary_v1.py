"""Tests for the fail-closed MVQueen publishing boundary."""
from __future__ import annotations

import copy
import unittest

try:
    from .PUBLISHING_BOUNDARY_V1 import BLOCKED, PUBLISHED, publish
    from .RELEASE_GATE_V1 import create_approval
except ImportError:
    from PUBLISHING_BOUNDARY_V1 import BLOCKED, PUBLISHED, publish
    from RELEASE_GATE_V1 import create_approval


def ready_record():
    return {
        "schema_version": "1.0",
        "identity": {"product_id": "p-100", "source_name": "supplier"},
        "pricing": {"source_price": 20, "approved_publish_price": 49.99},
        "source_truth": {"facts": [{"name": "material", "value": "satin", "source": "supplier", "verified": True}]},
        "protected_fields": {"fields": ["sku", "inventory_quantity"]},
        "images": {"items": [{"src": "https://example.test/a.jpg", "alt": "Satin dress"}]},
        "status": "PRODUCTION_READY",
        "qa": {"passed": True, "errors": [], "warnings": []},
    }


class PublishingBoundaryTests(unittest.TestCase):
    def test_missing_approval_blocks_without_publisher_call(self):
        record = ready_record()
        calls = []
        result, audit = publish(record, None, lambda value: calls.append(value))
        self.assertEqual(result, BLOCKED)
        self.assertEqual(calls, [])
        self.assertIn("approval", audit["reason"].lower())

    def test_stale_fingerprint_blocks_without_publisher_call(self):
        record = ready_record()
        approval = create_approval(record, "qa-user")
        record["copy"] = {"title": "Changed after approval"}
        calls = []
        result, _ = publish(record, approval, lambda value: calls.append(value))
        self.assertEqual(result, BLOCKED)
        self.assertEqual(calls, [])

    def test_valid_approval_invokes_publisher_once(self):
        record = ready_record()
        approval = create_approval(record, "release-manager")
        calls = []

        def fake_publisher(value):
            calls.append(value)
            return {"external_id": "shopify-100"}

        result, audit = publish(record, approval, fake_publisher)
        self.assertEqual(result, PUBLISHED)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0], record)
        self.assertEqual(audit["publisher_result"]["external_id"], "shopify-100")

    def test_publisher_receives_copy_and_cannot_mutate_canonical_record(self):
        record = ready_record()
        approval = create_approval(record, "release-manager")
        original = copy.deepcopy(record)

        def mutating_publisher(value):
            value["identity"]["product_id"] = "MUTATED"
            return "ok"

        result, _ = publish(record, approval, mutating_publisher)
        self.assertEqual(result, PUBLISHED)
        self.assertEqual(record, original)
        self.assertNotEqual(record["identity"]["product_id"], "MUTATED")

    def test_unapproved_product_blocks(self):
        record = ready_record()
        record["status"] = "CREATIVE_READY"
        approval = create_approval(record, "release-manager")
        calls = []
        result, _ = publish(record, approval, lambda value: calls.append(value))
        self.assertEqual(result, BLOCKED)
        self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
