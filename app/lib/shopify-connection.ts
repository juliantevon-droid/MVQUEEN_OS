export type ShopifyConnection<T> = {
  nodes?: T[];
  pageInfo?: { hasNextPage?: boolean; endCursor?: string | null };
};

export function shopifyProductWasDeleted(body: unknown): boolean {
  if (!body || typeof body !== "object") throw new Error("Shopify returned an invalid product response.");
  const result = body as { errors?: unknown[]; data?: { product?: unknown } };
  if (result.errors?.length) throw new Error("Shopify product query failed; deletion was not confirmed.");
  if (!result.data || !Object.prototype.hasOwnProperty.call(result.data, "product")) {
    throw new Error("Shopify returned an incomplete product response; deletion was not confirmed.");
  }
  if (result.data.product === null) return true;
  const product = result.data.product;
  if (!product || typeof product !== "object" || typeof (product as { id?: unknown }).id !== "string") {
    throw new Error("Shopify returned an invalid product record.");
  }
  return false;
}

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
