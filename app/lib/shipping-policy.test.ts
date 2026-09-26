import assert from "node:assert/strict";
import {
  DEFAULT_SHIPPING_DELIVERY_ESTIMATE,
  resolveShippingDeliveryEstimate,
} from "./shipping-policy";

assert.equal(
  resolveShippingDeliveryEstimate("  7–12 business days  "),
  "7–12 business days",
);
assert.equal(
  resolveShippingDeliveryEstimate("Ships in 3–5 days\nfrom verified source"),
  "Ships in 3–5 days from verified source",
);
assert.equal(
  resolveShippingDeliveryEstimate(""),
  DEFAULT_SHIPPING_DELIVERY_ESTIMATE,
);
assert.equal(
  resolveShippingDeliveryEstimate(null),
  DEFAULT_SHIPPING_DELIVERY_ESTIMATE,
);
assert.equal(
  DEFAULT_SHIPPING_DELIVERY_ESTIMATE,
  "7–15 business days",
);
assert.match(DEFAULT_SHIPPING_DELIVERY_ESTIMATE, /^7–15 business days$/);

console.log("shipping policy tests passed");
