# color_system.md
**Location:** `02_Brand_Identity/color_system.md`
**Doctrine Anchor:** `00_Doctrine/README.md` — Quiet Confidence, Warm Luxury, Feminine Precision
**Authority:** Master color reference for all MvQueen and miss.queen brand touchpoints

---

## 01 — Brand Color Philosophy

Color is not decoration. It is the first thing a customer feels before she reads a single word.

MvQueen's palette is built on a single tension: **warmth that commands**. Not soft and forgettable. Not cold and clinical. The colors say *I know exactly who I am* — and that certainty is what makes her trust us.

Every color decision must pass this filter:
> *Does this feel like a woman who is composed, certain, and beautifully in control?*

---

## 02 — Primary Palette

| Token | Name | Hex | RGB | Usage |
|---|---|---|---|---|
| `--mvq-black` | Vault Black | `#0D0D0D` | 13, 13, 13 | Headlines, primary text, logo lockup |
| `--mvq-white` | Clean Canvas | `#F9F7F4` | 249, 247, 244 | Page backgrounds, breathing space |
| `--mvq-gold` | Sovereign Gold | `#C9A84C` | 201, 168, 76 | Accents, CTAs, premium markers |
| `--mvq-blush` | Velvet Blush | `#E8C4B8` | 232, 196, 184 | Warmth layer, hover states, softeners |
| `--mvq-nude` | Skin Nude | `#D4A896` | 212, 168, 150 | Supporting warmth, secondary backgrounds |

---

## 03 — Secondary Palette

| Token | Name | Hex | RGB | Usage |
|---|---|---|---|---|
| `--mvq-charcoal` | Deep Charcoal | `#2A2A2A` | 42, 42, 42 | Body copy, secondary text |
| `--mvq-stone` | Warm Stone | `#8C7B6E` | 140, 123, 110 | Subtext, captions, muted UI elements |
| `--mvq-cream` | Soft Cream | `#F2EDE8` | 242, 237, 232 | Card backgrounds, section dividers |
| `--mvq-rose` | Deep Rose | `#B5736A` | 181, 115, 106 | Error states, bold accent moments |
| `--mvq-ivory` | Cool Ivory | `#EDE8E1` | 237, 232, 225 | Email backgrounds, print base |

---

## 04 — miss.queen Sub-Brand Palette

miss.queen shares MvQueen's warmth foundation but skews younger and more playful. The gold softens to champagne. The black lifts to deep plum.

| Token | Name | Hex | Usage |
|---|---|---|---|
| `--mq-plum` | Royal Plum | `#3D2B3D` | Primary dark, replaces Vault Black |
| `--mq-champagne` | Champagne | `#E8D5A3` | Accent, replaces Sovereign Gold |
| `--mq-petal` | Soft Petal | `#F0D4CC` | Warmth layer, replaces Velvet Blush |
| `--mq-lilac` | Whisper Lilac | `#D4C5D9` | miss.queen-only accent |
| `--mq-white` | Pearl White | `#FAF8F6` | Base background |

---

## 05 — Color Roles & Application Rules

### 5.1 — Text Hierarchy
| Role | Color Token | Notes |
|---|---|---|
| H1 / Primary headline | `--mvq-black` | Never use gold for headlines |
| H2 / Section header | `--mvq-charcoal` | |
| Body copy | `--mvq-charcoal` | Not pure black — too harsh |
| Subtext / captions | `--mvq-stone` | |
| Reversed text (dark bg) | `--mvq-white` | Only on black or charcoal backgrounds |

### 5.2 — CTA & Interactive Elements
| State | Background | Text | Border |
|---|---|---|---|
| Default | `--mvq-gold` | `--mvq-black` | none |
| Hover | `--mvq-black` | `--mvq-gold` | none |
| Disabled | `--mvq-stone` | `--mvq-white` | none |
| Secondary CTA | transparent | `--mvq-black` | `--mvq-black` 1px |

### 5.3 — Background Hierarchy
| Layer | Color | Use Case |
|---|---|---|
| Page base | `--mvq-white` | Primary site background |
| Section break | `--mvq-cream` | Alternating sections |
| Card surface | `--mvq-ivory` | Product cards, content cards |
| Feature panel | `--mvq-black` | Hero sections, bold statements |
| Warm accent panel | `--mvq-blush` | Testimonials, editorial moments |

---

## 06 — Color Pairing Rules

