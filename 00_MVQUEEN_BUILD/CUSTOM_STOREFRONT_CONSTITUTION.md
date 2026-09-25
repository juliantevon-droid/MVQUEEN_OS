# MVQueen Custom Storefront Constitution

Status: ACTIVE
Date: 2026-09-17

## Purpose

MVQueen is a custom editorial commerce experience built on Shopify's commerce infrastructure without using Horizon as the customer-experience foundation.

The storefront should feel personal, selective, calm, and intentionally curated even when the underlying catalog is large.

## Experience model

Private boutique × editorial journal × personal curator × digital atelier.

The interface should communicate taste through restraint rather than sales pressure.

## Non-commercial experience rules

- No marketplace-style density.
- No aggressive promotional hierarchy.
- No unnecessary countdowns, flashing offers, or repetitive urgency language.
- No generic theme-looking sections when a purposeful MVQueen component can express the idea better.
- Product discovery should feel guided, not forced.
- Recommendations should feel editorial and relevant, not like an ad network.
- Copy should be human, concise, confident, and specific.
- Whitespace is an intentional design element.
- Motion is subtle and purposeful.
- Mobile experience is first-class, not a compressed desktop layout.

## Custom architecture

Shopify remains responsible for commerce primitives: products, variants, inventory, cart, checkout, customer accounts, payments, orders, and APIs.

MVQueen owns the presentation and interaction layer:

- layout
- navigation
- typography
- visual hierarchy
- editorial modules
- collection discovery
- product presentation
- search interface
- filters
- cart presentation
- responsive behavior
- motion
- accessibility presentation
- structured data presentation

## Curated discovery model

The storefront should guide a customer through:

Brand → Story → Edit → Product → Related discovery → Cart

rather than:

Homepage → grid → grid → grid → checkout.

## Catalog scale principle

A large catalog must remain invisible as complexity. The customer should encounter curated entry points, meaningful collections, editorial context, and controlled product density.

## Brand discipline

Customer-facing product content uses MVQueen only. Supplier/legacy brand strings must remain excluded by the storefront contract.

## Technical standard

- Native Shopify Liquid/CSS/JavaScript first.
- GraphQL-first for new automation.
- No unnecessary apps.
- No secrets in GitHub.
- No automated live-theme publishing.
- Preserve handles, SKUs, inventory, variants, and media during catalog operations unless a separately governed operation explicitly authorizes a change.
- Every major UX component must work with keyboard navigation, reduced motion, touch input, and mobile viewport constraints.

## Definition of done

A customer should be able to enter MVQueen, understand the brand, discover something intentionally, evaluate a product comfortably, add it to cart, and reach checkout without encountering a generic-theme feel or a known blocking UX defect.
