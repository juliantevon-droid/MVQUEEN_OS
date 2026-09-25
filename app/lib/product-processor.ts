import { createHash } from "node:crypto";
import prisma from "../db.server";
import { unauthenticated } from "../shopify.server";
import type { ProductSnapshot } from "./mvqueen-intelligence";
import { buildEnterpriseProductDecision } from "./enterprise/product-decision-engine";

const AUTOMATION_VERSION = "mvq-enterprise-product-decision-v4";

// The React app is a transport/classification worker, not a copy generator.
// Live writes remain fail-closed and require explicit product approval.
const WRITE_ENABLED = process.env.MVQ_WRITE_ENABLED === "true";
const APPROVED_PRODUCT_GIDS = new Set(
  (process.env.MVQ_APPROVED_PRODUCT_GIDS ?? "")
    .split(",")
    .map((value) => value.trim())
    .filter(Boolean),
);

const PRODUCT_QUERY = `#graphql
query MVQueenProduct($id: ID!) {
  product(id: $id) {
    id title descriptionHtml productType vendor tags
    media(first: 100) { nodes { id alt } }
    variants(first: 1) { nodes { id price compareAtPrice } }
    commercialMetafields: metafields(first: 20, namespace: "commercial") {
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
mutation MVQueenFileAlt($files: [FileUpdateInput!]!) {
  fileUpdate(files: $files) {
    files { id }
    userErrors { field message }
  }
}`;

function sourceFingerprint(product: ProductSnapshot): string {
  const source = JSON.stringify({
    title: product.title ?? "",
    descriptionHtml: product.descriptionHtml ?? "",
    productType: product.productType ?? "",
    vendor: product.vendor ?? "",
    tags: [...(product.tags ?? [])].sort(),
    media: (product.media ?? [])
      .map((m) => ({ id: m.id, alt: m.alt ?? "" }))
      .sort((a, b) => a.id.localeCompare(b.id)),
    variants: (product.variants ?? [])
      .map((v) => ({ id: v.id, price: v.price ?? "", compareAtPrice: v.compareAtPrice ?? "" }))
      .sort((a, b) => a.id.localeCompare(b.id)),
    commercialMetafields: (product.commercialMetafields ?? [])
      .map((m) => ({ key: m.key, value: m.value ?? "", type: m.type ?? "" }))
      .sort((a, b) => a.key.localeCompare(b.key)),
  });

  return createHash("sha256").update(source).digest("hex");
}

export async function processProductJob(jobId: string) {
  const job = await prisma.productJob.findUnique({ where: { id: jobId } });
  if (!job) throw new Error("Product job not found");

  await prisma.productJob.update({
    where: { id: jobId },
    data: { status: "processing", attempts: { increment: 1 }, startedAt: new Date(), error: null },
  });

  try {
    const { admin } = await unauthenticated.admin(job.shop);
    const response = await admin.graphql(PRODUCT_QUERY, { variables: { id: job.productGid } });
    const body = await response.json();
    const product: ProductSnapshot | null = body.data?.product ?? null;
    if (!product) throw new Error("Shopify product not found");

    const fingerprint = sourceFingerprint(product);
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

    const decision = buildEnterpriseProductDecision(product);
    const c = decision.classification;
    const brandRoute = decision.brandRoute;
    const systemPrefixes = [
      "mvq:department:",
      "mvq:family:",
      "mvq:collection:",
      "mvq:brand:",
      "mvq:tone:",
      "mvq:pricing:",
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
    const marketing = decision.marketing;
    const lifecycle = decision.lifecycle;
    const metafields = [
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
      { namespace: "marketing", key: "campaign_state", type: "single_line_text_field", value: marketing.state },
      { namespace: "marketing", key: "brand_world", type: "single_line_text_field", value: marketing.brandWorld },
      { namespace: "marketing", key: "positioning", type: "multi_line_text_field", value: marketing.positioning },
      { namespace: "marketing", key: "paid_execution", type: "single_line_text_field", value: marketing.paidExecution },
      { namespace: "lifecycle", key: "plan_state", type: "single_line_text_field", value: lifecycle.state },
      { namespace: "lifecycle", key: "execution_state", type: "single_line_text_field", value: lifecycle.execution },
      { namespace: "analytics", key: "measurement_key", type: "single_line_text_field", value: decision.measurementKey },
    ];

    if (!WRITE_ENABLED || !APPROVED_PRODUCT_GIDS.has(product.id)) {
      const reason = !WRITE_ENABLED
        ? "DRY_RUN — Shopify writes disabled"
        : "DRY_RUN — product GID not explicitly approved";
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

    const update = await admin.graphql(PRODUCT_UPDATE, {
      variables: { product: productInput },
    });
    const updateBody = await update.json();
    const errors = updateBody.data?.productUpdate?.userErrors ?? [];
    if (errors.length) throw new Error(errors.map((e: { message: string }) => e.message).join("; "));

    // Missing ALT text may be filled from the product's existing title only.
    // Canonical editorial/SEO content is produced upstream and is never regenerated here.
    const media = (product.media ?? []).filter((m) => m.id && !m.alt);
    if (media.length) {
      const alt = product.title?.trim() || c.productType;
      const brandName = marketing.brandWorld === "Miss.Princess" ? "Miss.Princess" : "MVQueen";
      const fileUpdate = await admin.graphql(FILE_UPDATE, {
        variables: { files: media.map((m) => ({ id: m.id, alt: `${alt} | ${brandName}` })) },
      });
      const fileBody = await fileUpdate.json();
      const fileErrors = fileBody.data?.fileUpdate?.userErrors ?? [];
      if (fileErrors.length) {
        throw new Error(fileErrors.map((e: { message: string }) => e.message).join("; "));
      }
    }

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
