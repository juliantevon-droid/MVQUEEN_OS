"""Regression checks for the screenshot homepage release contract."""
import copy
import json
from pathlib import Path
import unittest

from storefront_release_audit import reference_home_issues


class ReferenceHomeContractTest(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[2]
        self.index = json.loads((root / "storefront/theme/templates/index.json").read_text())
        self.home = self.index["sections"]["reference_home"]

    def test_configured_home_is_complete(self):
        self.assertEqual(reference_home_issues(self.index), [])

    def test_unordered_or_disabled_brand_cannot_pass(self):
        for key in ("mvqueen", "princess"):
            for mode in ("unordered", "disabled"):
                with self.subTest(key=key, mode=mode):
                    index = copy.deepcopy(self.index)
                    home = index["sections"]["reference_home"]
                    if mode == "unordered":
                        home["block_order"].remove(key)
                    else:
                        home["blocks"][key]["disabled"] = True
                    self.assertTrue(reference_home_issues(index))

    def test_missing_customer_destinations_cannot_pass(self):
        self.home["blocks"]["mvqueen"]["settings"]["link"] = "/"
        self.home["settings"]["collection"] = ""
        self.home["blocks"]["activewear"]["settings"]["collection"] = ""
        self.home["settings"]["beauty_link"] = ""
        self.assertEqual(len(reference_home_issues(self.index)), 4)


if __name__ == "__main__":
    unittest.main()
