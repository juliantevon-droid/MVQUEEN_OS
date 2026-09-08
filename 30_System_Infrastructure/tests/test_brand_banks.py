"""Contract tests for the canonical MVQueen brand-bank layer."""

import unittest

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "15_Scripts_And_Code" / "mvqueen_engine"))

from mvqueen_brand_banks import (  # noqa: E402
    PERSONA_KEYWORDS,
    PROTECTED_COLUMNS,
    SHOPIFY_VALID_STATUSES,
    assign_brand_voice,
    assign_keywords,
    assign_persona,
    generate_persona_keywords,
    stable_seed,
    validate_shopify_row,
)


class BrandBankContractTests(unittest.TestCase):
    def test_persona_bank_has_at_least_1000_unique_keywords(self):
        keywords = generate_persona_keywords(1000)
        self.assertGreaterEqual(len(keywords), 1000)
        self.assertEqual(len(keywords), len(set(keywords)))
        self.assertEqual(len(PERSONA_KEYWORDS), 1000)

    def test_assignment_is_deterministic(self):
        key = "mvqueen-test-product-001"
        self.assertEqual(assign_persona(key), assign_persona(key))
        self.assertEqual(assign_brand_voice(key), assign_brand_voice(key))
        self.assertEqual(assign_keywords(key), assign_keywords(key))
        self.assertEqual(stable_seed(key), stable_seed(key))

    def test_keyword_rotation_is_bounded(self):
        keywords = assign_keywords("mvqueen-test-product-002", count=12)
        self.assertEqual(len(keywords), 12)
        self.assertTrue(all(keyword in PERSONA_KEYWORDS for keyword in keywords))

    def test_shopify_status_contract_does_not_mutate(self):
        row = {"Title": "Test Product", "Status": "active"}
        self.assertEqual(validate_shopify_row(row), [])
        self.assertEqual(row["Status"], "active")
        self.assertEqual(SHOPIFY_VALID_STATUSES, {"active", "draft", "archived"})

    def test_invalid_status_is_reported(self):
        errors = validate_shopify_row({"Title": "Test Product", "Status": "ACTIVE-ish"})
        self.assertTrue(errors)
        self.assertIn("Status isn't valid", errors[0])

    def test_protected_columns_exist(self):
        expected = {"handle", "sku", "inventory_quantity", "cost", "variant_tax_code", "status", "image_src", "published"}
        self.assertTrue(expected.issubset(set(PROTECTED_COLUMNS)))


if __name__ == "__main__":
    unittest.main()
