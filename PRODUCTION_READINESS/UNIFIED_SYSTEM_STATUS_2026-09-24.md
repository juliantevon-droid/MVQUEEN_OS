# MVQUEEN_OS Unified Production Status — 2026-09-24

## Canonical system

- **Active Git branch:** `main`
- **GitHub role:** source of truth for code, contracts, tests, theme and automation logic.
- **Shopify role:** source of truth for live commerce state.
- **Google Drive role:** archive, assets, references and backups only.
- **Live Shopify writer:** authenticated React Router application under `app/`.
- **Python role:** deterministic intelligence, dry-run, validation, QA and release artifacts.
- **Sister brand:** Miss.Princess.

## Active main hygiene

- 723 tracked files.
- Approximately 3.33 MB of tracked content.
- `.obsidian/`: not tracked.
- `_BACKUPS/`: not tracked.
- Python cache/bytecode: not tracked.
- Root generated session context: retired.
- Legacy local Drive/Termux bootstrap scripts: retired.
- Standalone Python Shopify REST/GraphQL network clients: retired.
- `15_Scripts_And_Code/` contains only its README/index and the canonical `mvqueen_engine/`.

## Drive

The active `MVQUEEN_OS` Drive root retains its original folder identity for compatibility.

Active root structure:
- 40 folders total, including one dated legacy archive.
- 0 loose root files.
- 0 duplicate folder names.
- older MVQUEEN root mirrors moved into `MVQUEEN_ARCHIVE_2026-09-24`.
- legacy runtime/workspace folders moved into `_ARCHIVE_LEGACY_2026-09-24`.

Drive intake validation is read-only and cannot commit or push to GitHub.

## Branch policy

There are 33 non-main historical branch refs. They are recovery references only and are recorded in:
`PRODUCTION_READINESS/HISTORICAL_BRANCH_ARCHIVE_2026-09-24.md`.

No open pull request is an approved production merge source.

## Production gates

Verified during consolidation:
- MVQUEEN Production Readiness — passing.
- MVQUEEN OS Lint and Index — passing.
- MVQUEEN_OS Overseer — passing.
- MVQUEEN Theme CI/CD — passing after theme config normalization.
- MVQUEEN Shopify App CI — TypeScript typecheck and production build passing.
- Unified-system invariant tests — passing.

## Security

Active `main` contains no default Python Shopify credential transport.

A historical branch/file version previously contained a live-looking Shopify credential. Because the repository is public, that credential must be treated as exposed and rotated/revoked in Shopify even though it is no longer part of the active architecture.

## Write boundary

A live product mutation requires both:

1. `MVQ_WRITE_ENABLED=true`
2. the exact product GID in `MVQ_APPROVED_PRODUCT_GIDS`

Protected handles, SKUs, inventory, variants, pricing and image relationships remain outside editorial automation.

## Status

**Architecture consolidation: COMPLETE.**

Further work should extend this canonical system, not create parallel runtimes, Drive code mirrors, duplicate app folders or new production branches.

## Production hardening update — 2026-09-24

### Storefront

- Shopify live theme remains `Helio` (`154610663622`).
- Canonical theme remains unpublished as `MVQUEEN — Custom Production Build` (`154611515590`).
- The canonical unpublished theme is synchronized to `main` for all **33 controlled deployment files**.
- All 33 controlled files are present on both sides and their file sizes match.
- Theme Check and the MVQUEEN storefront contract validator pass.
- Theme deployment remains fail-closed; validation does not publish the live theme.
- The homepage production defects discovered during synchronization were repaired on `main`: SEO SearchAction Liquid syntax, brand-story section, opt-in social-proof section, and trust-badges section.

### Live commerce

- Connected production store: `tsucu0-1i.myshopify.com`.
- Two active products are currently present in Shopify.
- Both live products now use `MVQUEEN` as vendor/customer-facing brand.
- The brown aventurine necklace received a cleaned factual title/description, SEO title/meta description, and image ALT text.
- The pink thulite pendant retained its existing factual product copy and received canonical vendor/SEO brand normalization.
- Handles, variant IDs, SKUs, prices, inventory quantities and image relationships were verified unchanged after the cleanup.
- All five images across the two live products now have ALT text.
- 63 collections are published; 58 are currently empty.
- Shopify currently reports 0 URL redirects.

### Historical catalog recovery

A complete historical Shopify-format recovery source was located in Git history:

- **948 unique products**
- **3,575 Shopify CSV rows**
- recovery source: historical `products_final.csv` and related blobs

The recovery source is **not approved for direct import**. It contains supplier/legacy branding, incomplete category/product-type coverage, missing custom editorial fields, incomplete media representation, zero ALT coverage on represented image rows, and repeated SKU relationships requiring review.

The canonical catalog worker now blocks the recovered supplier identities (including EPROLO, DROPSURE, JAYSUING, ROXELIS, DESIRE GEM and MIA JEWELRY) from customer-facing optimized content.

A read-only recovery audit now exists at:
`30_System_Infrastructure/catalog/catalog_recovery_audit.py`

It performs deterministic HOLD/READY_FOR_REVIEW checks and has no Shopify network transport or mutation capability. Recovery-control regression tests are included in Production Readiness CI.

### Remaining launch blockers

The system is production-capable but the customer-facing store is **not yet release-cleared** because:

1. `main` is not branch-protected. The connected GitHub App lacks repository administration permission to enable protection from this environment.
2. The historical live-looking Shopify credential still requires confirmed rotation/revocation.
3. The canonical MVQUEEN theme is intentionally still unpublished; live `Helio` has not been replaced.
4. Shopify legal/policy content still contains unresolved placeholders such as `[DATE]` and `[PROCESSING TIME]`; business-specific legal/operational values must not be invented.
5. The historical 948-product catalog must pass normalization, supplier/claim cleanup, classification, media reconciliation and explicit approval before controlled draft creation.
6. The current authenticated Shopify writer is update-only; no uncontrolled bulk `productCreate` path exists.

### Current release position

**Architecture consolidation: COMPLETE.**  
**Theme candidate synchronization: COMPLETE.**  
**Live two-product cleanup: COMPLETE.**  
**Catalog recovery discovery: COMPLETE.**  
**Catalog recovery release: HOLD.**  
**Full storefront launch clearance: NOT YET.**

Further production work must continue through the existing `main` architecture and governed release gates.

