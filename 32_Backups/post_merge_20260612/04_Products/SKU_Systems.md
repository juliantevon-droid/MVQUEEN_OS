# 👑 MVQUEEN — SKU Systems
### The Inventory & Product Code Reference

---

## What This File Is

SKUs (Stock Keeping Units) are the internal language of the MVQUEEN catalog. Every product, every variant, every bundle has a unique SKU that powers inventory management, Shopify operations, fulfillment, reporting, and reordering.

This file defines the SKU structure, naming conventions, variant codes, and the operational rules that keep the catalog organized at scale. SKUs are internal only — they never appear in customer-facing copy.

---

## THE SKU PHILOSOPHY

A good SKU system is invisible when working correctly and obvious when something goes wrong. MVQUEEN SKUs are built for clarity at a glance — any team member or system reading a SKU should be able to understand the brand, category, product, and variant without a lookup table.

---

## PART 1 — THE SKU STRUCTURE

Every MVQUEEN SKU follows this format:

```
[BRAND]-[CATEGORY]-[PRODUCT NUMBER]-[VARIANT CODE]
```

**Full example:** `MVQ-SKC-001-30ML`
- `MVQ` = MVQUEEN brand
- `SKC` = Skincare category
- `001` = Product number 001 in skincare
- `30ML` = 30ml size variant

---

## PART 2 — BRAND CODES

| Code | Brand |
|---|---|
| `MVQ` | MVQUEEN |
| `MXP` | Miss.Princess |

**Rule:** Every SKU begins with the brand code. MVQUEEN and Miss.Princess products never share SKU ranges — they have entirely separate numbering systems.

---

## PART 3 — CATEGORY CODES

### MVQUEEN Category Codes

| Code | Category | Examples |
|---|---|---|
| `SKC` | Skincare | Serums, moisturizers, cleansers, masks, toners, eye cream |
| `FRG` | Fragrance | EDPs, EDTs, body sprays, fragrance oils |
| `FSH` | Fashion | Dresses, tops, bottoms, outerwear, co-ords |
| `HRC` | Haircare | Shampoo, conditioner, masks, oils, sprays |
| `BEA` | Beauty | Foundation, blush, mascara, lip products, primer |
| `LFS` | Lifestyle | Candles, diffusers, body oil, home products |
| `GFT` | Gift Sets | Curated bundles and gift-ready sets |
| `ACC` | Accessories | Jewelry, bags, scarves, hair accessories |

### Miss.Princess Category Codes

| Code | Category |
|---|---|
| `BEA` | Beauty (same code, different brand prefix) |
| `SKC` | Skincare |
| `FRG` | Fragrance (mini and travel sizes) |
| `ACC` | Accessories |
| `LFS` | Lifestyle |
| `GFT` | Gift Sets |

**Full Miss.Princess example:** `MXP-BEA-001-RSE` = Miss.Princess Beauty Product 001, Rose colorway

---

## PART 4 — PRODUCT NUMBERING

Products are numbered sequentially within each brand-category combination, starting at `001`.

```
MVQ-SKC-001 = First MVQUEEN skincare product added to catalog
MVQ-SKC-002 = Second MVQUEEN skincare product
MVQ-SKC-003 = Third MVQUEEN skincare product
...
MVQ-FRG-001 = First MVQUEEN fragrance product
MVQ-FRG-002 = Second MVQUEEN fragrance product
```

**Rules:**
- Numbers are assigned at Stage 03 of the Product Framework (Naming & Positioning)
- Numbers are never reused — if a product is retired, its number is retired with it
- Numbering gaps are acceptable — no need to renumber when a product is retired
- Miss.Princess numbering starts at 001 independently for each category

---

## PART 5 — VARIANT CODES

Variants distinguish different sizes, colors, or formulas of the same product.

### Size / Volume Variants

| Code | Meaning |
|---|---|
| `5ML` | 5 millilitres |
| `10ML` | 10 millilitres |
| `15ML` | 15 millilitres |
| `30ML` | 30 millilitres |
| `50ML` | 50 millilitres |
| `100ML` | 100 millilitres |
| `150ML` | 150 millilitres |
| `200ML` | 200 millilitres |
| `250ML` | 250 millilitres |
| `30G` | 30 grams |
| `50G` | 50 grams |
| `100G` | 100 grams |
| `200G` | 200 grams |
| `1SZ` | One size (fashion, accessories) |
| `SET` | Set or bundle (no single size) |

