# MVQueen Content Automation Contract V1

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

The content engine may mark approved surfaces as publish-eligible after canonical product QA and content QA pass.

- Product FAQ content may publish with the approved product metafield payload (`content.faq`).
- Blog articles may auto-publish only when the blog output is `publish_eligible=true`; sparse or weak drafts remain held.
- Collection copy may update an existing matched collection; the publisher must not auto-create collections from product-level content.
- Governed static/editorial pages may publish when explicitly present in the approved content suite.
- Product-level FAQ output must not overwrite the global FAQ page.
- Privacy, terms, shipping, refund/returns, and other legal/policy pages are protected from automated content publishing.

All external writes still require the canonical release fingerprint/approval and the Shopify publishing boundary. Publication eligibility never permits fabricated product facts.

## Legacy rule

The old Omniluxe runtime, all-in-one processor, and fabricated metafield generators are retired and must fail closed. They may remain as import-compatible facades only if they cannot generate or mutate production content.
