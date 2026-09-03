# MVQUEEN Production QA Contract V1

## Purpose

This is the hard gate between generated product content and Shopify publication. A product is **PRODUCTION_READY** only when truth, copy, SEO, merchandising, commercial, creative, and protected-field rules pass.

## Non-negotiable rules

1. Never invent ingredients, materials, dimensions, sizing, performance, efficacy, certifications, safety claims, clinical claims, scarcity, reviews, or superiority claims.
2. Every factual product attribute must be traceable to `source_truth.facts` and marked `verified: true` before it can appear as a factual claim.
3. Protected fields—including inventory, SKU, variant identity, source identifiers, and IDs—must not be silently rewritten.
4. One canonical SEO title contract must be used: `MVQueen | {product title}`.
5. Meta descriptions must not exceed 160 characters and should target 150–160 when source data permits.
6. Every image must have usable ALT text derived only from verified product context.
7. `approved_publish_price` is distinct from `recommended_price`; recommendation logic cannot silently publish a price.
8. Missing evidence produces a QA error when the output would otherwise make the unsupported claim.
9. Warnings do not equal approval. Any QA error blocks publication.

## Required stage sequence

`RAW → NORMALIZED → INTELLIGENCE_READY → COPY_READY → SEO_READY → MERCH_READY → COMMERCIAL_READY → CREATIVE_READY → QA_PASSED → PRODUCTION_READY`

Stages may not be skipped. A failed stage cannot be promoted by a later generator.

## Hard-fail checks

- Required schema sections missing.
- Product identity missing.
- Source truth missing or unverifiable for factual copy.
- Protected-field mutation detected.
- Empty canonical title, short description, full description, SEO title, meta description, or primary keyword.
- Unsupported product claims detected.
- SEO ALT text missing for an image that is published.
- Publishable price absent or not explicitly approved.
- QA errors present.

## Commercial evidence

Commercial language may interpret verified facts into positioning, desire, use context, objections, and transformation language. It may not turn interpretation into a factual guarantee.

## Final gate

Only this condition may produce `PRODUCTION_READY`:

`schema_valid AND truth_valid AND protected_fields_intact AND copy_valid AND seo_valid AND merchandising_valid AND commercial_valid AND creative_valid AND no_qa_errors`