### Size Variants (Fashion)

| Code | Size |
|---|---|
| `XXS` | Extra extra small |
| `XS` | Extra small |
| `SM` | Small |
| `MD` | Medium |
| `LG` | Large |
| `XL` | Extra large |
| `XXL` | Extra extra large |

### Colorway / Shade Variants

| Code | Color |
|---|---|
| `IVR` | Ivory / Warm Ivory |
| `BLS` | Blush / Soft Blush |
| `RSE` | Rose / Dusty Rose |
| `TPE` | Taupe / Warm Taupe |
| `ESP` | Espresso |
| `GLD` | Gold / Champagne Gold |
| `CHR` | Charcoal |
| `BLK` | Black (fashion only — never primary) |
| `NDE` | Nude (lip products) |
| `BRY` | Berry (lip products) |
| `PLM` | Plum (lip products) |
| `PPK` | Petal Pink (Miss.Princess) |
| `LIL` | Lilac (Miss.Princess) |
| `RQZ` | Rose Quartz (Miss.Princess) |

### Formula Variants (where applicable)

| Code | Formula Type |
|---|---|
| `OIL` | Oil formula |
| `CRM` | Cream formula |
| `GEL` | Gel formula |
| `SRM` | Serum formula |
| `MST` | Mist / spray formula |
| `PWD` | Powder formula |
| `LQD` | Liquid formula |

---

## PART 6 — FULL SKU EXAMPLES

| SKU | Decoded |
|---|---|
| `MVQ-SKC-001-30ML` | MVQUEEN Skincare Product 001 (The Glow Serum), 30ml |
| `MVQ-SKC-001-50ML` | MVQUEEN Skincare Product 001 (The Glow Serum), 50ml |
| `MVQ-FRG-001-50ML` | MVQUEEN Fragrance Product 001 (Velvet Hour EDP), 50ml |
| `MVQ-FRG-001-10ML` | MVQUEEN Fragrance Product 001 (Velvet Hour EDP), 10ml travel |
| `MVQ-FSH-001-SM` | MVQUEEN Fashion Product 001 (The Arrival Dress), Small |
| `MVQ-FSH-001-IVR-SM` | MVQUEEN Fashion Product 001, Ivory colorway, Small |
| `MVQ-FSH-001-RSE-MD` | MVQUEEN Fashion Product 001, Rose colorway, Medium |
| `MVQ-BEA-001-NDE` | MVQUEEN Beauty Product 001 (Foundation), Nude shade |
| `MVQ-GFT-001-SET` | MVQUEEN Gift Set 001 (The Morning Ritual Set) |
| `MXP-BEA-001-PPK` | Miss.Princess Beauty Product 001 (Petal Glow Gloss), Petal Pink |
| `MXP-BEA-001-RSE` | Miss.Princess Beauty Product 001 (Petal Glow Gloss), Rose |
| `MXP-ACC-001-1SZ` | Miss.Princess Accessory Product 001 (Hair Clip Set), One Size |

---

## PART 7 — SHOPIFY SKU IMPLEMENTATION

**Where SKUs live in Shopify:**
- Product page → Variants → SKU field
- Every variant of every product has its own unique SKU entered
- SKU field is mandatory — no product goes live without a complete SKU

**Shopify inventory tracking:**
- Inventory tracked by SKU at the variant level
- Low stock threshold: 10 units triggers reorder alert
- Out of stock behavior: "Continue selling" OFF — show as sold out
- Sold-out products: page remains live with "Notify me when available" email capture

**Barcode field:**
If physical barcodes are used for wholesale or retail: barcode field in Shopify is separate from SKU. SKU remains the internal system code. Barcode is the EAN/UPC for external systems.

---

## PART 8 — BUNDLE / GIFT SET SKUs

Gift sets and bundles get their own SKU — they are not just a combination of individual product SKUs.

**Bundle SKU format:** `[BRAND]-GFT-[NUMBER]-SET`

**Example:** `MVQ-GFT-001-SET` = MVQUEEN Gift Set 001 (The Morning Ritual Set)

