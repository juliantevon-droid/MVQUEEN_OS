import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "30_System_Infrastructure/system/registry/enterprise_capabilities.json"

class EnterpriseOperatingSystemV2Tests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.workflows = json.loads(
            (ROOT / "30_System_Infrastructure/system/registry/enterprise_workflows.json").read_text(encoding="utf-8")
        )
        self.integrations = json.loads(
            (ROOT / "30_System_Infrastructure/system/registry/integration_requirements.json").read_text(encoding="utf-8")
        )

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
            "customer_support","inventory","orders_fulfillment","theme","qa","deployment",
            "finance","compliance","backup_recovery","media_alt_publication","production_database","catalog_health","commercial_cost_sync","commercial_settings"
        }
        self.assertTrue(required.issubset(ids))

    def test_money_and_ads_fail_closed(self):
        gates = self.data["non_negotiable_gates"]
        self.assertIn("No live price mutation", gates["money"])
        self.assertIn("No ad spend", gates["advertising"])
        pricing = next(x for x in self.data["capabilities"] if x["id"] == "pricing")
        ads = next(x for x in self.data["capabilities"] if x["id"] == "paid_advertising")
        self.assertEqual(pricing["writes"], "approved_single_variant_price_only")
        self.assertEqual(pricing["status"], "connected_approval_required")
        self.assertIn("MVQ_PRICE_PUBLISH_ENABLED=true", gates["money"])
        self.assertIn("authenticated human submission", gates["money"])
        self.assertEqual(ads["execution"], "disabled_until_provider_and_human_approval")

    def test_connected_capabilities_have_execution_contracts(self):
        by_id = {item["id"]: item for item in self.data["capabilities"]}
        self.assertEqual(by_id["content_intelligence"]["status"], "connected_approved_handoff")
        self.assertEqual(by_id["seo_intelligence"]["status"], "connected_approved_handoff")
        self.assertEqual(by_id["merchandising"]["status"], "connected_advisory_catalog_resolution")
        self.assertIn("no_live_relationship_write", by_id["merchandising"]["writes"])
        self.assertEqual(by_id["pricing"]["status"], "connected_approval_required")
        self.assertEqual(by_id["paid_advertising"]["status"], "adapter_interface_ready_external_connection_required")

    def test_operational_workflows_cover_enterprise_domains(self):
        ids = {item["id"] for item in self.workflows["workflows"]}
        required = {
            "product_intake","canonical_content_release","pricing_profitability",
            "merchandising","storefront_release","paid_media","analytics_learning",
            "retention_lifecycle","order_fulfillment","customer_care","finance",
            "compliance","backup_recovery","catalog_health_audit","commercial_configuration"
        }
        self.assertTrue(required.issubset(ids))
        paid = next(item for item in self.workflows["workflows"] if item["id"] == "paid_media")
        self.assertIn("no provider or human approval", paid["guard"].lower())
        content = next(item for item in self.workflows["workflows"] if item["id"] == "canonical_content_release")
        self.assertIn("MVQ_CONTENT_SURFACES_PUBLISH_ENABLED=true", content["guard"])
        self.assertIn("Legal policy pages are never automated", content["guard"])
        merchandising = next(item for item in self.workflows["workflows"] if item["id"] == "merchandising")
        self.assertEqual(merchandising["status"], "connected_advisory_catalog_resolution")
        self.assertIn("No cross-brand recommendations", merchandising["guard"])
        self.assertIn("no bundle creation without an approved bundle rule", merchandising["guard"].lower())

    def test_integration_requirements_make_blockers_explicit(self):
        by_capability = {item["capability"]: item for item in self.integrations["integrations"]}
        self.assertEqual(by_capability["media_alt_publication"]["state"], "permission_required")
        self.assertEqual(by_capability["paid_advertising"]["state"], "external_connection_required")
        self.assertEqual(by_capability["production_database"]["state"], "engineered_profile_deployment_required")
        self.assertEqual(by_capability["approved_price_publish"]["state"], "engineered_not_runtime_verified")
        self.assertIn("MVQ_PRICE_PUBLISH_ENABLED", by_capability["approved_price_publish"]["requirements"])
        self.assertEqual(by_capability["commercial_cost_sync"]["state"], "app_reauthorization_required")
        self.assertIn("read_inventory declared in Shopify app", by_capability["commercial_cost_sync"]["requirements"])

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
            "app/routes/app.catalog-health.tsx",
            "app/lib/enterprise/catalog-audit.ts",
            "app/lib/enterprise/commercial-settings.server.ts",
            "app/routes/app.commercial-settings.tsx",
            "storefront/theme/assets/mvqueen-analytics.js",
            "app/lib/enterprise/database-guard.server.ts",
            "prisma/production/schema.prisma",
            "prisma/production/migrations/20260925123000_init/migration.sql",
            "prisma/migrations/20260925170500_add_commercial_settings/migration.sql",
            "prisma/production/migrations/20260925170500_add_commercial_settings/migration.sql",
        ]
        for rel in required:
            self.assertTrue((ROOT / rel).is_file(), rel)

if __name__ == "__main__":
    unittest.main()
