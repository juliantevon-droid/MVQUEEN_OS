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

Verified against the canonical system on 2026-09-24:
- The latest production-status change is validated by MVQUEEN Production Readiness, MVQUEEN OS Lint and Index, and MVQUEEN_OS Overseer.
- MVQUEEN Catalog Governance is passing on the current catalog-governance inputs.
- MVQUEEN Theme CI/CD is passing; no theme/automation watched files changed after the last successful theme run.
- MVQUEEN Shopify App CI TypeScript typecheck and production build are passing; no app/config watched files changed after the last successful app run.
- MVQUEEN Deep Repository Audit is passing; its watched audit sources have not changed since that successful run.
- Unified-system invariant tests are passing.

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
- 63 collections are published; 58 are currently empty, but the live main-navigation Shop path uses only current non-empty collections.
- Main-navigation collection coverage is verified: MVQueen Edit (2 products), Jewelry (2), Necklaces (2), Pendant Necklaces (1).
- Shopify currently reports 0 URL redirects.
- All 11 currently published Online Store pages are free of literal bracket placeholders and draft-placeholder warnings.
- The duplicate regular Privacy Policy page and incomplete apparel Size Guide are unpublished; the footer continues to use Shopify's official Privacy Policy route.
- FAQ support contact is `miss.mvqueen@gmail.com`; its premature apparel-size-guide prompt is removed while the production catalog is jewelry-only.
- Contact uses the dedicated `contact` page template; its empty body is intentional.
- Storefront password protection is currently enabled.
- Shopify store identity is still named `My Store 4` in Admin even though product/vendor branding is MVQUEEN.

### Catalog source of truth

- **Production catalog source:** Shopify only.
- Historical CSV/product recovery artifacts are **archive/reference only** and are not approved production inputs.
- Current connected Shopify catalog: **2 products total, 2 ACTIVE, 0 DRAFT, 0 ARCHIVED**.
- Production product work applies only to products currently imported into Shopify.
- Historical product counts, historical media gaps, historical SKU collisions and recovery-dedupe results do **not** affect launch readiness.

### Completed launch-gate work — 2026-09-24

- The historical 948-product/media-recovery set is archive-only and is not a production gate.
- Current production catalog scope is only the 2 products imported into Shopify.
- All 5 live product images are present and have ALT text.
- Main-menu Shop navigation is aligned to current non-empty collections.
- Published Terms of Service, Refund & Returns, and Shipping pages were repaired from canonical MVQUEEN SOPs.
- All literal policy placeholders were removed from the published Terms of Service, Refund & Returns, and Shipping pages.
- A full published-page sweep found no remaining bracket placeholders or draft-placeholder warnings.
- Policy and FAQ contact email is `miss.mvqueen@gmail.com`.
- Refund/returns now use the documented 30-day eligible-return standard and prepaid-return-label process.
- Shipping now uses the documented 1–3 business-day processing standard and 5–8 business-day standard-transit estimate.
- Protected handles, SKUs, variant IDs, prices, inventory quantities and image relationships remain unchanged.
- GitHub main currently has no open pull requests and no repository rulesets.

### Remaining owner/admin launch gates

The system is production-capable. Full public release still requires the following owner/admin actions that cannot be completed by the connected integrations:

1. **Protect `main` in GitHub.** No repository ruleset exists, and the connected GitHub App receives 403 on the branch-protection administration endpoint.
2. **Historical Shopify credential — RESOLVED.** Live Shopify app-installation audit shows no merchant-created custom app is currently installed, and the Dev Dashboard contains no merchant app. The historical admin-style token is therefore no longer attached to an active custom-app installation; active `main` also contains no live Shopify token.
3. **Publish the canonical theme.** `MVQUEEN — Custom Production Build` (`154611515590`) is synchronized, validated and remains UNPUBLISHED; `Helio` (`154610663622`) is still MAIN. Automated theme publishing is intentionally blocked.
4. **Finish Shopify store identity/legal-policy branding.** Admin shop name remains `My Store 4`, and the built-in Privacy Policy still contains that name. A validated brand-only Privacy Policy update was rejected because the connected app lacks `write_legal_policies`.
5. **Remove storefront password protection when public launch is intended.** Shopify currently reports password protection enabled.

These are owner/account-control gates, not unresolved catalog, theme-code, app-code or navigation defects.

### Current release position

