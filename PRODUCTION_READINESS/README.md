# MVQueen Production Readiness

This directory contains the controlled production contracts for MVQUEEN_OS.

## Phase 2 V1 assets

- `PRODUCT_SCHEMA_V1.json` — canonical product record schema.
- `PRODUCT_PIPELINE_V1.py` — deterministic standard-library pipeline.
- `QA_CONTRACT_V1.md` — hard publication gate.
- `ENGINE_CONTRACTS_V1.md` — ownership and integration boundaries.
- `CONTENT_INTELLIGENCE_V1.py` — governed product-page, metafield, FAQ, collection, and blog draft generation.
- `CONTENT_AUTOMATION_CONTRACT_V1.md` — content truth and publishing rules.

## Release principle

The system must prove one product end-to-end before bulk catalog processing. Existing engines are not automatically authoritative merely because they already generate output.

## Current canonical flow

`RAW → NORMALIZED → INTELLIGENCE_READY → COPY_READY → SEO_READY → MERCH_READY → COMMERCIAL_READY → CREATIVE_READY → QA_PASSED → PRODUCTION_READY → APPROVED_FOR_PUBLISH → PUBLISHING_BOUNDARY → SHOPIFY`

## Real-product validation

The current specimen test uses a real Shopify product record without writing it back to Shopify. The specimen must pass the same canonical pipeline used for future products before any live publication is considered.

## Safety principle

Generated language may interpret verified facts, but it must never manufacture product facts, efficacy, certifications, reviews, scarcity, performance guarantees, or other unsupported claims.

## Governed content flow

`PRODUCTION_READY product → CONTENT_INTELLIGENCE_V1 → CONTENT_PUBLISH_ELIGIBLE → canonical approval/fingerprint → publishing boundary → Shopify content surfaces`

QA-passed content may publish to approved surfaces: product FAQ/metafields, qualifying blog articles, matched collection copy, and governed static pages. Sparse blog drafts remain held, product FAQ content does not overwrite the global FAQ page, and legal/policy pages remain excluded from automation. Product facts used in any surface must come from verified `source_truth` facts. Legacy generators that could synthesize protected or unsupported facts are retired and fail closed.
