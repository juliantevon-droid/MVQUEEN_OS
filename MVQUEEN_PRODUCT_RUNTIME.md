# MVQueen OS — Shopify Product Runtime

Shopify product event -> authenticated webhook -> idempotent ProductJob -> classification/transport worker -> guarded Admin GraphQL write.

## Protected data
The runtime must not modify SKU, inventory, pricing, variant configuration, fulfillment data, existing handles, product titles, descriptions, SEO copy, or factual product attributes unless a separate approved canonical publishing operation explicitly authorizes those fields.

## Current automation
The React worker classifies products, adds internal routing tags/classification metafields, and can fill missing image ALT text from the existing product title. It is not a product-copy generator.

Product titles, descriptions, SEO, verified factual metafields, FAQs, collection drafts, and blog drafts are owned by the governed production-readiness pipeline and CONTENT_INTELLIGENCE_V1. Those outputs remain review/approval controlled before Shopify publication.

## Deployment gate
shopify.app.toml intentionally uses a placeholder application URL and empty client ID until the actual Shopify app is linked. Do not deploy that configuration unchanged.

The runtime package uses the configured Shopify API version. Validate the app package and webhook version alignment before production deployment.


## Durable always-on safety net

The runtime now has three layers:

1. **Primary event path:** authenticated `products/create` and `products/update` webhooks create idempotent ProductJob records and process them immediately.
2. **Durable worker:** `POST /internal/product-worker` recovers stale jobs, retries failed jobs with exponential backoff, moves exhausted jobs to `dead_letter`, and processes queued work in bounded batches.
3. **Reconciliation:** when `MVQ_PRODUCT_RECONCILE_ENABLED=true`, the worker looks back over recently updated Shopify products and creates idempotent reconciliation jobs for any event the webhook path may have missed.

The repository workflow `.github/workflows/product-worker.yml` invokes the durable worker every 10 minutes only when repository variable `MVQ_PRODUCT_WORKER_ENABLED=true`. It additionally requires repository variable `MVQ_PRODUCT_WORKER_URL` and secret `MVQ_PRODUCT_WORKER_TOKEN`. The URL must be the production HTTPS endpoint ending in `/internal/product-worker`.

This scheduled worker is a recovery and reconciliation layer, not a substitute for Shopify webhooks. Until a real production app URL, client ID, database, worker token, and scheduler variables are configured, the code is deployment-ready but unattended 24/7 execution is not active.
