import type { CommercialConfigResolution } from "./commercial-config";

export type FinanceOrderLine = {
  currentQuantity: number;
  unitCost: number | null;
  inboundShipping: number | null;
};

export type FinanceOrder = {
  id: string;
  createdAt: string;
  cancelledAt: string | null;
  currency: string;
  currentTotalPrice: number;
  currentTotalTax: number;
  currentTotalDiscounts: number;
  totalRefunded: number;
  lineItems: FinanceOrderLine[];
  lineItemsComplete: boolean;
};

export type FinanceSummaryState =
  | "no_orders"
  | "needs_commercial_configuration"
  | "incomplete_costs"
  | "incomplete_line_items"
  | "commerce_ready_ads_missing"
  | "fully_loaded";

export type FinanceSummary = {
  state: FinanceSummaryState;
  currency: string;
  orderCount: number;
  cancelledOrderCount: number;
  grossCollected: number;
  taxAmount: number;
  netRevenueExTax: number;
  discountAmount: number;
  refundAmount: number;
  cogs: number | null;
  estimatedFulfillmentCost: number | null;
  estimatedPaymentFees: number | null;
  commerceContributionBeforeAds: number | null;
  targetCacBenchmarkContribution: number | null;
  actualAdSpend: number | null;
  fullyLoadedContribution: number | null;
  missingCostLineCount: number;
  incompleteLineItemOrderCount: number;
  missing: string[];
  notes: string[];
};

function round(value: number): number {
  return Math.round(value * 100) / 100;
}

function nonNegative(value: number | null | undefined): value is number {
  return value !== null && value !== undefined && Number.isFinite(value) && value >= 0;
}

