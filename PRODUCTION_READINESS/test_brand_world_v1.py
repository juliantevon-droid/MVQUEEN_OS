import unittest

from BRAND_WORLD_V1 import classify_brand_world


class BrandWorldV1Tests(unittest.TestCase):
    def record(self, **facts):
        return {
            "source_truth": {
                "facts": [
                    {"name": name, "value": value, "source": "fixture", "verified": True}
                    for name, value in facts.items()
                ]
            }
        }

    def test_soft_bright_color_routes_to_miss_princess(self):
        result = classify_brand_world(self.record(color="Pink"))
        self.assertEqual(result["brand_world"], "miss-princess")
        self.assertEqual(result["brand_name"], "Miss.Princess")

    def test_neutral_color_routes_to_mvqueen(self):
        result = classify_brand_world(self.record(color="Brown"))
        self.assertEqual(result["brand_world"], "mvqueen")
        self.assertEqual(result["brand_name"], "MVQueen")

    def test_style_can_route_when_color_is_ambiguous(self):
        result = classify_brand_world(self.record(color="Purple", style="soft romantic floral"))
        self.assertEqual(result["brand_world"], "miss-princess")

    def test_ambiguous_product_fails_closed(self):
        result = classify_brand_world(self.record(color="Purple"))
        self.assertEqual(result["brand_world"], "needs-review")
        self.assertEqual(result["brand_routing_confidence"], "review")


if __name__ == "__main__":
    unittest.main()
