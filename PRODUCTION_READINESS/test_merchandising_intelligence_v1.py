import unittest

from CANONICAL_ADAPTER_V1 import produce_catalog
from MERCHANDISING_INTELLIGENCE_V1 import resolve_catalog
from PRODUCT_PIPELINE_V1 import run
from SCHEMA_VALIDATOR_V1 import validate_record


class MerchandisingIntelligenceV1Tests(unittest.TestCase):
    def raw(self, product_id, product_type, color, material="Gold tone"):
        return {
            "schema_version": "1.0",
            "identity": {
                "product_id": product_id,
                "source_name": "Shopify",
                "handle": product_id.lower().replace(":", "-"),
                "sku": f"SKU-{product_id}",
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
            "images": {"items": [{"src": f"https://example.test/{product_id}.jpg"}]},
        }

    def raw_catalog(self):
        return [
            self.raw("M1", "Necklace", "Black"),
            self.raw("M2", "Earrings", "Black"),
            self.raw("M3", "Necklace", "Black", material="Sterling silver"),
            self.raw("P1", "Bracelet", "Pink"),
        ]

    def ready_catalog(self):
        return produce_catalog(self.raw_catalog())

    def test_resolver_is_brand_world_safe_and_schema_valid(self):
        resolved = self.ready_catalog()
        by_id = {item["identity"]["product_id"]: item for item in resolved}

        self.assertEqual(by_id["M1"]["intelligence"]["brand_world"], "mvqueen")
        self.assertEqual(by_id["P1"]["intelligence"]["brand_world"], "miss-princess")

        self.assertNotIn("P1", by_id["M1"]["merchandising"]["related_products"])
        self.assertNotIn("P1", by_id["M1"]["intelligence"]["cross_sell_candidates"])
        self.assertIn("M2", by_id["M1"]["intelligence"]["cross_sell_candidates"])
        self.assertEqual(by_id["M1"]["merchandising"]["bundles"], [])
        self.assertEqual(
            by_id["M1"]["merchandising"]["relationship_audit"]["bundle_policy"],
            "no_approved_bundle_rule_no_bundle",
        )

        for record in resolved:
            self.assertEqual(validate_record(record), [])

    def test_resolver_is_deterministic(self):
        first = self.ready_catalog()
        second = self.ready_catalog()
        self.assertEqual(first, second)

    def test_adapter_preserves_raw_catalog_and_integrates_resolution(self):
        raw = self.raw_catalog()
        before = [dict(item) for item in raw]
        resolved = produce_catalog(raw)
        self.assertEqual(raw, before)
        self.assertTrue(all("relationship_audit" in item["merchandising"] for item in resolved))

    def test_non_ready_record_is_rejected(self):
        record = self.raw("BLOCKED", "Necklace", "Black")
        with self.assertRaisesRegex(ValueError, "PRODUCTION_READY"):
            resolve_catalog([record])


if __name__ == "__main__":
    unittest.main()
