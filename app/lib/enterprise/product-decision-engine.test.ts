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
assert.equal(unresolvedDecision.brandRoute.brand, "mvqueen");
assert.equal(unresolvedDecision.brandRoute.confidence, "medium");
assert.equal(unresolvedDecision.brandRoute.reason, "default-primary-brand");
assert.ok(unresolvedDecision.tags.includes("mvq:brand:mvqueen"));
assert.ok(!unresolvedDecision.tags.includes("mvq:needs-review"));
assert.ok(unresolvedDecision.tags.includes("mvq:collection:fashion"));
assert.ok(unresolvedDecision.tags.includes("mvq:collection:activewear"));
assert.ok(unresolvedDecision.tags.includes("mvq:collection:activewear-sets"));

for (const { title, colors } of [
  { title: "Student Dormitory Fill-light Desktop Vanity Mirror With Charging Function", colors: ["Natural White", "Pink"] },
  { title: "Rose Loose Powder Makeup Brush Beauty Tool", colors: ["Rose Black Purple", "Rose Gradually Varied Pink", "Rose Red", "Rose Pink", "Rose Red Gradient", "Pink"] },
]) {
  const decision = buildEnterpriseProductDecision({
    id: "gid://shopify/Product/review-tool",
    title,
    productType: "Needs Review",
    options: [{ name: "Color", values: colors }],
    tags: ["mvq:brand:miss-princess", "mvq:needs-review"],
    variants: { nodes: [{ id: "gid://shopify/ProductVariant/review-tool", price: "18.16" }] },
  }, {
    // Test-only assumptions; product cost is deliberately absent.
    config: { paymentRate: 0.029, paymentFixed: 0.3, returnReserveRate: 0.03, targetContributionMarginRate: 0.3, targetCac: 5, inboundShippingDefault: 0, currency: "USD" },
    missing: [],
  });
  assert.equal(decision.classification.productType, "Beauty Tool", title);
  assert.equal(decision.brandRoute.brand, "miss-princess", title);
  assert.ok(!decision.tags.includes("mvq:needs-review"), title);
  assert.ok(decision.tags.includes("mvq:collection:beauty-tools"), title);
  // Resolving classification does not supply a cost or advertising clearance.
  assert.ok(decision.tags.includes("mvq:pricing:needs_cost"), title);
  assert.ok(decision.tags.includes("mvq:ads:not_ready"), title);
}

console.log("product decision routing tests passed");

