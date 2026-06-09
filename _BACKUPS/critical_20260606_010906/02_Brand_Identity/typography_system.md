# typography_system.md
**Location:** `02_Brand_Identity/typography_system.md`
**Doctrine Anchor:** `00_Doctrine/README.md` — Quiet Confidence, Warm Luxury, Feminine Precision
**Authority:** Master typography reference for all MvQueen and miss.queen brand touchpoints

---

## 01 — Typography Philosophy

Typography is the brand's voice made visible. Before tone, before copy — the typeface is already speaking.

MvQueen's type system is built around a single idea: **legible luxury**. Fonts that feel elevated but never pretentious. Editorial but never cold. The type system must work in a Shopify product description, an Instagram Story, a printed insert, and a Canva template — and feel like the same brand in all four.

Every type decision must pass this filter:
> *Does this feel composed, precise, and worth a second look?*

---

## 02 — Primary Typefaces

### 2.1 — Headline Font: Cormorant Garamond
| Property | Value |
|---|---|
| Family | Cormorant Garamond |
| Source | Google Fonts (free) |
| Style | Serif — editorial, high fashion |
| Weights in use | Light (300), Regular (400), SemiBold (600) |
| Use cases | H1, campaign headlines, hero text, product names |
| Character | Elevated. Quiet authority. The font of a woman who doesn't need to be loud. |

**Do not use:** Bold (700) or Black weight — too heavy for brand positioning.

---

### 2.2 — Body Font: DM Sans
| Property | Value |
|---|---|
| Family | DM Sans |
| Source | Google Fonts (free) |
| Style | Sans-serif — clean, modern, readable |
| Weights in use | Regular (400), Medium (500) |
| Use cases | Body copy, product descriptions, UI text, captions |
| Character | Precise. Effortless. Gets out of the way of the message. |

**Do not use:** Bold (700) in body copy — use Medium (500) for emphasis instead.

---

### 2.3 — Accent Font: Italiana (or Playfair Display Italic)
| Property | Value |
|---|---|
| Family | Italiana / Playfair Display Italic |
| Source | Google Fonts (free) |
| Style | Display serif — decorative, editorial |
| Weights in use | Regular only |
| Use cases | Pull quotes, section labels, brand moments, packaging overlays |
| Character | Expressive. For moments where the brand speaks directly — not for paragraphs. |

**Use sparingly.** One accent font moment per design unit maximum.

---

## 03 — miss.queen Sub-Brand Typography

miss.queen shares the body and accent fonts but swaps the headline font for something slightly more playful.

| Role | Font | Notes |
|---|---|---|
| Headline | **Josefin Sans** (Light 300, Regular 400) | Geometric, younger energy — replaces Cormorant |
| Body | DM Sans | Same as MvQueen |
| Accent | Playfair Display Italic | Same as MvQueen |

---

## 04 — Type Scale

### Desktop Scale
| Level | Size | Weight | Line Height | Letter Spacing | Font |
|---|---|---|---|---|---|
| H1 — Hero | 64px | Light 300 | 1.1 | -0.02em | Cormorant Garamond |
| H2 — Section | 44px | Regular 400 | 1.2 | -0.01em | Cormorant Garamond |
| H3 — Subsection | 32px | SemiBold 600 | 1.3 | 0 | Cormorant Garamond |
| H4 — Label | 18px | Medium 500 | 1.4 | 0.05em | DM Sans (uppercase) |
| Body Large | 18px | Regular 400 | 1.6 | 0 | DM Sans |
| Body Standard | 16px | Regular 400 | 1.6 | 0 | DM Sans |
| Caption / Fine | 13px | Regular 400 | 1.5 | 0.02em | DM Sans |
| Accent / Pull | 28px | Regular 400 | 1.3 | 0.01em | Italiana |

### Mobile Scale
| Level | Size | Notes |
|---|---|---|
| H1 — Hero | 40px | Reduce tracking to -0.01em |
| H2 — Section | 30px | |
| H3 — Subsection | 24px | |
| Body | 16px | No change |
| Caption | 12px | |

---

## 05 — Typography Rules

### 5.1 — Hierarchy Rules
- **Never mix two serif display fonts** in one layout — choose Cormorant OR Italiana per section
- H4 labels are **always uppercase** with 0.05em letter spacing
- Body copy is **never centered** at paragraph length — centered only for 1–2 line callouts
- Product names use **Cormorant Garamond SemiBold** — not DM Sans

