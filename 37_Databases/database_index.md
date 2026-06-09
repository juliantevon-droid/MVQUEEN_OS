# Database Index
## MVQUEEN_OS / 37_Databases

---

## Purpose

Documents all structured data stores within the MVQUEEN ecosystem — product databases, customer segments, keyword databases, and content libraries.

---

## Database Registry

| Database | Format | Location | Purpose |
|---|---|---|---|
| Product Catalog | Shopify / CSV | Shopify Admin | All active products |
| Keyword Database | Markdown / CSV | `05_SEO_And_Content` | SEO targeting |
| Customer Segments | Klaviyo | Klaviyo | Email targeting |
| Content Library | Markdown | `12_Content_Assets` | Reusable content |
| Hook Library | Markdown | `06_Tone_And_Voice` | Opening lines |
| CTA Library | Markdown | `06_Tone_And_Voice` | Call-to-action copy |
| Ecosystem Index | JSON | `_ecosystem_index.json` | OS file map |

---

## Data Standards

- All CSV files use UTF-8 encoding
- Markdown databases use consistent table formatting
- JSON files must be validated before use
- No PII stored in OS — customer data lives in Klaviyo/Shopify only

---

## Status
Active
