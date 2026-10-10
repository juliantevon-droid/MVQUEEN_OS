import {
  brandRoutingTags,
  classifyBrandWorld,
  classifyProduct,
  type ProductSnapshot,
} from "../mvqueen-intelligence";
import { buildMarketingPlan } from "./marketing-engine";
import { buildLifecyclePlan } from "./lifecycle-engine";
import { getCommercialConfig, type CommercialConfigResolution } from "./commercial-config";
import { evaluateVariantCommercial } from "./variant-commercial";
import { productClaimReviewReasons } from "../product-content-automation";

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
  const resolvedCommercial = commercial ?? getCommercialConfig();
  const variantCommercial = evaluateVariantCommercial(product, resolvedCommercial, effectiveSellingPrice);
  const { pricing } = variantCommercial;
  const catalogReviewReasons = [
    ...(classification.confidence === "review" ? ["classification_requires_review"] : []),
    ...(!brandRoute.brand ? ["brand_requires_review"] : []),
    ...productClaimReviewReasons(product).map((reason) => `source_claim:${reason}`),
  ];
  const restrictAdvertising = (health: typeof variantCommercial.commercialHealth) =>
    catalogReviewReasons.length && health.advertisingEligibility === "eligible"
      ? { ...health, advertisingEligibility: "blocked" as const,
          reasons: [...health.reasons, "Catalog classification or source claims still require review."] }
      : health;
  const commercialHealth = restrictAdvertising(variantCommercial.commercialHealth);
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
    ...(catalogReviewReasons.length ? ["mvq:needs-review"] : []),
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
    commercialSource: variantCommercial.commercialSource,
    variantDecisions: variantCommercial.variantDecisions.map((item) => ({
      ...item, commercialHealth: restrictAdvertising(item.commercialHealth),
    })),
    catalogReviewReasons,
    representativeVariantId: variantCommercial.representativeVariantId,
    costSyncState: variantCommercial.costSyncState,
    uniformVerifiedUnitCost: variantCommercial.uniformVerifiedUnitCost,
    tags,
    measurementKey: `product:${product.id}`,
  };
}
