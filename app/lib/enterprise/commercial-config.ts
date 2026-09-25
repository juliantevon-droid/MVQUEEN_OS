export type CommercialConfig = {
  paymentRate: number | null;
  paymentFixed: number | null;
  returnReserveRate: number | null;
  targetContributionMarginRate: number | null;
  targetCac: number | null;
  inboundShippingDefault: number | null;
  currency: string;
};

function envNumber(name: string): number | null {
  const raw = process.env[name]?.trim();
  if (!raw) return null;
  const value = Number(raw);
  return Number.isFinite(value) && value >= 0 ? value : null;
}

export function getCommercialConfig(): { config: CommercialConfig; missing: string[] } {
  const config: CommercialConfig = {
    paymentRate: envNumber("MVQ_PAYMENT_RATE"),
    paymentFixed: envNumber("MVQ_PAYMENT_FIXED"),
    returnReserveRate: envNumber("MVQ_RETURN_RESERVE_RATE"),
    targetContributionMarginRate: envNumber("MVQ_TARGET_CONTRIBUTION_MARGIN_RATE"),
    targetCac: envNumber("MVQ_TARGET_CAC"),
    inboundShippingDefault: envNumber("MVQ_INBOUND_SHIPPING_DEFAULT"),
    currency: process.env.MVQ_CURRENCY?.trim() || "USD",
  };

  const required: Array<[keyof CommercialConfig, string]> = [
    ["paymentRate", "MVQ_PAYMENT_RATE"],
    ["paymentFixed", "MVQ_PAYMENT_FIXED"],
    ["returnReserveRate", "MVQ_RETURN_RESERVE_RATE"],
    ["targetContributionMarginRate", "MVQ_TARGET_CONTRIBUTION_MARGIN_RATE"],
    ["targetCac", "MVQ_TARGET_CAC"],
  ];

  const missing = required
    .filter(([key]) => config[key] === null)
    .map(([, envName]) => envName);

  return { config, missing };
}
