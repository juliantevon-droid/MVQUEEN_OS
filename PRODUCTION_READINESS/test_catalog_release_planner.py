from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE_ROOT = ROOT / "15_Scripts_And_Code"
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

from mvqueen_engine.catalog_release_planner import build_release_plan


def row(handle, sku, title, category="beauty", product_type="mascara",
        image="", variant_image="", option="Default", price="10.00"):
    return {
        "Handle": handle,
        "Variant SKU": sku,
        "Title": title,
        "MVQ Category": category,
        "MVQ Product Type": product_type,
        "Image Src": image,
        "Variant Image": variant_image,
        "Option1 Value": option,
        "Variant Price": price,
    }


class CatalogReleasePlannerTests(unittest.TestCase):
    def test_numbered_duplicate_keeps_richer_media_member_without_rewriting(self):
        rows = [
            row("sample", "SKU-1", "Sample Mascara"),
            row("sample-1", "SKU-1", "Sample Mascara", image="https://example.com/a.jpg"),
            row("unique", "SKU-2", "Unique Mascara"),
        ]
        plan = build_release_plan(rows)
        self.assertEqual(plan["unresolved_collision_components"], 0)
        self.assertEqual(plan["excluded_duplicate_handles"], 1)
        self.assertEqual(plan["release_candidate_products"], 2)
        component = plan["components"][0]
        self.assertEqual(component["canonical_handle"], "sample-1")
        self.assertEqual(component["excluded"][0]["handle"], "sample")

    def test_supplier_prefixed_duplicate_prefers_clean_handle_on_equal_structure(self):
        rows = [
            row("mascara-natural", "SKU-1", "Mascara Natural"),
            row("eelhoe-mascara-natural", "SKU-1", "Mascara Natural"),
        ]
        plan = build_release_plan(rows)
        self.assertEqual(plan["unresolved_collision_components"], 0)
        component = plan["components"][0]
        self.assertEqual(component["canonical_handle"], "mascara-natural")
        self.assertEqual(component["excluded"][0]["handle"], "eelhoe-mascara-natural")

    def test_superset_product_keeps_all_unique_skus(self):
        rows = [
            row("setting-powder", "SKU-1", "Setting Powder Natural"),
            row("setting-powder", "SKU-2", "Setting Powder Natural"),
            row("eelhope-setting-powder", "SKU-2", "Setting Powder Beige"),
        ]
        plan = build_release_plan(rows)
        self.assertEqual(plan["unresolved_collision_components"], 0)
        component = plan["components"][0]
        self.assertEqual(component["canonical_handle"], "setting-powder")
        self.assertEqual(component["canonical_sku_count"], 2)
        self.assertEqual(component["excluded"][0]["handle"], "eelhope-setting-powder")

    def test_ambiguous_shared_sku_fails_closed(self):
        rows = [
            row("mascara-a", "SKU-1", "Mascara A", "beauty", "mascara"),
            row("face-cream-b", "SKU-1", "Face Cream B", "skincare", "moisturizer"),
        ]
        plan = build_release_plan(rows)
        self.assertEqual(plan["unresolved_collision_components"], 1)
        self.assertIn("unresolved_sku_collisions", plan["release_blockers"])
        self.assertEqual(plan["excluded_duplicate_handles"], 0)

    def test_media_gap_remains_release_blocker(self):
        rows = [row("sample", "SKU-1", "Sample Mascara")]
        plan = build_release_plan(rows)
        self.assertEqual(plan["handles_without_recovered_media"], 1)
        self.assertIn("incomplete_recovered_media", plan["release_blockers"])
        self.assertFalse(plan["release_importable"])


if __name__ == "__main__":
    unittest.main()
