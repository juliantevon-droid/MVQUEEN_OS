import assert from "node:assert/strict";
import { buildAutomaticSurfaceRecord, buildAutomatedProductFaq } from "./automated-content-surfaces";
import type { Classification, ProductSnapshot } from "./mvqueen-intelligence";
import type { AutomatedProductContent } from "./product-content-automation";

const classification: Classification = {
  department: "Fashion",
  family: "Dresses",
  subcollection: "Dresses",
  route: "dresses",
  productType: "Dress",
  confidence: "high",
};

const content: AutomatedProductContent = {
  title: "Black Satin Dress",
  shortDescription: "A black satin dress with source-listed details.",
  highlights: ["Material: Satin", "Color: Black", "Length: Midi"],
  focusKeyword: "dress",
  secondaryKeywords: ["dresses", "black satin dress"],
  longTailKeywords: ["black satin midi dress"],
  seoTitle: "Black Satin Dress | MVQueen",
  metaDescription: "Shop Black Satin Dress at MVQueen with current product details and imagery.",
  seoKeywords: ["dress", "dresses", "black satin midi dress"],
};

const richProduct: ProductSnapshot = {
  id: "gid://shopify/Product/1",
  title: "Black Satin Dress",
  handle: "black-satin-dress",
  descriptionHtml:
    "<p>This product page contains a detailed source description long enough to support a useful editorial guide without inventing new specifications. The description explains how to review the available details, options, imagery, and current information before purchasing, while keeping the source listing as the factual reference.</p>" +
    "<ul><li>Material: Satin</li><li>Color: Black</li><li>Length: Midi</li></ul>",
  productType: "Dress",
  variants: { nodes: [{ id: "gid://shopify/ProductVariant/1", price: "49.99" }] },
};

const faq = buildAutomatedProductFaq(richProduct, classification, content);
assert.ok(faq.length >= 3);
assert.ok(faq.some((item) => item.answer.includes("Material: Satin")));

const record = buildAutomaticSurfaceRecord(richProduct, classification, content);
assert.equal(record.status, "PRODUCTION_READY");
assert.equal(record.qa.passed, true);
assert.equal((record.content_suite.blog as any).auto_publish, true);
assert.equal((record.content_suite.blog as any).publish_eligible, true);
assert.equal((record.content_suite.collection as any).auto_publish, true);
assert.ok((record.content_suite.collection as any).target_handles.includes("dresses"));
assert.equal((record.content_suite.site_faq as any).scope, "product");
assert.equal(record.pricing.approved_publish_price, null);
assert.equal(record.shipping.delivery_estimate, "Confirmed at checkout based on destination and fulfillment source.");
assert.equal((record.content_suite.metafields as any)["shipping.delivery_estimate"].value, record.shipping.delivery_estimate);

const sparseProduct: ProductSnapshot = {
  ...richProduct,
  id: "gid://shopify/Product/2",
  handle: "sparse-dress",
  descriptionHtml: "<p>Short source description.</p>",
};
const sparseRecord = buildAutomaticSurfaceRecord(sparseProduct, classification, {
  ...content,
  highlights: [],
});
assert.equal((sparseRecord.content_suite.blog as any).auto_publish, false);
assert.equal((sparseRecord.content_suite.blog as any).status, "DRAFT_REVIEW");

console.log("automated content surface tests passed");
