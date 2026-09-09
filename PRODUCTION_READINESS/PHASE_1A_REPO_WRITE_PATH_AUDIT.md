# MVQUEEN_OS — Phase 1A Repository Write-Path Audit

## Purpose

This audit extends the architecture audit from the production branch to the full repository, with special attention to Shopify/API write paths. The goal is to ensure that the canonical production pipeline is the only route capable of publishing a product.

## Audited production branch

- Branch: `production/enterprise-hardening-v1`
- Baseline currently being hardened: `6e5791775bedf695f78a355849af528012bbd177`
- Scope: repository-wide; this is an audit of existing code paths, not a mass catalog rollout.

## Canonical production path

`RAW → NORMALIZED → INTELLIGENCE_READY → COPY_READY → SEO_READY → MERCH_READY → COMMERCIAL_READY → CREATIVE_READY → QA_PASSED → PRODUCTION_READY → APPROVED_FOR_PUBLISH → PUBLISHING_BOUNDARY → SHOPIFY`

Only the controlled production publisher may cross the final Shopify boundary.

## Findings

### CRITICAL — legacy Shopify sync engine still contains direct write capability

`15_Scripts_And_Code/mvqueen_engine/sync.py`

Observed capabilities:

- direct HTTP requests to Shopify Admin API
- product creation through `POST products.json`
- product updates through the sync transport
- metafield writes
- custom collection creation
- collection assignment
- variant construction including price/SKU/inventory settings
- a `sync_product()` method that chains creation, metafields, and collections

This conflicts with the enterprise publishing boundary and is capable of changing protected fields. It must not remain an independently callable production publisher.

### CRITICAL — legacy sync engine contains auto-publish behavior

`15_Scripts_And_Code/mvqueen_engine/sync_engine.py`

The current implementation can:

- create or update products
- write metafields
- upload images through an adapter
- call `publish_product()` automatically when `auto_publish` is enabled

This is a direct bypass of QA → approval → publishing boundary and must be retired from production use.

### CRITICAL — legacy bulk uploader remains capable of direct Shopify PUT

`15_Scripts_And_Code/shopify/mvqueen_api_uploader_v9_3.py`

Although the current file defaults to `DRY_RUN = True`, its live branch contains direct `requests.put()` against the Shopify Admin API. A production safety control cannot rely on a mutable source-code boolean. This path must be retired, isolated as historical tooling, or converted to a canonical release-artifact consumer.

### HIGH — legacy API abstraction exposes create/update/metafield operations

`15_Scripts_And_Code/mvqueen_engine/API.py`

The abstraction exposes `create_product()`, `update_product()`, and `update_metafields()`. These methods may be useful as a transport primitive, but they must not be exposed as independent production workflow entry points. Production code must reach transport only through the controlled publisher.

### HIGH — legacy metafield API wrapper exposes direct mutation

`15_Scripts_And_Code/mvqueen_engine/metafields_api.py`

This wrapper calls the legacy Shopify API abstraction for metafield writes. It must not be an independent production path.

### HIGH — legacy Shopify client contains multiple mutation surfaces

The repository contains both:

- `15_Scripts_And_Code/mvqueen_engine/shopify_client.py`
- `15_Scripts_And_Code/mvqueen_engine/shopify_api/shopify_client.py`

The existence of multiple transport/client implementations creates a governance and routing risk. They must be classified and reduced to one authoritative production transport behind the publisher boundary.

## Protected-field risk

The legacy sync layer can construct payloads containing fields that the current production contract explicitly protects, including:

- handle
- SKU
- variants/options
- variant price
- inventory quantity
- inventory management/policy

The production publisher V1 deliberately has a narrower write scope. Legacy sync code must not be allowed to bypass that scope.

## Required remediation order

1. **Quarantine legacy write entry points.** Preserve historical code where useful, but make production invocation fail closed.
2. **Keep one authoritative Shopify transport.** The controlled `SHOPIFY_PUBLISHER_V1` path is the production boundary.
3. **Make the publisher accept only approved release context.** A generated product record alone is not authorization to publish.
4. **Add idempotency before live publishing.** Repeating an approved operation must not create duplicate products or duplicate side effects.
5. **Add publish audit artifacts.** Every attempted publish needs a fingerprint, actor/system, timestamp, target, operation, result, and safe error/reference data.
6. **Add rollback/recovery.** Capture the pre-publish state for allowed mutable fields and restore only those fields.
7. **Expand CI static checks.** Detect new direct Shopify mutation calls outside the designated publisher/transport files.
8. **Add one-product end-to-end tests.** Prove the complete gate chain without requiring the 900+ catalog rollout.

## Production classification

| Component | Current classification | Required action |
|---|---|---|
| `PRODUCTION_READINESS/PRODUCT_PIPELINE_V1.py` | ACTIVE / CANONICAL | Keep authoritative |
| `PRODUCTION_READINESS/RELEASE_GATE_V1.py` | ACTIVE / CANONICAL | Keep authoritative |
| `PRODUCTION_READINESS/PUBLISHING_BOUNDARY_V1.py` | ACTIVE / CANONICAL | Keep authoritative |
| `PRODUCTION_READINESS/SHOPIFY_PUBLISHER_V1.py` | ACTIVE / CANONICAL | Harden and keep as only production publisher |
| `mvqueen_engine/sync.py` | LEGACY WRITE PATH | Quarantine |
| `mvqueen_engine/sync_engine.py` | LEGACY WRITE/PUBLISH PATH | Quarantine |
| `shopify/mvqueen_api_uploader_v9_3.py` | LEGACY BULK WRITE PATH | Quarantine |
| `mvqueen_engine/API.py` | LEGACY TRANSPORT API | Restrict to publisher transport use |
| `mvqueen_engine/metafields_api.py` | LEGACY MUTATION WRAPPER | Restrict/quarantine |
| duplicate Shopify clients | CONFLICTING TRANSPORTS | Consolidate authority |

## Non-goals

- No 900+ product rollout.
- No bulk publishing implementation.
- No automatic live Shopify changes during this hardening phase.
- No deletion of historical doctrine merely because it is not the current implementation.

## Exit criteria for this audit

The repository is not considered production-ready until no independent legacy path can publish, create, delete, or mutate Shopify data outside the canonical release boundary, and the remaining production publisher is covered by idempotency, audit, rollback, security, and end-to-end tests.
