import { createHash } from "node:crypto";
import { BRAND_VOCABULARY } from "./brand-vocabulary.server";
import prisma from "../db.server";
import { unauthenticated } from "../shopify.server";
import { createCorrelationId, errorFields, logMvqueenEvent } from "./enterprise/observability.server";
import { productTypeForWrite, type ProductSnapshot } from "./mvqueen-intelligence";
import {
  buildCatalogAttributeEnrichment,
  buildCatalogAttributeMetafields,
  buildVariantGoogleMetafields,
} from "./catalog-attribute-enrichment";
import { buildEnterpriseProductDecision } from "./enterprise/product-decision-engine";
import {
  buildAutomatedProductContent,
  needsMediaAltRepair,
  productClaimReviewReasons,
  shouldPublishAutomatedDescription,
} from "./product-content-automation";
import { buildAutomatedProductFaq, buildAutomaticSurfaceRecord } from "./automated-content-surfaces";
import { publishAutomaticContentSurfaces } from "./enterprise/content-publisher";
import { resolveShippingDeliveryEstimate } from "./shipping-policy";
import { buildShopifyCategoryMetafields } from "./shopify-category-publisher.server";
import {
  commercialPolicyFingerprint,
  resolveShopCommercialConfig,
} from "./enterprise/commercial-settings.server";

export const AUTOMATION_VERSION = "mvq-enterprise-product-decision-v34-factual-title-varied-copy-claim-safe-complete-highlights-" + BRAND_VOCABULARY.version;

const TAXONOMY_CATEGORY_BY_ROUTE: Record<string, string> = {
  "activewear-sets": "gid://shopify/TaxonomyCategory/aa-1-1",
  pendants: "gid://shopify/TaxonomyCategory/aa-6-8",
  necklaces: "gid://shopify/TaxonomyCategory/aa-6-8",
  earrings: "gid://shopify/TaxonomyCategory/aa-6-6",
  bracelets: "gid://shopify/TaxonomyCategory/aa-6-3",
  rings: "gid://shopify/TaxonomyCategory/aa-6-9",
  sunglasses: "gid://shopify/TaxonomyCategory/aa-2-27",
  "handbags-purses": "gid://shopify/TaxonomyCategory/aa-5-4",
  dresses: "gid://shopify/TaxonomyCategory/aa-1-4",
  "jumpsuits-rompers": "gid://shopify/TaxonomyCategory/aa-1-9",
  bodysuits: "gid://shopify/TaxonomyCategory/aa-1-13-2",
  "t-shirts": "gid://shopify/TaxonomyCategory/aa-1-13-8",
  blouses: "gid://shopify/TaxonomyCategory/aa-1-13-1",
  "jeans-denim": "gid://shopify/TaxonomyCategory/aa-1-12-4",
  pants: "gid://shopify/TaxonomyCategory/aa-1-12",
  shorts: "gid://shopify/TaxonomyCategory/aa-1-14",
  skirts: "gid://shopify/TaxonomyCategory/aa-1-15",
  makeup: "gid://shopify/TaxonomyCategory/hb-3-2-6",
  skincare: "gid://shopify/TaxonomyCategory/hb-3-2-9",
  shampoo: "gid://shopify/TaxonomyCategory/hb-3-10-13-3",
  conditioner: "gid://shopify/TaxonomyCategory/hb-3-10-13-1",
  "hair-treatments": "gid://shopify/TaxonomyCategory/hb-3-10-14",
  "hair-tools": "gid://shopify/TaxonomyCategory/hb-3-10-12",
  "beauty-tools": "gid://shopify/TaxonomyCategory/hb-3-2-5",
  "bath-body": "gid://shopify/TaxonomyCategory/hb-3-2-1",
  fragrance: "gid://shopify/TaxonomyCategory/hb-3-2-8",
};

function taxonomyCategoryForRoute(route: string, title: string): string | null {
  if (route === "wigs-extensions") {
    return /\bwig(?:s)?\b/i.test(title)
      ? "gid://shopify/TaxonomyCategory/aa-2-14-12"
      : "gid://shopify/TaxonomyCategory/aa-2-14-3";
  }
  return TAXONOMY_CATEGORY_BY_ROUTE[route] ?? null;
}

// The React app is the single live Shopify writer. Automatic enrollment may
// authorize newly created/updated products for safe editorial/catalog fields,
// while protected commerce fields remain outside this worker.
const WRITE_ENABLED = process.env.MVQ_WRITE_ENABLED === "true";
const AUTO_PRODUCT_ENROLLMENT_ENABLED =
  process.env.MVQ_AUTO_PRODUCT_ENROLLMENT_ENABLED === "true";
const EDITORIAL_PUBLISH_ENABLED =
  process.env.MVQ_EDITORIAL_PUBLISH_ENABLED === "true";
const TITLE_PUBLISH_ENABLED =
  process.env.MVQ_TITLE_PUBLISH_ENABLED === "true";
const SEO_PUBLISH_ENABLED =
  process.env.MVQ_SEO_PUBLISH_ENABLED === "true";
const DESCRIPTION_PUBLISH_ENABLED =
  process.env.MVQ_DESCRIPTION_PUBLISH_ENABLED === "true";
const DESCRIPTION_REWRITE_EXISTING_ENABLED =
  process.env.MVQ_DESCRIPTION_REWRITE_EXISTING_ENABLED === "true";
const PRICE_PUBLISH_ENABLED =
  process.env.MVQ_PRICE_PUBLISH_ENABLED === "true";
