from __future__ import annotations

import copy
import unittest

from PRODUCT_PIPELINE_V1 import run
from CONTENT_INTELLIGENCE_V1 import generate_content_suite, validate_content_suite


class ContentIntelligenceV1Tests(unittest.TestCase):
    def base(self):
        return {
            "schema_version": "1.0",
            "identity": {
                "product_id": "CONTENT-001",
                "source_name": "Shopify",
                "handle": "black-satin-dress",
                "sku": "SKU-CONTENT-001",
            },
            "source_truth": {
                "facts": [
                    {"name": "material", "value": "Satin", "source": "Shopify product record", "verified": True},
                    {"name": "color", "value": "Black", "source": "Shopify product record", "verified": True},
                    {"name": "use_context", "value": "Evening styling", "source": "Shopify product record", "verified": True},
                    {"name": "claim", "value": "clinically proven", "source": "supplier", "verified": False},
                ]
            },
            "protected_fields": {"fields": ["sku", "inventory", "variant_id"]},
            "category": {"product_type": "Dress", "category": "Fashion"},
            "pricing": {"source_price": 20, "approved_publish_price": 49.99},
            "images": {"items": [{"src": "https://example.test/dress.jpg"}]},
        }

    def canonical(self):
        result = run(self.base())
        self.assertEqual(result["status"], "PRODUCTION_READY")
        return result

    def test_generates_full_reviewable_content_suite(self):
        content = generate_content_suite(self.canonical())
        self.assertTrue(content["qa"]["passed"])
        self.assertEqual(content["qa"]["status"], "CONTENT_READY_FOR_REVIEW")
        self.assertTrue(content["product_page"]["title"])
        self.assertTrue(content["product_page"]["faq"])
        self.assertTrue(content["collection"]["description"])
        self.assertTrue(content["blog"]["sections"])
        self.assertFalse(content["blog"]["auto_publish"])
        self.assertFalse(content["site_faq"]["auto_publish"])

    def test_only_verified_facts_become_factual_content(self):
        content = generate_content_suite(self.canonical())
        serialized = str(content).lower()
        self.assertIn("satin", serialized)
        self.assertIn("black", serialized)
        self.assertNotIn("clinically proven", serialized)

    def test_metafields_do_not_invent_legacy_attributes(self):
        content = generate_content_suite(self.canonical())
        fields = content["metafields"]
        self.assertEqual(fields["attributes.material"]["value"], "Satin")
        self.assertEqual(fields["attributes.color"]["value"], "Black")
        forbidden = {
            "attributes.origin",
            "attributes.shelf_life",
            "trust.certifications",
            "catalog.badge",
            "custom.origin",
            "custom.shelf_life",
            "custom.certifications",
            "custom.badge",
        }
        self.assertFalse(forbidden.intersection(fields))

    def test_product_link_uses_existing_handle_without_mutating_it(self):
        canonical = self.canonical()
        before = copy.deepcopy(canonical["identity"])
        content = generate_content_suite(canonical)
        self.assertEqual(content["blog"]["internal_links"][0]["target"], "/products/black-satin-dress")
        self.assertEqual(canonical["identity"], before)

    def test_non_production_record_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "PRODUCTION_READY"):
            generate_content_suite(self.base())

    def test_output_is_deterministic(self):
        canonical = self.canonical()
        first = generate_content_suite(canonical)
        second = generate_content_suite(canonical)
        self.assertEqual(first, second)

    def test_collection_copy_is_stable_for_same_product_type(self):
        first_product = self.base()
        second_product = self.base()
        second_product["identity"]["product_id"] = "CONTENT-002"
        second_product["identity"]["sku"] = "SKU-CONTENT-002"
        first = generate_content_suite(run(first_product))
        second = generate_content_suite(run(second_product))
        self.assertEqual(first["collection"]["name"], second["collection"]["name"])
        self.assertEqual(first["collection"]["description"], second["collection"]["description"])

    def test_blog_drafts_are_product_specific_and_varied(self):
        titles = set()
        deks = set()
        for index in range(12):
            product = self.base()
            product["identity"]["product_id"] = f"CONTENT-VAR-{index:03d}"
            product["identity"]["handle"] = f"black-satin-dress-{index:03d}"
            product["identity"]["sku"] = f"SKU-CONTENT-VAR-{index:03d}"
            content = generate_content_suite(run(product))
            self.assertTrue(content["qa"]["passed"])
            titles.add(content["blog"]["title"])
            deks.add(content["blog"]["dek"])
            self.assertIn(content["product_page"]["title"], content["blog"]["title"])

        self.assertGreaterEqual(len(titles), 6)
        self.assertGreaterEqual(len(deks), 3)

    def test_validator_blocks_auto_publish(self):
        content = generate_content_suite(self.canonical())
        content["blog"]["auto_publish"] = True
        errors = validate_content_suite(content)
        self.assertTrue(any("review-only" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
