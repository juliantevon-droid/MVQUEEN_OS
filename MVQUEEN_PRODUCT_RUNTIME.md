# MVQUEEN OS — Shopify Product Runtime

Shopify product event -> authenticated webhook -> idempotent ProductJob -> classification/transport worker -> guarded Admin GraphQL write.

## Protected data
The runtime must not modify SKU, inventory, pricing, variant configuration, fulfillment data, existing handles, product titles, descriptions, SEO copy, or factual product attributes unless a separate approved canonical publishing operation explicitly authorizes those fields.

## Current automation
The React worker classifies products, adds internal routing tags/classification metafields, and can fill missing image ALT text from the existing product title. It is not a product-copy generator.

Product titles, descriptions, SEO, verified factual metafields, FAQs, collection drafts, and blog drafts are owned by the governed production-readiness pipeline and CONTENT_INTELLIGENCE_V1. Those outputs remain review/approval controlled before Shopify publication.

## Deployment gate
shopify.app.toml intentionally uses a placeholder application URL and empty client ID until the actual Shopify app is linked. Do not deploy that configuration unchanged.

The runtime package uses the configured Shopify API version. Validate the app package and webhook version alignment before production deployment.
