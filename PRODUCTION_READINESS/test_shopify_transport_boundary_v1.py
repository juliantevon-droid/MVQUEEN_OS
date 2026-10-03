"""Tests for the unified Shopify write boundary."""
from __future__ import annotations

import unittest
from pathlib import Path

from SHOPIFY_PUBLISHER_V1 import ShopifyPublisherError, publish_to_shopify


ROOT = Path(__file__).resolve().parents[1]


def record():
    return {
        "identity": {"product_id": "123"},
        "category": {"product_type": "dress"},
        "copy": {"title": "Midnight Satin", "description": "A polished evening silhouette."},
        "merchandising": {"tags": ["MVQueen", "Evening"]},
    }


class UnifiedTransportBoundaryTests(unittest.TestCase):
    def test_python_has_no_default_live_transport(self):
        with self.assertRaises(ShopifyPublisherError):
            publish_to_shopify(record())

    def test_legacy_transport_modules_are_absent(self):
        retired = [
            "15_Scripts_And_Code/mvqueen_engine/Access_token.py",
            "15_Scripts_And_Code/mvqueen_engine/shopify_client.py",
            "15_Scripts_And_Code/mvqueen_engine/shopify_graphql_client.py",
            "15_Scripts_And_Code/mvqueen_engine/shopify_api/shopify_client.py",
            "15_Scripts_And_Code/session_manager.py",
        ]
        for rel in retired:
            self.assertFalse((ROOT / rel).exists(), rel)

    def test_catalog_worker_has_no_network_write_transport(self):
        text = (ROOT / "30_System_Infrastructure/catalog/mvqueen_catalog_worker.py").read_text(encoding="utf-8")
        self.assertNotIn("urllib.request", text)
        self.assertNotIn("requests.post", text)
        self.assertNotIn("productUpdate(", text)

    def test_react_app_is_declared_live_writer(self):
        text = (ROOT / "app/lib/product-processor.ts").read_text(encoding="utf-8")
        self.assertIn("MVQ_APPROVED_PRODUCT_GIDS", text)
        self.assertIn("admin.graphql(PRODUCT_UPDATE", text)
        self.assertNotIn("generateCatalogPackage", text)
        self.assertNotIn("MVQ_CONTENT_REWRITE_ENABLED", text)


    def test_content_publisher_is_governed_and_legal_pages_are_blocked(self):
        text = (ROOT / "app/lib/enterprise/content-publisher.ts").read_text(encoding="utf-8")
        route = (ROOT / "app/routes/app.proposals.tsx").read_text(encoding="utf-8")
        self.assertIn("articleCreate", text)
        self.assertIn("articleUpdate", text)
        self.assertIn("collectionUpdate", text)
        self.assertIn("pageCreate", text)
        self.assertIn("LEGAL_PAGE_HANDLES", text)
        self.assertIn("shipping-policy", text)
        self.assertIn("refund-policy", text)
        self.assertIn("record.content_suite", text)
        self.assertIn('approval.decision !== "APPROVED_FOR_PUBLISH"', text)
        self.assertIn('MVQ_BLOG_PUBLISH_ENABLED !== "true"', text)
        self.assertIn('MVQ_COLLECTION_CONTENT_PUBLISH_ENABLED !== "true"', text)
        self.assertIn('MVQ_FAQ_PAGE_PUBLISH_ENABLED !== "true"', text)
        self.assertIn('MVQ_STATIC_PAGE_PUBLISH_ENABLED !== "true"', text)
        self.assertIn('MVQ_BLOG_CREATE_IF_MISSING !== "true"', text)
        self.assertIn('MVQ_CONTENT_SURFACES_PUBLISH_ENABLED === "true"', route)
        self.assertIn("contentSurfacesPublishEnabled", route)
        canonical = (ROOT / "app/lib/enterprise/canonical-proposal.ts").read_text(encoding="utf-8")
        self.assertIn('"seo"', canonical)
        self.assertIn('"internal_links"', canonical)
        self.assertIn('target.startsWith("/products/")', canonical)
        self.assertIn('target.startsWith("/collections/")', canonical)

    def test_shopify_app_declares_content_scopes(self):
        toml = (ROOT / "shopify.app.toml").read_text(encoding="utf-8")
        self.assertIn("read_content", toml)
        self.assertIn("write_content", toml)

    def test_shopify_app_declares_inventory_cost_scope(self):
        toml = (ROOT / "shopify.app.toml").read_text(encoding="utf-8")
        worker = (ROOT / "app/lib/product-processor.ts").read_text(encoding="utf-8")
        self.assertIn("read_inventory", toml)
        self.assertIn("MVQ_COST_SYNC_ENABLED", worker)
        self.assertIn("PRODUCT_QUERY_WITH_COST", worker)
        self.assertIn("read_inventory_scope_required", worker)


    def test_product_webhooks_are_fast_enqueue_only(self):
        for rel in [
            "app/routes/webhooks.products.create.tsx",
            "app/routes/webhooks.products.update.tsx",
        ]:
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("enqueueProductWebhook", text)
            self.assertNotIn("processProductJob", text)

        intake = (ROOT / "app/lib/product-job-intake.server.ts").read_text(encoding="utf-8")
        self.assertIn("productJob.upsert", intake)
        self.assertIn('status: "received"', intake)

    def test_always_on_product_worker_has_recovery_controls(self):
        worker = (ROOT / "app/lib/product-job-worker.server.ts").read_text(encoding="utf-8")
        route = (ROOT / "app/routes/internal.product-worker.ts").read_text(encoding="utf-8")
        schedule = (ROOT / ".github/workflows/product-worker.yml").read_text(encoding="utf-8")
        health = (ROOT / "app/routes/healthz.ts").read_text(encoding="utf-8")

        self.assertIn("recoverStaleProductJobs", worker)
        self.assertIn("dead_letter", worker)
        self.assertIn("reconcileRecentShopifyProducts", worker)
        self.assertIn("auditProductWebhookSubscriptions", worker)
        self.assertIn("ensureProductWebhookSubscriptions", worker)
        self.assertIn("registerWebhooks", worker)
        self.assertIn("product.webhooks.audit", worker)
        self.assertIn("product.webhooks.ensure", worker)
        self.assertIn('process.env.MVQ_WRITE_ENABLED !== "true"', worker)
        processor = (ROOT / "app/lib/product-processor.ts").read_text(encoding="utf-8")
        self.assertIn("automaticContentSurfaces: AUTO_CONTENT_SURFACES_ENABLED", processor)
        self.assertIn("editorialPublish: EDITORIAL_PUBLISH_ENABLED", processor)
        self.assertIn("titlePublish: TITLE_PUBLISH_ENABLED", processor)
        self.assertIn("seoPublish: SEO_PUBLISH_ENABLED", processor)
        self.assertIn("descriptionPublish: DESCRIPTION_PUBLISH_ENABLED", processor)
        self.assertIn("descriptionRewriteExisting: DESCRIPTION_REWRITE_EXISTING_ENABLED", processor)
        self.assertIn("pricePublish: PRICE_PUBLISH_ENABLED", processor)
        self.assertIn("compareAtPricePublish: COMPARE_AT_PRICE_PUBLISH_ENABLED", processor)
        self.assertIn('process.env.MVQ_TITLE_PUBLISH_ENABLED === "true"', processor)
        self.assertIn('process.env.MVQ_SEO_PUBLISH_ENABLED === "true"', processor)
        self.assertIn('process.env.MVQ_DESCRIPTION_PUBLISH_ENABLED === "true"', processor)
        self.assertIn('process.env.MVQ_DESCRIPTION_REWRITE_EXISTING_ENABLED === "true"', processor)
        self.assertIn('process.env.MVQ_PRICE_PUBLISH_ENABLED === "true"', processor)
        self.assertIn('process.env.MVQ_COMPARE_AT_PRICE_PUBLISH_ENABLED === "true"', processor)
        self.assertIn('process.env.MVQ_VENDOR_NORMALIZATION_ENABLED === "true"', processor)
        self.assertIn('productInput.vendor = "MVQueen"', processor)
        self.assertIn('key: "source_vendor"', processor)
        self.assertIn("if (TITLE_PUBLISH_ENABLED)", processor)
        self.assertIn("DESCRIPTION_PUBLISH_ENABLED &&", processor)
        self.assertIn("shouldPublishAutomatedDescription({", processor)
        self.assertIn("allowExistingRewrite: DESCRIPTION_REWRITE_EXISTING_ENABLED", processor)
        self.assertIn("if (SEO_PUBLISH_ENABLED)", processor)
        self.assertIn("PRODUCT_VARIANTS_BULK_UPDATE", processor)
        self.assertIn("variants(first: 100)", processor)
        self.assertIn("homogeneousVariantPricing", processor)
        self.assertIn("variantInputs", processor)
        self.assertIn("variant_cost_or_currency_mismatch", processor)
        self.assertIn("pricePublishable", processor)
        self.assertIn("input.compareAtPrice = null", processor)
        self.assertIn("Clear equal/lower/stale values", processor)
        self.assertIn("preliminaryDecision", processor)
        self.assertIn("recommendedPrice", processor)
        self.assertIn("buildEnterpriseProductDecision(", processor)
        self.assertIn("mediaAltSync: MEDIA_ALT_SYNC_ENABLED", processor)
        self.assertIn("costSync: COST_SYNC_ENABLED", processor)
        self.assertIn('"product.worker.paused"', worker)
        self.assertIn("attempted: 0", worker)
        self.assertIn("timingSafeEqual", route)
        self.assertIn("*/5 * * * *", schedule)
        self.assertIn("deadLetterJobs", health)
        self.assertIn("product-webhooks", health)
        self.assertIn("webhookHealthy", health)
        self.assertIn("capabilities: preflight.capabilities", health)
        self.assertNotIn("SHOPIFY_API_SECRET:", health)
        self.assertNotIn("MVQ_PRODUCT_WORKER_TOKEN:", health)


if __name__ == "__main__":
    unittest.main()