**Architecture consolidation: COMPLETE.**  
**Theme candidate synchronization: COMPLETE.**  
**Current Shopify two-product cleanup: COMPLETE.**  
**Historical catalog recovery: ARCHIVE ONLY / OUT OF PRODUCTION SCOPE.**  
**Automated/code/data launch gates: COMPLETE.**  
**Owner/admin launch gates: 4 REMAIN.**  
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

Current-store merchandising/navigation and the customer-facing policy pages have been verified or repaired. Remaining stabilization work is limited to owner/admin security, identity, password-protection and theme-publication controls listed above.

## Launch finalization update — 2026-09-24

This section supersedes earlier launch-blocker lists in this document.

### Verified complete

- Production catalog scope is Shopify-only: 2 current products, both ACTIVE.
- Both live products use `MVQUEEN` as vendor/customer-facing brand.
- Product titles, descriptions, SEO title/meta description and all 5 current product image ALT texts are complete.
- Product handles, SKUs, prices, inventory, variants and media relationships remain protected.
- Current product fulfillment profiles are configured for United States delivery.
- Main menu is aligned to the current assortment and no longer exposes empty fashion/beauty category trees.
- Miss.Princess menu is reduced to valid current destinations: Miss.Princess Home, Shop Jewelry, MVQueen Home and Contact.
- The former `Miss.Queen` page is unpublished and redirects to `/pages/miss-princess`.
- Footer Privacy Policy now points to Shopify's canonical `/policies/privacy-policy`.
- The former custom `/pages/privacy-policy` page is archived/unpublished and redirects to the canonical policy.
- Terms of Service, Refund & Returns Policy and Shipping Policy contain no placeholders and use the verified support email `miss.mvqueen@gmail.com`.
- Two URL redirects are active for the retired Privacy and Miss.Queen page paths.
- Empty Shopify collections remain preserved in admin and out of customer navigation. The canonical custom theme now emits `noindex,follow` on collections with zero products.
- Canonical custom theme `MVQUEEN — Custom Production Build` is synchronized to GitHub `main` for all 33 controlled files: 33/33 file sizes match, with no missing files or theme processing failures.
- Theme CI/CD, MVQUEEN_OS Overseer and Lint/Index pass on the current storefront code commit.
- The canonical theme contains no detected `Miss.Queen`, policy-placeholder, TODO/FIXME, lorem, example.com, Helio or Horizon references.
- The primary Shopify domain is SSL-enabled and has an English web presence.
- Storefront password protection is currently enabled as the pre-launch safety gate.
- Current `main` contains no discovered live `shpat_` credential; secret-like strings found by search are scanner/test patterns only.

### Account-level launch actions still required

These controls cannot be completed by the connected tools and must remain explicit launch gates:

1. **Publish the custom theme.** The connected Shopify mutation surface blocks theme publishing by safety policy. Publish `MVQUEEN — Custom Production Build` (`154611515590`) in Shopify admin only after the final visual preview.
2. **Disable storefront password protection immediately after the custom theme is published.** Password protection is currently ON; this also explains why external storefront browsing and product `onlineStoreUrl` checks are unavailable/null.
3. **Verify the payment provider in Shopify Admin → Settings → Payments.** The connected app lacks `read_shopify_payments` / `read_shopify_payments_accounts`, so payment-provider activation cannot be verified here. No digital wallets are reported through the accessible payment-settings field; that is not proof card checkout is unavailable.
4. **Enable GitHub protection/rules for `main`.** The connected GitHub App has no repository-administration permission, so branch protection cannot be set from this environment.
5. **Confirm rotation/revocation of the historical exposed-looking Shopify credential.** Active `main` is clean, but historical exposure must remain treated as compromised until Shopify-side revocation/rotation is confirmed.

### Release position

**Code / architecture:** READY  
**Current Shopify product catalog:** READY  
**Navigation / redirects:** READY  
**Policies / customer-facing legal pages:** READY for business use based on currently verified settings  
**Custom theme candidate:** READY TO PUBLISH  
**SEO / empty-collection handling:** READY in custom theme  
**Storefront access:** PASSWORD-PROTECTED UNTIL LAUNCH  
**Payments:** MANUAL ADMIN VERIFICATION REQUIRED  
**GitHub branch protection:** MANUAL ADMIN ACTION REQUIRED  
**Historical credential rotation:** MANUAL SECURITY CONFIRMATION REQUIRED  
**Full public launch:** FINAL ACCOUNT CONTROLS ONLY

