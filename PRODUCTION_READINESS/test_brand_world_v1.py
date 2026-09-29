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

    def test_authoritative_deep_color_routes_to_mvqueen(self):
        result = classify_brand_world(self.record(color="Black"))
        self.assertEqual(result["brand_world"], "mvqueen")
        self.assertEqual(result["brand_name"], "MVQueen")
        self.assertEqual(result["brand_tone"], "bold-authoritative")

    def test_mvqueen_authority_shades_route_to_mvqueen(self):
        for color in ("Gold", "Charcoal", "Burgundy", "Mustard"):
            with self.subTest(color=color):
                result = classify_brand_world(self.record(color=color))
                self.assertEqual(result["brand_world"], "mvqueen")
                self.assertEqual(result["brand_tone"], "bold-authoritative")

    def test_vivid_spring_summer_colors_route_to_miss_princess(self):
        for color in ("Sky Blue", "Electric Blue", "Lilac", "Mint", "Lemon"):
            with self.subTest(color=color):
                result = classify_brand_world(self.record(color=color))
                self.assertEqual(result["brand_world"], "miss-princess")
                self.assertEqual(result["brand_name"], "Miss.Princess")
                self.assertEqual(result["brand_tone"], "vivid-youthful")

    def test_colorful_base_color_routes_to_miss_princess(self):
        result = classify_brand_world(self.record(color="Pink"))
        self.assertEqual(result["brand_world"], "miss-princess")
        self.assertEqual(result["brand_routing_confidence"], "high")

    def test_colorful_base_color_remains_miss_princess_with_style_context(self):
        result = classify_brand_world(
            self.record(color="Pink", style="deep rich polished statement")
        )
        self.assertEqual(result["brand_world"], "miss-princess")

    def test_princess_style_can_route_ambiguous_color(self):
        result = classify_brand_world(
            self.record(color="Purple", style="bright vivid summer playful")
        )
        self.assertEqual(result["brand_world"], "miss-princess")

    def test_ambiguous_product_fails_closed(self):
        result = classify_brand_world(self.record(color="Purple"))
        self.assertEqual(result["brand_world"], "needs-review")
        self.assertEqual(result["brand_routing_confidence"], "review")


if __name__ == "__main__":
    unittest.main()
