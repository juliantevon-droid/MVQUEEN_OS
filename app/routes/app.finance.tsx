import type { LoaderFunctionArgs } from "react-router";
import { useLoaderData } from "react-router";
import { authenticate } from "../shopify.server";
import { resolveShopCommercialConfig } from "../lib/enterprise/commercial-settings.server";
import {
  buildFinanceSummary,
  type FinanceOrder,
} from "../lib/enterprise/finance-engine";

const ACCESS_QUERY = `#graphql
query MVQueenFinanceAccess {
  shop { currencyCode }
  appInstallation {
    accessScopes { handle }
  }
}
`;

const FINANCE_ORDERS_QUERY = `#graphql
query MVQueenFinanceOrders($first: Int!, $after: String) {
  orders(first: $first, after: $after, sortKey: CREATED_AT, reverse: true) {
    nodes {
      id
      createdAt
      cancelledAt
      currencyCode
      displayFinancialStatus
      currentTotalPriceSet { shopMoney { amount currencyCode } }
      currentTotalTaxSet { shopMoney { amount currencyCode } }
      currentTotalDiscountsSet { shopMoney { amount currencyCode } }
      totalRefundedSet { shopMoney { amount currencyCode } }
      lineItems(first: 100) {
        nodes {
          id
          currentQuantity
          sku
          variant {
            id
            product {
              id
              commercialUnitCost: metafield(namespace: "commercial", key: "unit_cost") { value }
              commercialInboundShipping: metafield(namespace: "commercial", key: "inbound_shipping") { value }
            }
          }
        }
        pageInfo { hasNextPage }
      }
    }
    pageInfo { hasNextPage endCursor }
  }
}
`;

type FinanceOrderNode = {
  id: string;
  createdAt: string;
  cancelledAt?: string | null;
  currencyCode: string;
  currentTotalPriceSet: { shopMoney: { amount: string; currencyCode: string } };
  currentTotalTaxSet: { shopMoney: { amount: string; currencyCode: string } };
  currentTotalDiscountsSet: { shopMoney: { amount: string; currencyCode: string } };
  totalRefundedSet: { shopMoney: { amount: string; currencyCode: string } };
  lineItems?: {
    nodes?: Array<{
      id: string;
      currentQuantity: number;
      sku?: string | null;
      variant?: {
        id: string;
        product?: {
          id: string;
          commercialUnitCost?: { value?: string | null } | null;
          commercialInboundShipping?: { value?: string | null } | null;
        } | null;
      } | null;
    }>;
    pageInfo?: { hasNextPage?: boolean };
  } | null;
};

function numeric(value: string | null | undefined): number {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : 0;
}

function optionalMoney(value: string | null | undefined): number | null {
  if (!value?.trim()) return null;
  const parsed = Number(value);
  return Number.isFinite(parsed) && parsed >= 0 ? parsed : null;
}

function money(value: number | null, currency: string): string {
  if (value === null) return "Unavailable";
  return `${currency} ${value.toFixed(2)}`;
}

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const { admin, session } = await authenticate.admin(request);

  const accessResponse = (await admin.graphql(ACCESS_QUERY)) as Response;
  const accessBody = (await accessResponse.json()) as {
    data?: {
      shop?: { currencyCode?: string | null } | null;
      appInstallation?: {
        accessScopes?: Array<{ handle?: string | null }>;
      } | null;
    };
  };
  const scopes = new Set(
    accessBody.data?.appInstallation?.accessScopes
      ?.map((scope) => scope.handle)
      .filter((handle): handle is string => Boolean(handle)) ?? [],
  );

  const hasReadOrders = scopes.has("read_orders");
  const currency = accessBody.data?.shop?.currencyCode ?? "USD";
  if (!hasReadOrders) {
    return {
      authorized: false as const,
      currency,
      message:
        "read_orders has not been granted to this app installation. No order data was read.",
    };
  }

  const commercial = await resolveShopCommercialConfig(session.shop);
  const cutoff = Date.now() - 30 * 24 * 60 * 60 * 1000;
  const orders: FinanceOrder[] = [];
  let after: string | null = null;
  let pages = 0;
  let reachedCutoff = false;

  while (pages < 25 && !reachedCutoff) {
    const response = (await admin.graphql(FINANCE_ORDERS_QUERY, {
      variables: { first: 100, after },
    })) as Response;
    const body = (await response.json()) as {
      data?: {
        orders?: {
          nodes?: FinanceOrderNode[];
          pageInfo?: { hasNextPage?: boolean; endCursor?: string | null };
        } | null;
      };
    };
    const connection = body.data?.orders;
    if (!connection) throw new Error("Shopify finance query returned no orders connection.");

    for (const order of connection.nodes ?? []) {
      const createdAt = Date.parse(order.createdAt);
      if (Number.isFinite(createdAt) && createdAt < cutoff) {
        reachedCutoff = true;
        continue;
      }

      orders.push({
        id: order.id,
        createdAt: order.createdAt,
        cancelledAt: order.cancelledAt ?? null,
        currency: order.currentTotalPriceSet.shopMoney.currencyCode || order.currencyCode,
        currentTotalPrice: numeric(order.currentTotalPriceSet.shopMoney.amount),
        currentTotalTax: numeric(order.currentTotalTaxSet.shopMoney.amount),
        currentTotalDiscounts: numeric(order.currentTotalDiscountsSet.shopMoney.amount),
        totalRefunded: numeric(order.totalRefundedSet.shopMoney.amount),
        lineItems: (order.lineItems?.nodes ?? []).map((line) => ({
          currentQuantity: line.currentQuantity,
          unitCost: optionalMoney(line.variant?.product?.commercialUnitCost?.value),
          inboundShipping: optionalMoney(
            line.variant?.product?.commercialInboundShipping?.value,
          ),
        })),
        lineItemsComplete: !order.lineItems?.pageInfo?.hasNextPage,
      });
    }

    pages += 1;
    if (reachedCutoff || !connection.pageInfo?.hasNextPage) break;
    after = connection.pageInfo.endCursor ?? null;
  }

  const summary = buildFinanceSummary(orders, commercial, null);
  return {
    authorized: true as const,
    currency,
    windowDays: 30,
    scannedPages: pages,
    truncated: pages >= 25 && !reachedCutoff,
    summary,
  };
};

