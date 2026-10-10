import assert from "node:assert/strict";
import { evaluateVariantCommercial } from "./variant-commercial";
import { buildPricingDecision } from "./pricing-engine";
import { auditCatalogProduct } from "./catalog-audit";
import type { CommercialConfigResolution } from "./commercial-config";
import type { ProductSnapshot } from "../mvqueen-intelligence";

const policy: CommercialConfigResolution = { config: {
  paymentRate: 0.03, paymentFixed: 0.3, returnReserveRate: 0.05,
  targetContributionMarginRate: 0.2, targetCac: 15,
  inboundShippingDefault: 5, currency: "USD",
}, missing: [] };
const product: ProductSnapshot = { id: "gid://shopify/Product/variant-commercial", title: "Necklace", variants: { nodes: [
  { id: "low", price: "100", unitCost: "20", costCurrency: "USD" },
  { id: "high", price: "200", unitCost: "90", costCurrency: "USD" },
] } };
const evaluated = evaluateVariantCommercial(product, policy);
assert.equal(evaluated.costSyncState, "verified_variant_costs");
assert.equal(evaluated.uniformVerifiedUnitCost, null);
assert.equal(evaluated.pricing.state, "ready_for_approval");
assert.equal(evaluated.commercialHealth.state, "healthy");
assert.equal(evaluated.representativeVariantId, "high");
assert.equal(evaluated.commercialHealth.sellingPrice, 200);
assert.equal(evaluated.commercialHealth.unitCost, 90);
assert.equal(evaluated.variantDecisions.length, 2);
assert.equal(evaluated.pricing.publishable, false);
assert.ok(evaluated.variantDecisions.every((item) => item.pricing.publishable === false));

for (const [variant, expectedSync] of [
  [{ id: "incomplete", price: "200", unitCost: null, costCurrency: "USD" }, "partial_variant_costs"],
  [{ id: "foreign", price: "200", unitCost: "90", costCurrency: "EUR" }, "currency_mismatch"],
  [{ id: "unknown-currency", price: "200", unitCost: "90", costCurrency: null }, "currency_mismatch"],
] as const) {
  const result = evaluateVariantCommercial({ ...product,
    commercialMetafields: { nodes: [{ key: "unit_cost", value: "1" }, { key: "cost_currency", value: "USD" }] },
    variants: { nodes: [product.variants!.nodes![0], variant] },
  }, policy);
  assert.equal(result.costSyncState, expectedSync);
  assert.equal(result.pricing.state, "needs_cost");
  assert.equal(result.commercialHealth.state, "needs_cost");
  assert.equal(result.commercialHealth.advertisingEligibility, "not_ready");
}
const mixedHealth = evaluateVariantCommercial({ ...product,
  variants: { nodes: [product.variants!.nodes![0], { id: "unprofitable", price: "10", unitCost: "90", costCurrency: "USD" }] },
}, policy);
assert.equal(mixedHealth.commercialHealth.state, "blocked");
assert.equal(mixedHealth.representativeVariantId, "unprofitable");
assert.equal(evaluateVariantCommercial({ ...product, variants: { nodes: [] } }, policy).commercialHealth.state, "needs_cost");

// Whole-dollar and just-above-.99 minimums must never round below the floor.
const simplePolicy: CommercialConfigResolution = { config: { ...policy.config,
  paymentRate: 0, paymentFixed: 0, returnReserveRate: 0,
  targetContributionMarginRate: 0, targetCac: 0, inboundShippingDefault: 0,
}, missing: [] };
for (const minimum of [0, 10, 10.99, 10.991, 10.999, 11]) {
  const price = buildPricingDecision({ currentPrice: null, unitCost: minimum, inboundShipping: 0 }, simplePolicy);
  assert.ok(price.recommendedPrice! >= minimum, `minimum ${minimum}`);
}
assert.equal(auditCatalogProduct({ id: product.id, title: "Necklace", status: "ACTIVE",
  tags: ["mvq:brand:mvqueen"], seoTitle: "Necklace | MVQUEEN", shortDescription: "An everyday detail.",
  unitCost: "20", variants: [{ id: "low", price: "100" }], hasMoreVariants: false, media: [], collections: [],
}).some((issue) => issue.code === "seo_brand_mismatch"), false);
console.log("variant commercial evaluation and pricing floor tests passed");
