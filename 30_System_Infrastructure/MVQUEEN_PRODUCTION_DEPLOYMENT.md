# MVQueen OS — Production Deployment

## Runtime topology

MVQUEEN_OS is designed as one HTTPS Shopify web application plus a durable product worker.

1. Shopify sends `products/create` and `products/update` webhooks to the deployed app.
2. The webhook route authenticates the request, persists an idempotent `ProductJob`, and acknowledges quickly.
3. `POST /internal/product-worker` drains queued jobs, retries transient failures, recovers stale leases, and reconciles recently updated products that may have missed webhook delivery.
4. `GET /healthz` reports environment/database readiness and queue health.
5. GitHub Actions `.github/workflows/product-worker.yml` provides a five-minute fallback scheduler after its URL/token secrets are configured.

## Required production infrastructure

- Public HTTPS application host capable of running the Dockerfile.
- Managed PostgreSQL database.
- Persistent Shopify offline session for the installed store.
- Deployment secrets; never commit real values.
- An external scheduler or continuously running worker caller. The included GitHub Actions scheduler can serve as the fallback.

## Required environment gates

The deployment must pass `npm run preflight:production`.

Required for full hands-off automation:

- `SHOPIFY_API_KEY`
- `SHOPIFY_API_SECRET`
- `SHOPIFY_APP_URL` — real HTTPS host
- `DATABASE_URL` — PostgreSQL
- `MVQ_DATABASE_PROFILE=production`
- `MVQ_WRITE_ENABLED=true`
- `MVQ_AUTO_PRODUCT_ENROLLMENT_ENABLED=true`
- `MVQ_EDITORIAL_PUBLISH_ENABLED=true`
- `MVQ_AUTO_CONTENT_SURFACES_ENABLED=true`
- `MVQ_MEDIA_ALT_SYNC_ENABLED=true`
- `MVQ_COST_SYNC_ENABLED=true`
- `MVQ_PRODUCT_RECONCILE_ENABLED=true`
- `MVQ_PRODUCT_WORKER_TOKEN` — at least 32 random characters
- Shopify scopes declared in `shopify.app.toml`

Per-surface content controls remain independently kill-switchable.

## GitHub Actions fallback secrets

Configure these repository secrets only after the public app host exists:

- `MVQ_PRODUCT_WORKER_URL=https://<real-host>/internal/product-worker`
- `MVQ_PRODUCT_WORKER_TOKEN=<same deployment secret>`

The workflow deliberately skips without printing secret values when they are not configured.

## Shopify app configuration

Before deployment/release:

- Replace the placeholder `client_id` in `shopify.app.toml` with the linked Shopify app client ID through the deployment configuration process.
- Replace `https://example.com` with the real production HTTPS application URL.
- Validate the configuration with Shopify CLI.
- Deploy/release the Shopify app configuration so the product webhook subscriptions point to the production host.
- Reauthorize the app if Shopify requires approval for changed scopes.

## Verification sequence

1. Deploy the container and PostgreSQL migrations.
2. Confirm `GET /healthz` returns HTTP 200.
3. Confirm Shopify app authentication works on the deployed host.
4. Confirm product webhook subscriptions are registered.
5. Add one safe test product.
6. Verify the webhook creates one durable job and acknowledges without doing heavy work inline.
7. Run the product worker and verify the job completes.
8. Verify only authorized editorial/catalog fields changed.
9. Verify product FAQ, matching collection content, and qualifying blog behavior.
10. Verify SKU, price, inventory, variants, handle, fulfillment configuration, and source media relationships remain unchanged.
11. Trigger a duplicate event and verify idempotency.
12. Trigger a controlled transient failure and verify retry/dead-letter behavior.
13. Configure the GitHub fallback scheduler secrets.
14. Re-check `/healthz` and production preflight.

## Current boundary

Repository implementation and CI readiness do not prove that the app is live. Live 24/7 status requires evidence from the deployed HTTPS host, PostgreSQL database, Shopify webhook delivery, and worker execution.
