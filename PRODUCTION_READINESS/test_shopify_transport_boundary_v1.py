"""Tests for the narrow Shopify transport mutation boundary."""
from __future__ import annotations

import unittest
from unittest.mock import Mock, patch

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "15_Scripts_And_Code"))

from mvqueen_engine.shopify_api import shopify_client


class ShopifyTransportBoundaryTests(unittest.TestCase):
    @patch("mvqueen_engine.shopify_api.shopify_client.requests.put")
    def test_editorial_allowlist_updates_only_approved_fields(self, put):
        response = Mock(status_code=200)
        response.json.return_value = {"product": {"id": "123"}}
        put.return_value = response

        result = shopify_client.update_product(
            "123",
            {
                "id": "123",
                "title": "Midnight Satin",
                "body_html": "A polished silhouette.",
                "vendor": "MVQueen",
                "product_type": "dress",
                "tags": "MVQueen, Evening",
            },
        )

        self.assertEqual(result["product"]["id"], "123")
        payload = put.call_args.kwargs["json"]["product"]
        self.assertNotIn("handle", payload)
        self.assertNotIn("variants", payload)
        self.assertNotIn("inventory", payload)
        self.assertNotIn("price", payload)

    def test_protected_fields_are_rejected(self):
        with self.assertRaises(ValueError):
            shopify_client.update_product("123", {"price": "19.99"})

    def test_unknown_fields_are_rejected(self):
        with self.assertRaises(ValueError):
            shopify_client.update_product("123", {"images": []})

    def test_variant_price_mutation_is_disabled(self):
        with self.assertRaises(RuntimeError):
            shopify_client.update_variant_price("456", "19.99")

    def test_metafield_mutation_is_disabled(self):
        with self.assertRaises(RuntimeError):
            shopify_client.update_metafields("123", {"mvqueen.material": "satin"})


if __name__ == "__main__":
    unittest.main()
