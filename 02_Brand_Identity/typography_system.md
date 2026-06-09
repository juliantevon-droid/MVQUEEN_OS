# 👑 MVQUEEN — Typography System
### The Type Reference

---

## What This File Is

This is not visual philosophy. That lives in the Brand Bible §16.
This is the working type system — font names, weights, size scales, pairing logic, platform rules, and every typographic decision made for MVQUEEN.

Every designer, developer, Shopify theme, email template, social graphic, and AI visual prompt pulls from this file.

---

## THE SYSTEM AT A GLANCE

| Role | Font | Weight | Use |
|---|---|---|---|
| Display / Hero | Cormorant Garamond | Light 300, Regular 400 | Headlines, campaign headers, logo adjacent |
| Display Italic | Cormorant Garamond | Light Italic 300i | Subheads, pull quotes, editorial moments |
| Body | Jost | Light 300, Regular 400 | All body copy, descriptions, UI text |
| Body Accent | Jost | Medium 500 | Emphasis, labels, nav, CTAs |
| Monospace / Detail | JetBrains Mono | Regular 400 | Hex codes, SKUs, technical specs only |

---

## PART 1 — TYPEFACES

### Primary Display — Cormorant Garamond

The brand's display font. Refined serif with Old Style proportions — elegant, feminine, literary. Carries softness and authority simultaneously.

Weights used: 300 Light, 400 Regular, 300i Light Italic, 400i Regular Italic
Google Fonts: Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400

Never use: Bold (600+), all-caps in large sizes, below 14px

### Primary Body — Jost

Geometric sans-serif with humanist proportions. Clean, modern, readable, warm.

Weights used: 200 Extra Light, 300 Light, 400 Regular, 500 Medium
Google Fonts: Jost:wght@200;300;400;500

Never use: 700 Bold or heavier, in display sizes, italic for emotional emphasis (use Cormorant italic instead)

### Miss.Princess Display Alternative
Playfair Display — Italic 400i. For campaign headers and social display copy. Never used in MVQUEEN primary contexts.

---

## PART 2 — SIZE SCALE

### Desktop (base: 16px)
Display XL: 72–96px / Cormorant 300 / Hero headlines
Display L: 48–64px / Cormorant 300–400 / Section heroes
Display M: 36–42px / Cormorant 400 / Page titles
Display S: 28–32px / Cormorant 400 / Sub-section headers
Subhead: 20–24px / Cormorant 400i / Pull quotes
Body L: 18–20px / Jost 300 / Long-form copy
Body: 16px / Jost 300–400 / Standard copy
Body S: 14px / Jost 400 / Captions, metadata
Label: 11–12px / Jost 500 / Navigation, tags
Micro: 10px / Jost 400–500 / Legal, footnotes

### Mobile (base: 15px)
Display XL: 42–52px | Display L: 32–38px | Display M: 26–30px
Body: 15px | Label: 11px minimum

---

## PART 3 — PAIRING PATTERNS

Pattern A — Editorial: Cormorant 300 headline / Cormorant 400i sub / Jost 300 body / Jost 500 label
Pattern B — Product Page: Cormorant 400 name / Cormorant 300i tagline / Jost 300 description / Jost 500 price
Pattern C — Campaign: Cormorant 300 large / Jost 200 small wide-spaced / Cormorant 300i or Jost 500 CTA
Pattern D — Navigation: Jost 400 13px nav / Jost 500 13px active / Jost 500 11px uppercase labels

---

## PART 4 — TYPOGRAPHIC RULES

Letter-spacing: Display -0.01em | MVQUEEN brand name 0.18em | Nav labels 0.12–0.18em | Body 0.01em | Overlines 0.25–0.3em

Line height: Display 1.0–1.1 | Sub-headers 1.2–1.3 | Body 1.6–1.75 | Captions 1.4 | Product descriptions 1.7

Text colors: Primary body = Espresso #3B2314 | Secondary = Charcoal #4A4240 | Accent/links = Dusty Rose #C9968A | Reversed = Ivory #FAF6F0

Uppercase: Jost only. Minimum 0.15em letter-spacing. Maximum 4–5 words.

System font fallbacks:
Cormorant → 'Palatino Linotype', 'Book Antiqua', Palatino, serif
Jost → 'Century Gothic', 'Trebuchet MS', sans-serif

---

## QUICK REFERENCE — FONT LOAD CODE

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=Jost:wght@200;300;400;500&display=swap" rel="stylesheet">
```

```css
:root {
  --font-display: 'Cormorant Garamond', 'Palatino Linotype', serif;
  --font-body: 'Jost', 'Century Gothic', sans-serif;
  --font-size-base: 16px;
  --line-height-body: 1.7;
  --letter-spacing-label: 0.15em;
  --letter-spacing-brand: 0.18em;
}
```

*Pairs with color_system.md, brand_rules.md, and visual_direction.md.*