import assert from "node:assert/strict";
import { collectionRoutingTags } from "./product-decision-engine";

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

console.log("product decision routing tests passed");
