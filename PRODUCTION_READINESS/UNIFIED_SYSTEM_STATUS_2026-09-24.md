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
- older MVQueen root mirrors moved into `MVQUEEN_ARCHIVE_2026-09-24`.
- legacy runtime/workspace folders moved into `_ARCHIVE_LEGACY_2026-09-24`.

Drive intake validation is read-only and cannot commit or push to GitHub.

## Branch policy

There are 33 non-main historical branch refs. They are recovery references only and are recorded in:
`PRODUCTION_READINESS/HISTORICAL_BRANCH_ARCHIVE_2026-09-24.md`.

No open pull request is an approved production merge source.

## Production gates

Verified against the canonical system on 2026-09-24:
- The latest production-status change is validated by MVQueen Production Readiness, MVQueen OS Lint and Index, and MVQUEEN_OS Overseer.
- MVQueen Catalog Governance is passing on the current catalog-governance inputs.
- MVQueen Theme CI/CD is passing; no theme/automation watched files changed after the last successful theme run.
- MVQueen Shopify App CI TypeScript typecheck and production build are passing; no app/config watched files changed after the last successful app run.
- MVQueen Deep Repository Audit is passing; its watched audit sources have not changed since that successful run.
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
- Canonical theme remains unpublished as `MVQueen — Custom Production Build` (`154611515590`).
- The canonical unpublished theme is synchronized to `main` for all **33 controlled deployment files**.
- All 33 controlled files are present on both sides and their file sizes match.
- Theme Check and the MVQueen storefront contract validator pass.
- Theme deployment remains fail-closed; validation does not publish the live theme.
- The homepage production defects discovered during synchronization were repaired on `main`: SEO SearchAction Liquid syntax, brand-story section, opt-in social-proof section, and trust-badges section.

### Live commerce

- Connected production store: `tsucu0-1i.myshopify.com`.
- Two active products are currently present in Shopify.
- Both live products now use `MVQueen` as vendor/customer-facing brand.
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
- Shopify store identity is still named `My Store 4` in Admin even though product/vendor branding is MVQueen.

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
- Published Terms of Service, Refund & Returns, and Shipping pages were repaired from canonical MVQueen SOPs.
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
3. **Publish the canonical theme.** `MVQueen — Custom Production Build` (`154611515590`) is synchronized, validated and remains UNPUBLISHED; `Helio` (`154610663622`) is still MAIN. Automated theme publishing is intentionally blocked.
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

The previously analyzed 948-product historical CSV set belongs to an old catalog and is **not part of the current MVQueen production assortment**.

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
- Both active products use `MVQueen` as vendor/customer-facing brand.

Current-store merchandising/navigation and the customer-facing policy pages have been verified or repaired. Remaining stabilization work is limited to owner/admin security, identity, password-protection and theme-publication controls listed above.

## Launch finalization update — 2026-09-24

This section supersedes earlier launch-blocker lists in this document.

### Verified complete

- Production catalog scope is Shopify-only: 2 current products, both ACTIVE.
- Both live products use `MVQueen` as vendor/customer-facing brand.
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
- Canonical custom theme `MVQueen — Custom Production Build` is synchronized to GitHub `main` for all 33 controlled files: 33/33 file sizes match, with no missing files or theme processing failures.
- Theme CI/CD, MVQUEEN_OS Overseer and Lint/Index pass on the current storefront code commit.
- The canonical theme contains no detected `Miss.Queen`, policy-placeholder, TODO/FIXME, lorem, example.com, Helio or Horizon references.
- The primary Shopify domain is SSL-enabled and has an English web presence.
- Storefront password protection is currently enabled as the pre-launch safety gate.
- Current `main` contains no discovered live `shpat_` credential; secret-like strings found by search are scanner/test patterns only.

### Account-level launch actions still required

These controls cannot be completed by the connected tools and must remain explicit launch gates:

1. **Publish the custom theme.** The connected Shopify mutation surface blocks theme publishing by safety policy. Publish `MVQueen — Custom Production Build` (`154611515590`) in Shopify admin only after the final visual preview.
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



## Public launch verification update — 2026-09-25

This section supersedes all earlier launch-gate and storefront-access status in this document.

### Verified public state

