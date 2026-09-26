import { createHash } from "node:crypto";
import prisma from "../db.server";
import { unauthenticated } from "../shopify.server";
import type { ProductSnapshot } from "./mvqueen-intelligence";
import { buildEnterpriseProductDecision } from "./enterprise/product-decision-engine";
import { buildAutomatedProductContent } from "./product-content-automation";
import { buildAutomatedProductFaq, buildAutomaticSurfaceRecord } from "./automated-content-surfaces";
import { publishAutomaticContentSurfaces } from "./enterprise/content-publisher";
import { resolveShippingDeliveryEstimate } from "./shipping-policy";
import {
  commercialPolicyFingerprint,
  resolveShopCommercialConfig,
} from "./enterprise/commercial-settings.server";

const AUTOMATION_VERSION = "mvq-enterprise-product-decision-v7";

// The React app is the single live Shopify writer. Automatic enrollment may
// authorize newly created/updated products for safe editorial/catalog fields,
// while protected commerce fields remain outside this worker.
const WRITE_ENABLED = process.env.MVQ_WRITE_ENABLED === "true";
const AUTO_PRODUCT_ENROLLMENT_ENABLED =
  process.env.MVQ_AUTO_PRODUCT_ENROLLMENT_ENABLED === "true";
const EDITORIAL_PUBLISH_ENABLED =
  process.env.MVQ_EDITORIAL_PUBLISH_ENABLED === "true";
const AUTO_CONTENT_SURFACES_ENABLED =
  process.env.MVQ_AUTO_CONTENT_SURFACES_ENABLED === "true";
const MEDIA_ALT_SYNC_ENABLED =
  process.env.MVQ_MEDIA_ALT_SYNC_ENABLED === "true";
const COST_SYNC_ENABLED = process.env.MVQ_COST_SYNC_ENABLED === "true";
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

const PRODUCT_QUERY = `#graphql
query MVQueenProduct($id: ID!) {
  product(id: $id) {
    id title handle descriptionHtml productType vendor tags
    media(first: 50) {
      nodes {
        ... on MediaImage { id alt }
      }
    }
    variants(first: 1) { nodes { id price compareAtPrice } }
    commercialMetafields: metafields(first: 20, namespace: "commercial") {
      nodes { key value type }
    }
    shippingMetafields: metafields(first: 10, namespace: "shipping") {
      nodes { key value type }
    }
  }
}`;

