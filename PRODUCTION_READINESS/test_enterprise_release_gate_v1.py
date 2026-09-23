import unittest

from ENTERPRISE_RELEASE_GATE_V1 import content_fingerprint, evaluate_release, make_approval
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
        self.assertEqual(content_fingerprint(record), content_fingerprint(record))

    def test_ready_record_still_requires_approval(self):
        record = run(self.base())
        ok, decision = evaluate_release(record)
        self.assertFalse(ok)
        self.assertEqual(decision["decision"], "HOLD")
        self.assertTrue(any("approval" in reason.lower() for reason in decision["reasons"]))

    def test_matching_approval_releases(self):
        record = run(self.base())
        approval = make_approval(record, "authorized-reviewer")
        ok, decision = evaluate_release(record, approval)
        self.assertTrue(ok)
        self.assertEqual(decision["decision"], "APPROVED_FOR_PUBLISH")

    def test_stale_approval_is_rejected(self):
        record = run(self.base())
        approval = make_approval(record, "authorized-reviewer")
        record["copy"]["title"] += " Updated"
        ok, decision = evaluate_release(record, approval)
        self.assertFalse(ok)
        self.assertEqual(decision["decision"], "HOLD")


if __name__ == "__main__":
    unittest.main()
