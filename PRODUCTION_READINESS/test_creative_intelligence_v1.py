import unittest

from CREATIVE_INTELLIGENCE_V1 import build_creative, validate_creative


class CreativeIntelligenceV1Tests(unittest.TestCase):
    def record(self):
        return {
            "identity": {"product_id": "P-001"},
            "source_truth": {"facts": [
                {"name": "material", "value": "satin", "source": "supplier", "verified": True},
                {"name": "claim", "value": "clinically proven", "source": "supplier", "verified": False},
            ]},
            "intelligence": {"desire": "Feel polished and confident."},
            "copy": {"title": "Midnight Satin Dress"},
            "commercial": {
                "angle": "Designed for an elevated evening look.",
                "proof_available": ["Verified material: satin"],
            },
        }

    def test_generates_channel_briefs(self):
        result = build_creative(self.record())
        channels = {asset["channel"] for asset in result["assets"]}
        self.assertTrue({"Meta", "TikTok", "UGC", "Email", "SMS"}.issubset(channels))

    def test_unverified_claim_is_not_used_as_proof(self):
        result = build_creative(self.record())
        joined = str(result)
        self.assertNotIn("clinically proven", joined)

    def test_creative_is_deterministic(self):
        self.assertEqual(build_creative(self.record()), build_creative(self.record()))

    def test_validation_passes_for_generated_briefs(self):
        result = build_creative(self.record())
        self.assertEqual(validate_creative(result), [])


if __name__ == "__main__":
    unittest.main()
