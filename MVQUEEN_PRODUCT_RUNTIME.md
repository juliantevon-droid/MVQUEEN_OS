# MVQueen OS — Shopify Product Runtime

Shopify product event -> authenticated webhook -> idempotent ProductJob -> classification/transport worker -> guarded Admin GraphQL write.

## Protected data
The runtime must not modify SKU, inventory, pricing, variant configuration, fulfillment data, existing handles, product titles, descriptions, SEO copy, or factual product attributes unless a separate approved canonical publishing operation explicitly authorizes those fields.

## Current automation
The React worker classifies products, adds internal routing tags/classification metafields, and can fill missing image ALT text from the existing product title. It is not a product-copy generator.

Product titles, descriptions, SEO, verified factual metafields, FAQs, collection drafts, and blog drafts are owned by the governed production-readiness pipeline and CONTENT_INTELLIGENCE_V1. Those outputs remain review/approval controlled before Shopify publication.

## Deployment state
The production Shopify app is linked in `shopify.app.toml` to the Railway application URL and client ID. The client secret remains deployment-only and must never be committed.

The runtime package uses the configured Shopify API version. App/package, webhook-version, and scope alignment remain production gates whenever those settings change.


## Durable always-on safety net

The runtime now has three layers:

1. **Primary event path:** authenticated `products/create` and `products/update` webhooks create idempotent ProductJob records and process them immediately.
2. **Durable worker:** `POST /internal/product-worker` recovers stale jobs, retries failed jobs with exponential backoff, moves exhausted jobs to `dead_letter`, and processes queued work in bounded batches.
3. **Reconciliation:** when `MVQ_PRODUCT_RECONCILE_ENABLED=true`, the worker looks back over recently updated Shopify products and creates idempotent reconciliation jobs for any event the webhook path may have missed.

The Railway `mvqueen-product-worker` service runs continuously and owns bounded queue draining, retries, stale-lease recovery, dead-letter handling, and reconciliation. GitHub does not duplicate that ownership.

The repository workflow `.github/workflows/product-worker.yml` now performs a five-minute HTTPS health check against the production `/healthz` endpoint. A green workflow therefore means the deployed runtime answered successfully instead of silently skipping because secrets were absent.

The primary recovery model is Shopify webhooks + the continuous Railway worker + reconciliation + persistent Postgres.
