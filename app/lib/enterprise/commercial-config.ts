export type CommercialConfig = {
  paymentRate: number | null;
  paymentFixed: number | null;
  returnReserveRate: number | null;
  targetContributionMarginRate: number | null;
  targetCac: number | null;
  inboundShippingDefault: number | null;
  currency: string;
};

export type CommercialConfigResolution = {
  config: CommercialConfig;
  missing: string[];
};

function envNumber(name: string): number | null {
  const raw = process.env[name]?.trim();
  if (!raw) return null;
  const value = Number(raw);
  return Number.isFinite(value) && value >= 0 ? value : null;
}

function overrideNumber(value: number | null | undefined, fallback: number | null): number | null {
  return value === null || value === undefined ? fallback : value;
}

export function getCommercialConfig(
  overrides: Partial<CommercialConfig> = {},
): CommercialConfigResolution {
  const envConfig: CommercialConfig = {
    paymentRate: envNumber("MVQ_PAYMENT_RATE"),
    paymentFixed: envNumber("MVQ_PAYMENT_FIXED"),
    returnReserveRate: envNumber("MVQ_RETURN_RESERVE_RATE"),
    targetContributionMarginRate: envNumber("MVQ_TARGET_CONTRIBUTION_MARGIN_RATE"),
    targetCac: envNumber("MVQ_TARGET_CAC"),
    inboundShippingDefault: envNumber("MVQ_INBOUND_SHIPPING_DEFAULT"),
    currency: process.env.MVQ_CURRENCY?.trim() || "USD",
  };

  const config: CommercialConfig = {
    paymentRate: overrideNumber(overrides.paymentRate, envConfig.paymentRate),
    paymentFixed: overrideNumber(overrides.paymentFixed, envConfig.paymentFixed),
    returnReserveRate: overrideNumber(overrides.returnReserveRate, envConfig.returnReserveRate),
    targetContributionMarginRate: overrideNumber(
      overrides.targetContributionMarginRate,
      envConfig.targetContributionMarginRate,
    ),
    targetCac: overrideNumber(overrides.targetCac, envConfig.targetCac),
    inboundShippingDefault: overrideNumber(
      overrides.inboundShippingDefault,
      envConfig.inboundShippingDefault,
    ),
    currency: overrides.currency?.trim() || envConfig.currency,
  };

  const required: Array<[keyof CommercialConfig, string]> = [
    ["paymentRate", "payment_rate"],
    ["paymentFixed", "payment_fixed"],
    ["returnReserveRate", "return_reserve_rate"],
    ["targetContributionMarginRate", "target_contribution_margin_rate"],
    ["targetCac", "target_cac"],
  ];

  const missing = required
    .filter(([key]) => config[key] === null)
    .map(([, label]) => label);

  return { config, missing };
}
