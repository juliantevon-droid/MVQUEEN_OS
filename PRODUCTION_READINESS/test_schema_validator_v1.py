import unittest

from SCHEMA_VALIDATOR_V1 import validate_record


class SchemaValidatorV1Tests(unittest.TestCase):
    def valid_record(self):
        return {
            "schema_version": "1.0",
            "identity": {"product_id": "p-001", "source_name": "supplier"},
            "source_truth": {"facts": [{"name": "material", "value": "satin", "source": "supplier", "verified": True}]},
            "protected_fields": {"fields": ["sku", "inventory"]},
            "category": {"product_type": "dress"},
            "pricing": {"source_price": 20, "approved_publish_price": 49.99},
            "images": {"items": [{"src": "https://example.test/image.jpg", "alt": "Black satin dress"}]},
            "intelligence": {"customer_need": "evening styling", "positioning": "polished confidence"},
            "copy": {"title": "Midnight Satin Dress", "short_description": "A polished evening silhouette.", "description": "Designed for confident styling."},
            "seo": {"seo_title": "MVQueen | Midnight Satin Dress", "meta_description": "A polished satin dress for confident evening styling.", "primary_keyword": "satin dress", "alt_texts": ["Black satin evening dress"]},
            "merchandising": {"collections": ["Dresses"], "tags": ["satin"]},
            "commercial": {"angle": "polished confidence", "proof_available": ["verified satin material"]},
            "creative": {"assets": [{"channel": "meta", "asset_type": "static", "brief": "Show the evening silhouette."}]},
            "measurement": {"events": ["ViewContent", "AddToCart", "BeginCheckout", "Purchase"], "primary_kpi": "conversion_rate"},
            "qa": {"errors": [], "warnings": [], "passed": True},
            "status": "PRODUCTION_READY",
        }

    def test_valid_record_passes(self):
        self.assertEqual(validate_record(self.valid_record()), [])

    def test_missing_required_property_fails(self):
        record = self.valid_record()
        del record["seo"]["primary_keyword"]
        self.assertTrue(any("primary_keyword" in error for error in validate_record(record)))

    def test_unexpected_property_fails(self):
        record = self.valid_record()
        record["unexpected"] = "blocked"
        self.assertTrue(any("unexpected" in error for error in validate_record(record)))

    def test_invalid_enum_fails(self):
        record = self.valid_record()
        record["status"] = "PUBLISHED"
        self.assertTrue(any("enum" in error for error in validate_record(record)))

    def test_meta_description_length_fails(self):
        record = self.valid_record()
        record["seo"]["meta_description"] = "x" * 161
        self.assertTrue(any("maxLength" in error for error in validate_record(record)))


if __name__ == "__main__":
    unittest.main()
