# MVQueen Catalog Engine

This package is the **offline intelligence and catalog-safety layer** for the
canonical MVQUEEN_OS architecture.

## Production source of truth

**Shopify is the sole source of truth for the current production catalog.**

Only products currently imported into Shopify are in production scope.
Historical CSV/catalog recovery artifacts are archive/reference material and do
not define the live assortment, launch readiness, media requirements, product
counts, or collection membership.

## Production role

- Shopify live commerce state is authoritative.
- Live commerce writes are owned by the authenticated React application under `app/`.
- This Python package performs offline curation, detection, validation, dry-runs,
  QA and safety checks when working with an explicitly supplied **current
  Shopify export or approved current-product artifact**.
- It must not contain a second Shopify transport or alternate production writer.
- Handles, IDs, SKUs, options, variants, pricing, inventory, publication state,
  and source-image relationships are protected from editorial automation.

## Canonical production path

```text
current Shopify product
  → verified facts/current export
  → offline editorial proposal (optional)
  → Catalog Guard / QA
  → explicit approval
  → authenticated application write boundary
  → Shopify
```

For offline curation of a current Shopify export:

```bash
python -m mvqueen_engine.main current-shopify-export.csv output.csv
```

The legacy `engine.run()` all-in-one generator is intentionally fail-closed.
It previously mixed editorial generation with operational commerce generation
and is not a production interface.

## Brand governance

Customer-facing language is governed, in order, by:

1. `00_Doctrine/master_doctrine.md`
2. `01_Brand_Strategy/Brand_Bible.md`
3. `02_Brand_Identity/brand_vocabulary.md`
4. `06_Tone_And_Voice/Brand_Vocabulary_Banks.md`
5. `06_Tone_And_Voice/Forbidden_Words.md`
6. `06_Tone_And_Voice/Product_Description_Voice.md`
7. `06_Tone_And_Voice/Tone_Guide.md`
8. Voice consistency and writing rules

Vocabulary may shape phrasing and tone. It may **not** invent materials,
ingredients, measurements, benefits, certifications, origin, efficacy, fit, or
other unverified product facts.

## Safety

- Direct Python Shopify publishing: disabled.
- Historical hard-coded phone/Android paths: retired.
- Import-time CSV execution: retired.
- Automatic compare-at price generation: retired from governed editorial flows.
- Bulk product creation: not provided here.
- Editorial automation may not overwrite protected commerce fields.

## Historical recovery tooling

Historical recovery/audit utilities remain available only for archival,
forensic, or migration reference. They are **not part of the active production
catalog pipeline and are not production readiness gates**.

No historical product is eligible for production work unless it is explicitly
reintroduced into the current Shopify catalog by the merchant.
