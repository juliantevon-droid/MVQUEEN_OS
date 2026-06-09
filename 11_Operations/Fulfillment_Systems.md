# 📬 MVQUEEN — Fulfillment Systems

---

## Purpose

Define the end-to-end fulfillment infrastructure that ensures every order is processed accurately, packed to brand standard, and delivered within the promised window — at every volume level.

---

## Fulfillment Models

### Model 1 — Self-Fulfillment (Current)
**Best for:** Under 50 orders/day
**Setup:** Home or small studio storage, self-packing, carrier drop-off

| Pros | Cons |
|------|------|
| Full quality control | Time-intensive |
| Brand packaging control | Doesn't scale past ~50 orders/day |
| No minimum commitments | Storage space required |
| Low cost at low volume | You are the bottleneck |

**Upgrade trigger:** When fulfillment consistently takes more than 3 hours/day — evaluate 3PL.

### Model 2 — 3PL (Third-Party Logistics)
**Best for:** 50+ orders/day consistently
**Setup:** Send inventory to 3PL warehouse, they pick/pack/ship

| Pros | Cons |
|------|------|
| Scales without your time | Less brand packaging control |
| Faster shipping speeds | Per-order fees add up |
| Multi-location = faster delivery | Requires minimum volumes |
| Frees founder for growth work | Requires careful onboarding |

**3PL evaluation criteria:**
- Luxury brand experience (not just commodity shipping)
- Custom packaging capability
- Shopify integration
- Real-time inventory visibility
- Returns processing
- Per-order cost under $[target] at projected volume

---

## Inventory Management

### Storage Standards
- All products stored away from direct sunlight and moisture
- Beauty products stored at consistent temperature
- FIFO (First In, First Out) — oldest stock ships first
- Damaged stock quarantined immediately — never shipped

### Inventory Thresholds

| Threshold | Action |
|-----------|--------|
| Below reorder point | Trigger reorder immediately |
| Below 20 units | Flag as low stock on product page |
| Below 5 units | Show "Almost Gone" indicator |
| 0 units | Auto-hide or show "Sold Out" + waitlist |

### Reorder Formula
```
Reorder Point = (Average Daily Sales × Lead Time in Days) + Safety Stock
Safety Stock = Average Daily Sales × 7 days
```

Example: 5 units/day average × 14-day lead time + (5 × 7) = 105 unit reorder point

---

## Quality Control Protocol

Every order before packing:
```
□ Correct product pulled
□ Correct variant (size, color, scent) confirmed
□ Product inspected — no damage, no defects
□ Expiry date checked (beauty products)
□ Packaging integrity confirmed
□ Brand insert included
□ Correct shipping label applied
□ Address verified against order
```

Failure at any step = order held until resolved. Never ship a compromised order.

---

## Fulfillment KPIs

| Metric | Target |
|--------|--------|
| Order processing time | Under 2 business days |
| Order accuracy rate | 99.5%+ |
| On-time shipment rate | 98%+ |
| Damage rate | Under 0.5% |
| Return rate (fulfillment errors) | Under 1% |

---
*MVQUEEN Fulfillment Systems — Operational Document*

---
---
---