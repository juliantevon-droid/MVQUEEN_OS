# MVQUEEN Enterprise Hardening V1

## Purpose

Move the canonical product pipeline from a content generator into a controlled production system. No product may be published merely because copy generation succeeded.

## Non-negotiable controls

1. **Source truth first** — factual claims must originate in verified source facts.
2. **Protected fields** — product identity, handles, SKUs, variants, and inventory references are immutable during editorial processing.
3. **Deterministic processing** — the same canonical input must produce the same editorial output.
4. **Explicit price approval** — `approved_publish_price` is required before a record can become production-ready.
5. **QA gate** — any QA error blocks production readiness.
6. **Approval gate** — `PRODUCTION_READY` is not equivalent to authorization to publish. Publishing requires a separate approval decision.
7. **Publishing boundary** — external writes may occur only after the release gate passes and the controlled publishing boundary authorizes hand-off.
8. **No bulk publishing by default** — the current production configuration keeps bulk publication disabled.
9. **Auditability** — release decisions must identify the product, schema version, content fingerprint, decision, actor/system, and timestamp.
10. **Idempotency** — repeated processing of the same canonical input must not create a different editorial result or duplicate release decision.
11. **Fail closed** — missing required evidence, malformed records, unsupported claims, or missing approval must block release.

## Release states

`RAW → NORMALIZED → INTELLIGENCE_READY → COPY_READY → SEO_READY → MERCH_READY → COMMERCIAL_READY → CREATIVE_READY → QA_PASSED → PRODUCTION_READY → APPROVED_FOR_PUBLISH → PUBLISHING_BOUNDARY → EXTERNAL PUBLISH`

`APPROVED_FOR_PUBLISH` is an operational release decision, not a product-record schema status. It must live in a separate audit/release artifact so the canonical product schema remains stable.

## Controlled publishing path

The only production path is:

`Canonical Product → Schema/QA → Release Fingerprint → Explicit Approval → Publishing Boundary → Dedicated Publisher → Shopify`

The publishing boundary is fail-closed and does not perform Shopify writes itself. It validates the release gate, then hands a deep copy of the approved canonical record to an injected publisher adapter.

Legacy catalog-processing code is not an alternate publishing route. Direct Shopify product, metafield, or variant updates from the legacy processor are disabled on the enterprise branch.

## Separation of duties

- **Generation:** creates the candidate product record.
- **QA:** evaluates the candidate against deterministic controls.
- **Approval:** authorizes publication after QA and commercial review.
- **Publishing boundary:** enforces the release authorization before any external side effect.
- **Publisher:** performs the external Shopify write only after the boundary authorizes it.

No generation function should call Shopify publication directly.

## Incident principle

If a release fails validation, the record is held. The system should report the blocking reason rather than silently repairing or inventing product facts.

## Scale principle

The system must prove correctness in this order:

`1 product → 10 products → 100 products → 900+ products → continuous operation`

Mass catalog processing comes only after the engine, QA, approval, idempotency, and rollback controls are proven.
