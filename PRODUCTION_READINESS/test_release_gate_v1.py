import unittest

from RELEASE_GATE_V1 import APPROVED, BLOCKED, canonical_fingerprint, create_approval, evaluate


class ReleaseGateV1Tests(unittest.TestCase):
    def product(self):
        return {
            "schema_version": "1.0",
            "identity": {"product_id": "SKU-001", "source_name": "supplier"},
            "pricing": {"approved_publish_price": 49.99},
            "status": "PRODUCTION_READY",
            "qa": {"passed": True, "errors": [], "warnings": []},
            "copy": {"title": "Black Dress"},
        }

    def test_no_approval_blocks(self):
        status, reason = evaluate(self.product())
        self.assertEqual(status, BLOCKED)
        self.assertIn("approval", reason.lower())

    def test_valid_approval_passes(self):
        product = self.product()
        approval = create_approval(product, "release-manager")
        status, reason = evaluate(product, approval)
        self.assertEqual(status, APPROVED)
        self.assertEqual(reason, "Release gate passed")

    def test_changed_record_invalidates_approval(self):
        product = self.product()
        approval = create_approval(product, "release-manager")
        product["copy"]["title"] = "Black Evening Dress"
        status, reason = evaluate(product, approval)
        self.assertEqual(status, BLOCKED)
        self.assertIn("fingerprint", reason.lower())

    def test_product_binding_is_enforced(self):
        product = self.product()
        approval = create_approval(product, "release-manager")
        product["identity"]["product_id"] = "SKU-002"
        status, reason = evaluate(product, approval)
        self.assertEqual(status, BLOCKED)
        self.assertIn("product_id", reason)

    def test_schema_binding_is_enforced(self):
        product = self.product()
        approval = create_approval(product, "release-manager")
        product["schema_version"] = "2.0"
        status, reason = evaluate(product, approval)
        self.assertEqual(status, BLOCKED)
        self.assertIn("schema_version", reason)

    def test_unsupported_decision_is_rejected(self):
        with self.assertRaises(ValueError):
            create_approval(self.product(), "release-manager", "APPROVE_ANYTHING")

    def test_missing_product_id_is_rejected(self):
        product = self.product()
        del product["identity"]["product_id"]
        with self.assertRaises(ValueError):
            create_approval(product, "release-manager")

    def test_no_approval_blocks(self):
        status, reason = evaluate(self.product())
        self.assertEqual(status, BLOCKED)
        self.assertIn("approval", reason.lower())

    def test_non_ready_product_blocks(self):
        product = self.product()
        product["status"] = "COPY_READY"
        approval = create_approval(product, "release-manager")
        status, _ = evaluate(product, approval)
        self.assertEqual(status, BLOCKED)

    def test_fingerprint_is_deterministic(self):
        product = self.product()
        self.assertEqual(canonical_fingerprint(product), canonical_fingerprint(product))


if __name__ == "__main__":
    unittest.main()
