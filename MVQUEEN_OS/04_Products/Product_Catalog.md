# 📦 MVQUEEN — Product Catalog Master

---

## Purpose

The Product Catalog is the master reference document for every active, draft, and planned product in the MVQUEEN ecosystem. It is updated whenever a product is added, changed, discontinued, or planned.

This document is for internal use — the operational source of truth.
The customer-facing presentation lives in Shopify.

---

## Catalog Structure

Products are organized by:
1. Category
2. Collection assignment
3. Status (Active / Draft / Planned / Discontinued)

Full product specifications (pricing, SKU, copy) live in `37_Databases/DB-01`.

---

## SKINCARE

### Active

| Product Name | SKU | Collection | Price | Status |
|-------------|-----|------------|-------|--------|
| Luminous Ritual Face Oil | MVQ-SK-OIL-30ML-001 | Luminous | $36 | Active |
| Soft Glow Daily Serum | MVQ-SK-SRM-30ML-001 | Luminous | $42 | Active |
| Overnight Renewal Serum | MVQ-SK-SRM-30ML-002 | Velvet | $48 | Active |
| Velvet Face Cream | MVQ-SK-CRM-50ML-001 | Velvet | $38 | Active |
| Featherlight Moisture Gel | MVQ-SK-CRM-50ML-002 | Ritual | $32 | Active |
| Barrier Restore Cream | MVQ-SK-CRM-50ML-003 | Ritual | $44 | Active |
| Ritual Cleansing Balm | MVQ-SK-CLN-100ML-001 | Ritual | $28 | Active |
| Soft Polish Exfoliant | MVQ-SK-CLN-100ML-002 | Ritual | $26 | Active |
| Micellar Rose Water Mist | MVQ-SK-MST-150ML-001 | Ritual | $22 | Active |
| Honey Glow Mask | MVQ-SK-MSK-75ML-001 | Luminous | $34 | Active |
| Overnight Sleep Mask | MVQ-SK-MSK-75ML-002 | Velvet | $36 | Active |
| Calm + Repair Sheet Mask | MVQ-SK-MSK-001-001 | Ritual | $6 | Active |
| Cooling Eye Gel | MVQ-SK-EYE-15ML-001 | Ritual | $28 | Active |
| Lift & Hydrate Eye Cream | MVQ-SK-EYE-15ML-002 | Luminous | $34 | Active |

---

## BODY CARE

### Active

| Product Name | SKU | Collection | Price | Status |
|-------------|-----|------------|-------|--------|
| Velvet Body Butter | MVQ-BC-BTR-250ML-001 | Velvet | $28 | Active |
| Honey Silk Body Cream | MVQ-BC-CRM-250ML-001 | Luminous | $24 | Active |
| 24-Hour Moisture Lotion | MVQ-BC-LTN-250ML-001 | Ritual | $18 | Active |
| Soft Ritual Body Oil | MVQ-BC-OIL-100ML-001 | Ritual | $32 | Active |
| Golden Glow Dry Oil | MVQ-BC-OIL-100ML-002 | Luminous | $36 | Active |
| Sugar Polish Body Scrub | MVQ-BC-SCB-250ML-001 | Ritual | $26 | Active |
| Coffee Revival Scrub | MVQ-BC-SCB-250ML-002 | Ritual | $24 | Active |

---

## HAIR CARE

### Active

| Product Name | SKU | Collection | Price | Status |
|-------------|-----|------------|-------|--------|
| Silk Restore Hair Mask | MVQ-HC-MSK-200ML-001 | Velvet | $32 | Active |
| Moisture Revival Treatment | MVQ-HC-MSK-200ML-002 | Velvet | $36 | Active |
| Protein Strength Treatment | MVQ-HC-MSK-200ML-003 | Ritual | $38 | Active |
| Soft Glow Hair Oil | MVQ-HC-OIL-50ML-001 | Luminous | $28 | Active |
| Scalp Nourishment Oil | MVQ-HC-OIL-50ML-002 | Ritual | $32 | Active |
| Frizz Control Serum | MVQ-HC-SRM-100ML-001 | Ritual | $26 | Active |
| Moisture Balance Shampoo | MVQ-HC-SMP-300ML-001 | Ritual | $22 | Active |
| Hydration Conditioner | MVQ-HC-CND-300ML-001 | Ritual | $22 | Active |
| Clarifying Shampoo | MVQ-HC-SMP-300ML-002 | Ritual | $20 | Active |
| Defining Curl Cream | MVQ-HC-STY-150ML-001 | Ritual | $24 | Active |
| Thermal Protection Spray | MVQ-HC-SPR-150ML-001 | Ritual | $22 | Active |
| Shine Mist | MVQ-HC-SPR-150ML-002 | Luminous | $20 | Active |

---

## FRAGRANCE

### Active

| Product Name | SKU | Collection | Price | Status |
|-------------|-----|------------|-------|--------|
| Warm Amber Eau de Parfum | MVQ-FR-EDP-50ML-AMB | Signature Fragrance | $58 | Active |
| Soft Rose Eau de Parfum | MVQ-FR-EDP-50ML-ROS | Signature Fragrance | $58 | Active |
| Velvet Musk Perfume Oil | MVQ-FR-OIL-10ML-MSK | Signature Fragrance | $34 | Active |
| Golden Hour Body Mist | MVQ-FR-MST-150ML-001 | Luminous | $22 | Active |
| Soft Evening Mist | MVQ-FR-MST-150ML-002 | Velvet | $22 | Active |
| Warm Ritual Candle | MVQ-FR-CND-200G-001 | Ritual | $34 | Active |

---

## KITS & SETS

### Active

| Product Name | SKU | Collection | Price | Status |
|-------------|-----|------------|-------|--------|
| Morning Ritual Starter Set | MVQ-KT-MRN-SET-001 | Ritual | $72 | Active |
| Luminous Skin Duo | MVQ-KT-LMN-SET-001 | Luminous | $64 | Active |
| Velvet Body Ritual Set | MVQ-KT-VLV-SET-001 | Velvet | $68 | Active |
| Hair Restore Kit | MVQ-KT-HC-SET-001 | Velvet | $76 | Active |
| MVQUEEN Signature Gift Set | MVQ-KT-GFT-SET-001 | Core | $88 | Active |

---

## Catalog Maintenance Protocol

- New product added to catalog BEFORE Shopify listing is created
- SKU assigned from `SKU_Systems.md` on catalog entry
- Status updated within 24 hours of any change
- Discontinued products moved to archive section — SKU never reassigned
- Full database entry created in `37_Databases/DB-01` on catalog addition

---

*04_Products / Product_Catalog.md*
*Every product in MVQUEEN's world — organized, tracked, and intentionally placed.*
