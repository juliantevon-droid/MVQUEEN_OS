import assert from "node:assert/strict";
import { assessCategoryPrice, getCategoryPriceBand } from "./category-pricing";
import { buildPricingDecision } from "./pricing-engine";
import type { CommercialConfigResolution } from "./commercial-config";

// Recorded Shopify brush cost plus known store assumptions. Existing paid
// advertising CAC must NOT be baked into a simple accessory's retail ceiling.
const paidConfig: CommercialConfigResolution = {
  config: { paymentRate: 0.03, paymentFixed: 0.3, returnReserveRate: 0.10,
    targetContributionMarginRate: 0.30, targetCac: 8,
    inboundShippingDefault: 3, currency: "USD" },
  missing: [],
};
const organicConfig: CommercialConfigResolution = {
  config: { ...paidConfig.config, targetCac: 0, targetContributionMarginRate: 0.20 },
  missing: [],
};
const input = { currentPrice: 32.99, unitCost: 7.23, inboundShipping: null };
const paid = buildPricingDecision(input, paidConfig);
const organic = buildPricingDecision(input, organicConfig);
const brush = assessCategoryPrice({
  title: "Shampoo Brush — Little Wash-Day Companion", productType: "Shampoo",
  variantTitle: "Blue", currentPrice: 32.99,
  paidFloor: paid.minimumPrice, organicFloor: organic.minimumPrice,
});
assert.equal(brush.band?.key, "scalp_brush");
assert.equal(brush.state, "paid_cost_conflict");
assert.equal(brush.suggestedOrganicPrice, 16.99);
assert.ok(paid.minimumPrice! > brush.band!.max);
assert.ok(organic.minimumPrice! < brush.suggestedOrganicPrice!);

const eyeliner = assessCategoryPrice({
  title: "Fine Line Liquid Eyeliner", productType: "Makeup",
  currentPrice: 30.99, paidFloor: null, organicFloor: 14.10,
});
assert.equal(eyeliner.state, "above_band");
assert.equal(eyeliner.suggestedOrganicPrice, 14.99);

const costlySoap = assessCategoryPrice({
  title: "Lemon & Turmeric Soap", productType: "Bath & Body",
  currentPrice: 48.99, paidFloor: 40, organicFloor: 29.5,
});
assert.equal(costlySoap.state, "organic_cost_conflict");
assert.equal(costlySoap.suggestedOrganicPrice, null);

assert.equal(getCategoryPriceBand({
  title: "Shampoo Brush", variantTitle: "Blue / 25PCS",
}).multipackReview, true);
assert.equal(getCategoryPriceBand({
  title: "Warm Contour Microcurrent Neck Massager",
}).band, null);

const underpriced = assessCategoryPrice({
  title: "Everyday Crop Top", productType: "Tops",
  currentPrice: 5.99, paidFloor: 8, organicFloor: 7,
});
assert.equal(underpriced.state, "below_band");
assert.ok(underpriced.suggestedOrganicPrice! >= underpriced.organicFloor!);
console.log("MVQUEEN category pricing safeguards passed");
