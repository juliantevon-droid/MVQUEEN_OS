export type ShopifyConnection<T> = {
  nodes?: T[];
  pageInfo?: { hasNextPage?: boolean; endCursor?: string | null };
};

export async function collectShopifyConnection<T>(
  initial: ShopifyConnection<T> | null | undefined,
  loadPage: (after: string) => Promise<ShopifyConnection<T> | null | undefined>,
  maxPages = 100,
): Promise<T[]> {
  const nodes: T[] = [];
  const cursors = new Set<string>();
  let connection = initial;
  for (let page = 0; page < maxPages; page += 1) {
    if (!connection || typeof connection.pageInfo?.hasNextPage !== "boolean") {
      throw new Error("Shopify returned an incomplete connection; full evaluation is blocked.");
    }
    nodes.push(...(connection.nodes ?? []));
    if (!connection.pageInfo.hasNextPage) return nodes;
    const cursor = connection.pageInfo.endCursor;
    if (!cursor || cursors.has(cursor)) throw new Error("Shopify pagination cursor is missing or repeated.");
    cursors.add(cursor);
    connection = await loadPage(cursor);
  }
  throw new Error("Shopify connection exceeds the page cap; full evaluation is blocked.");
}
