import type { LoaderFunctionArgs } from "react-router";
import { useLoaderData } from "react-router";
import { authenticate } from "../shopify.server";
import {
  summarizeCatalogAudit,
  type AuditProduct,
} from "../lib/enterprise/catalog-audit";

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
      unitCost: metafield(namespace: "commercial", key: "unit_cost") { value }
      variants(first: 2) {
        nodes { id price }
        pageInfo { hasNextPage }
      }
      media(first: 100) {
        nodes { id alt }
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
  const { admin } = await authenticate.admin(request);
  const products: AuditProduct[] = [];
  let after: string | null = null;
  let pages = 0;

  while (pages < 25) {
    const response = await admin.graphql(CATALOG_AUDIT_QUERY, {
      variables: { first: 100, after },
    });
    const body = await response.json();
    const connection = body.data?.products;

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
        shortDescription: product.shortDescription?.value ?? null,
        unitCost: product.unitCost?.value ?? null,
        variants: product.variants?.nodes ?? [],
        hasMoreVariants: Boolean(product.variants?.pageInfo?.hasNextPage),
        media: product.media?.nodes ?? [],
        collections: product.collections?.nodes ?? [],
      });
    }

    pages += 1;
    if (!connection.pageInfo?.hasNextPage) break;
    after = connection.pageInfo.endCursor;
  }

  const audit = summarizeCatalogAudit(products);
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
        <s-paragraph>Healthy products: {data.healthyProductCount}</s-paragraph>
        <s-paragraph>Blockers: {data.blockerCount}</s-paragraph>
        <s-paragraph>Warnings: {data.warningCount}</s-paragraph>
        <s-paragraph>Generated: {new Date(data.generatedAt).toLocaleString()}</s-paragraph>
        {data.truncated ? (
          <s-paragraph>Audit stopped at the safety page cap; run a bulk audit for a larger catalog.</s-paragraph>
        ) : null}
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