- **Store name:** `MVQueen`.
- **Primary domain:** `https://tsucu0-1i.myshopify.com`.
- **SSL:** enabled.
- **Shopify plan:** Basic.
- **Shop setupRequired:** false.
- **Storefront password protection:** **DISABLED**.
- **Live MAIN theme:** `MVQueen — Custom Production Build` (theme ID `154869825734`).
- Live theme processing: complete; `processingFailed=false`.
- Rollback theme: `MVQueen — Previous Production Build` (theme ID `154611515590`), unpublished.
- Helio is unpublished.
- Live header, footer, hero, brand story, product and collection theme files use canonical customer-facing `MVQueen` casing and contain no standalone legacy `MVQUEEN` brand spelling.
- Shopify pages, policies, collections, menus, product content and SEO audit contain no remaining customer-facing `MVQUEEN` brand hits.
- Built-in policy audit found no bracket placeholders.
- Two URL redirects are active.

### Current production catalog

- Shopify remains the sole source of truth for production products.
- 2 products total; both are ACTIVE.
- Both product vendors are `MVQueen`.
- Both product SEO titles use `MVQueen`.
- All 5 current product media items are READY and have ALT text.
- Historical recovery catalogs remain archive-only and outside production scope.
- Protected handles, SKUs, variant IDs, inventory, pricing and media relationships remain outside editorial automation.

### GitHub / system state

- Canonical repository: `juliantevon-droid/MVQUEEN_OS`, branch `main`.
- `MVQUEEN Main Protection` ruleset is active.
- Historical Shopify credential gate is resolved: live app-installation audit shows no merchant-created custom app installed and the Dev Dashboard contains no merchant app; active `main` contains no live Shopify token.
- Customer-facing/prose brand spelling is standardized to `MVQueen` across the repository while technical identifiers such as `MVQUEEN_OS`, workflow labels, paths and code identifiers remain unchanged where required for system stability.
- Editable Google Docs and Sheets were normalized in place to the canonical `MVQueen` display spelling; raw archival files remain historical snapshots.

### Remaining manual commerce verification

- **Payment provider activation is not verified by the connected integration.** Shopify exposes `shopifyPaymentsAccount.activated`, but this connection is denied access because it lacks `read_shopify_payments` / `read_shopify_payments_accounts`.
- Verify the active payment provider manually in **Shopify Admin → Settings → Payments** and perform a test checkout/order before treating payment acceptance as operationally certified.

### Final release position

**Architecture / code:** READY  
**Current Shopify catalog:** READY  
**Theme:** LIVE AND HEALTHY  
**Brand casing:** READY  
**Navigation / redirects:** READY  
**Policies / customer-facing pages:** READY based on verified current content  
**Storefront access:** PUBLIC — PASSWORD PROTECTION OFF  
**GitHub main protection:** ACTIVE  
**Historical credential gate:** RESOLVED  
**Payment acceptance:** MANUAL VERIFICATION REQUIRED  
**Public storefront:** LAUNCHED  
**Full commerce launch certification:** PENDING PAYMENT-PROVIDER / TEST-CHECKOUT VERIFICATION

## Verified staging promotion state — 2026-09-25

The canonical storefront deployment model is now:

- **Live MAIN:** `MVQueen — Custom Production Build` (`154869825734`)
- **Validated staging:** `MVQueen — Staging Preview` (`154876772550`)
- **Backup:** `MVQueen — Backup 2026-09-25`
- **Legacy themes:** Helio and Previous Production Build remain unpublished.

### Staging parity

The Theme CI controlled deployment set currently contains **39 files**.

- GitHub `main` → Staging Preview: **39 / 39 matched**
- Missing staging files: **0**
- Staging mismatches: **0**
- Staging processing failures: **0**
- Theme contract validator: **PASS**
- Shopify Theme Check: **PASS**

### Live delta

The current live MAIN theme matches **25 / 39** controlled files.

Files missing from live but present in staging:
- `assets/brand-gateway.css`
- `sections/brand-gateway.liquid`
- `sections/miss-princess-experience.liquid`
- `templates/page.mvqueen.json`
- `templates/page.miss-princess.json`

Live files with older versions than GitHub/staging:
- `layout/theme.liquid`
- `config/settings_schema.json`
- `assets/mvqueen-design-system.css`
- `assets/mvqueen-header.css`
- `assets/mvqueen-product.css`
- `sections/header.liquid`
- `sections/footer.liquid`
- `sections/main-product.liquid`
- `templates/index.json`

### Product-page / SEO architecture

The validated staging product page now includes:
- short description above the fold
- factual product-highlight bullets
- Product details accordion
- Measurements accordion when verified measurements exist
- Ingredients / How to use / Care / Size guide accordions when relevant metafields exist
- Shipping & returns accordion with live policy links
- secure native Shopify product form/cart behavior
- Product JSON-LD structured data
- canonical/meta/Open Graph/Twitter SEO
- factual primary keyword, secondary phrases, and long-tail keyword architecture in the canonical product pipeline

