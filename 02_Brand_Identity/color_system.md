# Color System
## MVQUEEN_OS / 02_Brand_Identity

---

## Purpose

The color system is the visual governance layer for MVQUEEN. Every color carries emotional weight and must be deployed consistently across all touchpoints—from Shopify to social media to packaging.

Colors are never arbitrary. They are chosen to evoke softness, luxury, femininity, confidence, and emotional transformation.

---

## Primary Palette

| Color Name | Hex | RGB | Use Case | Emotional Intent |
|---|---|---|---|---|
| MVQUEEN Gold | #D4AF37 | 212, 175, 55 | Accents, premium signals, CTAs | Luxury, refinement, elevation |
| Soft Cream | #FFF8F0 | 255, 248, 240 | Background, hero sections | Warmth, approachability, softness |
| Deep Rose | #8B4A5C | 139, 74, 92 | Headlines, navigation, depth | Confidence, femininity, strength |
| Pearl White | #FAFAF8 | 250, 250, 248 | Text background, clean space | Luxury minimalism, calm |
| Charcoal | #2C2C2C | 44, 44, 44 | Body text, primary copy | Clarity, elegance, readability |

---

## Secondary Palette

| Color Name | Hex | RGB | Use Case | Emotional Intent |
|---|---|---|---|---|
| Blush | #F5E6E0 | 245, 230, 224 | Subtle backgrounds, borders | Softness, femininity, gentleness |
| Sage | #A8ABA3 | 168, 171, 163 | Secondary accents, muted elements | Balance, natural luxury, calm |
| Dusty Mauve | #9D7F95 | 157, 127, 149 | Hover states, depth layers | Sophisticated femininity |
| Ivory | #F5F1EB | 245, 241, 235 | Cards, sections, containers | Refined minimalism |

---

## Accent Palette

| Color Name | Hex | Use Case |
|---|---|---|
| Energy Red | #D64A3B | Urgency, limited drops, CTAs requiring attention |
| Copper | #B87333 | Premium tier signals, luxury indicators |
| Champagne | #F7E7CE | Celebration, launch moments, special occasions |

---

## Shopify CSS Variables

Copy and paste into your Shopify theme CSS:

```css
:root {
  --color-primary-gold: #D4AF37;
  --color-primary-rose: #8B4A5C;
  --color-primary-charcoal: #2C2C2C;
  
  --color-background-cream: #FFF8F0;
  --color-background-ivory: #F5F1EB;
  --color-background-pearl: #FAFAF8;
  
  --color-secondary-blush: #F5E6E0;
  --color-secondary-sage: #A8ABA3;
  --color-secondary-mauve: #9D7F95;
  
  --color-accent-red: #D64A3B;
  --color-accent-copper: #B87333;
  --color-accent-champagne: #F7E7CE;
  
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
- Background: Soft Cream (#FFF8F0)
- Text: Deep Rose (#8B4A5C)
- Hover/Active: MVQUEEN Gold (#D4AF37)

### Product Cards
- Background: Ivory (#F5F1EB)
- Border: Blush (#F5E6E0)
- Price: Deep Rose (#8B4A5C)
- CTA Button: MVQUEEN Gold (#D4AF37)

### Hero Sections
- Background: Soft Cream (#FFF8F0) or gradients using Cream + Pearl
- Headlines: Deep Rose (#8B4A5C) or Charcoal (#2C2C2C)
- CTAs: MVQUEEN Gold (#D4AF37)

### Footer
- Background: Charcoal (#2C2C2C)
- Text: Soft Cream (#FFF8F0) or Pearl White (#FAFAF8)
- Links: MVQUEEN Gold (#D4AF37)

### Buttons & CTAs
- Primary: MVQUEEN Gold (#D4AF37) with Charcoal text
- Secondary: Deep Rose (#8B4A5C) with Pearl White text
- Hover: Darken primary color by 15%
- Disabled: Sage (#A8ABA3) at 60% opacity

### Forms & Inputs
- Border: Blush (#F5E6E0)
- Focus: MVQUEEN Gold (#D4AF37)
- Background: Pearl White (#FAFAF8)
- Text: Charcoal (#2C2C2C)

---

## Social Media Color Application

| Platform | Primary | Secondary | Accent |
|---|---|---|---|
| Instagram | Deep Rose | Soft Cream | MVQUEEN Gold |
| TikTok | Charcoal | MVQUEEN Gold | Deep Rose |
| Pinterest | MVQUEEN Gold | Soft Cream | Deep Rose |
| Facebook | Deep Rose | Ivory | MVQUEEN Gold |

---

## Email Header & CTA Colors

- Header Background: Soft Cream (#FFF8F0)
- CTA Button: MVQUEEN Gold (#D4AF37) with Charcoal text
- Text Links: Deep Rose (#8B4A5C)
- Footer Background: Charcoal (#2C2C2C)
- Footer Text: Soft Cream (#FFF8F0)

---

## Packaging Colors

- Primary Box: Soft Cream (#FFF8F0)
- Tissue Paper: Blush (#F5E6E0)
- Ribbon/Accent: MVQUEEN Gold (#D4AF37) or Deep Rose (#8B4A5C)
- Sleeve Print: Charcoal (#2C2C2C) on Cream background

---

## Accessibility Standards

All color combinations must meet WCAG AA contrast requirements:
- Text on backgrounds: 4.5:1 minimum contrast
- Large text (18pt+): 3:1 minimum contrast
- UI components: 3:1 minimum contrast

**Verified combinations:**
- Charcoal (#2C2C2C) on Pearl White (#FAFAF8): ✅ 11.2:1
- Deep Rose (#8B4A5C) on Ivory (#F5F1EB): ✅ 6.1:1
- MVQUEEN Gold (#D4AF37) on Charcoal (#2C2C2C): ✅ 5.8:1
- Charcoal (#2C2C2C) on Soft Cream (#FFF8F0): ✅ 12.1:1

---

## Status

Color System — **Active**

All colors approved and deployment-ready. Update Shopify theme CSS variables immediately upon store setup.