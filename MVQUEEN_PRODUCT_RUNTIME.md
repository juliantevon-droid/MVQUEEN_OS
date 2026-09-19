# MVQUEEN OS — Shopify Product Runtime

Shopify product event -> authenticated webhook -> idempotent ProductJob -> MVQueen intelligence -> Admin GraphQL write -> image alt enrichment.

## Protected data
The runtime must not modify SKU, inventory, pricing, variant configuration, fulfillment data, or existing handles unless a separate approved migration explicitly enables those fields.

## Current automation
The first implementation classifies products from title/description, generates catalog copy, writes SEO metadata and classification metafields, adds internal routing tags, and fills missing image alt text.

## Deployment gate
shopify.app.toml intentionally uses a placeholder application URL and empty client ID until the actual Shopify app is linked. Do not deploy that configuration unchanged.

The runtime package currently uses the React Router Shopify package's October 2025 API enum while webhook subscriptions use the July 2026 webhook API version. Validate and upgrade the application API package before production deployment.
