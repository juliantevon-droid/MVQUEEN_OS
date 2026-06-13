# 👑 MVQUEEN TYPOGRAPHY SYSTEM
*The complete type language of the MVQUEEN brand ecosystem*

---

## PURPOSE

Typography is tone made visible. Before she reads a word, she feels the font. The weight, the spacing, the curve of every letter communicates whether a brand feels luxurious or cheap, warm or cold, trustworthy or disposable.

MVQUEEN typography must feel the way the brand feels: elegant, feminine, warm, confident, and elevated.

---

## THE MVQUEEN TYPE PHILOSOPHY

MVQUEEN typography lives at the intersection of:
- **Serif elegance** — the timeless luxury of editorial fashion
- **Modern femininity** — clean lines that feel current, not dated
- **Warmth** — never cold, never mechanical, never stark

Three-tier hierarchy:
1. **Display / Editorial** — for headlines, hero text, campaign statements
2. **Body / Voice** — for product descriptions, copy, email content
3. **Utility / Accent** — for labels, tags, UI elements, captions

---

## TIER 1 — DISPLAY TYPOGRAPHY

### PRIMARY DISPLAY: Cormorant Garamond
**Style:** Serif / High Fashion Editorial
**Weight range:** Light (300), Regular (400), Italic, Semi-Bold (600)
**Source:** Google Fonts (free)

Use for: Homepage hero headlines, campaign taglines, section titles, email newsletter headers, packaging headlines, brand statement overlays.

Size guidelines:
- Hero/Banner: 52–80px (desktop), 36–52px (mobile)
- Section headers: 36–48px
- Campaign overlays: 40–72px

Tracking: 0.05em–0.15em — always slightly open, never compressed
Line height: 1.1–1.3 — tight but breathing

---

### DISPLAY VARIANT: Playfair Display
**Style:** Serif / Classic Luxury
**Weight:** Regular, Italic, Bold
**Source:** Google Fonts (free)

Use for: Sale/campaign headline banners, product category page headers, email callout text, social media quote graphics.

---

## TIER 2 — BODY TYPOGRAPHY

### PRIMARY BODY: Jost
**Style:** Geometric Sans-Serif / Modern Clean
**Weight range:** Light (300), Regular (400), Medium (500)
**Source:** Google Fonts (free)

Use for: All product description copy, email body text, website body paragraphs, blog content, captions, customer-facing communications.

Size guidelines:
- Body text: 16–18px (website), 14–16px (mobile)
- Large body / lead paragraphs: 18–22px
- Small print / footnotes: 12–13px

Tracking: 0.01em–0.03em
Line height: 1.6–1.8

---

## TIER 3 — UTILITY / ACCENT TYPOGRAPHY

### PRIMARY UTILITY: Jost Medium / ALL CAPS
Tracking: 0.12em–0.20em
Use: Navigation menus, product tags, category labels, CTA button text, form labels

Example: SHOP NOW · NEW ARRIVALS · BEAUTY · FRAGRANCE

### ACCENT: Cormorant Garamond Italic
Use: Pull quotes, testimonials, brand signature moments, closing statements in emails
Size: 18–24px

---

## TYPOGRAPHIC HIERARCHY — WEBSITE

| Element | Font | Weight | Size | Tracking |
|---|---|---|---|---|
| Hero Headline | Cormorant Garamond | Light Italic | 64–80px | 0.08em |
| Section Header | Cormorant Garamond | Regular | 40–52px | 0.05em |
| Subheader | Jost | Medium | 18–22px | 0.10em caps |
| Body Text | Jost | Light / Regular | 16–18px | 0.02em |
| Product Title | Cormorant Garamond | Regular | 24–32px | 0.04em |
| Product Price | Jost | Medium | 16–18px | 0.05em |
| CTA Button | Jost | Medium | 13–15px | 0.18em caps |
| Caption / Label | Jost | Light | 12–13px | 0.10em caps |
| Pull Quote | Cormorant Garamond | Italic | 20–26px | 0.03em |
| Navigation | Jost | Medium | 13–14px | 0.15em caps |

---

## TYPE RULES — NON-NEGOTIABLE

### Always
- Use Cormorant Garamond for all headline and display moments
- Pair serif headlines with Jost body text
- Use open tracking for all caps text
- Maintain generous line height in body copy
- Keep hierarchy clear: one dominant headline, one body, one utility

### Never
- Mix more than 3 fonts in one layout
- Use cold sans-serifs like Roboto or Open Sans
- Use all-caps body text
- Use compressed tracking on display text
- Center-align long body paragraphs

---

## FONT STACK (CSS)

```css
/* Display */
font-family: 'Cormorant Garamond', 'Playfair Display', Georgia, serif;

/* Body */
font-family: 'Jost', 'Lato', Arial, sans-serif;

/* Utility */
font-family: 'Jost', Arial, sans-serif;
letter-spacing: 0.15em;
text-transform: uppercase;
```

## GOOGLE FONTS IMPORT

```html
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Jost:wght@300;400;500&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
```

---

*Typography is the brand's first impression after color. Every font choice must honor the MVQUEEN promise: to make her feel elegant, seen, and luxuriously at home.*
