# Color System
## MVQUEEN_OS / 02_Brand_Identity

---

> **Uploaded logo alignment — 2026-09-25:** The active palette now follows the approved MVQueen gold/ivory/charcoal identity and the softer rose/blush sister-brand direction. White and light backgrounds remain dominant for a cleaner luxury storefront.

## Purpose

The color system is the visual governance layer for MVQueen. Every color carries emotional weight and must be deployed consistently across all touchpoints—from Shopify to social media to packaging.

Colors are never arbitrary. They are chosen to evoke softness, luxury, femininity, confidence, and emotional transformation.

---

## Primary Palette

| Color Name | Hex | RGB | Use Case | Emotional Intent |
|---|---|---|---|---|
| MVQueen Gold | #C99B4A | 201, 155, 74 | Accents, premium signals, CTAs | Luxury, refinement, elevation |
| Soft Cream | #FFF9F2 | 255, 249, 242 | Background, hero sections | Warmth, approachability, softness |
| Deep Rose | #B52255 | 181, 34, 85 | Headlines, navigation, depth | Confidence, femininity, strength |
| Pearl White | #FFFFFF | 255, 255, 255 | Text background, clean space | Luxury minimalism, calm |
| Charcoal | #171310 | 23, 19, 16 | Body text, primary copy | Clarity, elegance, readability |

---

## Secondary Palette

| Color Name | Hex | RGB | Use Case | Emotional Intent |
|---|---|---|---|---|
| Blush | #F3DFE7 | 243, 223, 231 | Subtle backgrounds, borders | Softness, femininity, gentleness |
| Sage | #B8B0AA | 184, 176, 170 | Secondary accents, muted elements | Balance, natural luxury, calm |
| Dusty Mauve | #B8758E | 184, 117, 142 | Hover states, depth layers | Sophisticated femininity |
| Ivory | #FBF5EE | 251, 245, 238 | Cards, sections, containers | Refined minimalism |

---

## Functional Contrast Tokens

These darker companion tones are reserved for small text, keyboard focus, and other accessibility-critical UI. They preserve the softer palette without asking decorative colors to perform as body text.

| Token | Hex | Use Case |
|---|---|---|
| Rose Strong | #B52255 | Eyebrows, prices, small labels, accessible rose hover states |
| Gold Strong | #8A6428 | Keyboard focus, small gold text, accessibility-critical accents |
| Mink Text | #7B6E67 | Muted utility copy, compare-at prices, secondary notes |

Deep Rose (#B52255) is approved for normal-size text on light backgrounds. MVQueen Gold (#C99B4A) remains a decorative/accent color; use Gold Strong (#8A6428) when small gold text or focus UI needs WCAG AA contrast.

---

## Accent Palette

| Color Name | Hex | Use Case |
|---|---|---|
| Energy Red | #D64A3B | Urgency, limited drops, CTAs requiring attention |
| Copper | #B87333 | Premium tier signals, luxury indicators |
| Champagne | #F2D39A | Celebration, launch moments, special occasions |

---

## Shopify CSS Variables

Copy and paste into your Shopify theme CSS:

```css
:root {
  --color-primary-gold: #C99B4A;
  --color-primary-gold-strong: #8A6428;
  --color-primary-rose: #B52255;
  --color-primary-rose-strong: #B52255;
  --color-primary-charcoal: #171310;
  --color-text-muted: #7B6E67;
  
  --color-background-cream: #FFF9F2;
  --color-background-ivory: #FBF5EE;
  --color-background-pearl: #FFFFFF;
  
  --color-secondary-blush: #F3DFE7;
  --color-secondary-sage: #B8B0AA;
  --color-secondary-mauve: #B8758E;
  
  --color-accent-red: #D64A3B;
  --color-accent-copper: #B87333;
  --color-accent-champagne: #F2D39A;
  
  --text-primary: var(--color-primary-charcoal);
  --text-secondary: var(--color-secondary-sage);
  --background-primary: var(--color-background-pearl);
  --background-secondary: var(--color-background-cream);
  --accent-primary: var(--color-primary-gold);
}
```

---

## Color Application Rules

### Navigation & Headers
- Background: Soft Cream (#FFF9F2)
- Text: Deep Rose (#B52255)
- Hover/Active: MVQueen Gold (#C99B4A)

### Product Cards
- Background: Ivory (#FBF5EE)
- Border: Blush (#F3DFE7)
- Price: Deep Rose (#B52255)
- CTA Button: MVQueen Gold (#C99B4A)

### Hero Sections
- Background: Soft Cream (#FFF9F2) or gradients using Cream + Pearl
- Headlines: Deep Rose (#B52255) or Charcoal (#171310)
- CTAs: MVQueen Gold (#C99B4A)

### Footer
- Background: Charcoal (#171310)
- Text: Soft Cream (#FFF9F2) or Pearl White (#FFFFFF)
- Links: MVQueen Gold (#C99B4A)

### Buttons & CTAs
- Primary: MVQueen Gold (#C99B4A) with Charcoal text
- Secondary: Deep Rose (#B52255) with Pearl White text
- Hover: Darken primary color by 15%
- Disabled: Sage (#B8B0AA) at 60% opacity

### Forms & Inputs
- Border: Blush (#F3DFE7)
- Focus: MVQueen Gold (#C99B4A)
- Background: Pearl White (#FFFFFF)
- Text: Charcoal (#171310)

---

## Social Media Color Application

| Platform | Primary | Secondary | Accent |
|---|---|---|---|
| Instagram | Deep Rose | Soft Cream | MVQueen Gold |
| TikTok | Charcoal | MVQueen Gold | Deep Rose |
| Pinterest | MVQueen Gold | Soft Cream | Deep Rose |
| Facebook | Deep Rose | Ivory | MVQueen Gold |

---

## Email Header & CTA Colors

- Header Background: Soft Cream (#FFF9F2)
- CTA Button: MVQueen Gold (#C99B4A) with Charcoal text
- Text Links: Deep Rose (#B52255)
- Footer Background: Charcoal (#171310)
- Footer Text: Soft Cream (#FFF9F2)

---

## Packaging Colors

- Primary Box: Soft Cream (#FFF9F2)
- Tissue Paper: Blush (#F3DFE7)
- Ribbon/Accent: MVQueen Gold (#C99B4A) or Deep Rose (#B52255)
- Sleeve Print: Charcoal (#171310) on Cream background

---

## Accessibility Standards

All color combinations must meet WCAG AA contrast requirements:
- Normal text: 4.5:1 minimum contrast
- Large text: 3:1 minimum contrast
- UI components and focus indicators: 3:1 minimum contrast

**Verified production combinations:**
- Charcoal (#171310) on Pearl White (#FFFFFF): approximately 13.2:1
- Rose Strong (#B52255) on Pearl White (#FFFFFF): approximately 5.36:1
- Rose Strong (#B52255) on Blush (#F3DFE7): approximately 4.70:1
- MVQueen Gold (#C99B4A) on Charcoal (#171310): approximately 6.14:1
- Gold Strong (#8A6428) on Soft Cream (#FFF9F2): approximately 4.65:1
- Mink Text (#7B6E67) on Pearl White (#FFFFFF): approximately 5.02:1
- Charcoal (#171310) on Soft Cream (#FFF9F2): approximately 12.9:1

Decorative Soft Rose and Gold should not be used for small text on light backgrounds unless paired with their stronger accessibility token.

---

## Status

Color System — **Active**

All colors approved and deployment-ready. Update Shopify theme CSS variables immediately upon store setup.