const COMPARE_AT_PRICE_PUBLISH_ENABLED =
  process.env.MVQ_COMPARE_AT_PRICE_PUBLISH_ENABLED === "true";
const VENDOR_NORMALIZATION_ENABLED =
  process.env.MVQ_VENDOR_NORMALIZATION_ENABLED === "true";
const AUTO_CONTENT_SURFACES_ENABLED =
  process.env.MVQ_AUTO_CONTENT_SURFACES_ENABLED === "true";
const MEDIA_ALT_SYNC_ENABLED =
  process.env.MVQ_MEDIA_ALT_SYNC_ENABLED === "true";
const COST_SYNC_ENABLED = process.env.MVQ_COST_SYNC_ENABLED === "true";
const CATEGORY_METAFIELDS_ENABLED =
  process.env.MVQ_CATEGORY_METAFIELDS_ENABLED === "true";
const APPROVED_PRODUCT_GIDS = new Set(
  (process.env.MVQ_APPROVED_PRODUCT_GIDS ?? "")
    .split(",")
    .map((value) => value.trim())
    .filter(Boolean),
);


const ACCESS_SCOPES_QUERY = `#graphql
query MVQueenAccessScopes {
  appInstallation {
    accessScopes { handle }
  }
}`;


const ACCESS_SCOPE_CACHE = new Map<
  string,
  { expiresAt: number; handles: Set<string> }
>();

async function accessScopesForShop(
  shop: string,
  admin: { graphql: (query: string, options?: { variables?: Record<string, unknown> }) => Promise<Response> },
): Promise<Set<string>> {
  const ttlMs = Math.max(
    60_000,
    Math.min(3_600_000, Number(process.env.MVQ_SCOPE_CACHE_TTL_MS ?? "300000") || 300000),
  );
  const cached = ACCESS_SCOPE_CACHE.get(shop);
  if (cached && cached.expiresAt > Date.now()) return cached.handles;

  const response = await admin.graphql(ACCESS_SCOPES_QUERY);
  const body = await response.json();
  const handles = new Set<string>(
    (body.data?.appInstallation?.accessScopes ?? [])
      .map((scope: { handle?: string | null }) => scope.handle)
      .filter((value: string | null | undefined): value is string => Boolean(value)),
  );
  ACCESS_SCOPE_CACHE.set(shop, { handles, expiresAt: Date.now() + ttlMs });
  return handles;
}

const PRODUCT_QUERY = `#graphql
query MVQueenProduct($id: ID!, $attributeNamespace: String!) {
  product(id: $id) {
    id title handle descriptionHtml productType vendor tags
    seo { title description }
    category { id fullName }
    options { name values }
    media(first: 50) {
      nodes {
        ... on MediaImage { id alt }
      }
    }
    variants(first: 100) {
      nodes {
        id
        price
        compareAtPrice
        sku
        barcode
        selectedOptions { name value }
        googleMetafields: metafields(first: 30, namespace: "mm-google-shopping") {
          nodes { key value type }
        }
      }
    }
    commercialMetafields: metafields(first: 20, namespace: "commercial") {
      nodes { key value type }
    }
    shippingMetafields: metafields(first: 10, namespace: "shipping") {
      nodes { key value type }
    }
    attributeMetafields: metafields(first: 40, namespace: $attributeNamespace) {
      nodes { key value type }
    }
  }
}`;

const PRODUCT_QUERY_WITH_COST = `#graphql
query MVQueenProductWithCost($id: ID!, $attributeNamespace: String!) {
  product(id: $id) {
    id title handle descriptionHtml productType vendor tags
    seo { title description }
    category { id fullName }
    options { name values }
    media(first: 50) {
      nodes {
        ... on MediaImage { id alt }
      }
    }
    variants(first: 100) {
      nodes {
        id
        price
        compareAtPrice
        sku
        barcode
        selectedOptions { name value }
        googleMetafields: metafields(first: 30, namespace: "mm-google-shopping") {
          nodes { key value type }
        }
        inventoryItem {
          unitCost { amount currencyCode }
        }
      }
    }
    commercialMetafields: metafields(first: 20, namespace: "commercial") {
      nodes { key value type }
    }
    shippingMetafields: metafields(first: 10, namespace: "shipping") {
      nodes { key value type }
    }
    attributeMetafields: metafields(first: 40, namespace: $attributeNamespace) {
      nodes { key value type }
    }
  }
}`;

const PRODUCT_UPDATE = `#graphql
mutation MVQueenProductUpdate($product: ProductUpdateInput!) {
  productUpdate(product: $product) {
    product { id title productType updatedAt }
    userErrors { field message }
  }
}`;

const FILE_UPDATE = `#graphql
mutation MVQueenFileAltUpdate($files: [FileUpdateInput!]!) {
  fileUpdate(files: $files) {
    userErrors { field message code }
  }
}`;

const PRODUCT_VARIANTS_BULK_UPDATE = `#graphql
mutation MVQueenVariantPricingUpdate(
  $productId: ID!
  $variants: [ProductVariantsBulkInput!]!
) {
  productVariantsBulkUpdate(productId: $productId, variants: $variants) {
    product { id }
    productVariants { id price compareAtPrice }
    userErrors { field message }
  }
}`;

function moneyNumber(value?: string | null): number | null {
  if (!value?.trim()) return null;
  const parsed = Number(value);
  return Number.isFinite(parsed) && parsed >= 0 ? parsed : null;
}

