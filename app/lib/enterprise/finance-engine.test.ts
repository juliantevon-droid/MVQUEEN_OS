import assert from "node:assert/strict";
import { buildFinanceSummary, type FinanceOrder } from "./finance-engine";
import type { CommercialConfigResolution } from "./commercial-config";

const policy: CommercialConfigResolution = {
  config: {
    paymentRate: 0.03,
    paymentFixed: 0.30,
    returnReserveRate: 0.05,
    targetContributionMarginRate: 0.20,
    targetCac: 15,
    inboundShippingDefault: 5,
    currency: "USD",
  },
  missing: [],
};

const order: FinanceOrder = {
  id: "gid://shopify/Order/1",
  createdAt: new Date().toISOString(),
  cancelledAt: null,
  currency: "USD",
  currentTotalPrice: 100,
  currentTotalTax: 8,
  currentTotalDiscounts: 10,
  totalRefunded: 20,
  lineItemsComplete: true,
  lineItems: [
    { currentQuantity: 1, unitCost: 20, inboundShipping: 2 },
    { currentQuantity: 2, unitCost: 10, inboundShipping: null },
  ],
};

const summary = buildFinanceSummary([order], policy, null);
assert.equal(summary.state, "commerce_ready_ads_missing");
assert.equal(summary.orderCount, 1);
assert.equal(summary.commerceOrderCount, 1);
assert.equal(summary.cancelledOrderCount, 0);
assert.equal(summary.grossCollected, 100);
assert.equal(summary.taxAmount, 8);
assert.equal(summary.netRevenueExTax, 92);
assert.equal(summary.refundAmount, 20);
assert.equal(summary.cogs, 40);
assert.equal(summary.estimatedFulfillmentCost, 12);
assert.equal(summary.estimatedPaymentFees, 3.3);
assert.equal(summary.commerceContributionBeforeAds, 36.7);
assert.equal(summary.targetCacBenchmarkContribution, 21.7);
assert.equal(summary.fullyLoadedContribution, null);

// Shopify current totals already reflect returns/refunds. Refund reporting must not be
// subtracted a second time from current net revenue.
assert.equal(summary.netRevenueExTax, 92);

const withAds = buildFinanceSummary([order], policy, 10);
assert.equal(withAds.state, "fully_loaded");
assert.equal(withAds.actualAdSpend, 10);
assert.equal(withAds.fullyLoadedContribution, 26.7);

const cancelled: FinanceOrder = {
  ...order,
  id: "gid://shopify/Order/2",
  cancelledAt: new Date().toISOString(),
  currentTotalPrice: 0,
  currentTotalTax: 0,
  totalRefunded: 100,
  lineItems: [{ currentQuantity: 0, unitCost: 20, inboundShipping: 2 }],
};
const cancellationSummary = buildFinanceSummary([order, cancelled], policy, null);
assert.equal(cancellationSummary.orderCount, 2);
assert.equal(cancellationSummary.commerceOrderCount, 1);
assert.equal(cancellationSummary.cancelledOrderCount, 1);
assert.equal(cancellationSummary.targetCacBenchmarkContribution, 21.7);

const missingCost: FinanceOrder = {
  ...order,
  lineItems: [{ currentQuantity: 1, unitCost: null, inboundShipping: 2 }],
};
const missingCostSummary = buildFinanceSummary([missingCost], policy, null);
assert.equal(missingCostSummary.state, "incomplete_costs");
assert.equal(missingCostSummary.cogs, null);
assert.equal(missingCostSummary.commerceContributionBeforeAds, null);
assert.equal(missingCostSummary.missingCostLineCount, 1);

const incompleteLines: FinanceOrder = {
  ...order,
  lineItemsComplete: false,
};
const incompleteSummary = buildFinanceSummary([incompleteLines], policy, null);
assert.equal(incompleteSummary.state, "incomplete_line_items");
assert.equal(incompleteSummary.cogs, null);

const incompletePolicy: CommercialConfigResolution = {
  config: {
    ...policy.config,
    paymentRate: null,
  },
  missing: ["payment_rate"],
};
const configSummary = buildFinanceSummary([order], incompletePolicy, null);
assert.equal(configSummary.state, "needs_commercial_configuration");
assert.equal(configSummary.estimatedPaymentFees, null);

const noOrders = buildFinanceSummary([], policy, null);
assert.equal(noOrders.state, "no_orders");
assert.equal(noOrders.orderCount, 0);
assert.equal(noOrders.commerceOrderCount, 0);

console.log("finance engine tests passed");
