import type { ActionFunctionArgs, LoaderFunctionArgs } from "react-router";
import { useActionData, useLoaderData } from "react-router";
import { authenticate } from "../shopify.server";
import prisma from "../db.server";
import {
  buildApprovedEditorialProductInput,
  validateApprovedReleaseBundle,
  type ApprovedReleaseBundle,
} from "../lib/enterprise/canonical-proposal";
import { publishApprovedContentSurfaces } from "../lib/enterprise/content-publisher";

const PRODUCT_FRESHNESS_QUERY = `#graphql
query MVQueenReleaseFreshness($id: ID!) {
  product(id: $id) {
    id
    title
    updatedAt
  }
}
`;

const PRODUCT_EDITORIAL_UPDATE = `#graphql
mutation MVQueenApprovedEditorialPublish($product: ProductUpdateInput!) {
  productUpdate(product: $product) {
    product {
      id
      title
      updatedAt
    }
    userErrors {
      field
      message
    }
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

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const { session } = await authenticate.admin(request);
  const recent = await prisma.productReleaseAudit.findMany({
    where: { shop: session.shop },
    orderBy: { createdAt: "desc" },
    take: 10,
    select: {
      id: true,
      productGid: true,
      actor: true,
      operation: true,
      result: true,
      error: true,
      createdAt: true,
    },
  });

  return {
    shop: session.shop,
    editorialPublishEnabled: process.env.MVQ_EDITORIAL_PUBLISH_ENABLED === "true",
    contentSurfacesPublishEnabled: process.env.MVQ_CONTENT_SURFACES_PUBLISH_ENABLED === "true",
    productWritesEnabled: process.env.MVQ_WRITE_ENABLED === "true",
    recent,
  };
};

export const action = async ({ request }: ActionFunctionArgs) => {
  const { admin, session } = await authenticate.admin(request);
  const form = await request.formData();
  const raw = String(form.get("bundle") ?? "").trim();

  if (!raw) return { ok: false, message: "Paste an approved release bundle." };
  if (raw.length > 1_500_000) return { ok: false, message: "Release bundle exceeds the 1.5 MB intake limit." };

  let bundle: ApprovedReleaseBundle;
  try {
    bundle = JSON.parse(raw) as ApprovedReleaseBundle;
  } catch {
    return { ok: false, message: "Release bundle is not valid JSON." };
  }

  const errors = validateApprovedReleaseBundle(bundle);
  if (errors.length) {
    return { ok: false, message: errors.join("; ") };
  }

  const { record, approval } = bundle;
  const productGid = record.identity.product_id;
  const fingerprint = approval.content_fingerprint;
  const operation = "EDITORIAL_PUBLISH";

  const audit = async (result: string, error: string | null = null) => {
    await prisma.productReleaseAudit.create({
      data: {
        shop: session.shop,
        productGid,
        contentFingerprint: fingerprint,
        actor: approval.actor,
        decision: approval.decision,
        operation,
        result,
        error,
      },
    });
  };

  const prior = await prisma.productReleaseAudit.findFirst({
    where: {
      shop: session.shop,
      productGid,
      contentFingerprint: fingerprint,
      operation,
      result: "SUCCESS",
    },
  });
  if (prior) {
    await audit("ALREADY_PUBLISHED");
    return { ok: true, message: "This exact approved product fingerprint was already published. No duplicate write was performed." };
  }

  if (process.env.MVQ_WRITE_ENABLED !== "true") {
    await audit("BLOCKED", "MVQ_WRITE_ENABLED is false");
    return { ok: false, message: "Blocked: global Shopify write gate is disabled." };
  }

  if (process.env.MVQ_EDITORIAL_PUBLISH_ENABLED !== "true") {
    await audit("BLOCKED", "MVQ_EDITORIAL_PUBLISH_ENABLED is false");
    return { ok: false, message: "Blocked: editorial publishing gate is disabled." };
  }

  if (!approvedProductIds().has(productGid)) {
    await audit("BLOCKED", "Product GID is not explicitly approved");
    return { ok: false, message: "Blocked: this product GID is not in MVQ_APPROVED_PRODUCT_GIDS." };
  }

  const freshnessResponse = await admin.graphql(PRODUCT_FRESHNESS_QUERY, {
    variables: { id: productGid },
  });
  const freshnessBody = await freshnessResponse.json();
  const currentProduct = freshnessBody.data?.product;
  if (!currentProduct) {
    await audit("FAILED", "Shopify product not found");
    return { ok: false, message: "Shopify product not found." };
  }

  if (new Date(currentProduct.updatedAt).getTime() > new Date(approval.timestamp).getTime()) {
    await audit("BLOCKED", "Shopify product changed after release approval");
    return {
      ok: false,
      message: "Blocked: the Shopify product changed after this approval was created. Re-run QA and create a fresh approval.",
    };
  }

  const productInput = buildApprovedEditorialProductInput(record);
  productInput.metafields.push(
    {
      namespace: "release",
      key: "content_fingerprint",
      type: "single_line_text_field",
      value: fingerprint,
    },
    {
      namespace: "release",
      key: "approved_by",
      type: "single_line_text_field",
      value: approval.actor,
    },
    {
      namespace: "release",
      key: "approved_at",
      type: "date_time",
      value: new Date(approval.timestamp).toISOString(),
    },
  );

  try {
    const updateResponse = await admin.graphql(PRODUCT_EDITORIAL_UPDATE, {
      variables: { product: productInput },
    });
    const updateBody = await updateResponse.json();
    const userErrors = updateBody.data?.productUpdate?.userErrors ?? [];

    if (userErrors.length) {
      const message = userErrors
        .map((error: { field?: string[] | null; message: string }) =>
          `${error.field?.join(".") || "product"}: ${error.message}`,
        )
        .join("; ");
      await audit("FAILED", message);
      return { ok: false, message };
    }

    await audit("SUCCESS");

    let contentSummary = "governed blog/page/collection publishing disabled";
    if (process.env.MVQ_CONTENT_SURFACES_PUBLISH_ENABLED === "true") {
      try {
        const contentResults = await publishApprovedContentSurfaces(admin, record, approval);
        for (const item of contentResults) {
          await prisma.productReleaseAudit.create({
            data: {
              shop: session.shop,
              productGid,
              contentFingerprint: fingerprint,
              actor: approval.actor,
              decision: approval.decision,
              operation: "CONTENT_" + item.surface.toUpperCase(),
              result: item.status,
              error: item.status === "SKIPPED" ? item.message : null,
            },
          });
        }
        contentSummary = contentResults.map((item) => item.surface + ": " + item.status).join(" · ");
      } catch (contentError) {
        const contentMessage = contentError instanceof Error ? contentError.message : String(contentError);
        await prisma.productReleaseAudit.create({
          data: {
            shop: session.shop,
            productGid,
            contentFingerprint: fingerprint,
            actor: approval.actor,
            decision: approval.decision,
            operation: "CONTENT_PUBLISH",
            result: "FAILED",
            error: contentMessage,
          },
        });
        contentSummary = "content: FAILED (" + contentMessage + ")";
      }
    }

    return {
      ok: true,
      message: `Published approved editorial/SEO release for ${updateBody.data?.productUpdate?.product?.title ?? productGid}. Approved product FAQ/metafields were included in the product release. Content surfaces: ${contentSummary}. Protected price, SKU, inventory, variants, handle and media relationships were not changed.`,
    };
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    await audit("FAILED", message);
    return { ok: false, message };
  }
};

export default function ProposalPublisher() {
  const loaderData = useLoaderData<typeof loader>();
  const actionData = useActionData<typeof action>();

  return (
    <s-page heading="Approved Product Releases">
      <s-section heading="Publishing gates">
        <s-paragraph>Shop: {loaderData.shop}</s-paragraph>
        <s-paragraph>Global product writes: {loaderData.productWritesEnabled ? "enabled" : "disabled"}</s-paragraph>
        <s-paragraph>Editorial publish gate: {loaderData.editorialPublishEnabled ? "enabled" : "disabled"}</s-paragraph>
        <s-paragraph>Governed content-surface gate: {loaderData.contentSurfacesPublishEnabled ? "enabled" : "disabled"}</s-paragraph>
        <s-paragraph>
          Only an exact QA-passed canonical record + matching approval fingerprint + explicitly approved product GID can publish.
        </s-paragraph>
      </s-section>

      <s-section heading="Release bundle">
        <form method="post">
          <label htmlFor="bundle">Approved release bundle JSON</label>
          <textarea
            id="bundle"
            name="bundle"
            rows={18}
            style={{ width: "100%", fontFamily: "monospace", marginTop: "8px", marginBottom: "12px" }}
          />
          <button type="submit">Validate and publish approved editorial release</button>
        </form>
        {actionData?.message ? <p>{actionData.message}</p> : null}
      </s-section>

      <s-section heading="Recent release audit">
        {loaderData.recent.length ? (
          loaderData.recent.map((item) => (
            <s-paragraph key={item.id}>
              {item.result} · {item.operation} · {item.productGid} · {new Date(item.createdAt).toLocaleString()}
              {item.error ? ` · ${item.error}` : ""}
            </s-paragraph>
          ))
        ) : (
          <s-paragraph>No release attempts recorded yet.</s-paragraph>
        )}
      </s-section>
    </s-page>
  );
}
