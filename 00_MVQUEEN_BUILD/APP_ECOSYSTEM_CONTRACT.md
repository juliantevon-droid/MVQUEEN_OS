# MVQueen App Ecosystem Contract

**Status:** ACTIVE  
**Consolidated:** 2026-09-23

## Core principle

Apps extend MVQueen. They do not become the source of truth for MVQueen.

Source-of-truth hierarchy:

1. MVQueen doctrine and brand contracts
2. MVQUEEN_OS production systems
3. Shopify native commerce primitives
4. Approved external apps
5. Temporary experiments

## Approved roles

Use Shopify-native capabilities first. External apps may provide narrow capabilities such as verified reviews, lifecycle marketing, measurement, specialized fulfillment, returns, subscriptions, or recovery when a measurable need exists.

MVQUEEN_OS remains responsible for storefront presentation, catalog intelligence, SEO/content governance, protected-field controls, QA, collection logic, and controlled Shopify synchronization.

## App admission gate

An app must:

- provide a capability not safely owned by MVQUEEN_OS or Shopify native functionality;
- avoid unnecessary theme bloat;
- not overwrite protected catalog fields without governance;
- not introduce supplier branding or conflicting copy;
- preserve mobile UX and performance;
- have an uninstall/rollback path;
- have a defined owner, purpose, data boundary, and success criterion;
- be tested on the unpublished development theme first where applicable;
- never require credentials to be committed to the repository.

## Explicitly avoid

Do not install overlapping AI copy generators, SEO rewriters, page builders, review platforms, popup/urgency stacks, collection managers, or duplicate image optimizers when the capability is already owned by MVQUEEN_OS or Shopify native functionality.

## Protected catalog boundary

Apps and automation must not change without explicit approval:

- handles and product/variant identity;
- SKU/barcode;
- inventory quantities or tracking;
- variant option values;
- shipping/tax state;
- image source, position, or variant relationships.

Editorial changes must remain compatible with the canonical catalog contract.
