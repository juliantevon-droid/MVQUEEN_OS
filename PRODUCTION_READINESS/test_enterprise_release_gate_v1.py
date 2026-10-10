import unittest

from RELEASE_GATE_V1 import APPROVED, BLOCKED, canonical_fingerprint, evaluate, create_approval
from PRODUCT_PIPELINE_V1 import run


class EnterpriseReleaseGateTests(unittest.TestCase):
    def base(self):
        return {
            "schema_version": "1.0",
            "identity": {"product_id": "EQ-001", "source_name": "supplier"},
            "source_truth": {"facts": [
                {"name": "material", "value": "satin", "source": "supplier", "verified": True},
                {"name": "color", "value": "black", "source": "supplier", "verified": True},
                {"name": "use_context", "value": "evening styling", "source": "supplier", "verified": True},
            ]},
            "protected_fields": {"fields": ["product_id", "sku", "inventory"]},
            "category": {"product_type": "dress"},
            "pricing": {"source_price": 18.0, "approved_publish_price": 49.99},
            "images": {"items": [{"src": "https://example.test/dress.jpg", "verified": True}]},
        }

    def test_same_record_has_same_fingerprint(self):
        record = run(self.base())
        self.assertEqual(canonical_fingerprint(record), canonical_fingerprint(record))

    def test_ready_record_still_requires_approval(self):
        record = run(self.base())
        status, reason = evaluate(record)
        self.assertEqual(status, BLOCKED)
        self.assertIn("approval", reason.lower())

    def test_matching_approval_releases(self):
        record = run(self.base())
        approval = create_approval(record, "authorized-reviewer")
        status, reason = evaluate(record, approval)
        self.assertEqual(status, APPROVED)

    def test_stale_approval_is_rejected(self):
        record = run(self.base())
        approval = create_approval(record, "authorized-reviewer")
        record["copy"]["title"] += " Updated"
        status, reason = evaluate(record, approval)
        self.assertEqual(status, BLOCKED)
        self.assertIn("fingerprint", reason.lower())


if __name__ == "__main__":
    unittest.main()
