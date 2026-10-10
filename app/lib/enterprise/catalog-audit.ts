import type { CommercialConfigResolution } from "./commercial-config";
import type { CommercialHealth } from "./commercial-health";
import { buildReleaseGate, type ReleaseGateDecision } from "./release-gate";
import { evaluateVariantCommercial } from "./variant-commercial";

export type CatalogAuditSeverity = "blocker" | "warning";

export type CatalogAuditIssue = {
  productGid: string;
  title: string;
  severity: CatalogAuditSeverity;
  code: string;
  message: string;
};

export type AuditProduct = {
  id: string;
  title: string;
  status: string;
  tags: string[];
  seoTitle?: string | null;
  shortDescription?: string | null;
  unitCost?: string | null;
  costCurrency?: string | null;
  inboundShipping?: string | null;
  variants: Array<{ id: string; price?: string | null; unitCost?: string | null; costCurrency?: string | null }>;
  hasMoreVariants: boolean;
  media: Array<{ id: string; alt?: string | null }>;
  mediaAuditAvailable?: boolean;
  collections: Array<{ handle: string }>;
};

export type CatalogProductEvaluation = {
  productGid: string;
  title: string;
  issues: CatalogAuditIssue[];
  commercialHealth: CommercialHealth;
  releaseGate: ReleaseGateDecision;
};

function money(value?: string | null): number | null {
  if (!value?.trim()) return null;
  const parsed = Number(value);
  return Number.isFinite(parsed) && parsed >= 0 ? parsed : null;
}

function brandOf(tags: string[]): "mvqueen" | "miss-princess" | "invalid" {
  const worlds = tags.filter((tag) =>
    tag === "mvq:brand:mvqueen" || tag === "mvq:brand:miss-princess",
  );
  if (worlds.length !== 1) return "invalid";
  return worlds[0] === "mvq:brand:miss-princess" ? "miss-princess" : "mvqueen";
}

export function auditCatalogProduct(product: AuditProduct, currency = "USD"): CatalogAuditIssue[] {
  const issues: CatalogAuditIssue[] = [];
  const brand = brandOf(product.tags);
  const collectionHandles = new Set(product.collections.map((item) => item.handle));

  const add = (severity: CatalogAuditSeverity, code: string, message: string) => {
    issues.push({
      productGid: product.id,
      title: product.title,
      severity,
      code,
      message,
    });
  };

  if (brand === "invalid") {
    add(
      "blocker",
      "brand_world_invalid",
      "Product must have exactly one canonical mvq:brand:* world tag.",
    );
  }

  if (!product.seoTitle?.trim()) {
    add("warning", "seo_title_missing", "SEO title is missing.");
  }

  if (!product.shortDescription?.trim()) {
    add("warning", "short_description_missing", "Approved/catalog short description is missing.");
  }

  if (brand === "miss-princess") {
    if (product.seoTitle && !product.seoTitle.includes("Miss.Princess")) {
      add("blocker", "seo_brand_mismatch", "Miss.Princess product SEO title does not identify Miss.Princess.");
    }
    if (collectionHandles.has("mvqueen-world")) {
      add("blocker", "cross_brand_world_collection", "Miss.Princess product is present in MVQueen World.");
    }
    if (collectionHandles.has("mvqueen-edit")) {
      add("warning", "legacy_mvqueen_edit_membership", "Miss.Princess product is still present in legacy MVQueen Edit.");
    }
  }

  if (brand === "mvqueen") {
    if (product.seoTitle && !/\bMVQUEEN\b/i.test(product.seoTitle)) {
      add("blocker", "seo_brand_mismatch", "MVQUEEN product SEO title does not identify MVQUEEN.");
    }
    if (collectionHandles.has("miss-princess-world")) {
      add("blocker", "cross_brand_world_collection", "MVQueen product is present in Miss.Princess World.");
    }
  }

  const fallbackCost = money(product.unitCost);
  const hasVariantCosts = product.variants.some((item) => money(item.unitCost) !== null);
  const fallbackCurrencyMatches = product.costCurrency?.toUpperCase() === currency.toUpperCase();
  if (product.hasMoreVariants) {
    add("blocker", "variant_audit_incomplete", "All variants must be inspected before commercial clearance.");
  }
  if (!product.variants.length) add("blocker", "selling_price_missing", "No priced variants found.");
  for (const variant of product.variants) {
    const unitCost = hasVariantCosts ? money(variant.unitCost) : fallbackCurrencyMatches ? fallbackCost : null;
    const costCurrency = hasVariantCosts ? variant.costCurrency : product.costCurrency;
    if (unitCost === null) {
      add("blocker", "unit_cost_missing", `Variant ${variant.id} needs a verified cost.`);
    } else if (costCurrency?.toUpperCase() !== currency.toUpperCase()) {
      add("blocker", "cost_currency_mismatch", `Variant ${variant.id} cost currency does not match ${currency}.`);
    }
    const price = money(variant.price);
    if (price === null || price <= 0) {
      add("blocker", "selling_price_missing", "Selling price is missing or invalid.");
    } else if (unitCost !== null && price <= unitCost) {
      add("blocker", "price_at_or_below_cost", `Variant ${variant.id} is priced at or below verified cost before fees.`);
    }
  }

  if (product.mediaAuditAvailable) {
    const missingAlt = product.media.filter((item) => !item.alt?.trim()).length;
    if (missingAlt > 0) {
      add(
        "warning",
        "media_alt_missing",
        `${missingAlt} media item(s) are missing ALT text; publication requires the separate Shopify Files permission.`,
      );
    }
  }

  return issues;
}

export function evaluateCatalogProduct(
  product: AuditProduct,
  commercial: CommercialConfigResolution,
): CatalogProductEvaluation {
  const issues = auditCatalogProduct(product, commercial.config.currency);
  const { commercialHealth } = evaluateVariantCommercial({
    id: product.id, title: product.title,
    variants: { nodes: product.variants },
    commercialMetafields: { nodes: [
      { key: "unit_cost", value: product.unitCost },
      { key: "cost_currency", value: product.costCurrency },
      { key: "inbound_shipping", value: product.inboundShipping },
    ] },
  }, commercial);
  const releaseGate = buildReleaseGate({ issues, commercialHealth });

  return {
    productGid: product.id,
    title: product.title,
    issues,
    commercialHealth,
    releaseGate,
  };
}

export function summarizeCatalogAudit(
  products: AuditProduct[],
  commercial: CommercialConfigResolution,
) {
  const evaluations = products.map((product) =>
    evaluateCatalogProduct(product, commercial),
  );
  const issues = evaluations.flatMap((item) => item.issues);
  const blockers = issues.filter((item) => item.severity === "blocker");
  const warnings = issues.filter((item) => item.severity === "warning");

  return {
    productCount: products.length,
    blockerCount: blockers.length,
    warningCount: warnings.length,
    healthyProductCount: evaluations.filter(
      (item) => item.releaseGate.state === "ready",
    ).length,
    publishReadyCount: evaluations.filter(
      (item) => item.releaseGate.publishEligible,
    ).length,
    advertisingEligibleCount: evaluations.filter(
      (item) => item.releaseGate.advertisingEligible,
    ).length,
    commercialBlockedCount: evaluations.filter(
      (item) =>
        item.commercialHealth.state === "blocked" ||
        item.commercialHealth.state === "thin" ||
        item.commercialHealth.state === "needs_configuration" ||
        item.commercialHealth.state === "needs_cost" ||
        item.commercialHealth.state === "needs_price" ||
        item.commercialHealth.state === "invalid_inputs",
    ).length,
    issues,
    evaluations,
  };
}
