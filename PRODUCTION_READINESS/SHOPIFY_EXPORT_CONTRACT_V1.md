# MVQUEEN Shopify Export Contract V1

## Purpose

This contract defines the only permitted path from a canonical production record to a Shopify-ready payload.

## Release gate

A product may enter Shopify export only when:

1. `schema_version` is `1.0`.
2. `status` is exactly `PRODUCTION_READY`.
3. `qa.passed` is `true`.
4. `pricing.approved_publish_price` is explicitly present.
5. Required copy and SEO fields are populated.
6. Image ALT text is present for every image being exported.
7. No unsupported/high-risk claims are present.
8. No generic/robotic marketing language is present.
9. Brand-voice validation passes.
10. Protected source fields are unchanged from the adapter snapshot.

## Protected fields

The exporter must preserve source identity and operational fields including:

- product ID
- handle unless an explicitly approved handle change is part of the export operation
- SKU / variant SKU
- variant ID
- option values
- inventory identifiers and quantities

The exporter must never silently rewrite inventory, SKU, variant identity, or source identifiers as a side effect of copy/SEO generation.

## Separation of responsibilities

`PRODUCT_PIPELINE_V1.py` produces the canonical production record.

`CANONICAL_ADAPTER_V1.py` validates the boundary and preserves protected values.

A future Shopify exporter may transform an approved canonical record into a Shopify payload, but it must not regenerate product copy, invent facts, recalculate unapproved prices, or bypass QA.

## No live writes in V1

The canonical adapter is side-effect free. V1 does not perform Shopify writes. Live publishing is a later phase after export contract tests, Shopify API compatibility checks, and a controlled dry run pass.

## Required flow

```text
Supplier / Shopify source
        ↓
Canonical Adapter
        ↓
Product Pipeline
        ↓
Brand + Claim + SEO + Commercial QA
        ↓
PRODUCTION_READY
        ↓
Shopify Export Contract
        ↓
Controlled Export
        ↓
Shopify
```
