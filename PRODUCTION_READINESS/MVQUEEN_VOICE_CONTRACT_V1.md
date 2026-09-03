# MVQUEEN Voice Contract V1

## Purpose

This is the production voice gate for all generated customer-facing content. Brand guidance is not merely reference material: generated output must pass this contract before it can become `PRODUCTION_READY`.

## Core voice

MVQueen speaks with:

- confident femininity
- modern elegance
- accessible everyday luxury
- polished simplicity
- emotional precision
- identity-led language
- warm confidence without hype

## Write toward

- how she wants to feel
- the version of herself she is expressing
- the moment or routine the product belongs in
- the visual or sensory experience that is actually supported
- clear, useful product understanding

## Do not write

- generic AI/e-commerce filler
- empty luxury adjectives stacked together
- keyword-stuffed sentences
- fake urgency or manufactured scarcity
- unsupported performance, medical, safety, certification, or efficacy claims
- invented ingredients, materials, dimensions, finishes, results, reviews, or use cases
- repetitive templates that make the catalog sound machine-generated
- phrases that describe the writing process rather than the product

## Anti-robot rules

1. No unresolved template language may ship (for example: `Describe ...`, `Close with ...`, `{keyword}`, `{persona}`).
2. Every product must contain at least one product-specific verified detail in its customer-facing copy.
3. Copy must connect the verified detail to a useful human context instead of merely restating the product type.
4. Titles, descriptions, ads, social copy, email, SMS, and creative briefs must not all use the same sentence frame.
5. Repetition across a batch is a QA signal. High-frequency phrase reuse must be reviewed before mass publication.
6. If the source record lacks enough information for distinctive copy, the correct output is a QA hold—not invented detail.

## Truth boundary

Customer-facing language may contain four layers:

1. **Verified fact** — directly supported by the source record.
2. **Brand interpretation** — MVQueen's aesthetic/emotional framing of a verified fact.
3. **Marketing language** — persuasive language that does not introduce new factual claims.
4. **SEO language** — search-oriented phrasing that remains truthful.

The engine must never convert an unverified supplier statement into a verified fact.

## Production gate

`PRODUCTION_READY` requires the voice validator, claim validator, SEO validator, required-field validator, and protected-field checks to pass. A product that sounds polished but violates truth or brand rules remains blocked.
