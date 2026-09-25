import { createHash } from "node:crypto";
import type { ActionFunctionArgs, LoaderFunctionArgs } from "react-router";
import { useActionData, useLoaderData } from "react-router";
import { authenticate } from "../shopify.server";
import prisma from "../db.server";
import { buildPricingDecision } from "../lib/enterprise/pricing-engine";
import { getCommercialConfig } from "../lib/enterprise/commercial-config";

const PRICING_TARGET_QUERY = `#graphql
query MVQueenPricingTarget($id: ID!) {
  product(id: $id) {
    id
    title
    variants(first: 2) {
      nodes { id price compareAtPrice }
      pageInfo { hasNextPage }
    }
    commercialMetafields: metafields(first: 20, namespace: "commercial") {
      nodes { key value type }
    }
  }
}
`;

const PRICE_UPDATE_MUTATION = `#graphql
mutation MVQueenApprovedPricePublish($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
  productVariantsBulkUpdate(productId: $productId, variants: $variants, allowPartialUpdates: false) {
    productVariants { id price compareAtPrice }
    userErrors { field message }
  }
}
`;

function approvedProductIds(): Set<string> {
  return new Set(
    (process.env.MVQ_APPROVED_PRODUCT_GIDS ?? "")
      .split(",")
      .map((value) => value.trim())
      .filter(Boolean),
  );
}

function numberValue(value: unknown): number | null {
  const n = Number(value);
  return Number.isFinite(n) && n >= 0 ? n : null;
}

function pricingFingerprint(input: Record<string, unknown>): string {
  return createHash("sha256").update(JSON.stringify(input), "utf8").digest("hex");
}

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const { session } = await authenticate.admin(request);
  const commercial = getCommercialConfig();
  const recent = await prisma.productReleaseAudit.findMany({
    where: { shop: session.shop, operation: "PRICE_PUBLISH" },
    orderBy: { createdAt: "desc" },
    take: 10,
    select: {
      id: true,
      productGid: true,
      actor: true,
      result: true,
      error: true,
      createdAt: true,
    },
  });

  return {
    shop: session.shop,
    globalWritesEnabled: process.env.MVQ_WRITE_ENABLED === "true",
    pricePublishEnabled: process.env.MVQ_PRICE_PUBLISH_ENABLED === "true",
    commercialConfigReady: commercial.missing.length === 0,
    commercialMissing: commercial.missing,
    recent,
  };
};

