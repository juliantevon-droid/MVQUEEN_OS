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

### Catalog source of truth

- **Production catalog source:** Shopify only.
- Historical CSV/product recovery artifacts are **archive/reference only** and are not approved production inputs.
- Current connected Shopify catalog: **2 products total, 2 ACTIVE, 0 DRAFT, 0 ARCHIVED**.
- Production product work applies only to products currently imported into Shopify.
- Historical product counts, historical media gaps, historical SKU collisions and recovery-dedupe results do **not** affect launch readiness.

### Remaining launch blockers

The system is production-capable but the customer-facing store is **not yet release-cleared** because:

1. `main` is not branch-protected. The connected GitHub App lacks repository administration permission to enable protection from this environment.
2. The historical live-looking Shopify credential still requires confirmed rotation/revocation.
3. The canonical MVQUEEN theme is intentionally still unpublished; live `Helio` has not been replaced.
4. Shopify legal/policy content still contains unresolved placeholders such as `[DATE]` and `[PROCESSING TIME]`; business-specific legal/operational values must not be invented.
5. Current Shopify merchandising/navigation still needs to be aligned to the products actually imported into Shopify; empty historical collection structure must not be treated as current assortment.

### Current release position

**Architecture consolidation: COMPLETE.**  
**Theme candidate synchronization: COMPLETE.**  
**Current Shopify two-product cleanup: COMPLETE.**  
**Historical catalog recovery: ARCHIVE ONLY / OUT OF PRODUCTION SCOPE.**  
**Full storefront launch clearance: NOT YET.**

Further production work must continue from the **current Shopify catalog only**, through the existing `main` architecture and governed release gates.

## Catalog scope correction — 2026-09-24

The previously analyzed 948-product historical CSV set belongs to an old catalog and is **not part of the current MVQUEEN production assortment**.

Effective immediately:

- Shopify is the sole source of truth for production products.
- Only products currently imported into Shopify are eligible for optimization, collection assignment, storefront display, SEO work, QA or publication decisions.
- Historical recovery/dedupe/media findings are retained only as archival engineering evidence.
- Historical recovery tooling is removed from active Catalog Governance and Production Readiness gates.
- No old product will be recreated, imported, deduplicated, assigned media, or counted toward readiness unless explicitly reintroduced by the merchant in the future.

Current verified Shopify state at the time of this correction:
- 2 total products.
- 2 ACTIVE.
- 0 DRAFT.
- 0 ARCHIVED.
- Both active products use `MVQUEEN` as vendor/customer-facing brand.

The next stabilization work is current-store merchandising, navigation, collection hygiene, policy completion, security/account controls, and final unpublished-theme QA.
