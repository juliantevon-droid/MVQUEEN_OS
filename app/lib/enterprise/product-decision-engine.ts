import {
  brandRoutingTags,
  classifyBrandWorld,
  classifyProduct,
  type ProductSnapshot,
} from "../mvqueen-intelligence";
import { buildMarketingPlan } from "./marketing-engine";
import { buildPricingDecision } from "./pricing-engine";
import { buildLifecyclePlan } from "./lifecycle-engine";
import { getCommercialConfig, type CommercialConfigResolution } from "./commercial-config";
import { buildCommercialHealth } from "./commercial-health";

function numberFrom(value?: string | null): number | null {
  if (!value?.trim()) return null;
  const parsed = Number(value);
  return Number.isFinite(parsed) && parsed >= 0 ? parsed : null;
}

function uniformNumber(values: Array<string | null | undefined>): number | null {
  if (!values.length) return null;
  const parsed = values.map(numberFrom);
  if (parsed.some((value) => value === null)) return null;
  const first = parsed[0] as number;
  return parsed.every((value) => Math.abs((value as number) - first) < 0.000001)
    ? first
    : null;
}

function uniformText(values: Array<string | null | undefined>): string | null {
  if (!values.length) return null;
  const normalized = values.map((value) => String(value ?? "").trim()).filter(Boolean);
  if (normalized.length !== values.length) return null;
  const first = normalized[0];
  return normalized.every((value) => value === first) ? first : null;
}

function metafieldValue(product: ProductSnapshot, key: string): string | null {
  return product.commercialMetafields?.nodes?.find((item) => item.key === key)?.value ?? null;
}

function slug(value: string): string {
  return value
    .toLowerCase()
    .replace(/&/g, "and")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

export function collectionRoutingTags(classification: {
  department: string;
  family: string;
  route: string;
}): string[] {
  const slugs = [
    slug(classification.department),
    slug(classification.family),
    slug(classification.route),
  ].filter((value) => value && value !== "unclassified" && value !== "needs-review");

  return Array.from(new Set(slugs)).map((value) => `mvq:collection:${value}`);
}

export function buildEnterpriseProductDecision(
  product: ProductSnapshot,
  commercial?: CommercialConfigResolution,
  effectiveSellingPrice?: number | null,
) {
  const classification = classifyProduct(
    product.title ?? "",
    product.descriptionHtml ?? "",
    product.productType ?? "",
  );
  const brandRoute = classifyBrandWorld(product);
  const variants = product.variants?.nodes ?? [];
  const currentPrice = uniformNumber(variants.map((variant) => variant.price));
  const authoritativeUnitCost = uniformNumber(
    variants.map((variant) => variant.unitCost),
  );
  const authoritativeCostCurrency =
    authoritativeUnitCost !== null
      ? uniformText(variants.map((variant) => variant.costCurrency))
      : null;
  const resolvedCommercial = commercial ?? getCommercialConfig();
  const unitCost =
    authoritativeUnitCost ?? numberFrom(metafieldValue(product, "unit_cost"));
  const inboundShipping = numberFrom(metafieldValue(product, "inbound_shipping"));

  const pricing = buildPricingDecision(
    {
      currentPrice,
      unitCost,
      inboundShipping,
    },
    resolvedCommercial,
  );
  const commercialHealth = buildCommercialHealth(
    {
      sellingPrice:
        effectiveSellingPrice === undefined ? currentPrice : effectiveSellingPrice,
      unitCost,
      inboundShipping,
    },
    resolvedCommercial,
  );
  const marketing = buildMarketingPlan(
    classification,
    brandRoute,
    pricing,
    commercialHealth,
  );
  const lifecycle = buildLifecyclePlan(classification, brandRoute);

  const tags = [
    "mvq:catalog",
    `mvq:department:${slug(classification.department)}`,
    `mvq:family:${slug(classification.family)}`,
    ...collectionRoutingTags(classification),
    ...brandRoutingTags(brandRoute),
    ...(classification.confidence === "review" || !brandRoute.brand ? ["mvq:needs-review"] : []),
    ...(pricing.state === "ready_for_approval" ? ["mvq:pricing:ready-for-approval"] : [`mvq:pricing:${pricing.state}`]),
    `mvq:commercial:${commercialHealth.state}`,
    `mvq:ads:${commercialHealth.advertisingEligibility}`,
    `mvq:marketing:${marketing.state}`,
    `mvq:lifecycle:${lifecycle.state}`,
  ];

  return {
    classification,
    brandRoute,
    pricing,
    commercialHealth,
    marketing,
    lifecycle,
    commercialSource: {
      unitCostSource:
        authoritativeUnitCost !== null
          ? "shopify_inventory_item"
          : "commercial_metafield",
      unitCostCurrency:
        authoritativeCostCurrency ?? metafieldValue(product, "cost_currency"),
    },
    tags,
    measurementKey: `product:${product.id}`,
  };
}
