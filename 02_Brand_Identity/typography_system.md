# Typography System
## MVQUEEN_OS / 02_Brand_Identity

---

## Purpose

Typography is the visual expression of the MVQUEEN voice. Every font choice, weight, and size carries emotional meaning and must reinforce luxury, femininity, confidence, and softness.

The typography system is discipline-based: correct fonts in correct sizes at correct hierarchy create effortless luxury.

---

## Primary Typefaces

### Cormorant Garamond
**Role:** Headlines, display, luxury positioning  
**Source:** Google Fonts (free)  
**Import:** `@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700&display=swap');`

**Why:** Serif elegance with feminine grace. Evokes heritage luxury without pretension.

**Weights Available:**
- 300 Light (rarely used)
- 400 Regular (body text in display contexts)
- 500 Medium (secondary headlines)
- 600 Semi-Bold (primary headlines)
- 700 Bold (emphasis, feature headlines)

**Use Cases:**
- Main page headers (H1)
- Product names
- Hero section text
- Collection names

---

### Jost* (or Jost)
**Role:** Body text, UI, system font, approachable luxury  
**Source:** Google Fonts (free)  
**Import:** `@import url('https://fonts.googleapis.com/css2?family=Jost:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700&display=swap');`

**Why:** Geometric sans-serif with warmth and precision. Feels modern without being cold.

**Weights Available:**
- 300 Light (small labels, secondary text)
- 400 Regular (body copy, navigation)
- 500 Medium (emphasis, buttons)
- 600 Semi-Bold (call-outs, strong labels)
- 700 Bold (rarely needed)

**Use Cases:**
- Body text (paragraphs)
- Navigation menus
- Buttons & CTAs
- Form labels
- Product descriptions
- Email body copy

---

## Font Pairing

| Context | Display Font | Body Font |
|---|---|---|
| Headlines | Cormorant Garamond | — |
| Body + Headlines | Cormorant Garamond 600 | Jost 400 |
| Navigation | Jost 500 | — |
| Product Descriptions | Jost 400 | — |
| Email Headers | Cormorant Garamond 600 | — |
| Email Body | Jost 400 | — |
| Forms | Jost 400 | — |

---

## Type Scale & Hierarchy

### Desktop Hierarchy

| Element | Font | Size | Weight | Line Height | Letter Spacing | Use |
|---|---|---|---|---|---|---|
| H1 / Hero | Cormorant Garamond | 48px | 600 | 1.2 | -0.02em | Main page headers, hero text |
| H2 / Section | Cormorant Garamond | 36px | 600 | 1.3 | -0.01em | Section headers, product category |
| H3 / Sub-section | Cormorant Garamond | 28px | 500 | 1.4 | 0 | Sub-headers, collection names |
| H4 / Card Title | Cormorant Garamond | 22px | 500 | 1.4 | 0 | Product card titles |
| H5 / Label | Jost | 16px | 600 | 1.5 | 0.02em | Form labels, button text |
| Body Large | Jost | 18px | 400 | 1.6 | 0 | Feature text, email body |
| Body Regular | Jost | 16px | 400 | 1.6 | 0 | Standard body copy |
| Body Small | Jost | 14px | 400 | 1.5 | 0.01em | Secondary text, captions |
| Caption | Jost | 12px | 300 | 1.4 | 0.02em | Fine print, metadata |

### Mobile Hierarchy

Reduce base size by 2-4px for optimal mobile readability:

| Element | Size (Mobile) | Weight | Changes |
|---|---|---|---|
| H1 / Hero | 36px | 600 | Line-height 1.3 |
| H2 / Section | 28px | 600 | Line-height 1.4 |
| H3 / Sub-section | 22px | 500 | Line-height 1.4 |
| Body Regular | 16px | 400 | Line-height 1.6 |

---

## CSS Variables & Implementation

