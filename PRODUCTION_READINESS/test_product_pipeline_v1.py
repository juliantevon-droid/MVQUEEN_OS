import unittest

from PRODUCT_PIPELINE_V1 import run


class ProductPipelineV1Tests(unittest.TestCase):
    def base(self):
        return {
            "schema_version": "1.0",
            "identity": {"product_id": "TEST-001", "source_name": "supplier", "sku": "SKU-001"},
            "source_truth": {"facts": [
                {"name": "material", "value": "satin", "source": "supplier", "verified": True},
                {"name": "color", "value": "black", "source": "supplier", "verified": True},
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

    def test_unapproved_price_blocks_publication(self):
        product = self.base()
        product["pricing"]["approved_publish_price"] = None
        result = run(product)
        self.assertNotEqual(result["status"], "PRODUCTION_READY")
        self.assertIn("No approved_publish_price; recommendation cannot publish automatically", result["qa"]["errors"])

    def test_unsupported_claim_blocks_publication(self):
        product = self.base()
        product["source_truth"]["facts"].append({"name": "claim", "value": "clinically proven", "source": "supplier", "verified": False})
        result = run(product)
        self.assertNotEqual(result["status"], "PRODUCTION_READY")


if __name__ == "__main__":
    unittest.main()
