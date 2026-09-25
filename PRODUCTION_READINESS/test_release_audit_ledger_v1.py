"""Tests for the MVQueen release audit ledger V1."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from RELEASE_AUDIT_LEDGER_V1 import append_entry, build_entry, read_entries


class ReleaseAuditLedgerV1Tests(unittest.TestCase):
    def _entry(self):
        return build_entry(
            product_id="123",
            schema_version="1.0",
            content_fingerprint="abc123",
            idempotency_key="UPDATE_PRODUCT_EDITORIAL:123:abc123",
            actor="test-operator",
            decision="APPROVED_FOR_PUBLISH",
            operation="UPDATE_PRODUCT_EDITORIAL",
            result="SUCCESS",
            timestamp="2026-09-17T00:00:00+00:00",
        )

    def test_build_entry_contains_required_audit_fields(self):
        entry = self._entry()
        self.assertEqual(entry["ledger_schema_version"], "1.0")
        self.assertEqual(entry["product_id"], "123")
        self.assertEqual(entry["content_fingerprint"], "abc123")
        self.assertEqual(entry["idempotency_key"], "UPDATE_PRODUCT_EDITORIAL:123:abc123")

    def test_missing_required_field_blocks_entry(self):
        with self.assertRaises(ValueError):
            build_entry(
                product_id="123",
                schema_version="1.0",
                content_fingerprint="",
                idempotency_key="key",
                actor="operator",
                decision="APPROVED_FOR_PUBLISH",
                operation="UPDATE_PRODUCT_EDITORIAL",
                result="SUCCESS",
                timestamp="now",
            )

    def test_append_and_read_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "release_audit.jsonl"
            entry = self._entry()
            append_entry(path, entry)
            self.assertEqual(list(read_entries(path)), [entry])

    def test_malformed_ledger_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "release_audit.jsonl"
            path.write_text('{not-json}\n', encoding="utf-8")
            with self.assertRaises(ValueError):
                list(read_entries(path))


if __name__ == "__main__":
    unittest.main()