**Bundle component tracking:**
When a bundle sells, Shopify deducts inventory from each component SKU. This requires the bundle to be set up as a bundle in Shopify (using a bundle app or multi-origin inventory management). Each component SKU must exist independently in the catalog.

---

## PART 9 — SKU MAINTENANCE RULES

1. **Assign SKUs at Stage 03** of the Product Framework — not at launch
2. **Never reuse retired SKU numbers** — they are permanently retired with the product
3. **Update SKU records immediately** when a product is retired, a variant is discontinued, or a formula changes
4. **Variant additions** get new variant codes — they do not replace existing ones
5. **SKU master list** is maintained in this file and mirrored in Shopify — the two must match at all times
6. **Miss.Princess and MVQUEEN SKUs** never share a number sequence — they are fully independent

---

## PART 10 — SKU MASTER LIST

*This section is updated whenever a new product is added to the catalog.*

### MVQUEEN SKU Register

| SKU Base | Product Name | Category | Status |
|---|---|---|---|
| MVQ-SKC-001 | The Glow Serum | Skincare | 🔵 Planned |
| MVQ-SKC-002 | Soft Reset Mask | Skincare | 🔵 Planned |
| MVQ-SKC-003 | Still Water Toner | Skincare | 🔵 Planned |
| MVQ-SKC-004 | Velvet Skin Cream | Skincare | 🔵 Planned |
| MVQ-SKC-005 | Warm Glow Oil | Skincare | 🔵 Planned |
| MVQ-SKC-006 | Calm Recovery Eye Cream | Skincare | 🔵 Planned |
| MVQ-SKC-007 | Soft Start Cleanser | Skincare | 🔵 Planned |
| MVQ-FRG-001 | Velvet Hour EDP | Fragrance | 🔵 Planned |
| MVQ-FRG-002 | Still Evening EDP | Fragrance | 🔵 Planned |
| MVQ-FRG-003 | Gold Dusk EDP | Fragrance | 🔵 Planned |
| MVQ-FRG-004 | Soft Midnight EDP | Fragrance | 🔵 Planned |
| MVQ-FRG-005 | The Signature Set | Fragrance | 🔵 Planned |
| MVQ-LFS-001 | Still Evening Candle | Lifestyle | 🔵 Planned |
| MVQ-LFS-002 | Warm Room Reed Diffuser | Lifestyle | 🔵 Planned |
| MVQ-FSH-001 | The Arrival Dress | Fashion | 🔵 Planned |
| MVQ-FSH-002 | The Sunday Blazer | Fashion | 🔵 Planned |
| MVQ-FSH-003 | Ivory Slip | Fashion | 🔵 Planned |
| MVQ-BEA-001 | Soft Glow Primer | Beauty | 🔵 Planned |
| MVQ-BEA-002 | Confidence Foundation | Beauty | 🔵 Planned |
| MVQ-GFT-001 | The Morning Ritual Set | Gift Set | 🔵 Planned |
| MVQ-GFT-002 | The Queen's Ritual Box | Gift Set | 🔵 Planned |

### Miss.Princess SKU Register

| SKU Base | Product Name | Category | Status |
|---|---|---|---|
| MXP-BEA-001 | Petal Glow Gloss | Beauty | 🔵 Planned |
| MXP-BEA-002 | Pretty Please Blush | Beauty | 🔵 Planned |
| MXP-BEA-003 | Dreamy Highlighter | Beauty | 🔵 Planned |
| MXP-SKC-001 | Dewy Dreams Serum | Skincare | 🔵 Planned |
| MXP-SKC-002 | Petal Skin Cream | Skincare | 🔵 Planned |
| MXP-FRG-001 | Petal Dream Mini EDP | Fragrance | 🔵 Planned |
| MXP-ACC-001 | Princess Hair Clip Set | Accessories | 🔵 Planned |
| MXP-GFT-001 | The Princess Starter Kit | Gift Set | 🔵 Planned |

---

*This file is the MVQUEEN SKU system. Update the master list every time a product is added or retired. Pairs with Product_Catalog.md (full product listing), Product_Framework.md (when SKUs are assigned), and Collection_Structure.md (how products are grouped in Shopify).*
