# 🔢 MVQUEEN — SKU Systems

---

## Why SKU Structure Matters

A well-built SKU system is invisible to the customer and indispensable to operations.
It powers inventory tracking, reporting, fulfillment accuracy, and AI product pipelines.

MVQUEEN's SKU system is designed to be:
- Human-readable at a glance
- Sortable by category, brand, and product type
- Scalable as the catalog grows
- Compatible with Shopify and any future ERP or inventory system

---

## SKU Architecture

```
[BRAND]-[CATEGORY]-[PRODUCT TYPE]-[VARIANT]-[NUMBER]
```

Every component is defined and consistent. No free-form SKU creation.

---

## Brand Prefix

| Brand | Prefix |
|-------|--------|
| MVQUEEN | MVQ |
| Miss.Princess | MXP |

All MVQUEEN products begin with `MVQ`.
All Miss.Princess products begin with `MXP`.
Never mixed.

---

## Category Codes

| Category | Code |
|----------|------|
| Skincare | SK |
| Body Care | BC |
| Hair Care | HC |
| Fragrance | FR |
| Makeup / Color | MK |
| Accessories | AC |
| Fashion | FS |
| Shoes | SH |
| Jewelry | JW |
| Lifestyle / Home | LH |
| Wellness | WL |
| Kits & Sets | KT |
| Limited Edition | LE |

---

## Product Type Codes (examples by category)

**Skincare (SK)**
- SRM = Serum
- MST = Mist / Toner
- CRM = Cream / Moisturizer
- OIL = Face Oil
- MSK = Mask
- CLN = Cleanser
- SPF = SPF / Sun Protection
- EYE = Eye Care

**Body Care (BC)**
- BTR = Body Butter
- OIL = Body Oil
- SCB = Scrub / Exfoliant
- LTN = Lotion
- WSH = Body Wash
- MLK = Body Milk

**Hair Care (HC)**
- SRM = Serum
- MSK = Hair Mask
- OIL = Hair Oil
- SMP = Shampoo
- CND = Conditioner
- SPR = Hair Spray / Mist

**Fragrance (FR)**
- EDP = Eau de Parfum
- EDT = Eau de Toilette
- OIL = Perfume Oil
- MST = Body / Hair Mist
- CND = Candle
- DIF = Diffuser

**Makeup (MK)**
- LIP = Lip Product
- EYE = Eye Product
- FND = Foundation / Base
- BLH = Blush / Highlighter
- BRW = Brow Product
- SET = Setting Product

---

## Variant Codes

| Variant Type | Code Format |
|-------------|-------------|
| Size / Volume | 30ML, 50ML, 100ML, 250ML |
| Shade / Color | shade name abbreviated: ROS (Rose), NUD (Nude), PLM (Plum), etc. |
| Scent | scent name abbreviated: AMB (Amber), VNL (Vanilla), FLR (Floral), etc. |
| Single unit | 001 |
| Bundle / Set | SET |

---

## Full SKU Examples

| Product | SKU |
|---------|-----|
| MVQUEEN Luminous Face Serum, 30ml | MVQ-SK-SRM-30ML-001 |
| MVQUEEN Velvet Body Butter, 250ml | MVQ-BC-BTR-250ML-001 |
| MVQUEEN Warm Amber Eau de Parfum, 50ml | MVQ-FR-EDP-50ML-AMB |
| MVQUEEN Soft Glam Lip Set, Rose | MVQ-MK-LIP-SET-ROS |
| MVQUEEN Silk Hair Mask, 200ml | MVQ-HC-MSK-200ML-001 |
| MVQUEEN Morning Ritual Kit | MVQ-KT-MRN-SET-001 |
| Miss.Princess Fairy Glow Serum, 30ml | MXP-SK-SRM-30ML-001 |
| Miss.Princess Princess Aura Mist | MXP-FR-MST-100ML-001 |

---

## SKU Governance Rules

**Rule 1 — Every product gets a unique SKU before it goes live.**
No two products share a SKU. Ever.

**Rule 2 — Variants are always separate SKUs.**
A 30ml and 50ml of the same serum are two SKUs — not one product with a note.

**Rule 3 — SKUs never change once assigned.**
Changing a SKU breaks inventory history, reporting, and fulfillment records.
If a product is discontinued — the SKU is archived, never reassigned.

**Rule 4 — SKUs are never used in customer-facing copy.**
SKUs are operational. They live in Shopify backend, inventory sheets, and order management — never in product titles, descriptions, or customer communications.

**Rule 5 — Limited edition SKUs use LE prefix in category code.**
Example: `MVQ-LE-KT-WNT-001` = MVQUEEN Limited Edition Winter Kit

---

## SKU Master Log

All active, archived, and discontinued SKUs are tracked in:
`37_Databases/DB-01 — Product Master Database`

Every new product SKU is logged there on creation — before the Shopify listing is built.

---

*04_Products / SKU_Systems.md*
*A clean SKU system is the foundation of scalable inventory. Build it right once.*
