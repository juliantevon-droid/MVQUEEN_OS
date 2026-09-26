import type { LoaderFunctionArgs } from "react-router";
import { useLoaderData } from "react-router";
import { authenticate } from "../shopify.server";
import prisma from "../db.server";
import { resolveShopCommercialConfig } from "../lib/enterprise/commercial-settings.server";
import { getEnterpriseIntegrationStatus } from "../lib/enterprise/integration-status";
import { databaseProfile } from "../lib/enterprise/database-guard.server";

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const { admin, session } = await authenticate.admin(request);
  const response = (await admin.graphql(`#graphql
    query MVQueenRuntimeHealth {
      shop { name myshopifyDomain currencyCode }
      appInstallation {
        accessScopes { handle }
      }
    }
  `)) as Response;
  const body = (await response.json()) as {
    data?: {
      shop?: { name?: string | null; myshopifyDomain?: string | null; currencyCode?: string | null } | null;
      appInstallation?: { accessScopes?: Array<{ handle?: string | null }> } | null;
    };
  };

  const integrations = getEnterpriseIntegrationStatus();
  const commercial = await resolveShopCommercialConfig(session.shop);
  const scopes = new Set(
    body.data?.appInstallation?.accessScopes
      ?.map((scope) => scope.handle)
      .filter((handle): handle is string => Boolean(handle)) ?? [],
  );

  const costSyncRequested = process.env.MVQ_COST_SYNC_ENABLED === "true";
  const hasReadInventory = scopes.has("read_inventory");
  const costSync = !costSyncRequested
    ? "disabled"
    : hasReadInventory
      ? "ready"
      : "reauthorization-required";

  const [
    receivedJobs,
    processingJobs,
    failedJobs,
    deadLetterJobs,
    commercialEvaluated,
    commercialHealthy,
    commercialStale,
    commercialBlocked,
    advertisingEligible,
  ] = await Promise.all([
    prisma.productJob.count({ where: { status: "received" } }),
    prisma.productJob.count({ where: { status: { in: ["leased", "processing"] } } }),
    prisma.productJob.count({ where: { status: "failed" } }),
    prisma.productJob.count({ where: { status: "dead_letter" } }),
    prisma.productCommercialHealthState.count({ where: { shop: session.shop } }),
    prisma.productCommercialHealthState.count({
      where: { shop: session.shop, state: "healthy", stale: false },
    }),
    prisma.productCommercialHealthState.count({
      where: { shop: session.shop, stale: true },
    }),
    prisma.productCommercialHealthState.count({
      where: {
        shop: session.shop,
        stale: false,
        state: { in: ["blocked", "thin", "needs_configuration", "needs_cost", "needs_price", "invalid_inputs"] },
      },
    }),
    prisma.productCommercialHealthState.count({
      where: { shop: session.shop, advertisingEligibility: "eligible", stale: false },
    }),
  ]);

  return {
    shop: body.data?.shop ?? null,
    runtime: {
      databaseProfile: databaseProfile(),
      productWrites: process.env.MVQ_WRITE_ENABLED === "true" ? "enabled" : "dry-run",
      automaticProductEnrollment:
        process.env.MVQ_AUTO_PRODUCT_ENROLLMENT_ENABLED === "true" ? "enabled" : "manual-allowlist",
      editorialPublish: process.env.MVQ_EDITORIAL_PUBLISH_ENABLED === "true" ? "enabled" : "disabled",
      contentSurfaces: process.env.MVQ_AUTO_CONTENT_SURFACES_ENABLED === "true" ? "enabled" : "disabled",
      reconciliation: process.env.MVQ_PRODUCT_RECONCILE_ENABLED === "true" ? "enabled" : "disabled",
      durableWorker:
        (process.env.MVQ_PRODUCT_WORKER_TOKEN?.trim().length ?? 0) >= 32 ? "configured" : "not-configured",
      mediaAltSync: process.env.MVQ_MEDIA_ALT_SYNC_ENABLED === "true" ? "enabled" : "disabled",
      pricePublish: process.env.MVQ_PRICE_PUBLISH_ENABLED === "true" ? "enabled" : "disabled",
      pricing: commercial.missing.length ? "needs-configuration" : "advisory-ready",
      pricingMissing: commercial.missing,
      costSync,
      hasReadInventory,
      paidMedia: integrations.paidMedia.state,
      analytics: integrations.analytics.state,
      lifecycle: integrations.lifecycle.state,
      queue: { receivedJobs, processingJobs, failedJobs, deadLetterJobs },
      commercialHealth: {
        evaluated: commercialEvaluated,
        healthy: commercialHealthy,
        stale: commercialStale,
        blockedOrReview: commercialBlocked,
        advertisingEligible,
      },
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
        <s-paragraph>
          Shopify remains the authority for live commerce state; GitHub main remains the authority for code, contracts, tests and theme source.
        </s-paragraph>
        <s-paragraph>Database profile: {runtime.databaseProfile}</s-paragraph>
      </s-section>

      <s-section heading="Runtime gates">
        <s-paragraph>Product write mode: {runtime.productWrites}</s-paragraph>
        <s-paragraph>Automatic product enrollment: {runtime.automaticProductEnrollment}</s-paragraph>
        <s-paragraph>Automatic editorial/SEO publishing: {runtime.editorialPublish}</s-paragraph>
        <s-paragraph>FAQ/blog/collection content surfaces: {runtime.contentSurfaces}</s-paragraph>
        <s-paragraph>Missed-webhook reconciliation: {runtime.reconciliation}</s-paragraph>
        <s-paragraph>Durable worker secret: {runtime.durableWorker}</s-paragraph>
        <s-paragraph>Automatic missing-ALT repair: {runtime.mediaAltSync}</s-paragraph>
        <s-paragraph>Approved price publishing: {runtime.pricePublish}</s-paragraph>
        <s-paragraph>Pricing/profitability: {runtime.pricing}</s-paragraph>
        <s-paragraph>
          Pricing configuration gaps: {runtime.pricingMissing.length ? runtime.pricingMissing.join(", ") : "none"}
        </s-paragraph>
      </s-section>

      <s-section heading="Commercial source truth">
        <s-paragraph>Shopify unit-cost sync: {runtime.costSync}</s-paragraph>
        <s-paragraph>read_inventory granted: {runtime.hasReadInventory ? "yes" : "no"}</s-paragraph>
        <s-paragraph>
          Cost sync remains fail-closed until Shopify grants read_inventory and MVQ_COST_SYNC_ENABLED=true.
        </s-paragraph>
      </s-section>

      <s-section heading="Commercial health">
        <s-paragraph>Evaluated products: {runtime.commercialHealth.evaluated}</s-paragraph>
        <s-paragraph>Healthy: {runtime.commercialHealth.healthy}</s-paragraph>
        <s-paragraph>Advertising eligible: {runtime.commercialHealth.advertisingEligible}</s-paragraph>
        <s-paragraph>Blocked/review: {runtime.commercialHealth.blockedOrReview}</s-paragraph>
        <s-paragraph>Stale after policy change: {runtime.commercialHealth.stale}</s-paragraph>
      </s-section>

      <s-section heading="External integrations">
        <s-paragraph>Paid media: {runtime.paidMedia}</s-paragraph>
        <s-paragraph>Analytics export: {runtime.analytics}</s-paragraph>
        <s-paragraph>Lifecycle/retention execution: {runtime.lifecycle}</s-paragraph>
        <s-paragraph>
          Planning remains available when execution adapters are disconnected; money/spend actions remain fail-closed.
        </s-paragraph>
      </s-section>

      <s-section heading="Product queue">
        <s-paragraph>Received: {runtime.queue.receivedJobs}</s-paragraph>
        <s-paragraph>Processing: {runtime.queue.processingJobs}</s-paragraph>
        <s-paragraph>Failed/retrying: {runtime.queue.failedJobs}</s-paragraph>
        <s-paragraph>Dead-letter: {runtime.queue.deadLetterJobs}</s-paragraph>
      </s-section>
    </s-page>
  );
}
