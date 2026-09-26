# System Blueprint: Shopify + MVQUEEN_OS Product Intelligence
## MVQUEEN_OS / 35_System_Blueprints

---

## 1. Purpose
This blueprint defines the production architecture for synchronization between MVQUEEN_OS and the Shopify Admin GraphQL API, with the product catalog treated as an automated, validated content-and-classification system.

Target behavior:
Shopify product enters or changes → webhook → MVQUEEN_OS product intelligence → validate → write approved fields → automatic collection routing → audit log

## 2. Current Platform Standard
- Shopify API: Admin GraphQL API.
- API version target: 2026-07 at this update; verify the latest stable version before deployment.
- Authentication: Shopify app authentication with persistent per-shop credentials stored outside source control.
- Webhook delivery: HTTPS endpoint with Shopify-managed HMAC verification.
- Processing: asynchronous job/queue architecture; webhook handlers acknowledge quickly.
- Runtime: Shopify app backend to be implemented in the production app project.
- Secrets: never committed to GitHub.

Legacy REST examples and former outdated API references are retired from the production design.

## 3. Product Automation Contract
Every newly created or meaningfully updated product is eligible for MVQUEEN_OS processing.

The processor reads product title, existing description, product type, vendor, category, variants and verified attributes, media information, existing tags, existing metafields, and source facts available on the product.

The processor may generate or normalize:
1. Customer-facing title
2. Short description
3. Full editorial Body HTML
4. Benefits/details where supported by source facts
5. SEO title
6. SEO meta description
7. SEO keyword set
8. Image alt text
9. Product type
10. MVQueen taxonomy
11. Collection-routing tags
12. Structured metafields
13. Data-quality/review state

## 4. Protected Fields
The product intelligence worker must not change these fields unless a separate explicitly authorized workflow is created:
- SKU
- inventory quantities
- inventory locations
- variant IDs
- variant option values
- pricing
- fulfillment configuration
- product images/media source files
- vendor
- handles
- redirects

Existing verified product facts must be preserved. Unknown facts remain unknown rather than being invented.

Handle changes, if ever required, must use a dedicated migration with redirect creation and validation.

## 5. Classification and Routing
MVQUEEN_OS uses deterministic classification before editorial generation.

Core hierarchy:
Department → Family → Collection → Subcollection → Style

Examples:
- Blouse → Fashion/Clothing → Tops → Blouses
- T-shirt → Fashion/Clothing → Tops → T-Shirts
- Pendant → Jewelry → Necklaces → Pendant Necklaces
- Dress → Fashion/Clothing → Dresses
- Skincare product → Beauty → Skincare

Routing tags use the internal namespace mvq:catalog and mvq:collection:<slug>.

Products that cannot be classified with sufficient confidence receive mvq:needs-review and are placed into the Needs Review smart collection.

Products may intentionally belong to multiple collections when their classification supports more than one customer discovery path.

## 6. Processing State
Recommended states:
- queued
- processing
- completed
- needs-review
- failed

Recommended operational metadata:
- processing version
- last processed timestamp
- classification confidence
- data quality status
- source/content fingerprint
- last error code/message where appropriate

## 7. Webhook Events
Required initial product events:
- products/create
- products/update

Required lifecycle/compliance events:
- app/uninstalled
- customers/data_request
- customers/redact
- shop/redact

Product webhook handlers must authenticate delivery, identify the shop and event, deduplicate using webhook/event ID, enqueue the product, return success quickly, process asynchronously, and record outcome.

## 8. Processing Pipeline
Stage A — Intake: receive webhook and create an idempotent job.
Stage B — Product Fetch: retrieve the authoritative current product through Admin GraphQL.
Stage C — Fact Extraction: separate verified source facts from classification signals.
Stage D — Deterministic Classification: determine taxonomy and structured attributes using controlled vocabulary.
Stage E — Editorial Generation: create MVQueen customer-facing copy while forbidding unsupported specifications, supplier filler, third-party brand leakage, and repetitive templates.
Stage F — SEO Generation: create concise metadata from actual product facts and classification.
Stage G — Media Accessibility: create descriptive image alt text without keyword stuffing.
Stage H — Validation: validate required fields, prohibited strings, unsupported claims, taxonomy, SEO limits, HTML safety, protected-field integrity, routing tags, and loop risk.
Stage I — Shopify Write: use Admin GraphQL mutations for approved fields only.
Stage J — Post-Write Verification: re-read and verify intended changes.
Stage K — Audit: record product ID, processing version, outcome, changed-field categories, timestamps, and errors without credentials.

