import { getCommercialConfig } from "./commercial-config";

export type PricingDecisionState =
  | "needs_configuration"
  | "needs_cost"
  | "invalid_inputs"
  | "ready_for_approval";

export type PricingInputs = {
  currentPrice: number | null;
  unitCost: number | null;
  inboundShipping: number | null;
};

export type PricingDecision = {
  state: PricingDecisionState;
  publishable: false;
  currency: string;
  currentPrice: number | null;
  minimumPrice: number | null;
  recommendedPrice: number | null;
  estimatedContributionDollars: number | null;
  estimatedContributionMarginRate: number | null;
  missing: string[];
  rationale: string[];
};

function validMoney(value: number | null): value is number {
  return value !== null && Number.isFinite(value) && value >= 0;
}

function money(value: number): number {
  return Math.round(value * 100) / 100;
}

function recommendationEnding(value: number): number {
  const whole = Math.ceil(value);
  return money(Math.max(0, whole - 0.01));
}

export function buildPricingDecision(input: PricingInputs): PricingDecision {
  const { config, missing } = getCommercialConfig();

  if (missing.length) {
    return {
      state: "needs_configuration",
      publishable: false,
      currency: config.currency,
      currentPrice: input.currentPrice,
      minimumPrice: null,
      recommendedPrice: null,
      estimatedContributionDollars: null,
      estimatedContributionMarginRate: null,
      missing,
      rationale: ["Commercial assumptions are incomplete; pricing remains advisory and blocked."],
    };
  }

  if (!validMoney(input.unitCost)) {
    return {
      state: "needs_cost",
      publishable: false,
      currency: config.currency,
      currentPrice: input.currentPrice,
      minimumPrice: null,
      recommendedPrice: null,
      estimatedContributionDollars: null,
      estimatedContributionMarginRate: null,
      missing: ["commercial.unit_cost"],
      rationale: ["Verified unit cost is required before MVQueen OS recommends a selling price."],
    };
  }

  const paymentRate = config.paymentRate!;
  const paymentFixed = config.paymentFixed!;
  const returnReserveRate = config.returnReserveRate!;
  const targetMargin = config.targetContributionMarginRate!;
  const targetCac = config.targetCac!;
  const inboundShipping = validMoney(input.inboundShipping)
    ? input.inboundShipping
    : (config.inboundShippingDefault ?? 0);

  const variableRate = paymentRate + returnReserveRate;
  const denominator = 1 - variableRate - targetMargin;
  if (denominator <= 0) {
    return {
      state: "invalid_inputs",
      publishable: false,
      currency: config.currency,
      currentPrice: input.currentPrice,
      minimumPrice: null,
      recommendedPrice: null,
      estimatedContributionDollars: null,
      estimatedContributionMarginRate: null,
      missing: [],
      rationale: ["Configured fees, reserve and target margin leave no viable pricing denominator."],
    };
  }

  const fixedCost = input.unitCost + inboundShipping + paymentFixed + targetCac;
  const minimumPrice = fixedCost / denominator;
  const recommendedPrice = recommendationEnding(minimumPrice);
  const variableCosts =
    input.unitCost +
    inboundShipping +
    paymentFixed +
    targetCac +
    recommendedPrice * variableRate;
  const contribution = recommendedPrice - variableCosts;
  const contributionRate = recommendedPrice > 0 ? contribution / recommendedPrice : 0;

  return {
    state: "ready_for_approval",
    publishable: false,
    currency: config.currency,
    currentPrice: input.currentPrice,
    minimumPrice: money(minimumPrice),
    recommendedPrice,
    estimatedContributionDollars: money(contribution),
    estimatedContributionMarginRate: money(contributionRate),
    missing: [],
    rationale: [
      "Recommendation is derived from verified cost plus configured fees, return reserve, CAC and target contribution margin.",
      "Price publication remains disabled until an explicit commercial approval path is enabled.",
    ],
  };
}
