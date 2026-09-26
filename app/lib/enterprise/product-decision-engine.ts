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
) {
  const classification = classifyProduct(
    product.title ?? "",
    product.descriptionHtml ?? "",
    product.productType ?? "",
  );
  const brandRoute = classifyBrandWorld(product);
  const firstVariant = product.variants?.nodes?.[0];
  const currentPrice = numberFrom(firstVariant?.price);
  const authoritativeUnitCost = numberFrom(firstVariant?.unitCost);
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
      sellingPrice: currentPrice,
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
    ...(classification.confidence === "review" ? ["mvq:needs-review"] : []),
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
      unitCostSource: authoritativeUnitCost !== null ? "shopify_inventory_item" : "commercial_metafield",
      unitCostCurrency: firstVariant?.costCurrency ?? metafieldValue(product, "cost_currency"),
    },
    tags,
    measurementKey: `product:${product.id}`,
  };
}
