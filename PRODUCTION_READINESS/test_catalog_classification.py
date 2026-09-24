from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE_ROOT = ROOT / "15_Scripts_And_Code"
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

from mvqueen_engine.catalog_classification import classify_product


class CatalogClassificationTests(unittest.TestCase):
    def test_historical_lip_glaze_is_not_dress(self):
        result = classify_product(
            title="Pudaier 18 Color Mini Capsule Lip Glaze Velvet Fog Color",
            handle="pudaier-18-color-mini-capsule-lip-glaze",
            tags="beauty, eprolo",
        )
        self.assertEqual((result.category, result.product_type), ("beauty", "lip color"))

    def test_historical_highlighter_is_not_jewelry(self):
        result = classify_product(
            title="QIBEST Highlighting Powder High Gloss Diamond Sparkling",
            handle="qibest-highlighting-powder",
            tags="beauty, eprolo",
        )
        self.assertEqual((result.category, result.product_type), ("beauty", "highlighter"))

    def test_historical_lipliner_is_not_home(self):
        result = classify_product(
            title="MISS ROSE Double-end Lasting Lipliner Waterproof Lip Liner Stick",
            handle="miss-rose-double-end-lasting-lipliner",
            tags="beauty, eprolo",
        )
        self.assertEqual((result.category, result.product_type), ("beauty", "lip color"))

    def test_historical_conditioner_is_haircare(self):
        result = classify_product(
            title="Deep Conditioner For Improving Dry Hair, Moisturizing And Smoothing Hair",
            handle="deep-conditioner-for-improving-dry-hair",
            tags="beauty, haircare",
        )
        self.assertEqual((result.category, result.product_type), ("haircare", "conditioner"))

    def test_fragrance_is_classified_from_identity(self):
        result = classify_product(
            title="Fresh Jasmines Perfume",
            handle="fresh-jasmines-perfume",
            tags="beauty, fragrance, perfume",
        )
        self.assertEqual((result.category, result.product_type), ("fragrance", "perfume"))

    def test_jewelry_is_classified_from_identity(self):
        result = classify_product(
            title="Pink Thulite Pendant in 925 Sterling Silver",
            handle="pink-thulite-pendant",
            tags="jewelry, pendant",
        )
        self.assertEqual((result.category, result.product_type), ("jewelry", "necklace"))

    def test_beauty_tag_is_safe_medium_fallback(self):
        result = classify_product(
            title="Multi Purpose Cosmetic Item",
            handle="multi-purpose-cosmetic-item",
            tags="beauty",
        )
        self.assertEqual((result.category, result.product_type), ("beauty", "beauty product"))
        self.assertEqual(result.confidence, "medium")

    def test_unknown_without_domain_evidence_stays_unclassified(self):
        result = classify_product(title="Mystery Item", handle="mystery-item", tags="")
        self.assertEqual(result.category, "unclassified")
        self.assertEqual(result.confidence, "low")


if __name__ == "__main__":
    unittest.main()
