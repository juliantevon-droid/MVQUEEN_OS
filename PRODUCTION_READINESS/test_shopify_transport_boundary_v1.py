"""Tests for the unified Shopify write boundary."""
from __future__ import annotations

import unittest
from pathlib import Path

from SHOPIFY_PUBLISHER_V1 import ShopifyPublisherError, publish_to_shopify


ROOT = Path(__file__).resolve().parents[1]


def record():
    return {
        "identity": {"product_id": "123"},
        "category": {"product_type": "dress"},
        "copy": {"title": "Midnight Satin", "description": "A polished evening silhouette."},
        "merchandising": {"tags": ["MVQueen", "Evening"]},
    }


class UnifiedTransportBoundaryTests(unittest.TestCase):
    def test_python_has_no_default_live_transport(self):
        with self.assertRaises(ShopifyPublisherError):
            publish_to_shopify(record())

    def test_legacy_transport_modules_are_absent(self):
        retired = [
            "15_Scripts_And_Code/mvqueen_engine/Access_token.py",
            "15_Scripts_And_Code/mvqueen_engine/shopify_client.py",
            "15_Scripts_And_Code/mvqueen_engine/shopify_graphql_client.py",
            "15_Scripts_And_Code/mvqueen_engine/shopify_api/shopify_client.py",
            "15_Scripts_And_Code/session_manager.py",
        ]
        for rel in retired:
            self.assertFalse((ROOT / rel).exists(), rel)

    def test_catalog_worker_has_no_network_write_transport(self):
        text = (ROOT / "30_System_Infrastructure/catalog/mvqueen_catalog_worker.py").read_text(encoding="utf-8")
        self.assertNotIn("urllib.request", text)
        self.assertNotIn("requests.post", text)
        self.assertNotIn("productUpdate(", text)

    def test_react_app_is_declared_live_writer(self):
        text = (ROOT / "app/lib/product-processor.ts").read_text(encoding="utf-8")
        self.assertIn("MVQ_APPROVED_PRODUCT_GIDS", text)
        self.assertIn("admin.graphql(PRODUCT_UPDATE", text)
        self.assertNotIn("generateCatalogPackage", text)
        self.assertNotIn("MVQ_CONTENT_REWRITE_ENABLED", text)


if __name__ == "__main__":
    unittest.main()
