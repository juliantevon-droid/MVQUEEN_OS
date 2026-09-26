import type { LoaderFunctionArgs } from "react-router";
import { useLoaderData } from "react-router";
import { authenticate } from "../shopify.server";
import {
  summarizeCatalogAudit,
  type AuditProduct,
} from "../lib/enterprise/catalog-audit";
import { resolveShopCommercialConfig } from "../lib/enterprise/commercial-settings.server";

type CatalogAuditNode = {
  id: string;
  title: string;
  status: string;
  tags: string[];
  seoTitle?: { value?: string | null } | null;
  shortDescription?: { value?: string | null } | null;
  unitCost?: { value?: string | null } | null;
  inboundShipping?: { value?: string | null } | null;
  automationShortDescription?: { value?: string | null } | null;
  variants?: {
    nodes?: Array<{ id: string; price?: string | null }>;
    pageInfo?: { hasNextPage?: boolean };
  } | null;
  collections?: {
    nodes?: Array<{ handle: string }>;
  } | null;
};

type CatalogAuditConnection = {
  nodes?: CatalogAuditNode[];
  pageInfo?: {
    hasNextPage?: boolean;
    endCursor?: string | null;
  };
};

const CATALOG_AUDIT_QUERY = `#graphql
query MVQueenCatalogAudit($first: Int!, $after: String) {
  products(first: $first, after: $after, sortKey: ID) {
    nodes {
      id
      title
      status
      tags
      seoTitle: metafield(namespace: "global", key: "title_tag") { value }
      shortDescription: metafield(namespace: "catalog", key: "short_description") { value }
      automationShortDescription: metafield(namespace: "automation", key: "short_description") { value }
      unitCost: metafield(namespace: "commercial", key: "unit_cost") { value }
      inboundShipping: metafield(namespace: "commercial", key: "inbound_shipping") { value }
      variants(first: 2) {
        nodes { id price }
        pageInfo { hasNextPage }
      }
      collections(first: 50) {
        nodes { handle }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
`;

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const { admin, session } = await authenticate.admin(request);
  const products: AuditProduct[] = [];
  const commercial = await resolveShopCommercialConfig(session.shop);
  let after: string | null = null;
  let pages = 0;

  while (pages < 25) {
    const response = (await admin.graphql(CATALOG_AUDIT_QUERY, {
      variables: { first: 100, after },
    })) as Response;
    const body = (await response.json()) as {
      data?: { products?: CatalogAuditConnection | null };
    };
    const connection: CatalogAuditConnection | null | undefined = body.data?.products;

    if (!connection) {
      throw new Error("Shopify catalog audit query returned no product connection.");
    }

    for (const product of connection.nodes ?? []) {
      products.push({
        id: product.id,
        title: product.title,
        status: product.status,
        tags: product.tags ?? [],
        seoTitle: product.seoTitle?.value ?? null,
        shortDescription:
          product.shortDescription?.value ??
          product.automationShortDescription?.value ??
          null,
        unitCost: product.unitCost?.value ?? null,
        inboundShipping: product.inboundShipping?.value ?? null,
        variants: product.variants?.nodes ?? [],
        hasMoreVariants: Boolean(product.variants?.pageInfo?.hasNextPage),
        media: [],
        mediaAuditAvailable: false,
        collections: product.collections?.nodes ?? [],
      });
    }

    pages += 1;
    if (!connection.pageInfo?.hasNextPage) break;
    after = connection.pageInfo.endCursor ?? null;
  }

  const audit = summarizeCatalogAudit(products, commercial);
  return {
    ...audit,
    truncated: pages >= 25,
    generatedAt: new Date().toISOString(),
  };
};

export default function CatalogHealth() {
  const data = useLoaderData<typeof loader>();

  return (
    <s-page heading="Catalog Health">
      <s-section heading="Live Shopify audit">
        <s-paragraph>Products scanned: {data.productCount}</s-paragraph>
        <s-paragraph>Release-ready products: {data.publishReadyCount}</s-paragraph>
        <s-paragraph>Advertising-eligible products: {data.advertisingEligibleCount}</s-paragraph>
        <s-paragraph>Commercially blocked/review products: {data.commercialBlockedCount}</s-paragraph>
        <s-paragraph>Blockers: {data.blockerCount}</s-paragraph>
        <s-paragraph>Warnings: {data.warningCount}</s-paragraph>
        <s-paragraph>Generated: {new Date(data.generatedAt).toLocaleString()}</s-paragraph>
        <s-paragraph>Media ALT audit: separate Shopify Files permission required.</s-paragraph>
        {data.truncated ? (
          <s-paragraph>Audit stopped at the safety page cap; run a bulk audit for a larger catalog.</s-paragraph>
        ) : null}
      </s-section>

      <s-section heading="Product commercial health">
        {data.evaluations.map((item) => (
          <s-paragraph key={item.productGid}>
            {item.title} · release {item.releaseGate.state} · commercial {item.commercialHealth.state} · ads {item.releaseGate.advertisingEligible ? "eligible" : "blocked"}
            {item.commercialHealth.maxBreakEvenCac !== null ? ` · max break-even CAC ${item.commercialHealth.maxBreakEvenCac.toFixed(2)}` : ""}
            {item.commercialHealth.breakEvenRoas !== null ? ` · break-even ROAS ${item.commercialHealth.breakEvenRoas.toFixed(2)}x` : ""}
          </s-paragraph>
        ))}
      </s-section>

      <s-section heading="Issues">
        {data.issues.length ? (
          data.issues.slice(0, 250).map((issue, index) => (
            <s-paragraph key={`${issue.productGid}:${issue.code}:${index}`}>
              {issue.severity.toUpperCase()} · {issue.title} · {issue.code} · {issue.message}
            </s-paragraph>
          ))
        ) : (
          <s-paragraph>No catalog-health issues detected by the current enterprise rules.</s-paragraph>
        )}
        {data.issues.length > 250 ? (
          <s-paragraph>Only the first 250 issues are shown. Total issues: {data.issues.length}.</s-paragraph>
        ) : null}
      </s-section>
    </s-page>
  );
}