### 5.2 — Spacing Rules
| Property | Value |
|---|---|
| Paragraph spacing | 0.75em below each paragraph |
| H1 → body gap | 24px minimum |
| H2 → body gap | 16px minimum |
| Section padding (desktop) | 80px top/bottom |
| Section padding (mobile) | 48px top/bottom |

### 5.3 — Line Length (Readability)
| Context | Max Characters Per Line |
|---|---|
| Body copy (desktop) | 65–75 characters |
| Body copy (mobile) | 40–50 characters |
| Pull quotes | 40–55 characters |
| Product descriptions | 60–70 characters |

Lines longer than 80 characters break reading rhythm — always constrain column width.

### 5.4 — Color + Type Rules
| Text Type | Approved Colors |
|---|---|
| H1, H2, H3 | `--mvq-black`, `--mvq-white` (on dark bg) |
| Body | `--mvq-charcoal` |
| Captions / subtext | `--mvq-stone` |
| Accent / pull quotes | `--mvq-black`, `--mvq-gold` (sparingly) |
| CTA button text | `--mvq-black` on gold, `--mvq-white` on black |

**Never use:** Gold for long-form text. Stone for headlines. Blush or Nude for any text.

---

## 06 — Shopify / Digital Implementation

### Google Fonts Import (paste into theme.liquid `<head>`)
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=DM+Sans:wght@400;500&family=Italiana&display=swap" rel="stylesheet">
```

### CSS Typography System
```css
/* Base */
body {
  font-family: 'DM Sans', sans-serif;
  font-size: 16px;
  font-weight: 400;
  line-height: 1.6;
  color: var(--mvq-charcoal);
}

/* Headlines */
h1 {
  font-family: 'Cormorant Garamond', serif;
  font-size: 64px;
  font-weight: 300;
  line-height: 1.1;
  letter-spacing: -0.02em;
}

h2 {
  font-family: 'Cormorant Garamond', serif;
  font-size: 44px;
  font-weight: 400;
  line-height: 1.2;
}

h3 {
  font-family: 'Cormorant Garamond', serif;
  font-size: 32px;
  font-weight: 600;
  line-height: 1.3;
}

h4 {
  font-family: 'DM Sans', sans-serif;
  font-size: 18px;
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

/* Accent */
.accent-text {
  font-family: 'Italiana', serif;
  font-size: 28px;
  font-weight: 400;
}

/* Caption */
.caption {
  font-size: 13px;
  color: var(--mvq-stone);
  letter-spacing: 0.02em;
}
```

---

## 07 — Email Typography

Email clients do not reliably load custom fonts. Use this fallback stack:

| Role | Font Stack |
|---|---|
| Headlines | `'Cormorant Garamond', Georgia, 'Times New Roman', serif` |
| Body | `'DM Sans', Helvetica, Arial, sans-serif` |
| Fallback-safe body | `Georgia, serif` for headline; `Arial, sans-serif` for body |

**Email type sizes:**
| Element | Size |
|---|---|
| Headline | 36px |
| Subheadline | 24px |
| Body | 16px |
| Footer / legal | 12px |

---

## 08 — Print & Packaging Typography

| Element | Font | Size | Notes |
|---|---|---|---|
| Product name (packaging) | Cormorant Garamond Light | 24–36pt | Depends on surface area |
| Tagline | Italiana Regular | 14–18pt | |
| Body / ingredients / care | DM Sans Regular | 9–11pt | Minimum 9pt for legibility |
| Legal / fine print | DM Sans Regular | 7–8pt | |
| Brand logo wordmark | See logo system | — | Never recreate from fonts |

---

## 09 — Prohibited Uses

| Violation | Reason |
|---|---|
| System fonts (Arial, Times) as primary | Off-brand — always load Google Fonts |
| Script or handwriting fonts | Not in brand system |
| Cormorant Bold/Black weight | Too heavy — brand voice is light, not loud |
| All-caps in body copy | Breaks reading flow |
| Tracking/letter-spacing on body text | Disrupts readability at paragraph length |
| Two decorative fonts in one layout | Visual noise — one accent font per unit |
| Font sizes below 12px on web | Accessibility violation |

---

## 10 — Version Control

| Version | Date | Change |
|---|---|---|
| 1.0 | Phase 2 Build | Initial enterprise build — replaces Brand Bible extraction |

---

*This file is the single source of truth for MvQueen and miss.queen typography. Any deviation requires doctrine review.*
