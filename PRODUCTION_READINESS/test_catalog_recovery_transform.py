from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE_ROOT = ROOT / "15_Scripts_And_Code"
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

from mvqueen_engine.catalog_recovery_transform import transform_csv


class CatalogRecoveryTransformTests(unittest.TestCase):
    HEADERS = [
        "Handle", "Title", "Body (HTML)", "Vendor", "Status",
        "Variant SKU", "Variant Price", "Image Src", "Image Alt Text",
        "Tags", "SEO Title", "SEO Description",
        "MVQ Category", "MVQ Product Type",
    ]

    def write_csv(self, rows):
        tmp = tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="", suffix=".csv", delete=False
        )
        with tmp:
            writer = csv.DictWriter(tmp, fieldnames=self.HEADERS)
            writer.writeheader()
            writer.writerows(rows)
        return Path(tmp.name)

    def read_csv(self, path):
        with Path(path).open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            return list(reader.fieldnames or []), list(reader)

    def test_transform_preserves_shopify_row_structure_and_protected_fields(self):
        source = self.write_csv([
            {
                "Handle": "brown-aventurine",
                "Title": "OUHOE Amazing Brown Aventurine Necklace (F221)",
                "Body (HTML)": "<p>EPROLO necklace. Bulk Orders Accepted.</p>",
                "Vendor": "eprolo",
                "Status": "active",
                "Variant SKU": "SKU-1",
                "Variant Price": "13.09",
                "Image Src": "https://example.com/one.jpg",
                "Image Alt Text": "",
                "Tags": "OUHOE, jewelry",
                "SEO Title": "",
                "SEO Description": "",
                "MVQ Category": "home",
                "MVQ Product Type": "accessory",
            },
            {
                "Handle": "brown-aventurine",
                "Title": "",
                "Body (HTML)": "",
                "Vendor": "",
                "Status": "",
                "Variant SKU": "SKU-2",
                "Variant Price": "14.09",
                "Image Src": "https://example.com/two.jpg",
                "Image Alt Text": "",
                "Tags": "OUHOE, alternate image",
                "SEO Title": "OUHOE alternate view",
                "SEO Description": "EPROLO alternate image",

            },
        ])
        output = source.with_name(source.stem + "-out.csv")
        try:
            report = transform_csv(source, output)
            headers, rows = self.read_csv(output)
        finally:
            source.unlink(missing_ok=True)
            output.unlink(missing_ok=True)

        self.assertEqual(headers, self.HEADERS)
        self.assertEqual(len(rows), 2)

        self.assertEqual(rows[0]["Handle"], "brown-aventurine")
        self.assertEqual(rows[1]["Handle"], "brown-aventurine")
        self.assertEqual(rows[0]["Variant SKU"], "SKU-1")
        self.assertEqual(rows[1]["Variant SKU"], "SKU-2")
        self.assertEqual(rows[0]["Variant Price"], "13.09")
        self.assertEqual(rows[1]["Variant Price"], "14.09")
        self.assertEqual(rows[0]["Status"], "active")
        self.assertEqual(rows[1]["Status"], "")

        self.assertNotIn("OUHOE", rows[0]["Title"].upper())
        self.assertNotIn("EPROLO", rows[0]["Body (HTML)"].upper())
        self.assertEqual(rows[0]["Vendor"], "MVQueen")
        self.assertEqual(rows[1]["Vendor"], "")
        self.assertEqual(rows[1]["Title"], "")
        self.assertEqual(rows[1]["Body (HTML)"], "")
        self.assertNotIn("OUHOE", rows[1]["Tags"].upper())
        self.assertNotIn("OUHOE", rows[1]["SEO Title"].upper())
        self.assertNotIn("EPROLO", rows[1]["SEO Description"].upper())

        self.assertTrue(rows[0]["Image Alt Text"])
        self.assertTrue(rows[1]["Image Alt Text"])
        self.assertFalse(report["release_importable"])
        self.assertEqual(report["unique_products"], 1)
        self.assertEqual(report["hold_products"], 0)
        self.assertEqual(report["review_products"], 1)
        self.assertEqual(report["products"][0]["tier1_voice_violations"], [])
        self.assertNotIn("Amazing", rows[0]["Title"])
        self.assertEqual(rows[0]["MVQ Category"], "jewelry")
        self.assertEqual(rows[0]["MVQ Product Type"], "necklace")

    def test_clean_normalization_reaches_review_not_release(self):
        source = self.write_csv([{
            "Handle": "pink-thulite",
            "Title": "Pink Thulite Pendant in 925 Sterling Silver",
            "Body (HTML)": "<p>Pink thulite pendant set in 925 sterling silver.</p>",
            "Vendor": "DESIRE GEM",
            "Status": "active",
            "Variant SKU": "SDP116759",
            "Variant Price": "26.39",
            "Image Src": "https://example.com/pink.jpg",
            "Image Alt Text": "Pink thulite pendant",
            "Tags": "pink thulite, sterling silver",
            "SEO Title": "",
            "SEO Description": "",
        }])
        output = source.with_name(source.stem + "-out.csv")
        try:
            report = transform_csv(source, output)
            _, rows = self.read_csv(output)
        finally:
            source.unlink(missing_ok=True)
            output.unlink(missing_ok=True)

        self.assertEqual(report["hold_products"], 0)
        self.assertEqual(report["review_products"], 1)
        self.assertFalse(report["release_importable"])
        self.assertEqual(rows[0]["Vendor"], "MVQueen")
        self.assertEqual(rows[0]["Variant SKU"], "SDP116759")
        self.assertEqual(rows[0]["Variant Price"], "26.39")
        self.assertEqual(rows[0]["Status"], "active")


if __name__ == "__main__":
    unittest.main()