Current Shopify products now have:
- `catalog.focus_keyword`
- `catalog.long_tail_keywords`
- `catalog.seo_keywords`
- `catalog.highlights`
- `catalog.short_description`

The two current product variants were verified unchanged after SEO/content metafield updates:
- Pink Thulite: SKU `SDP116759`, price `26.39`, inventory `1`
- Brown Aventurine: SKU `COFL-805`, price `13.09`, inventory `996`

### Engineering gates

- GitHub `main` protection: **ENABLED**
- Shopify App CI: **PASS** after repairing invalid TypeScript template literals in brand routing
- Lint & Index: **PASS**
- MVQUEEN_OS Overseer: **PASS**
- Production Readiness: **PASS**
- Theme CI/CD validation: **PASS**

### Promotion decision

Do **not** patch the current MAIN theme file-by-file. The correct release action is to promote the fully validated `MVQueen — Staging Preview` theme as a single theme release after visual preview. This preserves rollback safety and keeps GitHub/staging/live roles clear.

## Custom product UX + SEO architecture update — 2026-09-25

- GitHub `main` is now protected.
- Shopify storefront password protection is now OFF.
- `MVQueen — Custom Production Build` is currently the MAIN theme.
- The live MAIN theme is an older custom revision: 24/33 controlled files currently match GitHub `main`.
- `MVQueen — Staging Preview` is the release candidate and matches GitHub `main` exactly: **33/33 controlled files**.
- Staging includes the latest custom header/footer, design system, product-page CSS, UX JavaScript, homepage template and product section.
- Shopify's connected mutation policy blocks `themePublish`; promoting Staging to MAIN must be done manually in Shopify Admin.

### Product page UX

The canonical custom product section now provides:

- short description above the fold
- scannable product-highlight bullets
- Product details accordion
- Measurements accordion when verified dimensions exist
- Ingredients / How to use / Care / Size guide accordions when corresponding metafields exist
- Shipping & returns accordion with live policy links
- FAQ accordion when a verified FAQ metafield exists
- native Shopify product form, variants, quantity and secure cart routing

### SEO architecture

The canonical production pipeline now models:

- focus / primary short-tail keyword
- secondary keyword phrases
- factual long-tail keyword phrases
- SEO title
- meta description
- product image ALT text

Long-tail phrases are derived only from verified product facts such as product type, material, color, stone, size and occasion. The pipeline does not invent product claims to manufacture SEO phrases.

Shopify Product metafield definitions now include:

- `catalog.focus_keyword`
- `catalog.long_tail_keywords`
- `catalog.highlights`

Both current Shopify products have populated short descriptions, focus keywords, long-tail phrases, combined SEO keyword lists and verified product-highlight bullets.

Production Readiness, Theme CI/CD, Lint & Index and Overseer have passed after the canonical SEO/product UX changes.

### Remaining activation step

Publish `MVQueen — Staging Preview` to replace the older live custom revision. Shopify requires this to be done manually in Admin because the connected API safety layer refuses theme publishing.
## Release candidate update — 2026-09-27

This section supersedes earlier staging-name and current-catalog counts in this historical status file.

- **Live MAIN:** `MVQueen — Custom Production Build` (`154869825734`).
- **Release candidate:** `MVQueen — Release Candidate` (`154876772550`), still `UNPUBLISHED`, processing complete, no processing failure.
- **Rollback:** `MVQueen — Previous Production Build` (`154611515590`).
- **Backup:** `MVQueen — Backup 2026-09-25` (`154876674246`).
- **Current active Shopify catalog:** 3 products.
- All 3 active products have `shipping.delivery_estimate = 7–15 business days` and an active United States delivery method.
- `/pages/mvqueen` and `/pages/miss-princess` are both published.
- Footer Privacy Policy uses Shopify's native policy route; Terms, Refund & Returns, Shipping Policy, Privacy Choices, Contact Information, and Legal Notice destinations are published.
- GitHub `main` validation remains green at the latest verified head.
- **Remaining full-commerce certification gate:** verify the active payment provider in Shopify Admin and complete a test checkout/order.
- Theme publishing remains manual because the connected Shopify mutation safety layer blocks `themePublish`.

## Always-on product automation verification — 2026-09-27

Production automation has now been verified against a real newly imported Shopify product, not a synthetic fixture.

### Runtime

