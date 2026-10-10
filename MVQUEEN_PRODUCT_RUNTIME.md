# MVQueen OS — Shopify Product Runtime

Shopify product event -> authenticated webhook -> idempotent ProductJob -> classification/transport worker -> guarded Admin GraphQL write.

## Protected data
The runtime preserves existing handles, SKUs, barcodes, inventory and variant configuration. Product copy, factual enrichment and commercial writes follow their existing publication gates. Loading brand references does not authorize additional fields or enable a gate.

## Current automation
The React worker classifies products, adds internal routing tags/classification metafields, and can repair image ALT text. Its current governed copy writer also builds product names, descriptions and SEO when configured gates permit them. Authored names and openings take precedence; new naming identities are checked against the current Shopify catalog.

The [unified brand policy](06_Tone_And_Voice/UNIFIED_BRAND_GUIDE.md) connects substantive Drive material to that writer. Both runtime images carry the active policy. Loaded policy, vocabulary, naming and authored content contribute to the automation version. Historical sources remain searchable references instead of executable code or replacement product facts.

Descriptions, verified factual metafields, FAQs, collection drafts and blog drafts continue through existing review, claim and publication controls. This integration does not start a bulk backfill or import an old product CSV.

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
