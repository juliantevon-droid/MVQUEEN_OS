from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKER_PATH = ROOT / "30_System_Infrastructure" / "catalog" / "mvqueen_catalog_worker.py"


def load_worker():
    spec = importlib.util.spec_from_file_location("mvqueen_catalog_worker", WORKER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load catalog worker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CatalogRecoveryControlsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.worker = load_worker()

    def test_recovered_supplier_identities_are_blocked(self):
        required = {
            "EPROLO",
            "DROPSURE",
            "JAYSUING",
            "ROXELIS",
            "DESIRE GEM",
            "MIA JEWELRY",
            "OUHOE",
        }
        self.assertTrue(required.issubset(set(self.worker.FORBIDDEN)))

    def test_supplier_brand_in_customer_copy_fails_closed(self):
        record = {
            "id": "gid://shopify/Product/1",
            "verified_facts": {"title": "verified"},
            "optimized": {
                "title": "EPROLO Glow Serum",
                "description_html": "<p>Verified description.</p>",
                "seo_title": "Glow Serum",
                "seo_description": "Verified serum description.",
                "tags": [],
            },
            "protected_changes": [],
        }
        with self.assertRaisesRegex(ValueError, "forbidden supplier/legacy brand"):
            self.worker.validate_record(record, 1)

    def test_worker_remains_validation_only(self):
        text = WORKER_PATH.read_text(encoding="utf-8")
        forbidden_transport = (
            "productCreate(",
            "productUpdate(",
            "requests.post(",
            "requests.put(",
            "requests.patch(",
            "urllib.request",
        )
        for token in forbidden_transport:
            self.assertNotIn(token, text)


if __name__ == "__main__":
    unittest.main()
