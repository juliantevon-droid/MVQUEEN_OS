# MVQUEEN App Ecosystem Contract

**Status:** ACTIVE BUILD  
**Date:** 2026-09-17

## Purpose

MVQUEEN uses Shopify apps only where an app provides a capability that should remain external to the core MVQUEEN_OS architecture.

The storefront, catalog intelligence, SEO generation, protected-field controls, collection logic, QA, and Shopify synchronization remain owned by MVQUEEN_OS unless an explicit architecture decision says otherwise.

## Core Principle

**Apps extend MVQUEEN. They do not become the source of truth for MVQUEEN.**

Primary source-of-truth hierarchy:

1. MVQUEEN doctrine and brand contracts
2. MVQUEEN_OS production systems
3. Shopify native commerce primitives
4. Approved external apps
5. Temporary experiments

## Approved App Roles

### Reviews / Social Proof
Use one review platform when the catalog is ready for customer traffic.

Preferred role:
- verified customer reviews
- photo/video reviews where appropriate
- review request automation
- review structured-data support where compatible

The app must not control the visual identity of the storefront.

### Search / Discovery
Prefer Shopify native Search & Discovery first.

Responsibilities:
- filters
- search configuration
- product recommendations
- merchandising signals

MVQUEEN owns presentation and UX.

### Google Commerce / Measurement
Use Shopify's official Google & YouTube integration plus Google measurement infrastructure when ready.

Responsibilities:
- Merchant Center connectivity
- product feed eligibility
- Google Shopping foundation
- measurement integrations

MVQUEEN_OS remains responsible for product data quality before synchronization.

### Lifecycle Marketing
A single lifecycle platform may be introduced after the storefront and catalog foundation are stable.

Responsibilities:
- welcome flows
- browse/cart recovery
- post-purchase messaging
- segmentation
- campaign measurement

It must consume approved MVQUEEN customer/product data rather than rewriting catalog source data.

## Conditional App Roles

Install only when a measurable need exists:

- image optimization/CDN tooling
- backup/recovery
- advanced analytics
- subscriptions
- advanced returns
- specialized fulfillment

Each must pass the app admission test below.

## App Admission Test

An app may be added only when it:

1. Provides a capability not already safely owned by MVQUEEN_OS or Shopify native functionality.
2. Does not require unnecessary theme bloat.
3. Does not overwrite protected catalog fields without governance.
4. Does not introduce supplier branding or conflicting copy.
5. Does not degrade mobile UX or Core Web Vitals materially.
6. Has a clear uninstall/cleanup path.
7. Has a defined owner and purpose.
8. Can be tested on the unpublished development theme first where applicable.
9. Does not require exposing Shopify credentials to an untrusted workflow.
10. Has a measurable success criterion.

## Explicitly Avoid

Do not install multiple overlapping:

- AI product-description generators
- SEO rewriting tools
- duplicate image optimizers
- popup/urgency stacks
- review platforms
- page builders
- collection managers that replace MVQUEEN collection logic

Avoid app-driven storefront reconstruction when native Liquid/CSS/JavaScript can provide the required experience.

## Catalog Protection

Apps must not change without approval:

- Handle
- Product/Variant IDs
- SKU/barcode
- inventory quantities or tracking
- variant option values
- shipping/tax state
- image source/position/variant relationships

Editorial changes must remain compatible with the MVQUEEN catalog contract.

## Current Architecture

Shopify:
commerce primitives and native capabilities.

MVQUEEN custom storefront:
customer-facing presentation and interaction.

MVQUEEN_OS:
catalog intelligence, SEO, content governance, QA, collection assignment, protected-field validation, automation, and deployment controls.

Apps:
narrow capability extensions only.

## Current Install Strategy

**Now**
- Keep Shopify native functionality enabled.
- Do not add overlapping SEO/content apps.
- Establish reviews only when the review UX is ready.
- Establish Google commerce/measurement foundations.

**Next**
- Finish custom storefront.
- Finish catalog ingestion and QA.
- Establish collection/metafield synchronization.
- Validate performance and accessibility.

**Later**
- Add lifecycle marketing after the catalog and storefront are stable.
- Add specialized tooling only when measured requirements justify it.

## Definition of Done

Every installed app has:

- a documented purpose,
- a defined data boundary,
- a performance consideration,
- an uninstall/rollback path,
- a responsible MVQUEEN_OS workflow,
- and no unresolved overlap with an existing system.