export function buildFinanceSummary(
  orders: FinanceOrder[],
  commercial: CommercialConfigResolution,
  actualAdSpend: number | null = null,
): FinanceSummary {
  const currency =
    orders.find((order) => order.currency)?.currency ??
    commercial.config.currency;

  if (!orders.length) {
    return {
      state: "no_orders",
      currency,
      orderCount: 0,
      cancelledOrderCount: 0,
      grossCollected: 0,
      taxAmount: 0,
      netRevenueExTax: 0,
      discountAmount: 0,
      refundAmount: 0,
      cogs: 0,
      estimatedFulfillmentCost: 0,
      estimatedPaymentFees: 0,
      commerceContributionBeforeAds: 0,
      targetCacBenchmarkContribution: 0,
      actualAdSpend,
      fullyLoadedContribution: actualAdSpend === null ? null : -actualAdSpend,
      missingCostLineCount: 0,
      incompleteLineItemOrderCount: 0,
      missing: [],
      notes: ["No orders were found in the selected reporting window."],
    };
  }

  const grossCollected = orders.reduce(
    (sum, order) => sum + order.currentTotalPrice,
    0,
  );
  const taxAmount = orders.reduce(
    (sum, order) => sum + order.currentTotalTax,
    0,
  );
  const discountAmount = orders.reduce(
    (sum, order) => sum + order.currentTotalDiscounts,
    0,
  );
  const refundAmount = orders.reduce(
    (sum, order) => sum + order.totalRefunded,
    0,
  );
  const netRevenueExTax = grossCollected - taxAmount;
  const cancelledOrderCount = orders.filter((order) => order.cancelledAt).length;
  const incompleteLineItemOrderCount = orders.filter(
    (order) => !order.lineItemsComplete,
  ).length;

  let missingCostLineCount = 0;
  let cogsKnown = 0;
  let fulfillmentKnown = 0;
  let fulfillmentMissing = false;

  for (const order of orders) {
    for (const line of order.lineItems) {
      if (line.currentQuantity <= 0) continue;

      if (!nonNegative(line.unitCost)) {
        missingCostLineCount += 1;
      } else {
        cogsKnown += line.unitCost * line.currentQuantity;
      }

      const perUnitFulfillment = nonNegative(line.inboundShipping)
        ? line.inboundShipping
        : commercial.config.inboundShippingDefault;

      if (!nonNegative(perUnitFulfillment)) {
        fulfillmentMissing = true;
      } else {
        fulfillmentKnown += perUnitFulfillment * line.currentQuantity;
      }
    }
  }

  const commercialMissing = [...commercial.missing];
  const paymentConfigReady =
    nonNegative(commercial.config.paymentRate) &&
    nonNegative(commercial.config.paymentFixed);
  if (!paymentConfigReady) {
    if (!commercialMissing.includes("payment_rate")) commercialMissing.push("payment_rate");
    if (!commercialMissing.includes("payment_fixed")) commercialMissing.push("payment_fixed");
  }

  if (fulfillmentMissing) {
    commercialMissing.push("inbound_or_fulfillment_cost");
  }

  const cogs =
    missingCostLineCount === 0 && incompleteLineItemOrderCount === 0
      ? round(cogsKnown)
      : null;
  const estimatedFulfillmentCost =
    !fulfillmentMissing && incompleteLineItemOrderCount === 0
      ? round(fulfillmentKnown)
      : null;

  const estimatedPaymentFees = paymentConfigReady
    ? round(
        orders.reduce((sum, order) => {
          if (order.currentTotalPrice <= 0) return sum;
          return (
            sum +
            order.currentTotalPrice * commercial.config.paymentRate! +
            commercial.config.paymentFixed!
          );
        }, 0),
      )
    : null;

  const commerceContributionBeforeAds =
    cogs !== null &&
    estimatedFulfillmentCost !== null &&
    estimatedPaymentFees !== null
      ? round(
          netRevenueExTax -
          cogs -
          estimatedFulfillmentCost -
          estimatedPaymentFees,
        )
      : null;

  const targetCacBenchmarkContribution =
    commerceContributionBeforeAds !== null &&
    nonNegative(commercial.config.targetCac)
      ? round(
          commerceContributionBeforeAds -
          commercial.config.targetCac * orders.length,
        )
      : null;

  const fullyLoadedContribution =
    commerceContributionBeforeAds !== null &&
    nonNegative(actualAdSpend)
      ? round(commerceContributionBeforeAds - actualAdSpend)
      : null;

  let state: FinanceSummaryState = "commerce_ready_ads_missing";
  const missing: string[] = [];

  if (commercialMissing.length) {
    state = "needs_commercial_configuration";
    missing.push(...Array.from(new Set(commercialMissing)));
  } else if (incompleteLineItemOrderCount > 0) {
    state = "incomplete_line_items";
    missing.push("orders_with_more_than_100_line_items");
  } else if (missingCostLineCount > 0) {
    state = "incomplete_costs";
    missing.push("verified_product_cost");
  } else if (actualAdSpend !== null) {
    state = "fully_loaded";
  }

  const notes = [
    "Shopify current totals already reflect returns/refunds; refundAmount is reported separately and is not subtracted a second time.",
    "Payment fees are estimates from Commercial Settings until payment-processor transaction fees are connected.",
    "Fulfillment/inbound cost uses product-specific commercial.inbound_shipping when present, otherwise the shop default.",
  ];

  if (actualAdSpend === null) {
    notes.push(
      "Actual ad spend is not connected, so fully loaded contribution/profit is intentionally unavailable.",
    );
  }

  return {
    state,
    currency,
    orderCount: orders.length,
    cancelledOrderCount,
    grossCollected: round(grossCollected),
    taxAmount: round(taxAmount),
    netRevenueExTax: round(netRevenueExTax),
    discountAmount: round(discountAmount),
    refundAmount: round(refundAmount),
    cogs,
    estimatedFulfillmentCost,
    estimatedPaymentFees,
    commerceContributionBeforeAds,
    targetCacBenchmarkContribution,
    actualAdSpend,
    fullyLoadedContribution,
    missingCostLineCount,
    incompleteLineItemOrderCount,
    missing,
    notes,
  };
}
