import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "30_System_Infrastructure/system/registry/enterprise_capabilities.json"

class EnterpriseOperatingSystemV2Tests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(REGISTRY.read_text(encoding="utf-8"))

    def test_required_stages_exist(self):
        required = {
            "INGEST","SOURCE_TRUTH","CLASSIFY","BRAND_ROUTE","CONTENT","SEO",
            "MERCHANDISE","COMMERCIAL","PRICE","PROFITABILITY","CREATIVE",
            "QA","APPROVAL","PUBLISH","MEASURE","LEARN"
        }
        self.assertTrue(required.issubset(set(self.data["stages"])))

    def test_required_capabilities_registered(self):
        ids = {item["id"] for item in self.data["capabilities"]}
        required = {
            "brand_governance","catalog_ingest","classification","brand_routing",
            "content_intelligence","seo_intelligence","merchandising","pricing",
            "profitability","creative","paid_advertising","analytics","retention",
            "customer_support","inventory","orders_fulfillment","theme","qa","deployment"
        }
        self.assertTrue(required.issubset(ids))

    def test_money_and_ads_fail_closed(self):
        gates = self.data["non_negotiable_gates"]
        self.assertIn("No live price mutation", gates["money"])
        self.assertIn("No ad spend", gates["advertising"])
        pricing = next(x for x in self.data["capabilities"] if x["id"] == "pricing")
        ads = next(x for x in self.data["capabilities"] if x["id"] == "paid_advertising")
        self.assertEqual(pricing["writes"], "no_price_mutation")
        self.assertEqual(ads["execution"], "disabled")

    def test_connected_capabilities_have_execution_contracts(self):
        by_id = {item["id"]: item for item in self.data["capabilities"]}
        self.assertEqual(by_id["content_intelligence"]["status"], "connected_approved_handoff")
        self.assertEqual(by_id["seo_intelligence"]["status"], "connected_approved_handoff")
        self.assertEqual(by_id["pricing"]["status"], "connected_approval_required")
        self.assertEqual(by_id["paid_advertising"]["status"], "adapter_required")

    def test_runtime_files_exist(self):
        required = [
            "app/lib/enterprise/commercial-config.ts",
            "app/lib/enterprise/pricing-engine.ts",
            "app/lib/enterprise/marketing-engine.ts",
            "app/lib/enterprise/product-decision-engine.ts",
            "app/lib/enterprise/integration-status.ts",
            "app/lib/enterprise/lifecycle-engine.ts",
            "app/lib/enterprise/canonical-proposal.ts",
            "app/lib/product-processor.ts",
            "app/routes/app.proposals.tsx",
            "app/routes/app.pricing.tsx",
            "storefront/theme/assets/mvqueen-analytics.js",
        ]
        for rel in required:
            self.assertTrue((ROOT / rel).is_file(), rel)

if __name__ == "__main__":
    unittest.main()