const PRODUCT_QUERY_WITH_COST = `#graphql
query MVQueenProductWithCost($id: ID!) {
  product(id: $id) {
    id title handle descriptionHtml productType vendor tags
    media(first: 50) {
      nodes {
        ... on MediaImage { id alt }
      }
    }
    variants(first: 1) {
      nodes {
        id
        price
        compareAtPrice
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


function sourceFingerprint(
  product: ProductSnapshot,
  policyFingerprint: string,
): string {
  const source = JSON.stringify({
    policyFingerprint,
    title: product.title ?? "",
    descriptionHtml: product.descriptionHtml ?? "",
    productType: product.productType ?? "",
    vendor: product.vendor ?? "",
    tags: [...(product.tags ?? [])]
      .filter((tag) => !tag.toLowerCase().startsWith("mvq:"))
      .sort(),
    variants: (product.variants?.nodes ?? [])
      .map((v) => ({
        id: v.id,
        price: v.price ?? "",
        compareAtPrice: v.compareAtPrice ?? "",
        unitCost: v.unitCost ?? "",
        costCurrency: v.costCurrency ?? "",
      }))
      .sort((a, b) => a.id.localeCompare(b.id)),
    commercialMetafields: (product.commercialMetafields?.nodes ?? [])
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
  const job = await prisma.productJob.findUnique({ where: { id: jobId } });
  if (!job) throw new Error("Product job not found");

  await prisma.productJob.update({
    where: { id: jobId },
    data: { status: "processing", attempts: { increment: 1 }, startedAt: new Date(), error: null },
  });

  try {
    const { admin } = await unauthenticated.admin(job.shop);

    let hasReadInventory = false;
    let hasWriteFiles = false;
    if (COST_SYNC_ENABLED || MEDIA_ALT_SYNC_ENABLED) {
      const scopeResponse = await admin.graphql(ACCESS_SCOPES_QUERY);
      const scopeBody = await scopeResponse.json();
      const handles = new Set(
        (scopeBody.data?.appInstallation?.accessScopes ?? [])
          .map((scope: { handle?: string | null }) => scope.handle)
          .filter(Boolean),
      );
      hasReadInventory = handles.has("read_inventory");
      hasWriteFiles = handles.has("write_files");
    }

    const response = await admin.graphql(
      COST_SYNC_ENABLED && hasReadInventory ? PRODUCT_QUERY_WITH_COST : PRODUCT_QUERY,
      { variables: { id: job.productGid } },
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
                inventoryItem?: {
                  unitCost?: { amount?: string | null; currencyCode?: string | null } | null;
                } | null;
              }) => ({
                id: variant.id,
                price: variant.price ?? null,
                compareAtPrice: variant.compareAtPrice ?? null,
                unitCost: variant.inventoryItem?.unitCost?.amount ?? null,
                costCurrency: variant.inventoryItem?.unitCost?.currencyCode ?? null,
              }),
            ),
          },
        }
      : null;
    if (!product) throw new Error("Shopify product not found");

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

    const decision = buildEnterpriseProductDecision(product, commercialConfig);
    const c = decision.classification;
    const brandRoute = decision.brandRoute;
    const automatedContent =
      c.confidence === "review"
        ? null
        : buildAutomatedProductContent(product, c);
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
    const mergedTags = Array.from(new Set([...retainedTags, ...decision.tags]));
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

    const costVariant = product.variants?.nodes?.[0];
    const verifiedUnitCost = costVariant?.unitCost?.trim() || "";
    const costCurrency = costVariant?.costCurrency?.trim() || "";
    const shippingDeliveryEstimate = resolveShippingDeliveryEstimate(
      product.shippingMetafields?.nodes?.find((m) => m.key === "delivery_estimate")?.value,
    );
    const mediaNodes = product.media?.nodes ?? [];
    const missingAltMedia = mediaNodes.filter((item) => !item.alt?.trim());
    const mediaAltStatus =
      !mediaNodes.length
        ? "no_media"
        : !missingAltMedia.length
          ? "complete"
          : !MEDIA_ALT_SYNC_ENABLED
            ? "missing_alt"
            : !hasWriteFiles
              ? "write_files_scope_required"
              : "automatic";
    const metafields = [
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
        value: c.confidence === "review" || !brandRoute.brand ? "needs_review" : "classified",
      },
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
                      buildAutomatedProductFaq(product, c, automatedContent),
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
            ? verifiedUnitCost
              ? "verified"
              : "no_cost_value"
            : "read_inventory_scope_required",
      },
      { namespace: "commercial", key: "pricing_state", type: "single_line_text_field", value: pricing.state },
      { namespace: "commercial", key: "pricing_currency", type: "single_line_text_field", value: pricing.currency },
      {
        namespace: "commercial",
        key: "pricing_publishable",
        type: "boolean",
        value: "false",
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
      return;
    }

    const productInput: Record<string, unknown> = {
      id: product.id,
      productType: product.productType?.trim() ? product.productType : c.productType,
      tags: mergedTags,
      metafields,
    };

    if (EDITORIAL_PUBLISH_ENABLED && automatedContent) {
      productInput.title = automatedContent.title;
      if (product.handle?.trim()) productInput.handle = product.handle;
      productInput.seo = {
        title: automatedContent.seoTitle,
        description: automatedContent.metaDescription,
      };
    }

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

    await prisma.productAutomationState.upsert({
      where: { shop_productGid: { shop: job.shop, productGid: product.id } },
      update: {
        sourceFingerprint: fingerprint,
        lastAutomationUpdatedAt: new Date(updatedAt),
        automationVersion: AUTOMATION_VERSION,
      },
      create: {
        shop: job.shop,
        productGid: product.id,
        sourceFingerprint: fingerprint,
        lastAutomationUpdatedAt: new Date(updatedAt),
        automationVersion: AUTOMATION_VERSION,
      },
    });

    if (
      MEDIA_ALT_SYNC_ENABLED &&
      hasWriteFiles &&
      automatedContent &&
      missingAltMedia.length
    ) {
      const files = missingAltMedia.map((item, index) => ({
        id: item.id,
        alt: `${automatedContent.title} — product view ${index + 1}`,
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
      const surfaceRecord = buildAutomaticSurfaceRecord(product, c, automatedContent);
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

    await prisma.productJob.update({
      where: { id: jobId },
      data: { status: "completed", completedAt: new Date() },
    });
  } catch (error) {
    await prisma.productJob.update({
      where: { id: jobId },
      data: { status: "failed", error: error instanceof Error ? error.message : String(error) },
    });
    throw error;
  }
}