export default function FinancePage() {
  const data = useLoaderData<typeof loader>();

  if (!data.authorized) {
    return (
      <s-page heading="Finance">
        <s-section heading="Order access required">
          <s-paragraph>{data.message}</s-paragraph>
          <s-paragraph>
            The app requests read-only order access for finance reporting. Reauthorization is required before this screen can calculate order economics.
          </s-paragraph>
        </s-section>
      </s-page>
    );
  }

  const summary = data.summary;

  return (
    <s-page heading="Finance">
      <s-section heading="30-day commerce economics">
        <s-paragraph>State: {summary.state}</s-paragraph>
        <s-paragraph>Orders: {summary.orderCount}</s-paragraph>
        <s-paragraph>Cancelled orders: {summary.cancelledOrderCount}</s-paragraph>
        <s-paragraph>Gross/current collected: {money(summary.grossCollected, summary.currency)}</s-paragraph>
        <s-paragraph>Tax: {money(summary.taxAmount, summary.currency)}</s-paragraph>
        <s-paragraph>Net revenue excluding tax: {money(summary.netRevenueExTax, summary.currency)}</s-paragraph>
        <s-paragraph>Discounts: {money(summary.discountAmount, summary.currency)}</s-paragraph>
        <s-paragraph>Refunds reported by Shopify: {money(summary.refundAmount, summary.currency)}</s-paragraph>
        <s-paragraph>Verified COGS: {money(summary.cogs, summary.currency)}</s-paragraph>
        <s-paragraph>Estimated fulfillment/inbound cost: {money(summary.estimatedFulfillmentCost, summary.currency)}</s-paragraph>
        <s-paragraph>Estimated payment fees: {money(summary.estimatedPaymentFees, summary.currency)}</s-paragraph>
        <s-paragraph>Commerce contribution before ads: {money(summary.commerceContributionBeforeAds, summary.currency)}</s-paragraph>
        <s-paragraph>Target-CAC benchmark contribution: {money(summary.targetCacBenchmarkContribution, summary.currency)}</s-paragraph>
        <s-paragraph>Actual ad spend: {money(summary.actualAdSpend, summary.currency)}</s-paragraph>
        <s-paragraph>Fully loaded contribution: {money(summary.fullyLoadedContribution, summary.currency)}</s-paragraph>
      </s-section>

      <s-section heading="Data quality">
        <s-paragraph>Missing-cost line items: {summary.missingCostLineCount}</s-paragraph>
        <s-paragraph>Orders with more than 100 line items: {summary.incompleteLineItemOrderCount}</s-paragraph>
        <s-paragraph>Missing inputs: {summary.missing.length ? summary.missing.join(", ") : "none"}</s-paragraph>
        <s-paragraph>Order pages scanned: {data.scannedPages}</s-paragraph>
        {data.truncated ? (
          <s-paragraph>Report hit the safety page cap and is incomplete.</s-paragraph>
        ) : null}
      </s-section>

      <s-section heading="Interpretation">
        {summary.notes.map((note, index) => (
          <s-paragraph key={index}>{note}</s-paragraph>
        ))}
      </s-section>
    </s-page>
  );
}
