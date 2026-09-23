import unittest

from COMMERCIAL_INTELLIGENCE_V1 import build_commercial, validate_commercial


class CommercialIntelligenceV1Tests(unittest.TestCase):
    def base_record(self):
        return {
            "identity": {"product_id": "P-001", "source_name": "supplier"},
            "source_truth": {"facts": [
                {"name": "material", "value": "satin", "source": "supplier", "verified": True},
                {"name": "color", "value": "black", "source": "supplier", "verified": True},
                {"name": "secret_claim", "value": "clinically proven", "source": "supplier", "verified": False},
            ]},
            "category": {"product_type": "dress"},
            "pricing": {"approved_publish_price": 49.99},
            "intelligence": {
                "customer_need": "an elevated evening look",
                "desire": "Feel polished and confident.",
                "differentiators": ["satin finish"],
                "objections": ["fit or sizing uncertainty"],
            },
            "merchandising": {
                "related_products": ["P-002"],
                "bundles": ["BUNDLE-001"],
            },
        }

    def test_builds_commercial_record(self):
        result = build_commercial(self.base_record())
        self.assertIn("approved_bundle", result["offer_eligibility"])
        self.assertIn("approved_cross_sell", result["offer_eligibility"])
        self.assertEqual(result["price_guardrail"], "approved_publish_price_required")
        self.assertIn("fit_or_sizing_information", result["landing_page_requirements"])

    def test_unverified_fact_is_not_proof(self):
        result = build_commercial(self.base_record())
        self.assertNotIn("Verified secret_claim: clinically proven", result["proof_available"])

    def test_missing_price_blocks_commercial_release(self):
        record = self.base_record()
        record["pricing"]["approved_publish_price"] = None
        result = build_commercial(record)
        self.assertEqual(result["price_guardrail"], "blocked_until_price_approved")
        self.assertIn("Commercial release is blocked until price approval", validate_commercial(result))

    def test_deterministic(self):
        self.assertEqual(build_commercial(self.base_record()), build_commercial(self.base_record()))


if __name__ == "__main__":
    unittest.main()