- Railway Postgres: online.
- Railway `mvqueen-product-worker`: online, one continuous replica, no cron, no crash loop.
- Railway `mvqueen-web`: online from the repository Node Dockerfile.
- Web healthcheck is `/healthz`, not only `/livez`.
- The strict health deployment succeeded after enabling production gates; this proves production preflight, PostgreSQL access, queue/dead-letter health and continuous-worker heartbeat are healthy.
- Global automatic product enrollment, governed editorial publishing, SEO, ALT repair, vendor normalization, cost sync, pricing, compare-at validation, content surfaces and reconciliation are enabled in production.
- Existing-description rewrite remains disabled so later update events cannot casually overwrite already-curated copy.
- Pricing remains fail-closed when cost/commercial inputs are incomplete.
- Compare-at pricing remains fail-closed unless a verified higher reference price exists.

### Real Shopify automation proof

Current Shopify production catalog now contains **3 ACTIVE products**.

The newly imported product `gid://shopify/Product/9087726584006`, **Ruched Sports Bra and High-Waisted Shorts Active Set**, was processed by MVQUEEN_OS and now has:

- customer-facing vendor normalized to `MVQueen`
- source vendor preserved internally as `Trendsi`
- automatic routing to **Miss.Princess**
- Fashion → Activewear → Activewear Sets classification
- membership in Fashion, Activewear and Miss.Princess World collections
- governed short description
- scannable product highlights
- focus keyword and long-tail SEO phrases
- Shopify SEO title/meta description branded for Miss.Princess
- automatic FAQ content
- shipping estimate
- all 10 product image ALT texts repaired
- verified Shopify unit cost
- commercial-health and advertising-eligibility metrics
- analytics measurement key

A real Shopify update probe added a temporary MVQUEEN system department tag. Within the running automation loop the probe tag was removed and canonical classification was restored, proving the production update → queue/worker → Shopify write loop.

The same processing pass:
- changed all **12 variants** from **$39.24** to the governed recommended price **$54.99**
- preserved every SKU and inventory quantity
- did **not** create a compare-at price because no verified higher reference price existed
- changed `commercial.pricing_publishable` from false to true
- changed commercial health from thin to healthy
- changed advertising eligibility from blocked to eligible
- changed marketing state to ready for briefing

This is the production behavior expected for future imported products, subject to the same fail-closed data requirements.

### Storefront / theme state

- Storefront password protection: **OFF**.
- Public product URLs are available.
- Current live MAIN: `MVQueen — Custom Production Build` (`154869825734`).
- Live MAIN is an older custom revision and currently matches only **12/56** controlled GitHub theme files.
- Validated next-production theme: `MVQueen — Release Candidate` (`154876772550`).
- Release Candidate is **56/56 exact** against GitHub `main`.
- Release Candidate includes the latest custom product-page short description, bullet highlights, Product Details accordion, Measurements accordion, optional Ingredients / How to Use / Care / Size Guide / FAQ accordions, Shipping & Returns accordion, and current SEO/empty-collection safeguards.
- Release Candidate is unpublished, processing complete, `processingFailed=false`.
- Shopify API safety policy explicitly blocks `themePublish`; final promotion must be done manually in Shopify Admin.
- A live backup and older rollback themes remain available.

### Remaining launch action

**Publish `MVQueen — Release Candidate` in Shopify Admin.**

That is the only theme action blocked from automated execution. After publication, the release candidate becomes the customer-facing 56/56 custom build.

## Production reconciliation update — 2026-09-28

- Railway `mvqueen-product-worker` is deployed from current GitHub `main` commit `7e650fa8855ad0c6863f4765055bc1b69a0f1b5b`.
- Worker startup verifies both Shopify product webhooks and the durable queue is healthy with no failed/dead-letter jobs.
- Brown Aventurine Bead Necklace is priced at **$40.99** from the governed commercial policy and verified Shopify unit cost.
- Its commercial state is **healthy**, advertising eligibility is **eligible**, and contribution-after-target-CAC is positive; the prior same-pass stale-health mismatch is resolved in current code.
- Compare-at pricing remains fail-closed because there is no verified higher reference price.
- Current storefront MAIN is `MVQueen — Custom Production Build` (`154869825734`).
- `MVQueen — Release Candidate` (`154876772550`) remains **UNPUBLISHED**, processing complete, `processingFailed=false`.
- Shopify shop identity is `MVQueen`, public contact is `miss.mvqueen@gmail.com`, currency is USD, and Shopify reports `setupRequired=false`.
- Installed Shopify apps do **not** currently include Google & YouTube, Facebook & Instagram, TikTok, or Pinterest sales-channel apps.
- The custom homepage social-media hub supports Instagram, TikTok, Facebook, Snapchat, and YouTube, but real profile URLs are intentionally blank until authenticated profiles are provided.
- Direct Shopify Payments-account verification remains unavailable to the connected app because it lacks `read_shopify_payments` / `read_shopify_payments_accounts`; no digital wallets are currently reported through `shop.paymentSettings.supportedDigitalWallets`.
- Final owner-side commerce certification still requires confirming the active payment provider and completing a real/test checkout.
- Theme promotion remains a manual owner/admin action because automated `themePublish` is intentionally blocked by the Shopify mutation safety layer.



