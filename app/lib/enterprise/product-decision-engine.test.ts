import assert from "node:assert/strict";
import { buildEnterpriseProductDecision, collectionRoutingTags } from "./product-decision-engine";

assert.deepEqual(
  collectionRoutingTags({
    department: "Fashion",
    family: "Activewear",
    route: "activewear-sets",
  }),
  [
    "mvq:collection:fashion",
    "mvq:collection:activewear",
    "mvq:collection:activewear-sets",
  ],
);

assert.deepEqual(
  collectionRoutingTags({
    department: "Jewelry",
    family: "Necklaces",
    route: "necklaces",
  }),
  [
    "mvq:collection:jewelry",
    "mvq:collection:necklaces",
  ],
);

assert.deepEqual(
  collectionRoutingTags({
    department: "Unclassified",
    family: "Unclassified",
    route: "needs-review",
  }),
  [],
);

const unresolvedBrandProduct = {
  id: "gid://shopify/Product/unresolved-brand",
  title: "Performance Activewear Set",
  descriptionHtml: "<p>Two-piece activewear set with moderate stretch.</p>",
  tags: [],
  options: [{ name: "Size", values: ["S", "M", "L"] }],
  variants: { nodes: [{ id: "gid://shopify/ProductVariant/1", price: "39.24" }] },
};

const unresolvedDecision = buildEnterpriseProductDecision(unresolvedBrandProduct);
assert.equal(unresolvedDecision.classification.productType, "Activewear Set");
assert.equal(unresolvedDecision.brandRoute.brand, null);
assert.ok(unresolvedDecision.tags.includes("mvq:brand:needs-review"));
assert.ok(unresolvedDecision.tags.includes("mvq:needs-review"));
assert.ok(unresolvedDecision.tags.includes("mvq:collection:fashion"));
assert.ok(unresolvedDecision.tags.includes("mvq:collection:activewear"));
assert.ok(unresolvedDecision.tags.includes("mvq:collection:activewear-sets"));

console.log("product decision routing tests passed");
