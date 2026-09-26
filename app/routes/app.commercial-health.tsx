import type { LoaderFunctionArgs } from "react-router";
import { useLoaderData } from "react-router";
import { authenticate } from "../shopify.server";
import prisma from "../db.server";

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const { session } = await authenticate.admin(request);

  const [states, recent] = await Promise.all([
    prisma.productCommercialHealthState.findMany({
      where: { shop: session.shop },
      orderBy: [{ stale: "desc" }, { state: "asc" }, { updatedAt: "desc" }],
      take: 500,
    }),
    prisma.productCommercialHealthSnapshot.findMany({
      where: { shop: session.shop },
      orderBy: { createdAt: "desc" },
      take: 25,
    }),
  ]);

  const staleCount = states.filter((item) => item.stale).length;
  const blockedCount = states.filter(
    (item) => item.state === "blocked" || item.state === "invalid_inputs",
  ).length;
  const thinCount = states.filter((item) => item.state === "thin").length;
  const inputBlockedCount = states.filter(
    (item) =>
      item.state === "needs_configuration" ||
      item.state === "needs_cost" ||
      item.state === "needs_price",
  ).length;
  const healthyCount = states.filter(
    (item) => item.state === "healthy" && !item.stale,
  ).length;
  const advertisingEligibleCount = states.filter(
    (item) => item.advertisingEligibility === "eligible" && !item.stale,
  ).length;

  return {
    shop: session.shop,
    states,
    recent,
    summary: {
      productCount: states.length,
      healthyCount,
      staleCount,
      blockedCount,
      thinCount,
      inputBlockedCount,
      advertisingEligibleCount,
    },
  };
};

function money(value: number | null): string {
  return value === null ? "—" : `$${value.toFixed(2)}`;
}

function ratio(value: number | null): string {
  return value === null ? "—" : `${value.toFixed(2)}x`;
}

export default function CommercialHealthPage() {
  const data = useLoaderData<typeof loader>();

  return (
    <s-page heading="Commercial Health & Alerts">
      <s-section heading="Current health">
        <s-paragraph>Products with evaluated health: {data.summary.productCount}</s-paragraph>
        <s-paragraph>Healthy: {data.summary.healthyCount}</s-paragraph>
        <s-paragraph>Advertising eligible: {data.summary.advertisingEligibleCount}</s-paragraph>
        <s-paragraph>Thin margin: {data.summary.thinCount}</s-paragraph>
        <s-paragraph>Commercially blocked: {data.summary.blockedCount}</s-paragraph>
        <s-paragraph>Missing required inputs: {data.summary.inputBlockedCount}</s-paragraph>
        <s-paragraph>Stale after policy change: {data.summary.staleCount}</s-paragraph>
      </s-section>

      <s-section heading="Product alerts">
        {data.states.length ? (
          data.states.map((item) => (
            <s-paragraph key={item.id}>
              {item.stale ? "STALE" : item.state.toUpperCase()} · {item.productGid} · ads {item.advertisingEligibility}
              {" · "}max CAC {money(item.maxBreakEvenCac)}
              {" · "}break-even ROAS {ratio(item.breakEvenRoas)}
              {" · "}target ROAS {ratio(item.targetRoas)}
            </s-paragraph>
          ))
        ) : (
          <s-paragraph>
            No product commercial-health states exist yet. Product processing or a governed backfill will create them.
          </s-paragraph>
        )}
      </s-section>

      <s-section heading="Recent health history">
        {data.recent.length ? (
          data.recent.map((item) => (
            <s-paragraph key={item.id}>
              {new Date(item.createdAt).toLocaleString()} · {item.productGid} · {item.state} · ads {item.advertisingEligibility}
            </s-paragraph>
          ))
        ) : (
          <s-paragraph>No commercial-health history recorded yet.</s-paragraph>
        )}
      </s-section>
    </s-page>
  );
}
