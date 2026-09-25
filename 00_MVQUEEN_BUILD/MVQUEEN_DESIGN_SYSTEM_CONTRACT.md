# MVQueen DESIGN SYSTEM CONTRACT

**Status:** Production foundation
**Owner:** MVQUEEN_OS
**Customer experience:** Custom MVQueen storefront

## Purpose

This contract establishes one visual and interaction language for the MVQueen storefront. New sections should use these primitives instead of creating isolated styling systems.

## Brand Tokens

```css
:root {
  --mvq-gold: #D4AF37;
  --mvq-cream: #FFF8F0;
  --mvq-rose: #8B4A5C;
  --mvq-pearl: #FAFAF8;
  --mvq-charcoal: #2C2C2C;
  --mvq-blush: #F5E6E0;
  --mvq-ivory: #F5F1EB;
  --mvq-sage: #A8ABA3;
  --mvq-mauve: #9D7F95;
}
```

## Typography

- Display: Cormorant Garamond
- Interface/body: Jost
- Display typography communicates editorial character.
- Jost handles navigation, controls, metadata, descriptions, forms, and utility text.

## Layout

- Mobile is first-class, not a compressed desktop layout.
- Use generous whitespace and controlled content density.
- Prefer editorial asymmetry where it improves storytelling.
- Product grids should feel curated rather than marketplace-like.
- Avoid excessive cards, badges, banners, popups, and competing calls to action.

## Interaction

- Motion is subtle and purposeful.
- Respect `prefers-reduced-motion`.
- Every interactive control needs a visible keyboard focus state.
- Touch targets should be comfortably usable on mobile.
- Never make animation necessary to understand or purchase a product.

## Components

Approved reusable primitives:

- `.mvq-container`
- `.mvq-eyebrow`
- `.mvq-display`
- `.mvq-copy`
- `.mvq-button`
- `.mvq-card`
- `.mvq-section`
- product media/gallery
- product information panel
- editorial navigation
- filter/sort controls
- cart controls
- disclosure/accordion rows

## Commerce Presentation

Shopify remains the commerce engine. MVQueen controls presentation.

Shopify-owned primitives include products, variants, inventory, cart, checkout, payments, orders, and account infrastructure.

MVQUEEN-owned presentation includes navigation, editorial hierarchy, product storytelling, discovery, filters, recommendations, calls to action, typography, spacing, color, motion, and responsive behavior.

## Content Rules

- Customer-facing product content uses MVQueen language.
- Supplier/legacy brand names must not appear in customer-facing copy.
- Product copy should be useful before it is promotional.
- Recommendations should feel curated and relevant.
- Avoid manufactured urgency and repetitive promotional language.

## Accessibility

- Semantic landmarks are required.
- Images require meaningful alt text when informative.
- Decorative imagery must not create redundant screen-reader content.
- Color contrast must remain readable across all responsive states.
- Focus states must remain visible.
- Controls need accessible names and state communication.

## Performance

- Prefer CSS and native browser behavior before JavaScript.
- JavaScript must be progressive enhancement.
- Avoid unnecessary third-party scripts.
- Images should use responsive Shopify image delivery and lazy loading where appropriate.
- Critical rendering should not depend on nonessential scripts.

## Governance

Before adding a new component:

1. Check whether an existing primitive can express the experience.
2. Add the smallest reusable primitive if necessary.
3. Keep styling centralized in the MVQueen design system.
4. Test mobile, keyboard navigation, reduced motion, and visual hierarchy.
5. Run storefront contract validation and Shopify Theme Check.
6. Never deploy directly to the live MAIN theme through automation.

## Definition of Done

The design system is considered implemented when the storefront no longer depends on conflicting legacy style conventions and all major customer journeys share the same MVQueen visual, responsive, accessibility, and interaction language.
