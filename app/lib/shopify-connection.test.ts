import assert from "node:assert/strict";
import { collectShopifyConnection } from "./shopify-connection";
const initial = { nodes: ["one"], pageInfo: { hasNextPage: true, endCursor: "cursor-one" } };
let calls = 0;
assert.deepEqual(await collectShopifyConnection(initial, async (after) => {
  calls++; assert.equal(after, "cursor-one");
  return { nodes: ["two"], pageInfo: { hasNextPage: false, endCursor: "cursor-two" } };
}), ["one", "two"]);
assert.equal(calls, 1);
for (const invalid of [null, { nodes: ["one"] }, { nodes: ["one"], pageInfo: { hasNextPage: true } }]) {
  await assert.rejects(collectShopifyConnection(invalid, async () => null));
}
await assert.rejects(collectShopifyConnection(initial, async () => initial), /repeated/);
await assert.rejects(collectShopifyConnection(initial, async () => null), /incomplete/);
await assert.rejects(collectShopifyConnection(initial, async () => initial, 1), /page cap/);
console.log("complete Shopify connection tests passed");
