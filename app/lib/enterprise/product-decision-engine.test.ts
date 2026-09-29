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

const mixedColorActivewear = {
  id: "gid://shopify/Product/9087726584006",
  title: "Ruched Sports Bra and High-Waisted Shorts Active Set",
  descriptionHtml: "<ul><li>Material composition: 94% polyester, 6% elastane</li></ul>",
  tags: [],
  variants: { nodes: [{ id: "gid://shopify/ProductVariant/1", price: "39.24" }] },
};

const mixedDecision = buildEnterpriseProductDecision(mixedColorActivewear);
assert.equal(mixedDecision.classification.productType, "Activewear Set");
assert.equal(mixedDecision.brandRoute.brand, null);
assert.ok(mixedDecision.tags.includes("mvq:brand:needs-review"));
assert.ok(mixedDecision.tags.includes("mvq:needs-review"));
assert.ok(mixedDecision.tags.includes("mvq:collection:fashion"));
assert.ok(mixedDecision.tags.includes("mvq:collection:activewear"));
assert.ok(mixedDecision.tags.includes("mvq:collection:activewear-sets"));

console.log("product decision routing tests passed");
