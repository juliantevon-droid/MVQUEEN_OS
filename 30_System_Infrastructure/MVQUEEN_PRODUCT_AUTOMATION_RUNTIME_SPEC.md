# MVQueen Product Automation Runtime Specification
## MVQUEEN_OS / 30_System_Infrastructure

Status: IMPLEMENTED IN MAIN — deployment and end-to-end production activation pending

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

Not yet activated as an always-on production service:
- real HTTPS application host
- production PostgreSQL database
- real Shopify app client configuration
- required app reauthorization for current scopes
- production automation environment switches
- verified end-to-end webhook test on a safe Shopify product

## Deployment gate
Do not call this system 24/7 production-ready until:
- app authentication works
- webhook registration succeeds
- HMAC/authenticity verification is tested
- queue persistence works
- one safe test product completes end-to-end
- protected fields are verified unchanged
- duplicate webhook delivery is safely deduplicated
- failure/retry behavior is tested
- logs are observable
- secrets are external to GitHub