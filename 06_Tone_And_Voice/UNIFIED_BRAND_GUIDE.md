# MVQUEEN unified brand guide

MVQUEEN and Miss.Princess share an accessible luxury world and keep distinct voices. This guide brings substantive Drive material into the existing OS and identifies the rules used by the product writer.

The active, editable runtime policy is [Brand_Content_Policy.json](Brand_Content_Policy.json). The full source catalog is [the recovered brand source index](../31_AI_Knowledge_Base/brand_sources/README.md), with original Drive IDs, content hashes, retained paths, duplicate accounting and exclusions in its [manifest](../31_AI_Knowledge_Base/brand_sources/manifest.json).

## Identity and voice

| Element | MVQUEEN | Miss.Princess |
|---|---|---|
| Customer-facing spelling | MVQUEEN | Miss.Princess |
| Register | Warm, composed, confident, feminine, inviting | Warm, playful, dreamy, lighthearted, approachable |
| Shared standard | Specific, useful, truthful details; confidence without pressure | Specific, useful, truthful details; confidence without pressure |
| Product naming | Evocative, descriptive-poetic, identity-led | Separate pools using the same three registers |
| Copy rhythm | Considered declarations and flowing atmosphere | Lighter rhythm and playful personal choices |

Older spellings such as MvQueen, MVQueen and legacy sister-brand names remain visible in historical sources. The live copy writer normalizes recognized aliases to the two customer-facing names above. Technical IDs, URLs, existing vendor fields and internal routing tags are separate from that writing convention.

The messaging pillars are softness as strength, luxury that belongs to her, beauty as restoration, intentional feminine living, ritual over routine, and becoming. Use a pillar when it adds meaning; avoid repeating slogans on every product.

## Product writing

The writer uses current classification to choose from nine editorial categories: fashion, jewelry, skincare, beauty, fragrance, haircare, home, tools and general. Each brand has its own category openings. Product IDs seed the choices consistently, so rerunning a product does not randomly rename or rewrite it.

Authored names and openings take precedence. New naming identities retain the live catalog collision check: an identity must be distinct even when another product has a different product noun. Collision exhaustion requires editorial review instead of numbered duplicates.

Open with a feeling appropriate to the category, identify the actual named product, and include verified useful details. Ingredient, material, size, color, care and measurement information can use factual bullets and source tables. Styling or usage needs product evidence. Do not stretch a description merely to satisfy a historical word-count template.

The writer loads the editorial adjective pools, naming palette, forbidden-language rules and active policy together. It combines the existing hard-prohibited list with additional restrictions reconciled from the fuller recovered version. Category openings express editorial intent rather than invented manufacture, texture, scent notes, longevity, ethical claims or clinical results. Claims and forbidden wording in an authored opening require review.

Generated copy uses at most 180 characters for a short description, 80 for a generated title, 60 for an SEO title and 155 for a meta description. Keep complete sentences and the product identity. An opening that cannot fit requires review instead of silently clipping the name.

Vocabulary permission is not product evidence. A bank containing silk, vegan leather, botanicals, long-lasting or cruelty-free does not establish those facts for an imported product. Business tiers such as Hero, Viral and Best Seller are internal labels, not automatic social proof. Inspiration-brand persona names do not appear in customer copy.

## Channels and editorial registers

Email is personal and intentional. SMS is brief and human. Social adapts rhythm to the platform. Ads pair desire with truthful evidence. Blogs offer useful depth. SEO follows the real product category and verified attributes. Service copy preserves dates, quantities and delivery facts. Each execution has a clear intended action.

The ten source personas are retained as editorial references and translated into owned register names in the policy. The automated writer routes by the two brands and product category; this import does not imply that ten separate agents are running. Princess caption exceptions for trend language do not relax automated product-copy restrictions.

## Connected content outputs

The `profiles.<brand>.surfaces` section of the active policy supplies editable FAQ, blog, collection and invitation templates. Blog introductions and decision guidance route through the same nine editorial categories as product writing. Product IDs select wording consistently; shared collection copy uses the brand and category so it does not change with every product event.

