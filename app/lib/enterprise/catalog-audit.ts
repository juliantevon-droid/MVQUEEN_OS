export type CatalogAuditSeverity = "blocker" | "warning";

export type CatalogAuditIssue = {
  productGid: string;
  title: string;
  severity: CatalogAuditSeverity;
  code: string;
  message: string;
};

type AuditProduct = {
  id: string;
  title: string;
  status: string;
  tags: string[];
  seoTitle?: string | null;
  shortDescription?: string | null;
  unitCost?: string | null;
  variants: Array<{ id: string; price?: string | null }>;
  hasMoreVariants: boolean;
  media: Array<{ id: string; alt?: string | null }>;
  mediaAuditAvailable?: boolean;
  collections: Array<{ handle: string }>;
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

export function auditCatalogProduct(product: AuditProduct): CatalogAuditIssue[] {
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
    if (product.seoTitle && !product.seoTitle.includes("MVQueen")) {
      add("blocker", "seo_brand_mismatch", "MVQueen product SEO title does not identify MVQueen.");
    }
    if (collectionHandles.has("miss-princess-world")) {
      add("blocker", "cross_brand_world_collection", "MVQueen product is present in Miss.Princess World.");
    }
  }

  const unitCost = money(product.unitCost);
  if (unitCost === null) {
    add("blocker", "unit_cost_missing", "Verified commercial.unit_cost is missing.");
  }

  if (product.variants.length !== 1 || product.hasMoreVariants) {
    add(
      "warning",
      "variant_pricing_requires_variant_costs",
      "Multi-variant product requires variant-level costs before governed price publication.",
    );
  } else {
    const price = money(product.variants[0]?.price);
    if (price === null) {
      add("blocker", "selling_price_missing", "Selling price is missing or invalid.");
    } else if (unitCost !== null) {
      if (price <= unitCost) {
        add("blocker", "price_at_or_below_cost", "Selling price is at or below verified unit cost before fees.");
      } else {
        const grossMarginRate = (price - unitCost) / price;
        if (grossMarginRate < 0.20) {
          add(
            "warning",
            "thin_pre_fee_margin",
            "Pre-fee gross margin is below 20%; contribution pricing review is required.",
          );
        }
      }
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

export function summarizeCatalogAudit(products: AuditProduct[]) {
  const issues = products.flatMap(auditCatalogProduct);
  const blockers = issues.filter((item) => item.severity === "blocker");
  const warnings = issues.filter((item) => item.severity === "warning");

  return {
    productCount: products.length,
    blockerCount: blockers.length,
    warningCount: warnings.length,
    healthyProductCount: products.filter(
      (product) => !issues.some((issue) => issue.productGid === product.id),
    ).length,
    issues,
  };
}

export type { AuditProduct };
