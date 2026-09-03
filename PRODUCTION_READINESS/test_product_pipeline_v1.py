import copy
import unittest

from PRODUCT_PIPELINE_V1 import run, validate
from CANONICAL_ADAPTER_V1 import produce


class ProductPipelineV1Tests(unittest.TestCase):
    def base(self):
        return {
            "schema_version": "1.0",
            "identity": {"product_id": "TEST-001", "source_name": "supplier", "sku": "SKU-001"},
            "source_truth": {"facts": [
                {"name": "material", "value": "satin", "source": "supplier", "verified": True},
                {"name": "color", "value": "black", "source": "supplier", "verified": True},
                {"name": "use_context", "value": "evening styling", "source": "supplier", "verified": True},
            ]},
            "protected_fields": {"fields": ["sku", "inventory", "variant_id"]},
            "category": {"product_type": "dress"},
            "pricing": {"source_price": 20, "approved_publish_price": 49.99},
            "images": {"items": [{"src": "https://example.com/image.jpg"}]},
        }

    def test_verified_product_reaches_production_ready(self):
        result = run(self.base())
        self.assertEqual(result["status"], "PRODUCTION_READY")
        self.assertTrue(result["qa"]["passed"])
        self.assertTrue(result["seo"]["seo_title"].startswith("MVQueen | "))
        self.assertTrue(result["images"]["items"][0]["alt"])
        self.assertIn("confidence", result["copy"]["short_description"].lower())

    def test_unapproved_price_blocks_publication(self):
        product = self.base()
        product["pricing"]["approved_publish_price"] = None
        result = run(product)
        self.assertNotEqual(result["status"], "PRODUCTION_READY")
        self.assertIn("No approved_publish_price; recommendation cannot publish automatically", result["qa"]["errors"])

    def test_unverified_claim_is_not_promoted_into_copy(self):
        product = self.base()
        product["source_truth"]["facts"].append({"name": "claim", "value": "clinically proven", "source": "supplier", "verified": False})
        result = run(product)
        self.assertNotIn("clinically proven", str(result["copy"]).lower())
        self.assertEqual(result["status"], "PRODUCTION_READY")

    def test_generated_robotic_phrase_blocks_publication(self):
        result = run(self.base())
        result["copy"]["description"] += " This versatile and stylish piece is perfect for any occasion."
        errors, _ = validate(result)
        self.assertTrue(any("robotic" in error.lower() for error in errors))

    def test_deterministic_output(self):
        first = run(self.base())
        second = run(self.base())
        self.assertEqual(first["copy"], second["copy"])
        self.assertEqual(first["seo"], second["seo"])
        self.assertEqual(first["commercial"], second["commercial"])

    def test_adapter_preserves_protected_values_and_does_not_publish(self):
        product = self.base()
        original = copy.deepcopy(product)
        result = produce(product)
        self.assertEqual(product, original)
        self.assertEqual(result["identity"]["sku"], "SKU-001")
        self.assertEqual(result["status"], "PRODUCTION_READY")


if __name__ == "__main__":
    unittest.main()
