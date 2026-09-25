import type { LoaderFunctionArgs } from "react-router";
import { useLoaderData } from "react-router";
import { authenticate } from "../shopify.server";
import prisma from "../db.server";
import { getCommercialConfig } from "../lib/enterprise/commercial-config";
import { getEnterpriseIntegrationStatus } from "../lib/enterprise/integration-status";

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const { admin } = await authenticate.admin(request);
  const response = await admin.graphql(`#graphql
    query MVQueenRuntimeHealth {
      shop { name myshopifyDomain currencyCode }
    }
  `);
  const body = await response.json();
  const integrations = getEnterpriseIntegrationStatus();
  const commercial = getCommercialConfig();

  const [receivedJobs, processingJobs, failedJobs] = await Promise.all([
    prisma.productJob.count({ where: { status: "received" } }),
    prisma.productJob.count({ where: { status: "processing" } }),
    prisma.productJob.count({ where: { status: "failed" } }),
  ]);

  return {
    shop: body.data?.shop ?? null,
    runtime: {
      productWrites: process.env.MVQ_WRITE_ENABLED === "true" ? "enabled-with-product-approval" : "dry-run",
      pricing: commercial.missing.length ? "needs-configuration" : "advisory-ready",
      pricingMissing: commercial.missing,
      paidMedia: integrations.paidMedia.state,
      analytics: integrations.analytics.state,
      lifecycle: integrations.lifecycle.state,
      queue: { receivedJobs, processingJobs, failedJobs },
    },
  };
};

export default function Dashboard() {
  const data = useLoaderData<typeof loader>();
  const shop = data.shop;
  const runtime = data.runtime;

  return (
    <s-page heading="MVQueen OS — Enterprise Control Plane">
      <s-section heading="Commerce authority">
        <s-paragraph>
          Connected to {shop?.name ?? "Shopify"} ({shop?.myshopifyDomain ?? "unknown"}) · {shop?.currencyCode ?? "USD"}.
        </s-paragraph>
        <s-paragraph>Shopify remains the authority for live commerce state; GitHub main remains the authority for code, contracts, tests and theme source.</s-paragraph>
      </s-section>

      <s-section heading="Runtime gates">
        <s-paragraph>Product write mode: {runtime.productWrites}</s-paragraph>
        <s-paragraph>Pricing/profitability: {runtime.pricing}</s-paragraph>
        <s-paragraph>
          Pricing configuration gaps: {runtime.pricingMissing.length ? runtime.pricingMissing.join(", ") : "none"}
        </s-paragraph>
      </s-section>

      <s-section heading="External integrations">
        <s-paragraph>Paid media: {runtime.paidMedia}</s-paragraph>
        <s-paragraph>Analytics export: {runtime.analytics}</s-paragraph>
        <s-paragraph>Lifecycle/retention execution: {runtime.lifecycle}</s-paragraph>
        <s-paragraph>Planning remains available when execution adapters are disconnected; money/spend actions remain fail-closed.</s-paragraph>
      </s-section>

      <s-section heading="Product queue">
        <s-paragraph>Received: {runtime.queue.receivedJobs}</s-paragraph>
        <s-paragraph>Processing: {runtime.queue.processingJobs}</s-paragraph>
        <s-paragraph>Failed: {runtime.queue.failedJobs}</s-paragraph>
      </s-section>
    </s-page>
  );
}
