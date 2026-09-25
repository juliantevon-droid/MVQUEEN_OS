# MVQueen URL & REDIRECT GOVERNANCE

**Status:** Production control document  
**Owner:** MVQUEEN_OS  
**Commerce platform:** Shopify  
**Customer experience:** Fully custom MVQueen storefront  

## Purpose

Protect search visibility, bookmarks, campaign links, and customer journeys when MVQueen URLs change.

## Core Rules

1. Preserve existing product and collection handles whenever there is no compelling reason to change them.
2. A redirect is created only when an old URL genuinely changes, disappears, or needs a governed canonical destination.
3. Never mass-redirect every catalog item merely because titles or descriptions changed.
4. Redirects must point directly to the final destination; no chains.
5. Redirects must never create loops.
6. Redirect destinations must be valid Shopify paths at deployment time.
7. Redirects must not point to temporary staging URLs, unpublished theme URLs, or external destinations unless explicitly approved.
8. Product, collection, page, blog, and campaign URL changes must be recorded before production deployment.
9. Existing handles, SKUs, variants, inventory, and media remain protected by the catalog guard unless a separately approved migration changes them.
10. Redirect changes are part of the Catalog + URL + Technical SEO production gate.

## Redirect Classes

### Product
- old `/products/<handle>` -> new `/products/<handle>` when a handle actually changes
- retired product -> approved replacement product or relevant collection when justified

### Collection
- old `/collections/<handle>` -> replacement collection when a collection handle changes or is retired

### Pages / Campaigns
- retired campaign or editorial URL -> approved current destination
- legacy landing page -> current canonical experience when the old page is intentionally removed

### Canonical / Legacy
- duplicate or obsolete paths may be redirected only after validating the canonical destination

## Required Redirect Record

Each proposed redirect should record:

- `source`
- `destination`
- `reason`
- `resource_type`
- `resource_identifier`
- `status` (`planned`, `approved`, `applied`, `verified`, `rejected`)
- `created_at`
- `verified_at`

## Validation Gate

Before Shopify writes:

- source is a valid relative Shopify path
- destination is a valid relative Shopify path
- source != destination
- no self-loop
- no redirect chain
- no redirect loop
- no duplicate source entries
- destination exists or is explicitly approved as a future resource
- no accidental supplier/legacy brand contamination in generated campaign paths

## Deployment Sequence

```text
Catalog / Theme Change
        ↓
Handle & URL Audit
        ↓
Detect Actual URL Changes
        ↓
Generate Redirect Plan
        ↓
Validate Redirect Graph
        ├── no loops
        ├── no chains
        ├── no duplicate sources
        └── valid destinations
        ↓
Human Review / Approval
        ↓
Shopify Redirect Write
        ↓
Post-write Verification
        ↓
Search / Analytics Monitoring
```

## Safety

Redirect generation is dry-run by default. Production writes require explicit approval and a validated target. Live storefront publishing remains a separate action from redirect deployment.

## Definition of Done

A URL migration is complete only when the approved redirects are applied, direct destinations resolve correctly, no redirect chains or loops are detected, and the final URL map is retained as an auditable production artifact.
