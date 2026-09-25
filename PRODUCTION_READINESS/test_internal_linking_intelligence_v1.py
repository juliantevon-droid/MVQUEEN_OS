import copy
import unittest

from CANONICAL_ADAPTER_V1 import produce_catalog
from SCHEMA_VALIDATOR_V1 import validate_record


class InternalLinkingIntelligenceV1Tests(unittest.TestCase):
    def raw(self, product_id, product_type, color, material="Gold tone"):
        return {
            "schema_version": "1.0",
            "identity": {
                "product_id": product_id,
                "source_name": "Shopify",
                "handle": product_id.lower() + "-handle",
                "sku": "SKU-" + product_id,
            },
            "source_truth": {
                "facts": [
                    {"name": "material", "value": material, "source": "Shopify product record", "verified": True},
                    {"name": "color", "value": color, "source": "Shopify product record", "verified": True},
                    {"name": "use_context", "value": "Personal styling", "source": "Shopify product record", "verified": True},
                ]
            },
            "protected_fields": {"fields": ["sku", "inventory", "variant_id"]},
            "category": {
                "product_type": product_type,
                "category": "Jewelry",
                "subcategory": product_type,
            },
            "pricing": {"source_price": 20, "approved_publish_price": 49.99},
            "images": {"items": [{"src": "https://example.test/" + product_id + ".jpg"}]},
        }

    def catalog(self):
        return [
            self.raw("M1", "Necklace", "Black"),
            self.raw("M2", "Earrings", "Black"),
            self.raw("M3", "Necklace", "Black", material="Sterling silver"),
            self.raw("P1", "Bracelet", "Pink"),
        ]

    def test_links_use_real_same_brand_product_handles_and_explicit_collection_handles(self):
        raw = self.catalog()
        before = copy.deepcopy(raw)
        resolved = produce_catalog(
            raw,
            collection_handles={
                "MVQueen World": "mvqueen-edit",
                "Necklace": "necklaces",
                "Earrings": "earrings",
                "Miss.Princess World": "miss-princess",
                "Bracelet": "bracelets",
            },
        )
        self.assertEqual(raw, before)
        by_id = {item["identity"]["product_id"]: item for item in resolved}
        mvq_links = by_id["M1"]["seo"]["internal_links"]
        targets = {item["target"] for item in mvq_links}

        self.assertIn("/products/m2-handle", targets)
        self.assertIn("/products/m3-handle", targets)
        self.assertNotIn("/products/p1-handle", targets)
        self.assertIn("/collections/mvqueen-edit", targets)
        self.assertIn("/collections/necklaces", targets)

        blog_targets = {
            item["target"]
            for item in by_id["M1"]["content_suite"]["blog"]["internal_links"]
        }
        self.assertIn("/products/m1-handle", blog_targets)
        self.assertIn("/products/m2-handle", blog_targets)

        for record in resolved:
            self.assertEqual(validate_record(record), [])

    def test_collection_links_are_not_guessed(self):
        resolved = produce_catalog(self.catalog())
        for record in resolved:
            links = record["seo"]["internal_links"]
            self.assertFalse(any(item["type"] == "collection" for item in links))
            self.assertEqual(
                record["seo"]["internal_link_audit"]["collection_links"],
                0,
            )
            self.assertTrue(
                record["seo"]["internal_link_audit"]["collection_urls_require_explicit_handle"]
            )

    def test_output_is_deterministic(self):
        mapping = {"MVQueen World": "mvqueen-edit", "Necklace": "necklaces"}
        first = produce_catalog(self.catalog(), collection_handles=mapping)
        second = produce_catalog(self.catalog(), collection_handles=mapping)
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