## 9. Idempotency and Loop Prevention
Use Shopify webhook/event ID deduplication, product processing fingerprint/version, job status, source-change detection, and explicit MVQUEEN_OS write markers.

A product update caused by MVQUEEN_OS must not recursively trigger an endless processing loop.

## 10. Failure Handling
- transient Shopify/API errors → retry with backoff
- rate limiting → respect retry guidance
- malformed product data → mark needs-review
- unsupported classification → route to Needs Review
- generation failure → retain existing valid content and retry
- validation failure → do not publish invalid generated content
- repeated failures → stop retrying and surface an actionable error

No failure should silently destroy valid existing product data.

## 11. Existing Catalog Backfill
Webhooks only cover future events. The existing 900+ product catalog therefore requires a separate controlled backfill.

Backfill requirements:
- batch processing
- checkpointing
- rate-limit awareness
- dry-run capability
- per-product audit trail
- retry queue
- protected-field enforcement
- pause/resume capability
- no uncontrolled bulk mutation

Test on a small sample before the full catalog.

## 12. Security
Never commit Shopify API secrets, access tokens, webhook secrets, OAuth client secrets, database credentials, or AI provider keys.

Source code, schemas, prompts, taxonomy, validation rules, documentation, and non-secret configuration belong in MVQUEEN_OS.

Production secrets belong in the deployment platform's secret/environment system.

## 13. Current Implementation Status
Implemented on `main`:
- MVQUEEN_OS architecture and doctrine
- authenticated React Router Shopify app runtime
- products/create and products/update webhook subscriptions and handlers
- durable ProductJob idempotency records
- automatic product enrollment gate for new/updated Shopify products
- deterministic MVQueen taxonomy and Miss.Princess/MVQueen routing
- factual short description and product-highlight generation
- short-tail focus keywords and verified long-tail keyword generation
- Shopify SEO title/meta publishing behind a dedicated gate
- product classification, SEO and catalog metafields
- optional missing-image-ALT repair with dedicated file scopes/gate
- source fingerprint/version loop prevention
- protected-field policy
- commercial health and advertising eligibility metadata
- durable bounded existing-catalog backfill queue
- production environment preflight
- Needs Review fallback behavior

Still required for literal 24/7 production operation:
- deploy the app to a real always-on HTTPS host
- provision the production PostgreSQL database
- configure real Shopify app client credentials/application URL
- reauthorize the Shopify app for the current product/file scopes
- enable the production automation environment gates
- complete one safe products/create end-to-end test and one products/update test
- verify retry/observability behavior in the chosen host

Not yet claimed as complete:
Code present in GitHub is not the same as a continuously running service. MVQUEEN_OS becomes 24/7 automation only after the hosted app is live, authenticated, receiving Shopify webhooks, and the production preflight passes.

## 14. Success Criteria
- a new product can enter Shopify without manual catalog optimization
- the product automatically receives its MVQueen content/classification package
- valid products automatically route into appropriate collections
- uncertain products are isolated in Needs Review
- protected operational fields remain unchanged
- webhook duplicates do not duplicate work
- failures are observable and recoverable
- every automated write is auditable
- credentials are never stored in source control
- the existing catalog can be backfilled safely using the same processing engine

## 15. Change Control
MVQUEEN_OS is the source-controlled design authority for the automation system.

Production changes should be implemented in code/configuration, validated, tested against a safe product, documented, committed to GitHub, and deployed only after verification.

This prevents the live Shopify store from becoming the undocumented source of truth for system behavior.

## 16. Status
ACTIVE — Architecture and Shopify catalog foundation established. Production webhook/app runtime is the next implementation layer.