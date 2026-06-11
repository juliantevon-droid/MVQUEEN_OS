# 📦 MVQUEEN — Inventory Systems

---

## Inventory Philosophy

Inventory management in MVQUEEN is not just operational logistics.
It is brand protection.

Running out of a hero product with no communication damages trust.
Overstocking products that don't move ties up capital and creates pressure to discount.

The goal: the right products available, at the right stock levels, communicated clearly — always.

---

## Inventory Tiers

### Tier 1 — Core Products (Always In Stock)
These are the products that define the brand. Running out is never acceptable without a communication plan.

**Core products:**
- Velvet Body Butter
- Luminous Ritual Face Oil
- Soft Glow Daily Serum
- Silk Restore Hair Mask
- Warm Amber Eau de Parfum
- Morning Ritual Starter Set

**Reorder trigger:** When stock hits 30% of optimal inventory level.
**Safety stock:** Minimum 4-week supply at current sales velocity.

---

### Tier 2 — Regular Products (Managed Stock)
Consistent sellers. Reordered on cycle. Communicate early when approaching low stock.

**Reorder trigger:** When stock hits 25% of optimal inventory level.
**Low stock communication:** Email segment of customers who purchased in last 90 days.

---

### Tier 3 — Seasonal Products (Time-Limited)
Produced for a defined season or campaign. Not restocked after season ends — unless demand justifies a core product upgrade.

**Stock calculation:** Based on prior season performance + projected growth + 15% buffer.
**Sell-through target:** 85%+ before end of season window.
**Leftover protocol:** Offer to loyalty tier as exclusive end-of-season pricing — never sitewide discount.

---

### Tier 4 — Limited Edition (Scarce by Design)
Scarcity is part of the product's value proposition.

**Stock calculation:** Conservative. It should sell out.
**Communication:** Explicit availability communicated at launch ("Available in limited quantity")
**Restock policy:** Usually no restock. If restock is planned — never communicate it before the initial run sells out.

---

## Inventory Metrics

Track weekly for Tier 1 and 2, monthly for Tier 3:

| Metric | Definition | Target |
|--------|-----------|--------|
| Sell-through rate | Units sold / Units received | >80% Tier 1–2 |
| Days of inventory | Current stock / daily sales rate | 30–60 days Tier 1 |
| Stockout frequency | Times per quarter a Tier 1 hits 0 | Zero |
| Overstock rate | Products at >90 days inventory | <10% of catalog |
| Return rate | Units returned / units shipped | <5% |

---

## Shopify Inventory Settings

### Inventory Tracking
- Track quantity: **ON** for all products
- Continue selling when out of stock: **OFF** for standard products
- Continue selling when out of stock: **ON** for made-to-order or pre-order only

### Low Stock Alerts
- Set Shopify low stock notifications at:
  - Tier 1 products: alert at 50 units
  - Tier 2 products: alert at 30 units
  - Tier 3 products: alert at 20 units

### Back-In-Stock Notifications
- Enable back-in-stock waitlist on all Tier 1 products when out of stock
- Email waitlist within 24 hours of restock going live
- SMS to VIP tier simultaneously

---

## Supplier Lead Times

| Product Type | Average Lead Time | Buffer Added |
|-------------|------------------|-------------|
| Skincare (private label) | 4–6 weeks | +1 week |
| Body care | 3–5 weeks | +1 week |
| Hair care | 4–6 weeks | +1 week |
| Fragrance | 6–10 weeks | +2 weeks |
| Fashion | 4–8 weeks | +1 week |
| Accessories | 2–4 weeks | +1 week |

**Rule:** Reorder is always placed with enough lead time to avoid stockout. Reorder trigger dates factor in full lead time + buffer.

---

## Inventory Record Keeping

All inventory data tracked in `37_Databases/DB-01 — Product Master Database`.

Updated:
- When new stock is received
- When a product is launched or discontinued
- Weekly for Tier 1 products during active seasons
- Monthly for all other tiers

---

*04_Products / inventory_systems.md*
*Inventory management is customer experience management. She should never want something she can't have — without knowing why.*