export const action = async ({ request }: ActionFunctionArgs) => {
  const { admin, session } = await authenticate.admin(request);
  const form = await request.formData();
  const productGid = String(form.get("productGid") ?? "").trim();
  const approvedPrice = numberValue(form.get("approvedPrice"));

  if (!productGid.startsWith("gid://shopify/Product/")) {
    return { ok: false, message: "Enter a valid Shopify product GID." };
  }
  if (approvedPrice === null || approvedPrice <= 0) {
    return { ok: false, message: "Approved price must be a positive number." };
  }

  const actor = session.id;
  const audit = async (fingerprint: string, result: string, error: string | null = null) => {
    await prisma.productReleaseAudit.create({
      data: {
        shop: session.shop,
        productGid,
        contentFingerprint: fingerprint,
        actor,
        decision: "APPROVED_PRICE",
        operation: "PRICE_PUBLISH",
        result,
        error,
      },
    });
  };

  if (process.env.MVQ_WRITE_ENABLED !== "true") {
    const fp = pricingFingerprint({ productGid, approvedPrice, blocked: "global_write_gate" });
    await audit(fp, "BLOCKED", "MVQ_WRITE_ENABLED is false");
    return { ok: false, message: "Blocked: global Shopify write gate is disabled." };
  }
  if (process.env.MVQ_PRICE_PUBLISH_ENABLED !== "true") {
    const fp = pricingFingerprint({ productGid, approvedPrice, blocked: "price_publish_gate" });
    await audit(fp, "BLOCKED", "MVQ_PRICE_PUBLISH_ENABLED is false");
    return { ok: false, message: "Blocked: approved price publishing is disabled." };
  }
  if (!approvedProductIds().has(productGid)) {
    const fp = pricingFingerprint({ productGid, approvedPrice, blocked: "product_not_approved" });
    await audit(fp, "BLOCKED", "Product GID is not explicitly approved");
    return { ok: false, message: "Blocked: product GID is not explicitly approved." };
  }

  const response = await admin.graphql(PRICING_TARGET_QUERY, { variables: { id: productGid } });
  const body = await response.json();
  const product = body.data?.product;
  if (!product) {
    const fp = pricingFingerprint({ productGid, approvedPrice, blocked: "not_found" });
    await audit(fp, "FAILED", "Shopify product not found");
    return { ok: false, message: "Shopify product not found." };
  }

  const variants = product.variants?.nodes ?? [];
  if (variants.length !== 1 || product.variants?.pageInfo?.hasNextPage) {
    const fp = pricingFingerprint({ productGid, approvedPrice, blocked: "multi_variant" });
    await audit(fp, "BLOCKED", "Variant-level cost model required for multi-variant products");
    return {
      ok: false,
      message: "Blocked: multi-variant products require variant-level costs and a variant-specific pricing workflow.",
    };
  }

  const commercial = new Map(
    (product.commercialMetafields?.nodes ?? []).map((item: { key: string; value: string }) => [item.key, item.value]),
  );

  const decision = buildPricingDecision({
    currentPrice: numberValue(variants[0].price),
    unitCost: numberValue(commercial.get("unit_cost")),
    inboundShipping: numberValue(commercial.get("inbound_shipping")),
  });

  const fingerprint = pricingFingerprint({
    productGid,
    variantId: variants[0].id,
    currentPrice: variants[0].price,
    approvedPrice,
    unitCost: commercial.get("unit_cost") ?? null,
    inboundShipping: commercial.get("inbound_shipping") ?? null,
    state: decision.state,
    minimumPrice: decision.minimumPrice,
  });

  if (decision.state !== "ready_for_approval" || decision.minimumPrice === null) {
    await audit(fingerprint, "BLOCKED", `Pricing engine state: ${decision.state}; missing: ${decision.missing.join(", ")}`);
    return {
      ok: false,
      message: `Blocked: pricing decision is ${decision.state}. Missing/required inputs: ${decision.missing.join(", ") || "review configuration"}.`,
    };
  }

  if (approvedPrice + 0.0001 < decision.minimumPrice) {
    await audit(fingerprint, "BLOCKED", `Approved price ${approvedPrice} is below floor ${decision.minimumPrice}`);
    return {
      ok: false,
      message: `Blocked: approved price $${approvedPrice.toFixed(2)} is below the calculated contribution floor of $${decision.minimumPrice.toFixed(2)}.`,
    };
  }

  const prior = await prisma.productReleaseAudit.findFirst({
    where: {
      shop: session.shop,
      productGid,
      contentFingerprint: fingerprint,
      operation: "PRICE_PUBLISH",
      result: "SUCCESS",
    },
  });
  if (prior) {
    await audit(fingerprint, "ALREADY_PUBLISHED");
    return { ok: true, message: "This exact approved price decision was already published. No duplicate write was performed." };
  }

  try {
    const update = await admin.graphql(PRICE_UPDATE_MUTATION, {
      variables: {
        productId: productGid,
        variants: [{ id: variants[0].id, price: approvedPrice.toFixed(2) }],
      },
    });
    const updateBody = await update.json();
    const userErrors = updateBody.data?.productVariantsBulkUpdate?.userErrors ?? [];

    if (userErrors.length) {
      const message = userErrors
        .map((error: { field?: string[] | null; message: string }) =>
          `${error.field?.join(".") || "variant"}: ${error.message}`,
        )
        .join("; ");
      await audit(fingerprint, "FAILED", message);
      return { ok: false, message };
    }

    await audit(fingerprint, "SUCCESS");
    const published = updateBody.data?.productVariantsBulkUpdate?.productVariants?.[0];
    return {
      ok: true,
      message: `Approved price published for ${product.title}: $${published?.price ?? approvedPrice.toFixed(2)}. Compare-at price, SKU, inventory, options and media were not changed.`,
    };
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    await audit(fingerprint, "FAILED", message);
    return { ok: false, message };
  }
};

export default function PricingPublisher() {
  const loaderData = useLoaderData<typeof loader>();
  const actionData = useActionData<typeof action>();

  return (
    <s-page heading="Pricing & Profitability">
      <s-section heading="Pricing gates">
        <s-paragraph>Shop: {loaderData.shop}</s-paragraph>
        <s-paragraph>Global Shopify writes: {loaderData.globalWritesEnabled ? "enabled" : "disabled"}</s-paragraph>
        <s-paragraph>Approved price publishing: {loaderData.pricePublishEnabled ? "enabled" : "disabled"}</s-paragraph>
        <s-paragraph>Commercial configuration: {loaderData.commercialConfigReady ? "ready" : "incomplete"}</s-paragraph>
        <s-paragraph>
          Missing commercial inputs: {loaderData.commercialMissing.length ? loaderData.commercialMissing.join(", ") : "none"}
        </s-paragraph>
      </s-section>

      <s-section heading="Publish an approved price">
        <form method="post">
          <div style={{ marginBottom: "12px" }}>
            <label htmlFor="productGid">Shopify product GID</label>
            <input id="productGid" name="productGid" style={{ display: "block", width: "100%", marginTop: "6px" }} />
          </div>
          <div style={{ marginBottom: "12px" }}>
            <label htmlFor="approvedPrice">Approved selling price</label>
            <input id="approvedPrice" name="approvedPrice" type="number" min="0.01" step="0.01" style={{ display: "block", width: "100%", marginTop: "6px" }} />
          </div>
          <button type="submit">Validate floor and publish approved price</button>
        </form>
        {actionData?.message ? <p>{actionData.message}</p> : null}
      </s-section>

      <s-section heading="Recent pricing audit">
        {loaderData.recent.length ? (
          loaderData.recent.map((item) => (
            <s-paragraph key={item.id}>
              {item.result} · {item.productGid} · {new Date(item.createdAt).toLocaleString()}
              {item.error ? ` · ${item.error}` : ""}
            </s-paragraph>
          ))
        ) : (
          <s-paragraph>No pricing publication attempts recorded yet.</s-paragraph>
        )}
      </s-section>
    </s-page>
  );
}
