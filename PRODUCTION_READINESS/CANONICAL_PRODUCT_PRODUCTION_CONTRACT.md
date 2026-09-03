# MVQUEEN Canonical Product Production Contract

**Purpose:** Single production contract for turning one verified product into a sellable, searchable, marketable and measurable MVQUEEN product record.

## Non-Negotiable Principle

The system may enrich and interpret product data, but it may not invent product facts. Generated content must preserve the distinction between source facts, verified attributes, brand interpretation, marketing language and SEO language.

## Canonical Pipeline

`RAW → NORMALIZED → INTELLIGENCE_READY → COPY_READY → SEO_READY → MERCH_READY → COMMERCIAL_READY → CREATIVE_READY → QA_PASSED → PRODUCTION_READY`

Any failed stage blocks downstream publication.

## 1. Product Truth

Required inputs:

- source/product identifier
- supplier/source data
- product category
- product type
- verified materials/ingredients where applicable
- verified dimensions/sizing where applicable
- variants
- price
- inventory reference
- source images
- source image metadata

Protected fields must not be silently altered: inventory, SKU, variant identity and source identifiers.

## 2. Product Intelligence

The engine derives, without fabricating facts:

- customer need/desire
- use context
- aesthetic/emotional positioning
- primary benefit when supported by source facts
- differentiators
- likely objections
- related products
- collection candidates
- bundle/cross-sell candidates

## 3. Copy Package

Required outputs:

- canonical product title
- short description
- full description
- benefits/features section
- product details
- FAQ inputs where supported
- approved CTA

Copy must follow MVQUEEN voice: elegant, confident, premium-but-simple and empowering.

## 4. SEO Package

Required outputs:

- canonical SEO title
- meta description
- URL/handle recommendation when allowed by workflow
- primary keyword
- secondary keywords
- image ALT text for every eligible image
- internal-link targets

### Canonical SEO naming rule

The production engine must use **one** SEO title contract. Do not allow competing title conventions to run independently. The selected convention must be stored as configuration and tested globally before mass production.

## 5. Merchandising Package

Required outputs:

- primary collection
- secondary collections
- merchandising tags
- related products
- cross-sell candidates
- bundle candidates
- merchandising rationale

## 6. Commercial Package

Required outputs:

- customer desire/problem
- transformation angle
- positioning angle
- offer eligibility
- price guardrail result
- proof/evidence available
- trust signals
- objections
- objection responses
- funnel stage
- landing-page requirements

## 7. Creative Package

For each qualified product, the system should be able to produce structured assets for:

### Paid

- Meta primary text variants
- Meta headlines
- short-form video hooks
- TikTok concepts/captions
- retargeting variants
- Google-oriented headline/description inputs where applicable

### Organic

- Instagram caption variants
- Reel hooks
- TikTok concepts
- Pinterest title/description
- UGC prompts

### Lifecycle

- launch email
- product email
- abandoned-cart inputs
- browse/product-view inputs
- post-purchase content
- review request
- SMS variants where applicable

## 8. Measurement Package

Every production product/campaign record must be traceable to:

- product identifier
- campaign identifier
- channel
- creative identifier
- funnel stage
- offer identifier
- landing destination

Minimum funnel events:

`ViewContent → AddToCart → BeginCheckout → Purchase`

## 9. QA Gates

### Hard failures

- missing product truth
- unsupported factual claim
- missing required title/description
- missing required SEO fields
- missing required ALT text
- invalid pricing/offer configuration
- missing commercial positioning
- missing required creative assets
- missing tracking identifier
- conflicting canonical fields
- protected data mutation

### Soft warnings

- weak differentiation
- repetitive language
- low keyword relevance
- insufficient proof
- weak objection coverage
- incomplete cross-sell opportunities

Soft warnings may be reviewed; hard failures block production.

## 10. Production Output

A product may receive `PRODUCTION_READY` only when:

- all required fields exist
- all hard QA gates pass
- claims are supported
- canonical SEO rules pass
- commercial requirements pass
- creative manifest is complete
- measurement identifiers exist
- Shopify export validation passes

## Ownership Model

The contract is the bridge between MVQUEEN brand doctrine, product processing, SEO, copy, merchandising, marketing, analytics, QA and Shopify export. Individual engines may implement stages, but no engine may redefine the canonical contract independently.