## Current unified production status — 2026-09-29

This section supersedes all earlier runtime, theme-role, catalog-count, Drive-automation and launch-state statements in this historical status document.

### Canonical topology

- **GitHub `main`** is the sole authority for code, contracts, tests, theme source and automation logic.
- **Railway** is the production runtime for `mvqueen-web`, the continuously running `mvqueen-product-worker`, and persistent Postgres.
- **Shopify** is the sole live-commerce authority for products, variants, inventory, collections, menus, pages, publications, policies, orders and theme role.
- **Google Drive** is knowledge/assets/archive/backup storage and an optional manually reviewed intake source. It is not executable source and never automatically overwrites GitHub.
- Python remains proposal/validation intelligence; the authenticated React app remains the live Shopify writer.

### Runtime

- Railway web, worker and Postgres are online.
- Web and worker are sourced from `juliantevon-droid/MVQUEEN_OS` `main`.
- Current deployed runtime commit is `04e239e7de8248ae45fcd6923ea987674071a478`; later GitHub changes through this status update affect workflow/governance/theme configuration, not app runtime.
- Railway automatic deploy-on-push is not enabled because the Railway GitHub App is not installed on the repository. Manual deployment remains required after future app-runtime changes until that account-level integration is installed.
- Shopify product webhook delivery to Railway has been verified with HTTP 200 responses and successful worker processing with no failed/dead-letter job in the verification pass.
- The Railway worker continuously owns queue draining, retries, stale-lease recovery, dead-letter handling and reconciliation.
- GitHub's five-minute runtime workflow is now a real read-only `/healthz` monitor rather than a secret-missing worker no-op.

### Drive

- The active Drive `MVQUEEN_OS` root remains organized by operating domain with dated legacy/archive areas retained for recovery/history.
- Historical duplicate indexes, blueprints, copies and local/rclone-era material remain reference/archive only and have no production authority.
- The GitHub Drive intake workflow is now **manual and fail-closed**. It has no schedule, never commits/pushes, and fails when Drive source authentication is not configured instead of reporting a misleading green no-op.
- Approved Drive material must be intentionally reviewed and promoted through normal GitHub changes.

### Theme release architecture

- Shopify MAIN is **MVQueen — Release Candidate** (`154876772550`).
- The former automatic deployment target is no longer used for staging because it is live.
- **MVQueen — Staging Preview** (`155002798278`) is the current verified UNPUBLISHED automated deployment target.
- GitHub Theme CI/CD is pinned to Staging Preview and passed validation, deployment gate, deployment and post-deploy unpublished-role verification.
- Automated theme deployment can never target Shopify MAIN under the current guard.

### Current Shopify commerce scope

- Store identity: MVQueen.
- SSL: enabled.
- Shopify setupRequired: false.
- Current production catalog: **1 ACTIVE product, 0 DRAFT, 0 ARCHIVED**.
- Current active product routes to Miss.Princess.
- Miss.Princess World contains 1 product; MVQueen World currently contains 0 products.
- Only Pink / XL on the current active product has online sellable quantity (2); zero-stock variants remain DENY and are not oversold.
- Core policies are present and footer policy links target canonical Shopify policy resources.
- MVQueen and Miss.Princess pages are published; the old Miss.Queen page and incomplete Size Guide remain unpublished.
- The active product is published to Online Store.

### Launch position

Engineering/runtime/storefront architecture is launch-capable. Remaining commerce/business completion is intentionally separate from architecture:

1. Complete one real/test checkout so payment/order creation is proven end-to-end.
2. Add the real MVQueen and broader Miss.Princess launch assortment; catalog depth is currently the largest commercial limitation.
3. Install the Railway GitHub App and enable deploy-on-push if fully automatic GitHub → Railway deployment is desired.
4. Branded domain remains intentionally deferred by merchant decision.

Do not reopen retired branch, Drive-mirror, local-rclone, direct-Python-Shopify-writer or live-theme-auto-deploy architectures.
