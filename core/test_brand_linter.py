import unittest
from core.brand_linter import deterministic, MAX_TITLE, MAX_META_TITLE, MAX_META_DESCRIPTION

class CanonicalBrandLinterTests(unittest.TestCase):
    def test_both_brand_worlds(self):
        for brand in ("MVQUEEN", "Miss.Princess"):
            self.assertEqual(deterministic({"title":"Personal Edit Face Cream", "description":"Net content: 30ml.", "brand":brand})[0], "PASS")

    def test_claim_and_language_boundaries(self):
        self.assertEqual(deterministic({"title":"Personal Edit Face Cream", "description":"Clinically proven to cure eczema."})[0], "HOLD")
        self.assertEqual(deterministic({"title":"Amazing Face Cream", "description":"Net content: 30ml."})[0], "HOLD")
        self.assertEqual(deterministic({"title":"Personal Edit Face Cream", "description":"Suitable for a familiar evening edit."})[0], "PASS")

    def test_active_policy_limits(self):
        self.assertEqual((MAX_TITLE,MAX_META_TITLE,MAX_META_DESCRIPTION),(80,60,155))

if __name__ == "__main__":
    unittest.main()
