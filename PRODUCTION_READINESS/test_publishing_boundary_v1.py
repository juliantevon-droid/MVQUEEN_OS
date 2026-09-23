"""Tests for the fail-closed MVQueen publishing boundary."""
from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

try:
    from .PUBLISHING_BOUNDARY_V1 import ALREADY_PUBLISHED, BLOCKED, PUBLISHED, idempotency_key, publish
    from .RELEASE_AUDIT_LEDGER_V1 import read_entries
    from .RELEASE_GATE_V1 import create_approval
except ImportError:
    from PUBLISHING_BOUNDARY_V1 import ALREADY_PUBLISHED, BLOCKED, PUBLISHED, idempotency_key, publish
    from RELEASE_AUDIT_LEDGER_V1 import read_entries
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

    def test_same_approved_fingerprint_is_idempotent(self):
        record = ready_record()
        approval = create_approval(record, "release-manager")
        store = {}
        calls = []

        def fake_publisher(value):
            calls.append(value)
            return {"external_id": "shopify-100"}

        first, first_audit = publish(record, approval, fake_publisher, store)
        second, second_audit = publish(record, approval, fake_publisher, store)

        self.assertEqual(first, PUBLISHED)
        self.assertEqual(second, ALREADY_PUBLISHED)
        self.assertEqual(len(calls), 1)
        self.assertEqual(first_audit["idempotency_key"], idempotency_key(record))
        self.assertEqual(second_audit["publisher_result"], {"external_id": "shopify-100"})

    def test_changed_content_creates_new_idempotency_key(self):
        record = ready_record()
        original_key = idempotency_key(record)
        record["copy"] = {"title": "Different approved content"}
        self.assertNotEqual(original_key, idempotency_key(record))

    def test_successful_publish_is_written_to_audit_ledger(self):
        record = ready_record()
        approval = create_approval(record, "release-manager")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "release_audit.jsonl"
            result, audit = publish(
                record,
                approval,
                lambda value: {"external_id": "shopify-100"},
                ledger_path=path,
            )
            self.assertEqual(result, PUBLISHED)
            entries = list(read_entries(path))
            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0]["product_id"], "p-100")
            self.assertEqual(entries[0]["content_fingerprint"], audit["content_fingerprint"])
            self.assertEqual(entries[0]["actor"], "release-manager")
            self.assertEqual(entries[0]["operation"], "PUBLISH")
            self.assertEqual(entries[0]["result"], PUBLISHED)

    def test_blocked_release_is_written_to_audit_ledger_without_publisher_call(self):
        record = ready_record()
        calls = []
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "release_audit.jsonl"
            result, _ = publish(
                record,
                None,
                lambda value: calls.append(value),
                ledger_path=path,
            )
            self.assertEqual(result, BLOCKED)
            self.assertEqual(calls, [])
            entries = list(read_entries(path))
            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0]["operation"], "RELEASE_GATE")
            self.assertEqual(entries[0]["result"], BLOCKED)
            self.assertEqual(entries[0]["actor"], "SYSTEM")


if __name__ == "__main__":
    unittest.main()
