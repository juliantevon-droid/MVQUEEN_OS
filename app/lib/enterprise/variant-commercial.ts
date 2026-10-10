import type { ProductSnapshot } from "../mvqueen-intelligence";
import type { CommercialConfigResolution } from "./commercial-config";
import { buildCommercialHealth, type CommercialHealthState } from "./commercial-health";
import { buildPricingDecision } from "./pricing-engine";

function numberFrom(value?: string | null): number | null {
  if (!value?.trim()) return null;
  const parsed = Number(value);
  return Number.isFinite(parsed) && parsed >= 0 ? parsed : null;
}

const HEALTH_PRIORITY: Record<CommercialHealthState, number> = {
  needs_configuration: 7, invalid_inputs: 6, needs_cost: 5,
  needs_price: 4, blocked: 3, thin: 2, healthy: 1,
};

export function evaluateVariantCommercial(
  product: ProductSnapshot,
  commercial: CommercialConfigResolution,
  effectiveSellingPrice?: number | null,
) {
  const variants = product.variants?.nodes ?? [];
  const fields = product.commercialMetafields?.nodes ?? [];
  const field = (key: string) => fields.find((item) => item.key === key)?.value;
  const inboundShipping = numberFrom(field("inbound_shipping"));
  const currency = commercial.config.currency.toUpperCase();
  const currencyMatches = (value?: string | null) => value?.trim().toUpperCase() === currency;
  const hasInventoryCosts = variants.some((variant) => numberFrom(variant.unitCost) !== null);
  // A legacy product cost can apply only when no inventory costs are present.
  // It must never hide a missing variant or a currency mismatch.
  const fallbackCost = !hasInventoryCosts && currencyMatches(field("cost_currency"))
    ? numberFrom(field("unit_cost")) : null;
  const fallbackVariants = variants.length ? variants : [{ id: product.id, price: null, unitCost: null, costCurrency: null }];
  const decisions = fallbackVariants.map((variant) => {
    const inventoryCost = numberFrom(variant.unitCost);
    const unitCost = inventoryCost !== null
      ? (currencyMatches(variant.costCurrency) ? inventoryCost : null)
      : fallbackCost;
    const currentPrice = numberFrom(variant.price);
    return {
      variantId: variant.id,
      costSource: inventoryCost !== null ? "shopify_inventory_item" : fallbackCost !== null ? "commercial_metafield" : "unverified",
      costCurrency: variant.costCurrency ?? field("cost_currency") ?? null,
      pricing: buildPricingDecision({ currentPrice, unitCost, inboundShipping }, commercial),
      commercialHealth: buildCommercialHealth({
        sellingPrice: effectiveSellingPrice === undefined ? currentPrice : effectiveSellingPrice,
        unitCost, inboundShipping,
      }, commercial),
    };
  });
  const healthDecision = [...decisions].sort((a, b) =>
    HEALTH_PRIORITY[b.commercialHealth.state] - HEALTH_PRIORITY[a.commercialHealth.state] ||
    (a.commercialHealth.contributionMarginAfterTargetCac ?? -Infinity) -
    (b.commercialHealth.contributionMarginAfterTargetCac ?? -Infinity),
  )[0];
  const blockedPricing = decisions.find((item) => item.pricing.state !== "ready_for_approval");
  const pricingDecision = blockedPricing ?? [...decisions].sort((a, b) =>
    (b.pricing.recommendedPrice ?? 0) - (a.pricing.recommendedPrice ?? 0),
  )[0];
  const allInventoryCosts = variants.length > 0 && variants.every((variant) => numberFrom(variant.unitCost) !== null);
  const allCurrenciesMatch = variants.every((variant) => currencyMatches(variant.costCurrency));
  const uniformCost = allInventoryCosts && variants.every((variant) =>
    numberFrom(variant.unitCost) === numberFrom(variants[0].unitCost),
  );
  const costSyncState = !hasInventoryCosts ? "no_cost_value"
    : !allInventoryCosts ? "partial_variant_costs"
    : !allCurrenciesMatch ? "currency_mismatch"
    : uniformCost ? "verified" : "verified_variant_costs";
  return {
    variantDecisions: decisions,
    // These summaries describe real variant pairs. Every variant must pass;
    // mixing the lowest price with another variant's highest cost is invalid.
    pricing: pricingDecision.pricing,
    commercialHealth: healthDecision.commercialHealth,
    representativeVariantId: healthDecision.variantId,
    costSyncState,
    uniformVerifiedUnitCost: uniformCost && allCurrenciesMatch ? numberFrom(variants[0].unitCost) : null,
    commercialSource: {
      unitCostSource: decisions.every((item) => item.costSource === "shopify_inventory_item")
        ? "shopify_inventory_item"
        : decisions.every((item) => item.costSource === "commercial_metafield") ? "commercial_metafield" : "unverified",
      unitCostCurrency: decisions.every((item) => item.commercialHealth.unitCost !== null) ? currency : null,
    },
  };
}