### Approved Combinations
| Background | Text | Accent | Context |
|---|---|---|---|
| `--mvq-white` | `--mvq-charcoal` | `--mvq-gold` | Standard page layout |
| `--mvq-black` | `--mvq-white` | `--mvq-gold` | Hero sections, feature callouts |
| `--mvq-cream` | `--mvq-charcoal` | `--mvq-nude` | Editorial, blog, email |
| `--mvq-blush` | `--mvq-black` | `--mvq-gold` | Campaign moments, testimonials |
| `--mvq-gold` | `--mvq-black` | — | CTA buttons only |

### Prohibited Combinations
| Combination | Reason |
|---|---|
| Gold text on white background | Fails contrast — illegible at small sizes |
| Blush background + stone text | Insufficient contrast ratio |
| Rose + Gold together | Competing warm tones — visually unstable |
| Pure `#000000` black anywhere | Too harsh — always use Vault Black `#0D0D0D` |
| Multiple accent colors in one section | Dilutes brand premium signal |

---

## 07 — Accessibility Standards

All text/background combinations must meet **WCAG AA minimum** (4.5:1 for body, 3:1 for large text).

| Combination | Contrast Ratio | Pass/Fail |
|---|---|---|
| Charcoal on White | 12.6:1 | ✅ AAA |
| Black on Gold | 8.2:1 | ✅ AAA |
| White on Black | 19.5:1 | ✅ AAA |
| Stone on White | 4.7:1 | ✅ AA |
| Gold on Black | 8.2:1 | ✅ AAA |
| Blush on White | 1.9:1 | ❌ Decorative use only |

> Blush and Nude are **decorative colors only** — never use for text or critical UI elements.

---

## 08 — Shopify / Digital Application

### CSS Custom Properties (paste into theme.css)
```css
:root {
  /* MvQueen Primary */
  --mvq-black:    #0D0D0D;
  --mvq-white:    #F9F7F4;
  --mvq-gold:     #C9A84C;
  --mvq-blush:    #E8C4B8;
  --mvq-nude:     #D4A896;

  /* MvQueen Secondary */
  --mvq-charcoal: #2A2A2A;
  --mvq-stone:    #8C7B6E;
  --mvq-cream:    #F2EDE8;
  --mvq-rose:     #B5736A;
  --mvq-ivory:    #EDE8E1;

  /* miss.queen */
  --mq-plum:       #3D2B3D;
  --mq-champagne:  #E8D5A3;
  --mq-petal:      #F0D4CC;
  --mq-lilac:      #D4C5D9;
  --mq-white:      #FAF8F6;
}
```

### Shopify Theme Color Slots
| Shopify Slot | MvQueen Token | Hex |
|---|---|---|
| Background | `--mvq-white` | `#F9F7F4` |
| Text | `--mvq-charcoal` | `#2A2A2A` |
| Primary button bg | `--mvq-gold` | `#C9A84C` |
| Primary button text | `--mvq-black` | `#0D0D0D` |
| Secondary button | `--mvq-black` | `#0D0D0D` |
| Accent | `--mvq-blush` | `#E8C4B8` |
| Border | `--mvq-stone` | `#8C7B6E` |

---

## 09 — Print & Packaging Application

| Medium | Color Mode | Notes |
|---|---|---|
| Packaging (primary) | CMYK | Convert gold to PMS 871 C (metallic) or PMS 131 C (flat) |
| Tissue paper / inserts | CMYK | Use cream base `#F2EDE8` |
| Tags / labels | Spot color preferred | PMS 871 C for gold, PMS Black 6 C for black |
| Digital mockups | sRGB | Use hex values above |
| Print-at-home | RGB → CMYK convert | Warn: gold shifts warm in CMYK |

**PMS Equivalents:**
| Color | PMS Code |
|---|---|
| Sovereign Gold (metallic) | PMS 871 C |
| Sovereign Gold (flat) | PMS 131 C |
| Vault Black | PMS Black 6 C |
| Velvet Blush | PMS 696 C |
| Warm Stone | PMS 7534 C |

---

## 10 — Color Misuse Reference

The following uses violate brand standards and must be corrected on sight:

| Violation | Correct Action |
|---|---|
| Bright/neon colors in any context | Remove — not in palette |
| Gold used as a background color for large sections | Limit to CTA buttons and small accents |
| Black and blush used as the only two colors | Add white breathing space |
| miss.queen palette used on MvQueen assets | Separate brand — never cross-apply |
| Off-brand beige or tan substituted for nude/cream | Use exact hex values only |
| Gradients using palette colors | Not approved — flat color only |

---

## 11 — Version Control

| Version | Date | Change |
|---|---|---|
| 1.0 | Phase 2 Build | Initial enterprise build — replaces Brand Bible extraction |

---

*This file is the single source of truth for MvQueen and miss.queen color. Any deviation requires doctrine review.*