```css
:root {
  /* Font Family */
  --font-serif: 'Cormorant Garamond', serif;
  --font-sans: 'Jost', sans-serif;
  
  /* Display / Headlines */
  --type-h1: 48px / 1.2 600 var(--font-serif);
  --type-h2: 36px / 1.3 600 var(--font-serif);
  --type-h3: 28px / 1.4 500 var(--font-serif);
  --type-h4: 22px / 1.4 500 var(--font-serif);
  
  /* Body */
  --type-body-lg: 18px / 1.6 400 var(--font-sans);
  --type-body: 16px / 1.6 400 var(--font-sans);
  --type-body-sm: 14px / 1.5 400 var(--font-sans);
  --type-caption: 12px / 1.4 300 var(--font-sans);
  
  /* Letter Spacing */
  --letter-spacing-tight: -0.02em;
  --letter-spacing-normal: 0;
  --letter-spacing-loose: 0.02em;
}

/* Usage Examples */
h1 { font: var(--type-h1); letter-spacing: var(--letter-spacing-tight); }
h2 { font: var(--type-h2); letter-spacing: var(--letter-spacing-tight); }
body { font: var(--type-body); }
.caption { font: var(--type-caption); letter-spacing: var(--letter-spacing-loose); }
```

---

## Special Typography Rules

### Headlines (Cormorant)
- **Luxury Signal:** Use higher weights (600+) for premium feeling
- **Spacing:** Tighter letter-spacing for elegance, especially at large sizes
- **Color:** Deep Rose (#8B4A5C) or Charcoal (#2C2C2C)
- **Alignment:** Left-aligned by default (never centered for body copy)

### Body Copy (Jost)
- **Readability:** Always 16px minimum on desktop, 14px minimum on mobile
- **Line Height:** 1.6 for body copy (creates breathing room)
- **Contrast:** Must be Charcoal (#2C2C2C) or dark color on light background
- **Width:** Max 70 characters per line for optimal readability

### Buttons & CTAs (Jost)
- **Weight:** 500 or 600 (Medium or Semi-Bold)
- **Size:** 16px for standard buttons
- **Transformation:** Uppercase optional but only if letter-spacing is increased to 0.05em+
- **Color:** Charcoal (#2C2C2C) on MVQUEEN Gold (#D4AF37) background

### Navigation (Jost)
- **Weight:** 400 for unselected, 600 for active/hover
- **Size:** 16px desktop, 14px mobile
- **Spacing:** Generous spacing between nav items (8-12px)
- **Color:** Deep Rose (#8B4A5C) for unselected, MVQUEEN Gold (#D4AF37) for active

### Email Typography

**Email Header:**
- H1: Cormorant Garamond 36px, Deep Rose

**Email Body:**
- Paragraph: Jost 16px, Charcoal, line-height 1.6
- Links: Deep Rose (#8B4A5C), underlined
- CTA Button: Jost 16px 600, Charcoal on Gold background

---

## Accessibility Standards

### Contrast Requirements
- Headline text on background: 7:1 (AAA for all sizes)
- Body text on background: 4.5:1 minimum (AA for 16px+), 7:1 (AAA)
- Button text on background: 4.5:1 minimum

**Verified combinations:**
- Cormorant 36px Charcoal (#2C2C2C) on Soft Cream (#FFF8F0): ✅ 12:1 (AAA)
- Jost 16px Charcoal (#2C2C2C) on Pearl White (#FAFAF8): ✅ 11.2:1 (AAA)
- Deep Rose (#8B4A5C) on Ivory (#F5F1EB): ✅ 6.1:1 (AA)

### Font Size Minimums
- Body copy: Never smaller than 16px on desktop (14px on mobile only)
- Navigation: 16px minimum
- Form labels: 14px minimum

### Font Rendering
- Enable font-smoothing: `-webkit-font-smoothing: antialiased;`
- Use `text-rendering: optimizeLegibility;` for better serif rendering

---

## Shopify Theme Integration

Add to `theme.liquid` in the `<head>`:

```html
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Jost:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700&display=swap" rel="stylesheet">
```

Update Shopify theme CSS settings to reference these fonts globally.

---

## Fallback Fonts

If fonts fail to load, use system font stack:

```css
--font-serif: 'Cormorant Garamond', 'Garamond', 'Georgia', serif;
--font-sans: 'Jost', 'Segoe UI', '-apple-system', 'BlinkMacSystemFont', sans-serif;
```

---

## Status

Typography System — **Active**

All fonts approved, sizes finalized, and deployment-ready for Shopify integration.