# MVQueen Theme Drift & Sync Policy

## Current production topology — 2026-10-03

- Shopify store: `tsucu0-1i.myshopify.com`
- Live MAIN: **MVQueen — Release Candidate** (`154876772550`)
- Automated development/staging target: **MVQueen — Staging Preview** (`155002798278`, UNPUBLISHED)
- Older custom builds/backups remain rollback references only.
- GitHub `storefront/theme/` is the source of truth for MVQUEEN-owned storefront code.

## Source-of-truth model

MVQueen is a **fully custom Shopify storefront experience**. Dawn, Helio and Horizon are not the customer-experience foundation.

Shopify remains the secure commerce infrastructure underneath the experience: products, variants, inventory, cart, checkout, customer accounts, payments, orders and platform services are Shopify-managed. MVQueen owns the presentation and interaction layer through its custom Liquid, CSS, JavaScript, snippets, sections and JSON templates.

## Deployment safety rules

1. Never publish from automation.
2. Never deploy to a `MAIN` theme.
3. Automated theme writes target only `MVQueen — Staging Preview` (`155002798278`).
4. Deploy only governed MVQUEEN-owned files through the explicit workflow allowlist.
5. Never overwrite `config/settings_data.json` from automation.
6. Validate source before every Shopify theme write.
7. Keep Shopify credentials out of Git history.
8. Preserve product handles, SKUs, inventory, variants and source-media relationships outside separately governed catalog operations.
9. Preserve mobile usability, accessibility, reduced-motion behavior, performance and graceful failure states.
10. Customer-facing content uses MVQueen / Miss.Princess routing and blocks supplier/legacy identity leakage.

## Promotion model

```text
GitHub main
  → contract / Theme Check / release audit
  → MVQueen — Staging Preview (UNPUBLISHED)
  → staging preview QA + Lighthouse
  → explicit merchant approval
  → manual Shopify theme promotion
  → former MAIN retained as rollback
```

Automation must fail closed if the configured target becomes MAIN.

## Drift rule

After any manual theme promotion, update the deployment target immediately to a verified unpublished theme before the next automated theme write. A formerly safe theme ID is not permanently safe; **theme role is authoritative**.