| Output | Active connection |
|---|---|
| Product titles | Naming palette, authored names, current product noun, live identity collision check |
| Short and full descriptions | Brand/category opening, verified details and original measurement tables |
| Product SEO | Named product, factual keywords, canonical brand and policy length limits |
| Product FAQ | Brand FAQ templates plus current product highlights in `content.faq`; the product theme displays these entries |
| Blogs | Reader-first category introduction, actual listed details, useful decision guidance, brand invitation and product link |
| Blog search listing | Policy-limited title and description written to Shopify `global.title_tag` and `global.description_tag` |
| Collection description and SEO | Stable brand/category templates, canonical brand and policy length limits |
| Calls to action | Distinct warm invitations for each brand |
| Image alternative text | The governed product title and image-view number when the existing media gate allows repair |

Blog headline changes retain the established article handle. Product FAQ content stays on its product; each product event preserves the global FAQ page. Global FAQ and other static pages continue through the separate approved-page workflow and publication gates. Email, SMS, social and ad guidance is available in the source corpus and policy; this connection does not start campaigns.

Short product guides publish only when the existing source-content and factual-highlight requirements pass. Sparse products stay in draft review. A useful short guide does not become a long article by adding unsupported facts. Shipping and return answers point to current store terms. Legal and policy pages remain protected.

Blog search metadata follows Shopify's [search listing guidance](https://shopify.dev/docs/apps/build/marketing/optimize-storefront-seo). The previous custom SEO description remains available to integrations alongside the native search fields.

## Source conflicts and authority

| Conflict | Resolution |
|---|---|
| Timestamp versus content | Inspect the body. A vocabulary excerpt named Product_Naming_System does not replace a naming system. |
| Multiple spellings | Use the active writing convention; retain originals in references. |
| Three-part versus five-part descriptions | Keep feeling → named product and facts → personal relevance. Add sections when useful and supported. |
| “Never list features” versus detail bullets | Keep the emotional opening and useful factual bullets, care and measurements. |
| Restrained vocabulary versus large banks | Preserve broader banks as references; automate with the approved editorial subset. |
| Clinical or material examples versus missing evidence | Examples show structure and do not authorize facts for another product. |
| Quiet visual drafts versus current creative direction | Current owner decisions and governed storefront design take precedence. This import does not recolor the site. |
| Human-review language versus the always-on worker | Preserve current gates and curated decisions. Do not enable a gate or start a bulk rewrite. |
| “300+” editorial frames | The recovered native library contains 51 quoted frames. Unsafe example claims do not become runtime templates. |
| Historical systems and code | Retain text with provenance, without executing it or importing legacy catalogs. |

Current owner instructions and verified product facts have first priority. The active policy and current publication safeguards come next, followed by canonical documents and historical references. The [brand constitution](../00_Doctrine/brand_constitution.md), [identity rules](../02_Brand_Identity/brand_rules.md), [naming system](../04_Products/Product_Naming_System.md), [tone guide](Tone_Guide.md), [writing rules](Writing_Rules.md) and [voice consistency rules](Voice_Consistency_Rules.md) supply detailed doctrine.

## Runtime and maintenance

`app/lib/brand-vocabulary.server.ts` validates and loads the policy. The product writer uses its labels, category openings, restrictions and copy limits. The naming module uses its generated-title limit. `app/lib/automated-content-surfaces.ts` uses the brand's surface templates and the same policy limits. Unknown placeholders, empty templates, forbidden wording and unsupported claim templates fail validation. Both Docker images include the voice directory and carry the same policy.

The processor records `product.content_surfaces.completed` with the policy version and each actual publication result. A generated blog or collection is not proof of publication: check the result and read the Shopify output. Existing publication gates still determine whether each surface is written.

All loaded files contribute to the automation fingerprint. Editing the active policy changes that fingerprint. Recovered references stay outside the runtime source list: an old draft changes live behavior only after its guidance is reconciled into the active policy.

Existing handles, SKUs, barcodes, inventory and variant configuration remain protected. Current claim-review and publication controls continue. Historical SKU conventions, old datasets and deployment snippets are not migration instructions.

Run `npm run test:brand-content`, `npm run test:catalog-automation`, `npm run typecheck`, `npm run build` and the source-security scan when changing policy or writer. The catalog accounts for 1,693 matched Drive files: 468 substantive original content versions, 35 distinct placeholder contents and one empty content. Identical readable copies and existing OS documents are linked instead of duplicated unnecessarily.
