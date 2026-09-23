import { createHash } from "node:crypto";
import prisma from "../db.server";
import { unauthenticated } from "../shopify.server";
import { generateCatalogPackage, type ProductSnapshot } from "./mvqueen-intelligence";

const AUTOMATION_VERSION = "mvq-catalog-v1";

// Fail closed: live Shopify writes and replacement of existing editorial/SEO
// content both require explicit environment gates.
const WRITE_ENABLED = process.env.MVQ_WRITE_ENABLED === "true";
const CONTENT_REWRITE_ENABLED = process.env.MVQ_CONTENT_REWRITE_ENABLED === "true";

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

    const pkg = generateCatalogPackage(product);
    const mergedTags = Array.from(new Set([...(product.tags ?? []), ...pkg.tags]));
    const descriptionHtml = CONTENT_REWRITE_ENABLED || !product.descriptionHtml?.trim()
      ? pkg.descriptionHtml
      : product.descriptionHtml;
    const seoTitle = CONTENT_REWRITE_ENABLED ? pkg.seoTitle : undefined;
    const seoDescription = CONTENT_REWRITE_ENABLED ? pkg.seoDescription : undefined;
    const metafields = [
      { namespace: "classification", key: "department", type: "single_line_text_field", value: pkg.c.department },
      { namespace: "classification", key: "family", type: "single_line_text_field", value: pkg.c.family },
      { namespace: "classification", key: "subcollection", type: "single_line_text_field", value: pkg.c.subcollection },
      { namespace: "classification", key: "style", type: "single_line_text_field", value: "MVQueen Edit" },
      ...(pkg.attributes.material ? [{ namespace: "attributes", key: "material", type: "single_line_text_field", value: pkg.attributes.material }] : []),
      ...(pkg.attributes.color ? [{ namespace: "attributes", key: "color", type: "single_line_text_field", value: pkg.attributes.color }] : []),
      ...(pkg.attributes.fit ? [{ namespace: "attributes", key: "fit", type: "single_line_text_field", value: pkg.attributes.fit }] : []),
      ...(pkg.attributes.occasion ? [{ namespace: "attributes", key: "occasion", type: "single_line_text_field", value: pkg.attributes.occasion }] : []),
      { namespace: "catalog", key: "short_description", type: "single_line_text_field", value: pkg.shortDescription },
      { namespace: "catalog", key: "seo_keywords", type: "list.single_line_text_field", value: JSON.stringify(pkg.keywords) },
      { namespace: "catalog", key: "classification_confidence", type: "single_line_text_field", value: pkg.c.confidence },
      { namespace: "catalog", key: "review_status", type: "single_line_text_field", value: pkg.c.confidence === "review" ? "needs_review" : "ready" },
    ];

    if (!WRITE_ENABLED) {
      await prisma.productJob.update({
        where: { id: jobId },
        data: { status: "completed", completedAt: new Date(), error: "DRY_RUN — Shopify writes disabled" },
      });
      return;
    }

    const productInput: Record<string, unknown> = {
      id: product.id,
      title: CONTENT_REWRITE_ENABLED && pkg.title !== product.title ? pkg.title : product.title,
      descriptionHtml,
      productType: product.productType?.trim() ? product.productType : pkg.c.productType,
      tags: mergedTags,
      metafields,
    };
    if (seoTitle || seoDescription) productInput.seo = { title: seoTitle, description: seoDescription };

    const update = await admin.graphql(PRODUCT_UPDATE, {
      variables: { product: productInput },
    });
    const updateBody = await update.json();
    const errors = updateBody.data?.productUpdate?.userErrors ?? [];
    if (errors.length) throw new Error(errors.map((e: { message: string }) => e.message).join("; "));

    const media = (product.media ?? []).filter((m) => m.id && !m.alt);
    if (media.length) {
      const fileUpdate = await admin.graphql(FILE_UPDATE, {
        variables: { files: media.map((m) => ({ id: m.id, alt: `${pkg.title} | MVQueen` })) },
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
