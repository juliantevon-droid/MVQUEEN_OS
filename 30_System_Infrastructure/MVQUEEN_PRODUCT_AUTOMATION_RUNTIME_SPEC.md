# MVQueen Product Automation Runtime Specification
## MVQUEEN_OS / 30_System_Infrastructure

Status: LIVE AND VERIFIED — always-on Shopify product automation is active in production

## Objective
Automatically process every eligible Shopify product after creation or meaningful update.

## Runtime flow
1. Shopify emits products/create or products/update.
2. Webhook endpoint verifies Shopify authenticity.
3. Event ID is checked for idempotency.
4. Product ID is placed on the MVQueen processing queue.
5. Worker fetches authoritative product data with Admin GraphQL.
6. Deterministic classifier assigns taxonomy and routing.
7. Editorial/SEO generator creates content from verified facts.
8. Validator rejects unsupported claims and protected-field changes.
9. Approved fields are written to Shopify.
10. Image alt text is updated where appropriate.
11. Product is automatically routed through mvq collection tags.
12. Worker re-reads Shopify and verifies the result.
13. Processing result is recorded for audit/recovery.

## Required runtime components
- Shopify app configuration
- authenticated Admin GraphQL client
- webhook endpoints
- persistent job store/queue
- idempotency store
- product processor
- taxonomy/routing engine
- content generator adapter
- validation engine
- audit logger
- retry/dead-letter handling
- health/observability endpoint

## Safety contract
Never modify SKU, inventory, variants, price, fulfillment settings, vendor, source media, handles, or redirects through the automatic catalog worker.

Never invent product specifications, materials, ingredients, measurements, performance claims, certifications, or benefits that are not supported by available source facts.

Existing valid content should be preserved when generation fails.

## Processing policy
Draft products may be processed for completeness, but publication status must not be changed by the catalog worker unless a separate publication policy is explicitly enabled.

Products with low classification confidence or conflicting source facts go to Needs Review instead of receiving fabricated classification.

## Loop prevention
Every write must be traceable to a processing version/fingerprint. A webhook caused by the worker's own write must not start an infinite processing cycle.

## Backfill
Existing catalog processing is a separate queue-driven operation. It must support pause, resume, checkpointing, dry-run, retry, and per-product audit records.

## Current implementation
Implemented in the React/Shopify runtime:
- authenticated products/create and products/update webhook routes
- webhook/event-key idempotency through ProductJob
- automatic safe product enrollment behind MVQ_AUTO_PRODUCT_ENROLLMENT_ENABLED
- deterministic taxonomy and brand routing
- factual short-description, highlights, focus-keyword and long-tail SEO enrichment
- Shopify SEO title/meta writes behind MVQ_EDITORIAL_PUBLISH_ENABLED
- missing image ALT repair behind MVQ_MEDIA_ALT_SYNC_ENABLED and write_files
- source fingerprint/version loop prevention
- protected commerce-field boundary
- durable catalog backfill queue and bounded worker path
- production environment preflight
- durable product worker with concurrency-safe claims
- exponential retry and dead-letter handling
- stale-processing recovery
- missed-webhook reconciliation against recently updated Shopify products
- automatic product FAQ publishing
- automatic matching collection-content updates
- qualifying source-rich blog publishing
- queue-aware health endpoint
- five-minute GitHub Actions fallback scheduler

## Verified production activation — 2026-10-02

- Railway production project: `MVQUEEN_OS`.
- `mvqueen-web`, `mvqueen-product-worker`, `mvqueen-agent-worker`, and PostgreSQL are deployed successfully.
- Production source is GitHub `main`; verified runtime commit: `9dab8a85f8e4e1e0eff463a4f4c7398d87a65699`.
- MVQueen OS authenticated Shopify webhook audit reports:
  - `PRODUCTS_CREATE=true`
  - `PRODUCTS_UPDATE=true`
  - 2 product webhook subscriptions
  - webhook health `true`
- The continuous Railway product worker is running and polling the durable queue.
- Post-deploy queue state verified at `received=0 / processing=0 / failed=0 / deadLetter=0`.
- The strict public `/healthz` gate returned 503 while the worker was starting, then 200 after the worker/webhook heartbeat became healthy. This confirms the health endpoint fails closed rather than reporting readiness before the complete runtime is available.
- Reconciliation remains enabled as the missed-webhook recovery path.
- Source-fingerprint/version state plus Shopify update timestamps suppress automation-generated update loops.
- GitHub's scheduled runtime workflow is a read-only health monitor; Railway remains the continuous queue/reconciliation owner.
- Current Shopify products contain production evidence of the automation path: MVQueen/Miss.Princess brand routing, taxonomy, collection tags, short descriptions, highlights, focus and long-tail SEO fields, image ALT status, Google Shopping attributes, commercial-health state, lifecycle/marketing planning state, and governed pricing metadata.


## Production operating contract

The always-on product runtime is production-active.

A Shopify product create or meaningful update now follows this governed path:

`Shopify product event → authenticated webhook → idempotent ProductJob → continuous Railway worker → authoritative Shopify re-read → classification/brand routing → factual editorial/SEO/metafields/ALT/commercial processing → protected-field-safe Shopify write → automation-state fingerprint → self-generated webhook suppression`

The runtime remains fail-closed:

- no publication-status changes from this worker
- no SKU or inventory mutation
- no variant-option mutation
- no handle mutation
- no invented materials, ingredients, dimensions, certifications, efficacy or product claims
- no manufactured compare-at discount
- low-confidence classification routes to review rather than fabrication
- established nonblank product descriptions are not rewritten on ordinary update events unless the separate existing-description rewrite gate is explicitly enabled
- product-content surfaces only publish when their individual eligibility and kill-switch requirements are satisfied
- legal/policy pages remain protected from product-content automation

Production readiness is continuously observable through Railway health, worker/webhook heartbeats, queue state, and the scheduled GitHub `/healthz` monitor.
