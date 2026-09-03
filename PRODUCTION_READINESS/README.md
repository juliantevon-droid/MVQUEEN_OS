# MVQUEEN Production Readiness

This directory contains the controlled production contracts for MVQUEEN_OS.

## Phase 2 V1 assets

- `PRODUCT_SCHEMA_V1.json` — canonical product record schema.
- `PRODUCT_PIPELINE_V1.py` — deterministic standard-library pipeline.
- `QA_CONTRACT_V1.md` — hard publication gate.
- `ENGINE_CONTRACTS_V1.md` — ownership and integration boundaries.

## Release principle

The system must prove one product end-to-end before bulk catalog processing. Existing engines are not automatically authoritative merely because they already generate output.

## Current canonical flow

`RAW → NORMALIZED → INTELLIGENCE_READY → COPY_READY → SEO_READY → MERCH_READY → COMMERCIAL_READY → CREATIVE_READY → QA_PASSED → PRODUCTION_READY`

## Safety principle

Generated language may interpret verified facts, but it must never manufacture product facts, efficacy, certifications, reviews, scarcity, performance guarantees, or other unsupported claims.
