# MVQUEEN Catalog Engine

This package is the **offline intelligence and catalog-safety layer** for the
canonical MVQUEEN_OS architecture.

## Production role

- Shopify live commerce writes are owned by the authenticated React application under `app/`.
- This Python package performs offline CSV curation, detection, validation,
  dry-runs, safety checks, recovery audits, and release preparation.
- It must not contain a second Shopify transport or an alternate production writer.
- Handles, IDs, SKUs, options, variants, pricing, inventory, publication state,
  and source-image relationships are protected from editorial automation.

## Canonical offline path

```text
historical/source CSV
  → catalog recovery audit
  → offline editorial proposal
  → Catalog Guard
  → approval/release artifact
  → authenticated application write boundary
```

For basic offline curation:

```bash
python -m mvqueen_engine.main input.csv output.csv
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
- Automatic compare-at price generation in recovery flows: retired.
- Bulk product creation: not provided here.
- Maximum Shopify release file: 850 unique products.
- Every release file must include the original header row and keep all rows for
  a product together.

## Recovery tooling

The governed recovery audit lives at:

`30_System_Infrastructure/catalog/catalog_recovery_audit.py`

It is read-only and returns `HOLD` or `READY_FOR_REVIEW`.