function uniformMoney(
  values: Array<string | null | undefined>,
): number | null {
  if (!values.length) return null;
  const parsed = values.map(moneyNumber);
  if (parsed.some((value) => value === null)) return null;
  const first = parsed[0] as number;
  return parsed.every(
    (value) => Math.abs((value as number) - first) < 0.000001,
  )
    ? first
    : null;
}

function uniformText(
  values: Array<string | null | undefined>,
): string | null {
  if (!values.length) return null;
  const normalized = values.map((value) => String(value ?? "").trim());
  if (normalized.some((value) => !value)) return null;
  const first = normalized[0];
  return normalized.every((value) => value === first) ? first : null;
}

function commercialNumber(product: ProductSnapshot, key: string): number | null {
  return moneyNumber(
    product.commercialMetafields?.nodes?.find((item) => item.key === key)?.value,
  );
}



function sourceFingerprint(
  product: ProductSnapshot,
  policyFingerprint: string,
): string {
  const source = JSON.stringify({
    policyFingerprint,
    capabilities: {
      editorialPublish: EDITORIAL_PUBLISH_ENABLED,
      titlePublish: TITLE_PUBLISH_ENABLED,
      seoPublish: SEO_PUBLISH_ENABLED,
      descriptionPublish: DESCRIPTION_PUBLISH_ENABLED,
      descriptionRewriteExisting: DESCRIPTION_REWRITE_EXISTING_ENABLED,
      pricePublish: PRICE_PUBLISH_ENABLED,
      compareAtPricePublish: COMPARE_AT_PRICE_PUBLISH_ENABLED,
      vendorNormalization: VENDOR_NORMALIZATION_ENABLED,
      automaticContentSurfaces: AUTO_CONTENT_SURFACES_ENABLED,
      mediaAltSync: MEDIA_ALT_SYNC_ENABLED,
      costSync: COST_SYNC_ENABLED,
      categoryMetafields: CATEGORY_METAFIELDS_ENABLED,
    },
    title: product.title ?? "",
    descriptionHtml: product.descriptionHtml ?? "",
    seo: product.seo ?? null,
    category: product.category?.id ?? null,
    productType: product.productType ?? "",
    vendor: product.vendor ?? "",
    tags: [...(product.tags ?? [])]
      .filter((tag) => !tag.toLowerCase().startsWith("mvq:"))
      .sort(),
    options: (product.options ?? [])
      .map((option) => ({
        name: option.name,
        values: [...(option.values ?? [])].sort(),
      }))
      .sort((a, b) => a.name.localeCompare(b.name)),
    variants: (product.variants?.nodes ?? [])
      .map((v) => ({
        id: v.id,
        price: v.price ?? "",
        compareAtPrice: v.compareAtPrice ?? "",
        sku: v.sku ?? "",
        barcode: v.barcode ?? "",
        selectedOptions: v.selectedOptions ?? [],
        googleMetafields: (v.googleMetafields?.nodes ?? [])
          .map((m) => ({ key: m.key, value: m.value ?? "", type: m.type ?? "" }))
          .sort((a, b) => a.key.localeCompare(b.key)),
        unitCost: v.unitCost ?? "",
        costCurrency: v.costCurrency ?? "",
      }))
      .sort((a, b) => a.id.localeCompare(b.id)),
    commercialMetafields: (product.commercialMetafields?.nodes ?? [])
      .map((m) => ({ key: m.key, value: m.value ?? "", type: m.type ?? "" }))
      .sort((a, b) => a.key.localeCompare(b.key)),
    attributeMetafields: (product.attributeMetafields?.nodes ?? [])
      .map((m) => ({ key: m.key, value: m.value ?? "", type: m.type ?? "" }))
      .sort((a, b) => a.key.localeCompare(b.key)),
    shippingDeliveryEstimate: resolveShippingDeliveryEstimate(
      product.shippingMetafields?.nodes?.find((m) => m.key === "delivery_estimate")?.value,
    ),
  });

  return createHash("sha256").update(source).digest("hex");
}

