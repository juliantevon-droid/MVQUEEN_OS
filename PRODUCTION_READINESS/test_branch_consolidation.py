from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE_ROOT = ROOT / "15_Scripts_And_Code"
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

from mvqueen_engine.catalog_approval import build_product_update_input
from mvqueen_engine.catalog_dry_run import dry_run_product


class BranchConsolidationTests(unittest.TestCase):
    def _source(self):
        return {
            "Product GID": "gid://shopify/Product/123",
            "Handle": "example-serum",
            "Variant SKU": "SKU-1",
            "Title": "OUHOE Glow Serum",
            "Body (HTML)": "<p>OUHOE hydrating serum.</p>",
            "Product Type": "Skincare",
            "Tags": "supplier, hydration",
            "SEO Title": "",
            "SEO Description": "",
        }

    def test_dry_run_is_write_free_and_preserves_identity(self):
        result = dry_run_product(self._source())
        self.assertFalse(result["write_performed"])
        self.assertEqual(result["before"]["Handle"], result["proposed"]["Handle"])
        self.assertEqual(result["before"]["Variant SKU"], result["proposed"]["Variant SKU"])
        self.assertNotIn("OUHOE", result["proposed"]["Title"].upper())

    def test_approval_is_explicit_and_editorial_only(self):
        result = dry_run_product(self._source())
        with self.assertRaises(PermissionError):
            build_product_update_input(result)

        payload = build_product_update_input(result, approved=True)
        self.assertEqual(payload["id"], "gid://shopify/Product/123")
        self.assertNotIn("handle", payload)
        self.assertNotIn("sku", payload)
        self.assertNotIn("inventoryQuantity", payload)

    def test_protected_change_fails_closed(self):
        result = dry_run_product(self._source())
        result["proposed"]["Variant SKU"] = "MUTATED"
        with self.assertRaises(ValueError):
            build_product_update_input(result, approved=True)


if __name__ == "__main__":
    unittest.main()
