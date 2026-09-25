# MVQUEEN_OS Live Shopify Verification — 2026-09-25

**Store:** `tsucu0-1i.myshopify.com`
**Mode:** read-only verification against Shopify Admin API
**Currency:** USD
**Plan:** Basic

## Verified production state

### Products
- Shopify product count: **2**
- Both observed products are **ACTIVE**.
- Both now use **Vendor = MVQueen**.
- Product routing tags are present, including MVQueen/Miss.Princess brand-routing tags.
- The live catalog is still far below the intended large-catalog architecture, so catalog release is not complete.

### Collections
- Shopify collection count: **65**.
- Product-populated collections currently include Home page, MVQueen Edit, Jewelry, Necklaces, Pendant Necklaces, MVQueen World, and Miss.Princess World.
- Most taxonomy collections are still empty because the live product catalog contains only two products.
- Empty taxonomy is useful as prepared structure but must not be mistaken for a populated launch catalog.

### Navigation
Verified menus:
- `MVQueen Mega Menu` — handle `main-menu`, default/main navigation.
- `Miss.Princess Mega Menu` — handle `miss-princess-menu`.
- `Footer menu`.
- `Customer account main menu`.

The two-brand navigation architecture therefore exists in Shopify Admin now, not only in GitHub.

### Themes
Verified theme state:
- **MVQueen — Custom Production Build** — `MAIN`
- MVQueen — Staging Preview — unpublished
- MVQueen — Backup 2026-09-25 — unpublished
- MVQueen — Previous Production Build — unpublished
- Helio — unpublished

This supersedes older audits that reported Helio as the live theme. The custom MVQueen production theme is currently the published MAIN theme.

### Redirects
Shopify URL redirect count: **2**.
Verified redirects:
- `/pages/privacy-policy` → `/policies/privacy-policy`
- `/pages/miss-queen` → `/pages/miss-princess`

Redirect architecture therefore exists but is not yet comprehensive for a future large catalog.

## Current launch interpretation

### Verified improvements
- Correct Shopify store connection.
- Canonical MVQueen vendor applied to current products.
- Custom production theme is MAIN.
- Separate MVQueen and Miss.Princess mega menus exist.
- Brand-world routing collections exist.
- Legacy Miss.Queen page redirect exists.
- Basic policy redirect exists.

### Remaining production gaps
1. Live catalog contains only 2 products.
2. Most of the 65 collection taxonomy nodes are empty.
3. Redirect coverage is only 2 records and will need product/page migration coverage as the catalog grows.
4. Menu tag-filter routes need storefront/browser verification to confirm every nested collection-filter URL resolves correctly in the published theme.
5. Product metafield completeness, page/policy content, storefront rendering, mobile UX, accessibility, performance, and checkout path still need direct verification.
6. Large-catalog ingestion must remain gated until protected-field, factual-copy, media, and release controls pass on real imported products.

## Release posture

The theme/navigation foundation is substantially ahead of the live catalog. Do not use repository completeness as a proxy for catalog launch readiness.

Next release gate:
`Shopify state → storefront route/render checks → product/metafield truth audit → mobile/CRO/accessibility/performance → catalog ingestion dry-run → release decision`


## Theme parity and product-truth verification — 2026-09-25

### Custom source independence
The canonical GitHub theme contract now performs static dependency closure checks across MVQueen Liquid source. It fails if an MVQueen-owned Liquid file renders a missing snippet, invokes a missing section, or references an undeclared local theme asset. Shopify Theme Check and the strengthened custom-source contract both passed in Theme CI run 226 after this control was added.

This means the MVQueen-owned source tree does not require hidden inherited snippet/section/asset dependencies to satisfy its declared storefront integrations. Remote Shopify-native files may remain on staging/live for rollback safety, but they are not accepted as invisible dependencies of the canonical custom source.

### Staging synchronization
The governed Theme CI deployment allowlist contains 39 unique MVQueen-controlled files. A live read-only comparison initially found 38/39 path/size parity; the sole mismatch was `sections/main-product.liquid`, whose latest canonical metafield/accordion update landed during a cancelled concurrent Theme CI run.

That single file was then synchronized directly to the **UNPUBLISHED** `MVQueen — Staging Preview` theme from current GitHub source. Shopify returned no user errors. Post-write theme health:
- role: `UNPUBLISHED`
- processing: `false`
- processingFailed: `false`

The live MAIN theme was not modified by this synchronization.

### Current-product truth audit
Both production products were inspected completely for status, SEO, metafields, media, and variants.

Verified:
- 2/2 products ACTIVE.
- 2/2 vendors = `MVQueen`.
- 2/2 products have SEO title and meta description.
- 5/5 media images are READY and have non-empty ALT text.
- Current SKUs, prices, and inventory values remain unchanged.
- Both products have canonical catalog short description, focus keyword, long-tail keywords, highlights, and SEO keyword data.

Data-quality observation:
- The pink thulite pendant has richer structured `classification` and `attributes` metafields.
- The brown aventurine necklace has complete catalog/SEO metafields but a sparser structured attributes layer. Any enrichment should use only verified facts already present in its canonical product record and must not alter protected commerce fields.

### Current release implication
The safest theme release path remains **GitHub main → validated Staging Preview → visual/purchase-path verification → manual promotion**, never file-by-file patching of MAIN and never automated live-theme publication.


## Custom customer-care/editorial surface update — 2026-09-25

The custom storefront deployment contract was expanded from 39 to **48 governed files** so published customer-facing pages no longer depend on ungoverned fallback theme templates.

Added to the governed release surface:
- custom MVQueen Contact section and `page.contact` template
- About template
- FAQ template
- Journal template + editorial hub section
- Lookbook template + lookbook section
- canonical main-page section

The Contact implementation uses Shopify's native Liquid `contact` form with required email/message fields, optional order number, request category, accessible success/error handling, and MVQueen customer-care styling.

Validation:
- strengthened self-contained dependency contract: PASS
- Shopify Theme Check: PASS
- unpublished Staging Preview controlled parity after synchronization: **48/48**
- missing controlled staging files: **0**
- controlled path/size mismatches: **0**
- staging `processing=false`
- staging `processingFailed=false`

No live MAIN theme file was modified. Staging remains the governed release candidate.
