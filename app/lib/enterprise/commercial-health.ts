import type { CommercialConfigResolution } from "./commercial-config";

export type CommercialHealthState =
  | "needs_configuration"
  | "needs_cost"
  | "needs_price"
  | "invalid_inputs"
  | "blocked"
  | "thin"
  | "healthy";

export type AdvertisingEligibility =
  | "not_ready"
  | "blocked"
  | "eligible";

export type CommercialHealth = {
  state: CommercialHealthState;
  advertisingEligibility: AdvertisingEligibility;
  currency: string;
  sellingPrice: number | null;
  unitCost: number | null;
  inboundShipping: number | null;
  paymentCost: number | null;
  returnReserve: number | null;
  contributionBeforeAds: number | null;
  maxBreakEvenCac: number | null;
  maxCacAtTargetMargin: number | null;
  targetCac: number | null;
  contributionAfterTargetCac: number | null;
  contributionMarginAfterTargetCac: number | null;
  targetContributionMarginRate: number | null;
  breakEvenRoas: number | null;
  targetMarginRoasFloor: number | null;
  targetRoas: number | null;
  missing: string[];
  reasons: string[];
};

function validMoney(value: number | null): value is number {
  return value !== null && Number.isFinite(value) && value >= 0;
}

function round(value: number): number {
  return Math.round(value * 10000) / 10000;
}

export function buildCommercialHealth(
  input: {
    sellingPrice: number | null;
    unitCost: number | null;
    inboundShipping: number | null;
  },
  commercial: CommercialConfigResolution,
): CommercialHealth {
  const { config, missing } = commercial;
  const base = {
    currency: config.currency,
    sellingPrice: input.sellingPrice,
    unitCost: input.unitCost,
    inboundShipping: input.inboundShipping,
    paymentCost: null,
    returnReserve: null,
    contributionBeforeAds: null,
    maxBreakEvenCac: null,
    maxCacAtTargetMargin: null,
    targetCac: config.targetCac,
    contributionAfterTargetCac: null,
    contributionMarginAfterTargetCac: null,
    targetContributionMarginRate: config.targetContributionMarginRate,
    breakEvenRoas: null,
    targetMarginRoasFloor: null,
    targetRoas: null,
    missing,
    reasons: [] as string[],
  };

  if (missing.length) {
    return {
      ...base,
      state: "needs_configuration",
      advertisingEligibility: "not_ready",
      reasons: ["Commercial assumptions are incomplete."],
    };
  }

  if (!validMoney(input.unitCost)) {
    return {
      ...base,
      state: "needs_cost",
      advertisingEligibility: "not_ready",
      missing: ["commercial.unit_cost"],
      reasons: ["Verified unit cost is required."],
    };
  }

  if (!validMoney(input.sellingPrice) || input.sellingPrice <= 0) {
    return {
      ...base,
      state: "needs_price",
      advertisingEligibility: "not_ready",
      missing: ["selling_price"],
      reasons: ["A valid selling price is required."],
    };
  }

  const paymentRate = config.paymentRate!;
  const paymentFixed = config.paymentFixed!;
  const returnReserveRate = config.returnReserveRate!;
  const targetCac = config.targetCac!;
  const targetMargin = config.targetContributionMarginRate!;
  const inboundShipping = validMoney(input.inboundShipping)
    ? input.inboundShipping
    : (config.inboundShippingDefault ?? 0);

  if (
    paymentRate < 0 ||
    returnReserveRate < 0 ||
    targetMargin < 0 ||
    paymentRate + returnReserveRate + targetMargin >= 1
  ) {
    return {
      ...base,
      state: "invalid_inputs",
      advertisingEligibility: "not_ready",
      reasons: ["Commercial percentages are internally inconsistent."],
    };
  }

  const paymentCost = input.sellingPrice * paymentRate + paymentFixed;
  const returnReserve = input.sellingPrice * returnReserveRate;
  const contributionBeforeAds =
    input.sellingPrice -
    input.unitCost -
    inboundShipping -
    paymentCost -
    returnReserve;
  const maxBreakEvenCac = Math.max(0, contributionBeforeAds);
  const targetContributionDollars = input.sellingPrice * targetMargin;
  const maxCacAtTargetMargin = Math.max(
    0,
    contributionBeforeAds - targetContributionDollars,
  );
  const contributionAfterTargetCac = contributionBeforeAds - targetCac;
  const contributionMarginAfterTargetCac =
    contributionAfterTargetCac / input.sellingPrice;
  const breakEvenRoas =
    maxBreakEvenCac > 0 ? input.sellingPrice / maxBreakEvenCac : null;
  const targetMarginRoasFloor =
    maxCacAtTargetMargin > 0
      ? input.sellingPrice / maxCacAtTargetMargin
      : null;
  const targetRoas =
    targetCac > 0 ? input.sellingPrice / targetCac : null;

  let state: CommercialHealthState = "healthy";
  let advertisingEligibility: AdvertisingEligibility = "eligible";
  const reasons: string[] = [];

  if (contributionBeforeAds <= 0 || contributionAfterTargetCac <= 0) {
    state = "blocked";
    advertisingEligibility = "blocked";
    reasons.push("Current price does not support positive contribution after configured CAC.");
  } else if (contributionMarginAfterTargetCac < targetMargin) {
    state = "thin";
    advertisingEligibility = "blocked";
    reasons.push("Current contribution margin is below the configured target margin.");
  } else {
    reasons.push("Current price supports the configured CAC and target contribution margin.");
  }

  return {
    ...base,
    state,
    advertisingEligibility,
    inboundShipping: round(inboundShipping),
    paymentCost: round(paymentCost),
    returnReserve: round(returnReserve),
    contributionBeforeAds: round(contributionBeforeAds),
    maxBreakEvenCac: round(maxBreakEvenCac),
    maxCacAtTargetMargin: round(maxCacAtTargetMargin),
    contributionAfterTargetCac: round(contributionAfterTargetCac),
    contributionMarginAfterTargetCac: round(contributionMarginAfterTargetCac),
    breakEvenRoas: breakEvenRoas === null ? null : round(breakEvenRoas),
    targetMarginRoasFloor:
      targetMarginRoasFloor === null ? null : round(targetMarginRoasFloor),
    targetRoas: targetRoas === null ? null : round(targetRoas),
    reasons,
  };
}
