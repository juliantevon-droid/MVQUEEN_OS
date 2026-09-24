from __future__ import annotations

import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / "30_System_Infrastructure" / "catalog" / "catalog_recovery_audit.py"


def load_audit():
    spec = importlib.util.spec_from_file_location("catalog_recovery_audit", AUDIT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load catalog recovery audit")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CatalogRecoveryAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = load_audit()

    def write_csv(self, rows):
        headers = [
            "Handle", "Title", "Body (HTML)", "Vendor", "Status",
            "SEO Title", "SEO Description", "Tags", "Image Src",
            "Image Alt Text", "Variant SKU", "MVQ Category",
            "MVQ Product Type",
        ]
        tmp = tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="", suffix=".csv", delete=False
        )
        with tmp:
            writer = csv.DictWriter(tmp, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
        return Path(tmp.name)

    def test_dirty_supplier_catalog_is_held(self):
        path = self.write_csv([{
            "Handle": "sample",
            "Title": "OUHOE Glow Cream",
            "Body (HTML)": "<p>Supplier copy</p>",
            "Vendor": "eprolo",
            "Status": "active",
            "SEO Title": "OUHOE Glow Cream",
            "SEO Description": "Supplier description",
            "Tags": "beauty",
            "Image Src": "https://example.com/product.jpg",
            "Image Alt Text": "",
            "Variant SKU": "SKU-1",
            "MVQ Category": "",
            "MVQ Product Type": "",
        }])
        try:
            report = self.audit.audit_csv(path)
        finally:
            path.unlink(missing_ok=True)

        self.assertEqual(report["decision"], "HOLD")
        self.assertIn(
            "supplier_or_legacy_brand_in_customer_copy", report["hold_reasons"]
        )
        self.assertIn("missing_image_alt_text", report["hold_reasons"])
        self.assertIn("missing_mvqueen_category", report["hold_reasons"])
        self.assertIn("missing_product_type", report["hold_reasons"])

    def test_tier1_forbidden_brand_language_is_held(self):
        path = self.write_csv([{
            "Handle": "sample",
            "Title": "Amazing Rose Lip Tint",
            "Body (HTML)": "<p>Verified rose lip tint.</p>",
            "Vendor": "MVQUEEN",
            "Status": "draft",
            "SEO Title": "Rose Lip Tint | MVQUEEN",
            "SEO Description": "Verified rose lip tint.",
            "Tags": "beauty,lip",
            "Image Src": "https://example.com/product.jpg",
            "Image Alt Text": "MVQUEEN rose lip tint",
            "Variant SKU": "SKU-1",
            "MVQ Category": "beauty",
            "MVQ Product Type": "lip tint",
        }])
        try:
            report = self.audit.audit_csv(path)
        finally:
            path.unlink(missing_ok=True)

        self.assertEqual(report["decision"], "HOLD")
        self.assertIn("tier1_forbidden_brand_language", report["hold_reasons"])
        self.assertIn("Amazing", report["brand_voice"]["tier1_violations"])
        self.assertGreater(report["brand_voice"]["tier1_terms_loaded"], 0)
        self.assertIn(
            "06_Tone_And_Voice/Forbidden_Words.md",
            report["brand_voice"]["governance_sources"],
        )

    def test_clean_catalog_can_reach_review_gate(self):
        path = self.write_csv([{
            "Handle": "sample",
            "Title": "MVQUEEN Rose Lip Tint",
            "Body (HTML)": "<p>Verified rose lip tint.</p>",
            "Vendor": "MVQUEEN",
            "Status": "draft",
            "SEO Title": "Rose Lip Tint | MVQUEEN",
            "SEO Description": "A verified rose lip tint.",
            "Tags": "beauty,lip",
            "Image Src": "https://example.com/product.jpg",
            "Image Alt Text": "MVQUEEN rose lip tint",
            "Variant SKU": "SKU-1",
            "MVQ Category": "beauty",
            "MVQ Product Type": "lip tint",
        }])
        try:
            report = self.audit.audit_csv(path)
        finally:
            path.unlink(missing_ok=True)

        self.assertEqual(report["decision"], "READY_FOR_REVIEW")
        self.assertEqual(report["hold_reasons"], [])
        self.assertFalse(report["safety"]["shopify_network_io"])
        self.assertFalse(report["safety"]["publishes_products"])


if __name__ == "__main__":
    unittest.main()
