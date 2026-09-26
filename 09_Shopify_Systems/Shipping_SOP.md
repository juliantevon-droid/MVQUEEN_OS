# 📦 MVQueen — Shipping SOP

---

## Purpose

Define the standard operating procedure for all order fulfillment and shipping — ensuring every package that leaves MVQueen delivers a luxury experience from the moment it ships to the moment it arrives.

Shipping is not logistics. It is the last brand touchpoint before she holds the product.

---

## Shipping Standards

### Customer-facing delivery estimates

Customer-facing shipping times are product-specific and evidence-based.

1. Use the product metafield `shipping.delivery_estimate`.
2. If a verified supplier/carrier transit window exists, store that exact supported range.
3. If no verified window exists, use: **Confirmed at checkout based on destination and fulfillment source.**
4. Never publish an optimistic generic transit promise simply because a supplier, old document, or sample configuration once used it.
5. Checkout options and the current Shopify delivery profile remain authoritative for a specific order.

### Internal processing targets

Internal handling targets may be used operationally, but they are not customer promises unless the active fulfillment source supports them and they have been approved for customer-facing use.

### Shipping methods

Carrier/service names, rates, and availability come from the active Shopify delivery profile. Current profiles may include general, supplier-specific, or location-specific methods. Do not hard-code carriers or transit days into customer copy unless verified against the current profile or fulfillment source.

### International shipping

Do not promise international delivery by default. Availability is controlled by current Shopify shipping zones and must be confirmed at checkout.

---

## Fulfillment Process (Per Order)

```
□ 1. Order received — confirm payment cleared
□ 2. Pull inventory — verify item is in stock and undamaged
□ 3. Inspect product — quality check before packing
□ 4. Pack order per packaging standards (see below)
□ 5. Insert brand card and any promotional inserts
□ 6. Seal package securely
□ 7. Apply shipping label — verify address accuracy
□ 8. Scan/log order as fulfilled in Shopify
□ 9. Drop off at carrier or schedule pickup
□ 10. Confirm tracking number uploaded to Shopify order
□ 11. Shipping confirmation email auto-triggers — verify sent
```

---

## Packaging Standards

Every MVQueen package must reflect the brand:

| Element | Standard |
|---------|----------|
| Outer box/mailer | Branded, clean, premium feel |
| Inner wrap | Tissue paper — brand color |
| Brand card | Handwritten-style message or printed insert |
| Sticker/seal | Brand logo seal on tissue |
| Padding | Appropriate for product fragility |
| No excess | No cheap filler that undermines luxury feel |

**The unboxing test:** Would she want to photograph this? Would it feel special?
If no — repackage.

---

## Shipping Issue Protocols

### Lost Package (No tracking update 10+ days)
```
1. Verify shipping address was correct
2. Check carrier tracking for last known location
3. File carrier claim if eligible
4. Contact customer with empathy — offer replacement or refund
5. Do not make her wait more than 14 days for resolution
```

### Damaged Package
```
1. Request photo of damage from customer
2. Apologize immediately — no investigation theater
3. Send replacement within 2 business days
4. File carrier insurance claim if applicable
5. Log incident for packaging review
```

### Wrong Item Sent
```
1. Apologize immediately
2. Ship correct item with expedited shipping at no charge
3. Provide prepaid return label for wrong item
4. Do not require her to return item before sending correct one
```

---

## Shipping Notification Email Standard

Triggered automatically when tracking number is uploaded to Shopify.

**Tone:** Warm, anticipatory — never robotic.

Template: `17_Templates/T-02 Email Campaign Template`

Subject line example: *"She's on her way to you."*

---
*MVQueen Shipping SOP — Operational Document*

---
---
---