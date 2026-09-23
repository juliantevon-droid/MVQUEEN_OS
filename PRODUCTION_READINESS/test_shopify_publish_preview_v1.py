"""Tests for the Shopify publish preview boundary."""
from __future__ import annotations
import unittest
from SHOPIFY_PUBLISHER_V1 import ShopifyPublisherError
from SHOPIFY_PUBLISH_PREVIEW_V1 import build_preview

class ShopifyPublishPreviewTests(unittest.TestCase):
    def fixture(self):
        return {
            "identity": {"product_id": "gid://shopify/Product/9072508567750"},
            "category": {"product_type": "925 Sterling Silver Pendant"},
            "copy": {"title": "Pink Thulite Pendant", "description": "<p>A polished MVQueen jewelry story.</p>"},
            "merchandising": {"tags": ["Pink Thulite", "Pendant"]},
            "handle": "must-not-be-read",
            "pricing": {"approved_publish_price": 26.39},
        }

    def test_preview_is_explicitly_non_live_and_scoped(self):
        preview = build_preview(self.fixture())
        self.assertFalse(preview["live_write_performed"])
        self.assertTrue(preview["authorization_required"])
        self.assertEqual(preview["operation"], "UPDATE_PRODUCT_EDITORIAL")
        self.assertEqual(preview["product_id"], "gid://shopify/Product/9072508567750")
        self.assertEqual(set(preview["proposed_updates"]), {"title", "body_html", "vendor", "product_type", "tags"})
        self.assertIn("sku", preview["protected_fields"])
        self.assertIn("inventory_quantity", preview["protected_fields"])
        self.assertNotIn("price", preview["proposed_updates"])

    def test_payload_rejects_missing_product_id(self):
        with self.assertRaises(ShopifyPublisherError):
            build_preview({})

    def test_preview_does_not_mutate_record(self):
        source = self.fixture()
        before = dict(source)
        build_preview(source)
        self.assertEqual(source, before)

if __name__ == "__main__":
    unittest.main()