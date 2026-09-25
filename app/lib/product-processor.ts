import { createHash } from "node:crypto";
import prisma from "../db.server";
import { unauthenticated } from "../shopify.server";
import { brandRoutingTags, classifyBrandWorld, classifyProduct, type Classification, type ProductSnapshot } from "./mvqueen-intelligence";

const AUTOMATION_VERSION = "mvq-classification-brand-routing-v3";

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
  });

  return createHash("sha256").update(source).digest("hex");
}

function slug(value: string): string {
  return value
    .toLowerCase()
    .replace(/&/g, "and")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

function routingTags(c: Classification): string[] {
  return [
    "mvq:catalog",
    `mvq:department:${slug(c.department)}`,
    `mvq:family:${slug(c.family)}`,
    `mvq:collection:${slug(c.route)}`,
    ...(c.confidence === "review" ? ["mvq:needs-review"] : []),
  ];
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

    const c = classifyProduct(product.title ?? "", product.descriptionHtml ?? "", product.productType ?? "");
    const brandRoute = classifyBrandWorld(product);
    const retainedTags = (product.tags ?? []).filter(
      (tag) => !tag.startsWith("mvq:brand:") && !tag.startsWith("mvq:tone:"),
    );
    const mergedTags = Array.from(
      new Set([...retainedTags, ...routingTags(c), ...brandRoutingTags(brandRoute)]),
    );
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
      {
        namespace: "classification",
        key: "brand_world",
        type: "single_line_text_field",
        value: brandRoute.brand ?? "needs_review",
      },
      {
        namespace: "classification",
        key: "brand_tone",
        type: "single_line_text_field",
        value: brandRoute.tone,
      },
      {
        namespace: "catalog",
        key: "brand_routing_reason",
        type: "single_line_text_field",
        value: brandRoute.reason,
      },
      { namespace: "catalog", key: "classification_confidence", type: "single_line_text_field", value: c.confidence },
      { namespace: "catalog", key: "review_status", type: "single_line_text_field", value: c.confidence === "review" ? "needs_review" : "classified" },
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
      const fileUpdate = await admin.graphql(FILE_UPDATE, {
        variables: { files: media.map((m) => ({ id: m.id, alt: `${alt} | MVQueen` })) },
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
