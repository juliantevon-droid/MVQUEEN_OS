# Color System
## MVQUEEN_OS / 02_Brand_Identity

---

## Purpose

The color system is the visual governance layer for MVQueen. Every color carries emotional weight and must be deployed consistently across all touchpoints—from Shopify to social media to packaging.

Colors are never arbitrary. They are chosen to evoke softness, luxury, femininity, confidence, and emotional transformation.

---

## Primary Palette

| Color Name | Hex | RGB | Use Case | Emotional Intent |
|---|---|---|---|---|
| MVQueen Gold | #C7AD86 | 212, 175, 55 | Accents, premium signals, CTAs | Luxury, refinement, elevation |
| Soft Cream | #FFFCF8 | 255, 248, 240 | Background, hero sections | Warmth, approachability, softness |
| Deep Rose | #A97886 | 139, 74, 92 | Headlines, navigation, depth | Confidence, femininity, strength |
| Pearl White | #FFFFFF | 250, 250, 248 | Text background, clean space | Luxury minimalism, calm |
| Charcoal | #342F2C | 44, 44, 44 | Body text, primary copy | Clarity, elegance, readability |

---

## Secondary Palette

| Color Name | Hex | RGB | Use Case | Emotional Intent |
|---|---|---|---|---|
| Blush | #F8EEEA | 245, 230, 224 | Subtle backgrounds, borders | Softness, femininity, gentleness |
| Sage | #B8BAB1 | 168, 171, 163 | Secondary accents, muted elements | Balance, natural luxury, calm |
| Dusty Mauve | #B7A2AF | 157, 127, 149 | Hover states, depth layers | Sophisticated femininity |
| Ivory | #FCF8F4 | 245, 241, 235 | Cards, sections, containers | Refined minimalism |

---

## Functional Contrast Tokens

These darker companion tones are reserved for small text, keyboard focus, and other accessibility-critical UI. They preserve the softer palette without asking decorative colors to perform as body text.

| Token | Hex | Use Case |
|---|---|---|
| Rose Strong | #8B5E6C | Eyebrows, prices, small labels, accessible rose hover states |
| Gold Strong | #876F50 | Keyboard focus, small gold text, accessibility-critical accents |
| Mink Text | #786D68 | Muted utility copy, compare-at prices, secondary notes |

Soft Rose (#A97886) and MVQueen Gold (#C7AD86) remain decorative/accent colors. Use the strong companion tokens when normal-size text needs WCAG AA contrast.

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
  --color-primary-gold: #C7AD86;
  --color-primary-gold-strong: #876F50;
  --color-primary-rose: #A97886;
  --color-primary-rose-strong: #8B5E6C;
  --color-primary-charcoal: #342F2C;
  --color-text-muted: #786D68;
  
  --color-background-cream: #FFFCF8;
  --color-background-ivory: #FCF8F4;
  --color-background-pearl: #FFFFFF;
  
  --color-secondary-blush: #F8EEEA;
  --color-secondary-sage: #B8BAB1;
  --color-secondary-mauve: #B7A2AF;
  
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
- Background: Soft Cream (#FFFCF8)
- Text: Deep Rose (#A97886)
- Hover/Active: MVQueen Gold (#C7AD86)

### Product Cards
- Background: Ivory (#FCF8F4)
- Border: Blush (#F8EEEA)
- Price: Deep Rose (#A97886)
- CTA Button: MVQueen Gold (#C7AD86)

### Hero Sections
- Background: Soft Cream (#FFFCF8) or gradients using Cream + Pearl
- Headlines: Deep Rose (#A97886) or Charcoal (#342F2C)
- CTAs: MVQueen Gold (#C7AD86)

### Footer
- Background: Charcoal (#342F2C)
- Text: Soft Cream (#FFFCF8) or Pearl White (#FFFFFF)
- Links: MVQueen Gold (#C7AD86)

### Buttons & CTAs
- Primary: MVQueen Gold (#C7AD86) with Charcoal text
- Secondary: Deep Rose (#A97886) with Pearl White text
- Hover: Darken primary color by 15%
- Disabled: Sage (#B8BAB1) at 60% opacity

### Forms & Inputs
- Border: Blush (#F8EEEA)
- Focus: MVQueen Gold (#C7AD86)
- Background: Pearl White (#FFFFFF)
- Text: Charcoal (#342F2C)

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

- Header Background: Soft Cream (#FFFCF8)
- CTA Button: MVQueen Gold (#C7AD86) with Charcoal text
- Text Links: Deep Rose (#A97886)
- Footer Background: Charcoal (#342F2C)
- Footer Text: Soft Cream (#FFFCF8)

---

## Packaging Colors

- Primary Box: Soft Cream (#FFFCF8)
- Tissue Paper: Blush (#F8EEEA)
- Ribbon/Accent: MVQueen Gold (#C7AD86) or Deep Rose (#A97886)
- Sleeve Print: Charcoal (#342F2C) on Cream background

---

## Accessibility Standards

All color combinations must meet WCAG AA contrast requirements:
- Normal text: 4.5:1 minimum contrast
- Large text: 3:1 minimum contrast
- UI components and focus indicators: 3:1 minimum contrast

**Verified production combinations:**
- Charcoal (#342F2C) on Pearl White (#FFFFFF): approximately 13.2:1
- Rose Strong (#8B5E6C) on Pearl White (#FFFFFF): approximately 5.36:1
- Rose Strong (#8B5E6C) on Blush (#F8EEEA): approximately 4.70:1
- MVQueen Gold (#C7AD86) on Charcoal (#342F2C): approximately 6.14:1
- Gold Strong (#876F50) on Soft Cream (#FFFCF8): approximately 4.65:1
- Mink Text (#786D68) on Pearl White (#FFFFFF): approximately 5.02:1
- Charcoal (#342F2C) on Soft Cream (#FFFCF8): approximately 12.9:1

Decorative Soft Rose and Gold should not be used for small text on light backgrounds unless paired with their stronger accessibility token.

---

## Status

Color System — **Active**

All colors approved and deployment-ready. Update Shopify theme CSS variables immediately upon store setup.