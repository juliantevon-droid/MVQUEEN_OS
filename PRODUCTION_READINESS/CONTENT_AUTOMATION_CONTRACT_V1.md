# MVQUEEN Content Automation Contract V1

## Purpose

This contract governs product-page content, verified metafields, product FAQs, collection copy, site FAQ entries, and blog drafts generated from canonical product records.

## Required input

Content generation may consume only a canonical product record with status PRODUCTION_READY and qa.passed=true.

## Truth boundary

Product facts may come only from verified source_truth facts. Missing facts stay missing. The content layer must not manufacture ingredients, materials, sizing, performance, efficacy, certifications, reviews, scarcity, origin, shelf life, bestseller status, or other factual claims.

## Outputs

- Product page package: title, short description, full description, benefits/features, verified detail rows, FAQ, CTA, SEO metadata, ALT text.
- Metafield package: canonical copy/SEO plus fact-backed attributes only.
- Collection draft: name, description, metadata, keyword, draft status.
- Blog draft: title, slug, dek, sections, internal product link, metadata.
- Site FAQ draft: product-specific entries sourced from verified facts.

## Publishing rule

This engine generates drafts only. Blog and FAQ outputs are review-only and auto_publish=false. Shopify transport remains downstream of the release and publishing boundaries.

## Legacy rule

The old Omniluxe runtime, all-in-one processor, and fabricated metafield generators are retired and must fail closed. They may remain as import-compatible facades only if they cannot generate or mutate production content.
