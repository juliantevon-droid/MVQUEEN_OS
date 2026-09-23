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

    def shopify_specimen(self):
        return {
            "schema_version": "1.0",
            "identity": {
                "product_id": "gid://shopify/Product/9072508567750",
                "source_name": "Shopify",
                "handle": "natural-pink-thulite-norway-pendant-p-1664-sdp116759",
                "sku": "SDP116759",
            },
            "source_truth": {"facts": [
                {"name": "brand", "value": "DESIRE GEM", "source": "Shopify product record", "verified": True},
                {"name": "material", "value": "925 Sterling Silver", "source": "Shopify product record", "verified": True},
                {"name": "item_code", "value": "SDP116759", "source": "Shopify product record", "verified": True},
                {"name": "design_code", "value": "P-1664", "source": "Shopify product record", "verified": True},
                {"name": "main_stone", "value": "Pink Thulite", "source": "Shopify product record", "verified": True},
                {"name": "creation", "value": "Natural", "source": "Shopify product record", "verified": True},
                {"name": "size_length", "value": "1 2/5 inch", "source": "Shopify product record", "verified": True},
                {"name": "total_weight", "value": "6.70 Grams (Including Gemstone & Silver)", "source": "Shopify product record", "verified": True},
                {"name": "main_stone_size", "value": "17x22 mm", "source": "Shopify product record", "verified": True},
                {"name": "color", "value": "Pink", "source": "Shopify product record", "verified": True},
            ]},
            "protected_fields": {
                "fields": [
                    "product_id", "handle", "sku", "variant_id", "inventory_quantity",
                    "option1", "option2", "option3"
                ],
                "values": {
                    "product_id": "gid://shopify/Product/9072508567750",
                    "handle": "natural-pink-thulite-norway-pendant-p-1664-sdp116759",
                    "sku": "SDP116759",
                    "variant_id": "gid://shopify/ProductVariant/47269565890758",
                    "inventory_quantity": 1,
                },
            },
            "category": {
                "product_type": "925 Sterling Silver Pendant",
                "category": "Jewelry",
                "subcategory": "Pendant",
            },
            "pricing": {
                "source_price": 26.39,
                "currency": "USD",
                "approved_publish_price": 26.39,
            },
            "images": {"items": [
                {"src": "https://cdn.shopify.com/s/files/1/0764/2618/2854/files/SDP116759_2.jpg?v=1789676736"},
                {"src": "https://cdn.shopify.com/s/files/1/0764/2618/2854/files/SDP116759_1_bdbbc142-7e5c-4df0-b688-b660a50db6e0.jpg?v=1789676736"},
                {"src": "https://cdn.shopify.com/s/files/1/0764/2618/2854/files/SDP116759_3.jpg?v=1789676737"},
            ]},
        }

    def test_verified_product_reaches_production_ready(self):
        result = run(self.base())
        self.assertEqual(result["status"], "PRODUCTION_READY")
        self.assertTrue(result["qa"]["passed"])
        self.assertTrue(result["seo"]["seo_title"].startswith("MVQueen | "))
        self.assertTrue(result["images"]["items"][0]["alt"])
        self.assertTrue(any(term in result["copy"]["short_description"].lower() for term in ("satin", "polished", "style")))
        self.assertTrue(any(term in result["copy"]["description"].lower() for term in ("modern", "feminine", "polished", "intentional")))

    def test_live_shopify_specimen_reaches_production_ready(self):
        product = self.shopify_specimen()
        protected_before = copy.deepcopy(product["protected_fields"]["values"])

        result = produce(product)

        self.assertEqual(result["status"], "PRODUCTION_READY")
        self.assertTrue(result["qa"]["passed"])
        self.assertEqual(result["qa"]["errors"], [])
        self.assertEqual(result["identity"]["product_id"], protected_before["product_id"])
        self.assertEqual(result["identity"]["handle"], protected_before["handle"])
        self.assertEqual(result["identity"]["sku"], protected_before["sku"])
        self.assertEqual(result["pricing"]["approved_publish_price"], 26.39)
        self.assertEqual(len(result["seo"]["alt_texts"]), 3)
        self.assertEqual(len(result["creative"]["assets"]), 5)
        self.assertEqual(result["commercial"]["funnel_stage"], "consideration")
        self.assertEqual(product["protected_fields"]["values"], protected_before)

    def test_canonical_commercial_engine_is_enforced(self):
        result = run(self.base())
        commercial = result["commercial"]
        self.assertEqual(commercial["funnel_stage"], "consideration")
        self.assertIn("PRODUCT → COMPLEMENT → BUNDLE → THRESHOLD", commercial["aov_strategy"]["path"])
        self.assertIn("verified_specifications", commercial["landing_page_requirements"])

    def test_canonical_creative_engine_is_enforced(self):
        result = run(self.base())
        assets = result["creative"]["assets"]
        channels = {asset["channel"] for asset in assets}
        self.assertTrue({"Meta", "TikTok", "UGC", "Email", "SMS"}.issubset(channels))
        self.assertTrue(all(asset["hook"] and asset["cta"] for asset in assets))
        self.assertTrue(all(asset["testing_variable"] for asset in assets))

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
        self.assertEqual(first["creative"], second["creative"])

    def test_adapter_preserves_protected_values_and_does_not_publish(self):
        product = self.base()
        original = copy.deepcopy(product)
        result = produce(product)
        self.assertEqual(product, original)
        self.assertEqual(result["identity"]["sku"], "SKU-001")
        self.assertEqual(result["status"], "PRODUCTION_READY")


if __name__ == "__main__":
    unittest.main()
