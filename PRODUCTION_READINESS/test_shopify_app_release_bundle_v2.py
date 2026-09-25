import hashlib
import json
import unittest

from RELEASE_GATE_V1 import create_approval
from SHOPIFY_APP_RELEASE_BUNDLE_V2 import build_bundle, canonical_record_json


class ShopifyAppReleaseBundleV2Tests(unittest.TestCase):
    def fixture(self):
        return {
            "schema_version": "1.0",
            "identity": {"product_id": "gid://shopify/Product/1", "source_name": "fixture"},
            "pricing": {"source_price": "10.00", "approved_publish_price": "19.99"},
            "qa": {"errors": [], "warnings": [], "passed": True},
            "status": "PRODUCTION_READY",
        }

    def test_bundle_preserves_exact_fingerprint_bytes(self):
        record = self.fixture()
        approval = create_approval(record, actor="qa-owner")
        bundle = build_bundle(record, approval)
        canonical = bundle["canonical_record_json"]
        self.assertEqual(canonical, canonical_record_json(record))
        self.assertEqual(
            hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
            approval["content_fingerprint"],
        )
        self.assertEqual(json.loads(canonical), record)

    def test_blocked_approval_cannot_build_bundle(self):
        record = self.fixture()
        approval = create_approval(record, actor="qa-owner", decision="BLOCKED")
        with self.assertRaises(ValueError):
            build_bundle(record, approval)


if __name__ == "__main__":
    unittest.main()