export async function processProductJob(
  jobId: string,
  options: { allowWrites?: boolean } = {},
) {
  const invocationWritesAllowed = options.allowWrites !== false;
  const correlationId = createCorrelationId("product-job");
  const job = await prisma.productJob.findUnique({ where: { id: jobId } });
  if (!job) throw new Error("Product job not found");

  logMvqueenEvent("product.job.started", {
    correlationId,
    jobId,
    shop: job.shop,
    productGid: job.productGid,
    topic: job.topic,
    invocationWritesAllowed,
  });

  await prisma.productJob.update({
    where: { id: jobId },
    data: { status: "processing", attempts: { increment: 1 }, startedAt: new Date(), error: null },
  });

  try {
    const { admin } = await unauthenticated.admin(job.shop);

    let hasReadInventory = false;
    let hasWriteFiles = false;
    let hasWriteMetaobjects = false;
    if (
      COST_SYNC_ENABLED ||
      MEDIA_ALT_SYNC_ENABLED ||
      CATEGORY_METAFIELDS_ENABLED
    ) {
      const handles = await accessScopesForShop(job.shop, admin);
      hasReadInventory = handles.has("read_inventory");
      hasWriteFiles = handles.has("write_files");
      hasWriteMetaobjects = handles.has("write_metaobjects");
    }

    const response = await admin.graphql(
      COST_SYNC_ENABLED && hasReadInventory ? PRODUCT_QUERY_WITH_COST : PRODUCT_QUERY,
      { variables: { id: job.productGid, attributeNamespace: "attributes" } },
    );
    const body = await response.json();
    const rawProduct = body.data?.product ?? null;
    const product: ProductSnapshot | null = rawProduct
      ? {
          ...rawProduct,
          variants: {
            nodes: (rawProduct.variants?.nodes ?? []).map(
              (variant: {
                id: string;
                price?: string | null;
                compareAtPrice?: string | null;
                sku?: string | null;
                barcode?: string | null;
                selectedOptions?: Array<{ name: string; value: string }>;
                googleMetafields?: {
                  nodes?: Array<{
                    key: string;
                    value?: string | null;
                    type?: string | null;
                  }>;
                };
                inventoryItem?: {
                  unitCost?: { amount?: string | null; currencyCode?: string | null } | null;
                } | null;
              }) => ({
                id: variant.id,
                price: variant.price ?? null,
                compareAtPrice: variant.compareAtPrice ?? null,
                sku: variant.sku ?? null,
                barcode: variant.barcode ?? null,
                selectedOptions: variant.selectedOptions ?? [],
                googleMetafields: variant.googleMetafields ?? { nodes: [] },
                unitCost: variant.inventoryItem?.unitCost?.amount ?? null,
                costCurrency: variant.inventoryItem?.unitCost?.currencyCode ?? null,
              }),
            ),
          },
        }
      : null;
    if (!product) throw new Error("Shopify product not found");

    logMvqueenEvent("product.job.snapshot", {
      correlationId,
      jobId,
      shop: job.shop,
      productGid: product.id,
      productTitle: product.title,
      topic: job.topic,
      variantCount: product.variants?.nodes?.length ?? 0,
      mediaCount: product.media?.nodes?.length ?? 0,
      protectedFields: ["handle", "sku", "barcode", "inventory"],
    });

    const commercialConfig = await resolveShopCommercialConfig(job.shop);
    const policyFingerprint = commercialPolicyFingerprint(commercialConfig);
    const fingerprint = sourceFingerprint(product, policyFingerprint);
    const state = await prisma.productAutomationState.findUnique({
      where: { shop_productGid: { shop: job.shop, productGid: product.id } },
      select: { sourceFingerprint: true, automationVersion: true },
    });

    if (state?.sourceFingerprint === fingerprint && state.automationVersion === AUTOMATION_VERSION) {
      await prisma.productJob.update({
        where: { id: jobId },
        data: { status: "completed", completedAt: new Date(), error: null },
      });
      return;
    }

    const preliminaryDecision = buildEnterpriseProductDecision(
      product,
      commercialConfig,
    );
    const variants = product.variants?.nodes ?? [];
    const preliminaryPricing = preliminaryDecision.pricing;
    const recommendedPrice = preliminaryPricing.recommendedPrice;
    const uniformCurrentPrice = uniformMoney(
      variants.map((variant) => variant.price),
    );
    const uniformUnitCost = uniformMoney(
      variants.map((variant) => variant.unitCost),
    );
    const uniformCostCurrency = uniformText(
      variants.map((variant) => variant.costCurrency),
    );
    const uniformExistingCompareAtPrice = uniformMoney(
      variants.map((variant) => variant.compareAtPrice),
    );
    const explicitCompareAtPrice = commercialNumber(product, "compare_at_price");
    const homogeneousVariantPricing = Boolean(
      variants.length &&
      uniformCurrentPrice !== null &&
      (
        variants.length === 1 ||
        (uniformUnitCost !== null && uniformCostCurrency !== null)
      ),
    );
    const pricePublishable = Boolean(
      PRICE_PUBLISH_ENABLED &&
      homogeneousVariantPricing &&
      preliminaryPricing.state === "ready_for_approval" &&
      recommendedPrice !== null,
    );
    const compareAtPrice = (
      COMPARE_AT_PRICE_PUBLISH_ENABLED &&
      pricePublishable &&
      recommendedPrice !== null
    )
      ? [
          explicitCompareAtPrice,
          uniformExistingCompareAtPrice,
          uniformCurrentPrice,
        ].find(
          (value): value is number =>
            value !== null && value > recommendedPrice,
        ) ?? null
      : null;

    const decision =
      pricePublishable && recommendedPrice !== null
        ? buildEnterpriseProductDecision(
            product,
            commercialConfig,
            recommendedPrice,
          )
        : preliminaryDecision;
    const c = decision.classification;
    const brandRoute = decision.brandRoute;
    const brandLabel =
      brandRoute.brand === "miss-princess" ? "Miss.Princess" : "MVQueen";
    const claimReviewReasons = productClaimReviewReasons(product);
    const requiresClaimReview = claimReviewReasons.length > 0;
    // Claim-risk products still receive sanitized customer-facing copy while
    // the original source claims remain flagged internally for review. Only
    // genuinely unclassified products block automatic editorial generation.
    const automatedContent =
      c.confidence === "review" || !brandRoute.brand
        ? null
        : buildAutomatedProductContent(product, c, brandLabel);
    const attributeEnrichment = buildCatalogAttributeEnrichment(product, c);
    const attributeMetafields = buildCatalogAttributeMetafields(
      attributeEnrichment,
      c,
      brandRoute.brand,
    );
    const variantGoogleMetafields = buildVariantGoogleMetafields(
      product,
      attributeEnrichment,
      c,
      brandRoute.brand,
    );
    const systemPrefixes = [
      "mvq:department:",
      "mvq:family:",
      "mvq:collection:",
      "mvq:brand:",
      "mvq:tone:",
      "mvq:pricing:",
      "mvq:commercial:",
      "mvq:ads:",
      "mvq:marketing:",
      "mvq:lifecycle:",
    ];
    const retainedTags = (product.tags ?? []).filter(
      (tag) =>
        tag !== "mvq:catalog" &&
        tag !== "mvq:needs-review" &&
        !systemPrefixes.some((prefix) => tag.startsWith(prefix)),
    );
    const mergedTags = Array.from(
      new Set([
        ...retainedTags,
        ...decision.tags,
        ...(requiresClaimReview ? ["mvq:needs-review", "mvq:claim-review"] : []),
      ]),
    );
    const pricing = decision.pricing;
    const commercialHealth = decision.commercialHealth;
    const marketing = decision.marketing;
    const lifecycle = decision.lifecycle;
    const healthData = {
      shop: job.shop,
      productGid: product.id,
      sourceFingerprint: fingerprint,
      policyFingerprint,
      state: decision.commercialHealth.state,
      advertisingEligibility: decision.commercialHealth.advertisingEligibility,
      maxBreakEvenCac: decision.commercialHealth.maxBreakEvenCac,
      maxCacAtTargetMargin: decision.commercialHealth.maxCacAtTargetMargin,
      breakEvenRoas: decision.commercialHealth.breakEvenRoas,
      targetMarginRoasFloor: decision.commercialHealth.targetMarginRoasFloor,
      targetRoas: decision.commercialHealth.targetRoas,
      contributionAfterTargetCac: decision.commercialHealth.contributionAfterTargetCac,
      contributionMarginAfterTargetCac:
        decision.commercialHealth.contributionMarginAfterTargetCac,
    };

    const previousHealth = await prisma.productCommercialHealthState.findUnique({
      where: {
        shop_productGid: {
          shop: job.shop,
          productGid: product.id,
        },
      },
    });

    const healthChanged =
      !previousHealth ||
      previousHealth.sourceFingerprint !== fingerprint ||
      previousHealth.policyFingerprint !== policyFingerprint ||
      previousHealth.state !== decision.commercialHealth.state ||
      previousHealth.advertisingEligibility !==
        decision.commercialHealth.advertisingEligibility;

    await prisma.productCommercialHealthState.upsert({
      where: {
        shop_productGid: {
          shop: job.shop,
          productGid: product.id,
        },
      },
      update: {
        ...healthData,
        stale: false,
        evaluatedAt: new Date(),
      },
      create: {
        ...healthData,
        stale: false,
      },
    });

    if (healthChanged) {
      await prisma.productCommercialHealthSnapshot.create({
        data: healthData,
      });
    }

    const uniformVerifiedUnitCost = uniformMoney(
      variants.map((variant) => variant.unitCost),
    );
    const uniformVerifiedCostCurrency = uniformText(
      variants.map((variant) => variant.costCurrency),
    );
    const verifiedUnitCost =
      uniformVerifiedUnitCost !== null ? String(uniformVerifiedUnitCost) : "";
    const costCurrency = uniformVerifiedCostCurrency ?? "";
    const hasAnyVariantCost = variants.some(
      (variant) => moneyNumber(variant.unitCost) !== null,
    );
    const allVariantsHaveCost =
      variants.length > 0 &&
      variants.every((variant) => moneyNumber(variant.unitCost) !== null);
    const shippingDeliveryEstimate = resolveShippingDeliveryEstimate(
      product.shippingMetafields?.nodes?.find((m) => m.key === "delivery_estimate")?.value,
    );
    const mediaNodes = product.media?.nodes ?? [];
    const repairableAltMedia = mediaNodes
      .map((item, index) => ({ item, index }))
      .filter(({ item }) => needsMediaAltRepair(item.alt));
    const safeMediaAltBase =
      automatedContent?.title ??
      (c.confidence !== "review" ? `${brandLabel} ${c.productType}` : "");
    const mediaAltStatus =
      !mediaNodes.length
        ? "no_media"
        : !repairableAltMedia.length
          ? "complete"
          : !safeMediaAltBase
            ? "needs_review"
            : !MEDIA_ALT_SYNC_ENABLED
              ? "needs_repair"
              : !hasWriteFiles
                ? "write_files_scope_required"
                : "automatic";
    const metafields = [
      ...(VENDOR_NORMALIZATION_ENABLED &&
      product.vendor?.trim() &&
      product.vendor.trim().toLowerCase() !== "mvqueen"
        ? [
            {
              namespace: "catalog",
              key: "source_vendor",
              type: "single_line_text_field",
              value: product.vendor.trim(),
            },
          ]
        : []),
      {
        namespace: "shipping",
        key: "delivery_estimate",
        type: "single_line_text_field",
        value: shippingDeliveryEstimate,
      },
      { namespace: "classification", key: "department", type: "single_line_text_field", value: c.department },
      { namespace: "classification", key: "family", type: "single_line_text_field", value: c.family },
      { namespace: "classification", key: "subcollection", type: "single_line_text_field", value: c.subcollection },
      {
        namespace: "classification",
        key: "style",
        type: "single_line_text_field",
        value:
          brandRoute.brand === "miss-princess"
            ? "Miss.Princess World"
            : brandRoute.brand === "mvqueen"
              ? "MVQueen World"
              : "Needs Review",
      },
      { namespace: "classification", key: "brand_world", type: "single_line_text_field", value: brandRoute.brand ?? "needs_review" },
      { namespace: "classification", key: "brand_tone", type: "single_line_text_field", value: brandRoute.tone },
      { namespace: "catalog", key: "brand_routing_reason", type: "single_line_text_field", value: brandRoute.reason },
      { namespace: "catalog", key: "classification_confidence", type: "single_line_text_field", value: c.confidence },
      {
        namespace: "catalog",
        key: "review_status",
        type: "single_line_text_field",
        value:
          c.confidence === "review"
            ? "needs_classification_review"
            : !brandRoute.brand
              ? "needs_brand_review"
              : requiresClaimReview
                ? "claim_review"
                : "classified",
      },
      {
        namespace: "catalog",
        key: "claim_review_status",
        type: "single_line_text_field",
        value: requiresClaimReview ? "needs_review" : "clear",
      },
      ...(claimReviewReasons.length
        ? [{
            namespace: "catalog",
            key: "claim_review_reasons",
            type: "list.single_line_text_field",
            value: JSON.stringify(claimReviewReasons),
          }]
        : []),
      ...attributeMetafields,
      ...(EDITORIAL_PUBLISH_ENABLED && automatedContent
        ? [
            {
              namespace: "catalog",
              key: "short_description",
              type: "single_line_text_field",
              value: automatedContent.shortDescription,
            },
            {
              namespace: "catalog",
              key: "focus_keyword",
              type: "single_line_text_field",
              value: automatedContent.focusKeyword,
            },
            {
              namespace: "catalog",
              key: "long_tail_keywords",
              type: "list.single_line_text_field",
              value: JSON.stringify(automatedContent.longTailKeywords),
            },
            {
              namespace: "catalog",
              key: "seo_keywords",
              type: "list.single_line_text_field",
              value: JSON.stringify(automatedContent.seoKeywords),
            },
            ...(automatedContent.highlights.length
              ? [
                  {
                    namespace: "catalog",
                    key: "highlights",
                    type: "list.single_line_text_field",
                    value: JSON.stringify(automatedContent.highlights),
                  },
                ]
              : []),
            ...(AUTO_CONTENT_SURFACES_ENABLED
              ? [
                  {
                    namespace: "content",
                    key: "faq",
                    type: "json",
                    value: JSON.stringify(
                      buildAutomatedProductFaq(product, c, automatedContent, brandLabel),
                    ),
                  },
                ]
              : []),
          ]
        : []),
      ...(verifiedUnitCost
        ? [
            { namespace: "commercial", key: "unit_cost", type: "number_decimal", value: verifiedUnitCost },
            { namespace: "commercial", key: "cost_currency", type: "single_line_text_field", value: costCurrency || pricing.currency },
            { namespace: "commercial", key: "cost_source", type: "single_line_text_field", value: "Shopify inventoryItem.unitCost" },
          ]
        : []),
      {
        namespace: "commercial",
        key: "cost_sync_state",
        type: "single_line_text_field",
        value: !COST_SYNC_ENABLED
          ? "disabled"
          : hasReadInventory
            ? verifiedUnitCost && costCurrency
              ? "verified"
              : hasAnyVariantCost && allVariantsHaveCost
                ? "variant_cost_or_currency_mismatch"
                : hasAnyVariantCost
                  ? "partial_variant_costs"
                  : "no_cost_value"
            : "read_inventory_scope_required",
      },
      { namespace: "commercial", key: "pricing_state", type: "single_line_text_field", value: pricing.state },
      { namespace: "commercial", key: "pricing_currency", type: "single_line_text_field", value: pricing.currency },
      {
        namespace: "commercial",
        key: "pricing_publishable",
        type: "boolean",
        value: pricePublishable ? "true" : "false",
      },
      {
        namespace: "commercial",
        key: "compare_at_publishable",
        type: "boolean",
        value:
          COMPARE_AT_PRICE_PUBLISH_ENABLED && compareAtPrice !== null
            ? "true"
            : "false",
      },
      ...(pricing.minimumPrice !== null
        ? [{ namespace: "commercial", key: "minimum_viable_price", type: "number_decimal", value: String(pricing.minimumPrice) }]
        : []),
      ...(pricing.recommendedPrice !== null
        ? [{ namespace: "commercial", key: "recommended_price", type: "number_decimal", value: String(pricing.recommendedPrice) }]
        : []),
      ...(pricing.estimatedContributionDollars !== null
        ? [{ namespace: "commercial", key: "estimated_contribution", type: "number_decimal", value: String(pricing.estimatedContributionDollars) }]
        : []),
      { namespace: "commercial", key: "health_state", type: "single_line_text_field", value: commercialHealth.state },
      { namespace: "commercial", key: "advertising_eligibility", type: "single_line_text_field", value: commercialHealth.advertisingEligibility },
      ...(commercialHealth.maxBreakEvenCac !== null
        ? [{ namespace: "commercial", key: "max_break_even_cac", type: "number_decimal", value: String(commercialHealth.maxBreakEvenCac) }]
        : []),
      ...(commercialHealth.maxCacAtTargetMargin !== null
        ? [{ namespace: "commercial", key: "max_cac_at_target_margin", type: "number_decimal", value: String(commercialHealth.maxCacAtTargetMargin) }]
        : []),
      ...(commercialHealth.breakEvenRoas !== null
        ? [{ namespace: "commercial", key: "break_even_roas", type: "number_decimal", value: String(commercialHealth.breakEvenRoas) }]
        : []),
      ...(commercialHealth.targetMarginRoasFloor !== null
        ? [{ namespace: "commercial", key: "target_margin_roas_floor", type: "number_decimal", value: String(commercialHealth.targetMarginRoasFloor) }]
        : []),
      ...(commercialHealth.targetRoas !== null
        ? [{ namespace: "commercial", key: "target_roas", type: "number_decimal", value: String(commercialHealth.targetRoas) }]
        : []),
      ...(commercialHealth.contributionAfterTargetCac !== null
        ? [{ namespace: "commercial", key: "contribution_after_target_cac", type: "number_decimal", value: String(commercialHealth.contributionAfterTargetCac) }]
        : []),
      ...(commercialHealth.contributionMarginAfterTargetCac !== null
        ? [{ namespace: "commercial", key: "contribution_margin_after_target_cac", type: "number_decimal", value: String(commercialHealth.contributionMarginAfterTargetCac) }]
        : []),
      { namespace: "marketing", key: "campaign_state", type: "single_line_text_field", value: marketing.state },
      { namespace: "marketing", key: "paid_planning_eligibility", type: "single_line_text_field", value: marketing.paidPlanningEligibility },
      { namespace: "marketing", key: "brand_world", type: "single_line_text_field", value: marketing.brandWorld },
      { namespace: "marketing", key: "positioning", type: "multi_line_text_field", value: marketing.positioning },
      { namespace: "marketing", key: "paid_execution", type: "single_line_text_field", value: marketing.paidExecution },
      { namespace: "lifecycle", key: "plan_state", type: "single_line_text_field", value: lifecycle.state },
      { namespace: "lifecycle", key: "execution_state", type: "single_line_text_field", value: lifecycle.execution },
      { namespace: "analytics", key: "measurement_key", type: "single_line_text_field", value: decision.measurementKey },
      {
        namespace: "catalog",
        key: "media_alt_status",
        type: "single_line_text_field",
        value: mediaAltStatus,
      },
    ];

    const productAuthorized =
      AUTO_PRODUCT_ENROLLMENT_ENABLED || APPROVED_PRODUCT_GIDS.has(product.id);

    if (!WRITE_ENABLED || !invocationWritesAllowed || !productAuthorized) {
      const reason = !WRITE_ENABLED
        ? "DRY_RUN — Shopify writes disabled"
        : !invocationWritesAllowed
          ? "DRY_RUN — this invocation is explicitly read/evaluate only"
          : "DRY_RUN — automatic enrollment disabled and product GID not explicitly approved";
      await prisma.productJob.update({
        where: { id: jobId },
        data: { status: "completed", completedAt: new Date(), error: reason },
      });
      logMvqueenEvent("product.job.completed", {
        correlationId,
        jobId,
        shop: job.shop,
        productGid: product.id,
        productTitle: product.title,
        topic: job.topic,
        result: "dry_run",
        reason,
        protectedFieldsPreserved: ["handle", "sku", "barcode", "inventory"],
      });
      return;
    }

    const mappedTaxonomyCategory = taxonomyCategoryForRoute(c.route, product.title ?? "");
    const nativeCategoryMetafields =
      CATEGORY_METAFIELDS_ENABLED &&
      hasWriteMetaobjects &&
      rawProduct.category?.id
        ? await buildShopifyCategoryMetafields({
            admin: admin as unknown as {
              graphql: (
                query: string,
                options?: { variables?: Record<string, unknown> },
              ) => Promise<Response>;
            },
            categoryId: rawProduct.category.id,
            product,
            enrichment: attributeEnrichment,
            classification: c,
          })
        : [];

    const productInput: Record<string, unknown> = {
      id: product.id,
      productType: productTypeForWrite(product.productType, c),
      tags: mergedTags,
      metafields: [...metafields, ...nativeCategoryMetafields],
    };
    if (!rawProduct.category?.id && mappedTaxonomyCategory) {
      productInput.category = mappedTaxonomyCategory;
    }

    if (
      VENDOR_NORMALIZATION_ENABLED &&
      product.vendor?.trim() &&
      product.vendor.trim().toLowerCase() !== "mvqueen"
    ) {
      productInput.vendor = "MVQueen";
    }

    if (EDITORIAL_PUBLISH_ENABLED && automatedContent) {
      if (TITLE_PUBLISH_ENABLED) {
        productInput.title = automatedContent.title;
        // Preserve the current handle when an automated title publication is
        // explicitly enabled so a content change cannot change the product URL.
        if (product.handle?.trim()) productInput.handle = product.handle;
      }

      if (
        DESCRIPTION_PUBLISH_ENABLED &&
        shouldPublishAutomatedDescription({
          topic: job.topic,
          currentDescriptionHtml: product.descriptionHtml,
          allowExistingRewrite: DESCRIPTION_REWRITE_EXISTING_ENABLED,
        })
      ) {
        productInput.descriptionHtml = automatedContent.descriptionHtml;
      }

      if (SEO_PUBLISH_ENABLED) {
        productInput.seo = {
          title: automatedContent.seoTitle,
          description: automatedContent.metaDescription,
        };
      }
    }

    const productFields = Object.keys(productInput).filter((key) => key !== "id");
    logMvqueenEvent("product.job.write_planned", {
      correlationId,
      jobId,
      shop: job.shop,
      productGid: product.id,
      productTitle: product.title,
      topic: job.topic,
      productFields,
      variantPriceWriteEnabled: pricePublishable && recommendedPrice !== null,
      compareAtPriceWriteEnabled: COMPARE_AT_PRICE_PUBLISH_ENABLED && compareAtPrice !== null,
      mediaAltWriteCount:
        MEDIA_ALT_SYNC_ENABLED && hasWriteFiles && safeMediaAltBase
          ? repairableAltMedia.length
          : 0,
      protectedFieldsPreserved: ["handle", "sku", "barcode", "inventory"],
    });

    const update = await admin.graphql(PRODUCT_UPDATE, {
      variables: { product: productInput },
    });
    const updateBody = await update.json();
    const errors = updateBody.data?.productUpdate?.userErrors ?? [];
    if (errors.length) throw new Error(errors.map((e: { message: string }) => e.message).join("; "));

    // Media ALT updates use Shopify's Files mutation and require an additional
    // Files write scope. The catalog worker deliberately does not attempt that
    // mutation unless a separately governed media capability is authorized.
    const updatedAt = updateBody.data?.productUpdate?.product?.updatedAt;
    if (!updatedAt) throw new Error("Shopify product update did not return updatedAt");

    // Record Shopify's own update timestamp immediately so the resulting
    // products/update webhook is suppressed, but keep the automation version
    // pending until every downstream surface succeeds. Failed ALT/blog/
    // collection work therefore remains retryable.
    await prisma.productAutomationState.upsert({
      where: { shop_productGid: { shop: job.shop, productGid: product.id } },
      update: {
        sourceFingerprint: fingerprint,
        lastAutomationUpdatedAt: new Date(updatedAt),
        automationVersion: AUTOMATION_VERSION + ":pending",
      },
      create: {
        shop: job.shop,
        productGid: product.id,
        sourceFingerprint: fingerprint,
        lastAutomationUpdatedAt: new Date(updatedAt),
        automationVersion: AUTOMATION_VERSION + ":pending",
      },
    });

    if (variants.length) {
      const variantInputs: Record<string, unknown>[] = variants.map((variant) => {
        const input: Record<string, unknown> = { id: variant.id };
        const google = variantGoogleMetafields.find((item) => item.id === variant.id);
        if (google?.metafields.length) {
          input.metafields = google.metafields;
        }

        if (pricePublishable && recommendedPrice !== null) {
          input.price = recommendedPrice.toFixed(2);

          if (COMPARE_AT_PRICE_PUBLISH_ENABLED) {
            if (compareAtPrice !== null) {
              input.compareAtPrice = compareAtPrice.toFixed(2);
            } else if (moneyNumber(variant.compareAtPrice) !== null) {
              // A compare-at price must represent a real higher reference price.
              // Clear equal/lower/stale values instead of manufacturing a discount.
              input.compareAtPrice = null;
            }
          }
        }

        return input;
      });

      if (
        variantInputs.some(
          (input) =>
            Object.prototype.hasOwnProperty.call(input, "metafields") ||
            Object.prototype.hasOwnProperty.call(input, "price") ||
            Object.prototype.hasOwnProperty.call(input, "compareAtPrice"),
        )
      ) {
        const variantUpdate = await admin.graphql(PRODUCT_VARIANTS_BULK_UPDATE, {
          variables: {
            productId: product.id,
            variants: variantInputs,
          },
        });
        const variantBody = await variantUpdate.json();
        const variantErrors =
          variantBody.data?.productVariantsBulkUpdate?.userErrors ?? [];
        if (variantErrors.length) {
          throw new Error(
            variantErrors.map((e: { message: string }) => e.message).join("; "),
          );
        }
      }
    }

    if (
      MEDIA_ALT_SYNC_ENABLED &&
      hasWriteFiles &&
      safeMediaAltBase &&
      repairableAltMedia.length
    ) {
      const files = repairableAltMedia.map(({ item, index }) => ({
        id: item.id,
        alt: `${safeMediaAltBase} — product view ${index + 1}`,
      }));
      const mediaUpdate = await admin.graphql(FILE_UPDATE, {
        variables: { files },
      });
      const mediaBody = await mediaUpdate.json();
      const mediaErrors = mediaBody.data?.fileUpdate?.userErrors ?? [];
      if (mediaErrors.length) {
        throw new Error(
          mediaErrors.map((e: { message: string }) => e.message).join("; "),
        );
      }
    }

    if (AUTO_CONTENT_SURFACES_ENABLED && automatedContent) {
      const surfaceRecord = buildAutomaticSurfaceRecord(product, c, automatedContent, brandLabel);
      await publishAutomaticContentSurfaces(
        admin as unknown as {
          graphql: (
            query: string,
            options?: { variables?: Record<string, unknown> },
          ) => Promise<Response>;
        },
        surfaceRecord,
      );
    }

    await prisma.productAutomationState.update({
      where: { shop_productGid: { shop: job.shop, productGid: product.id } },
      data: {
        sourceFingerprint: fingerprint,
        automationVersion: AUTOMATION_VERSION,
      },
    });

    await prisma.productJob.update({
      where: { id: jobId },
      data: { status: "completed", completedAt: new Date() },
    });
    logMvqueenEvent("product.job.completed", {
      correlationId,
      jobId,
      shop: job.shop,
      productGid: product.id,
      productTitle: product.title,
      topic: job.topic,
      result: "success",
      productFields,
      protectedFieldsPreserved: ["handle", "sku", "barcode", "inventory"],
    });
  } catch (error) {
    await prisma.productJob.update({
      where: { id: jobId },
      data: { status: "failed", error: error instanceof Error ? error.message : String(error) },
    });
    logMvqueenEvent(
      "product.job.failed",
      {
        correlationId,
        jobId,
        shop: job.shop,
        productGid: job.productGid,
        topic: job.topic,
        ...errorFields(error),
      },
      "error",
    );
    throw error;
  }
}
