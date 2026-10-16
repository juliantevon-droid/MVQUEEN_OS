"""Offline tests for the read-only public storefront SEO crawler."""
import importlib.util
from pathlib import Path
import unittest

FILE = Path(__file__).with_name("storefront_seo_crawler.py")
spec = importlib.util.spec_from_file_location("storefront_seo_crawler", FILE)
assert spec and spec.loader
crawler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(crawler)


class CrawlerTests(unittest.TestCase):
    def test_url_allowlist(self):
        assert crawler.approved_url("https://tsucu0-1i.myshopify.com/robots.txt")
        assert crawler.approved_url("https://tsucu0-1i.myshopify.com/products/a?variant=10") == "https://tsucu0-1i.myshopify.com/products/a"
        for bad in ("http://tsucu0-1i.myshopify.com/products/a",
                    "https://evil.com/products/a",
                    "https://tsucu0-1i.myshopify.com/admin",
                    "https://tsucu0-1i.myshopify.com.evil.org/products/a"):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                crawler.approved_url(bad)

    def test_good_html_and_decorative_image(self):
        page = crawler.assess("https://tsucu0-1i.myshopify.com/products/a", b"""
          <title>A curated MVQueen dress</title>
          <meta name="description" content="A thoughtful everyday dress with elegant details, styled for comfort and confidence in your daily wardrobe.">
          <link rel="canonical" href="https://tsucu0-1i.myshopify.com/products/a">
          <h1>Dress</h1><img src="x" alt="">
        """)
        self.assertEqual(page["issues"], [])

    def test_missing_metadata_and_alt(self):
        page = crawler.assess("https://tsucu0-1i.myshopify.com/products/a", b'<img src="x">')
        self.assertTrue({"missing_title", "missing_meta_description", "missing_canonical",
                         "image_alt_missing", "h1_count_review"}.issubset(set(page["issues"])))

    def test_noindex_and_canonical_mismatch(self):
        page = crawler.assess("https://tsucu0-1i.myshopify.com/pages/a", b"""
          <title>Page</title><meta name="robots" content="noindex,follow">
          <link rel="canonical" href="https://tsucu0-1i.myshopify.com/pages/b"><h1>Page</h1>
        """)
        self.assertIn("noindex_review", page["issues"])
        self.assertIn("canonical_mismatch_review", page["issues"])


    def test_svg_payment_titles_do_not_extend_seo_title(self):
        url = "https://tsucu0-1i.myshopify.com/products/a"
        page = crawler.assess(url, b"""
          <html><head><title>Denim After Dark | MVQUEEN</title>
          <meta name="description" content="Explore our denim matching set and review its listed sizes, fabric, and available options for everyday outfits.">
          <link rel="canonical" href="https://tsucu0-1i.myshopify.com/products/a">
          </head><body><h1>Denim After Dark</h1>
          <svg><title>American Express</title></svg>
          <svg><title>Apple Pay</title></svg><img src="x" alt="">
          </body></html>
        """)
        self.assertEqual(page["title"], "Denim After Dark | MVQUEEN")
        self.assertNotIn("long_title", page["issues"])

    def test_rate_limited_scan_stops_and_is_incomplete(self):
        from unittest.mock import patch
        url = "https://tsucu0-1i.myshopify.com/products/a"
        with patch.object(crawler, "download", side_effect=[
            (200, "text/plain", b"User-agent: *" + bytes([10]) + b"Allow: /"),
            (429, "text/html", b""),
        ]) as fetch, patch.object(crawler, "sitemap_pages", return_value=[url]):
            result = crawler.run(120, 0.2)
        self.assertEqual(fetch.call_count, 2)
        self.assertTrue(result["scan_incomplete"])
        self.assertEqual(result["pages"][0]["issues"], ["rate_limited"])
        self.assertEqual(result["pages"][0]["status"], 429)

if __name__ == "__main__":
    unittest.main()
