import assert from "node:assert/strict";
import { buildAutomaticSurfaceRecord, buildAutomatedProductFaq } from "./automated-content-surfaces";
import type { Classification, ProductSnapshot } from "./mvqueen-intelligence";
import type { AutomatedProductContent } from "./product-content-automation";
import { BRAND_VOCABULARY, PRODUCT_EDITORIAL_CATEGORIES } from "./brand-vocabulary.server";

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
  descriptionHtml: "<p>A black satin dress with source-listed details.</p><h3>Product Details</h3><ul><li>Material: Satin</li><li>Color: Black</li><li>Length: Midi</li></ul>",
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
assert.equal(record.copy.description, content.descriptionHtml);
assert.ok(record.content_suite.content_version.endsWith(BRAND_VOCABULARY.version));
assert.equal(record.status, "PRODUCTION_READY");
assert.equal(record.qa.passed, true);
assert.equal((record.content_suite.blog as any).auto_publish, true);
assert.equal((record.content_suite.blog as any).publish_eligible, true);
assert.equal((record.content_suite.collection as any).auto_publish, true);
assert.ok((record.content_suite.collection as any).target_handles.includes("dresses"));
assert.equal((record.content_suite.site_faq as any).scope, "product");
assert.equal(record.pricing.approved_publish_price, null);
assert.equal(record.shipping.delivery_estimate, "7–15 business days");
assert.equal((record.content_suite.metafields as any)["shipping.delivery_estimate"].value, record.shipping.delivery_estimate);


const princessFaq = buildAutomatedProductFaq(richProduct, classification, content, "Miss.Princess");
assert.ok(princessFaq[0].answer.includes("Miss.Princess edit"));
assert.ok(!princessFaq[0].answer.includes("MVQueen catalog"));

const princessRecord = buildAutomaticSurfaceRecord(
  richProduct,
  classification,
  content,
  "Miss.Princess",
);
assert.ok((princessRecord.content_suite.collection as any).name.startsWith("Miss.Princess "));
assert.ok((princessRecord.content_suite.blog as any).dek.includes("Miss.Princess"));
assert.ok(
  ((princessRecord.content_suite.blog as any).sections as any[])
    .flatMap((section: any) => section.paragraphs ?? [])
    .some((paragraph: string) => paragraph.includes("Miss.Princess")),
);

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

const categoryCases = [
  ["fashion", "Fashion", "Dress"], ["jewelry", "Jewelry", "Necklace"],
  ["skincare", "Beauty", "Face Cream"], ["beauty", "Beauty", "Lipstick"],
  ["fragrance", "Beauty", "Fragrance"], ["haircare", "Hair", "Shampoo"],
  ["home", "Home", "Candle"], ["tools", "Beauty", "Makeup Brush"],
  ["general", "Lifestyle Accessories", "Pouch"],
] as const;
assert.equal(categoryCases.length, PRODUCT_EDITORIAL_CATEGORIES.length);
for (const [category, department, productType] of categoryCases) {
  const c = { ...classification, department, family: productType, productType };
  for (const brand of ["MVQUEEN", "Miss.Princess"]) {
    const introductions = new Set<string>();
    let previousCollection: unknown;
    for (let index = 0; index < 8; index++) {
      const product = { ...richProduct, id: `surface-${brand}-${category}-${index}` };
      const before = structuredClone(product);
      const generated = buildAutomaticSurfaceRecord(product, c, content, brand);
      assert.deepEqual(product, before);
      const blog = generated.content_suite.blog as any;
      const collection = generated.content_suite.collection as any;
      const customerCopy = [blog.title, blog.dek, blog.introduction, ...blog.sections.flatMap((s: any) => [s.heading, ...s.paragraphs]), collection.description, generated.copy.cta].join(" ");
      assert.ok(!/editorial framing|source information|verified product fact|\{\w+\}/i.test(customerCopy));
      assert.ok(!/\b(?:clinically|vegan|cruelty|heals|guaranteed|handmade|longevity)\b/i.test(customerCopy));
      assert.ok(blog.dek.includes(brand));
      assert.ok(blog.sections.some((s: any) => s.paragraphs.some((p: string) => p.includes("Material: Satin"))));
      assert.ok(blog.seo_title.length <= BRAND_VOCABULARY.contentPolicy.limits.seoTitle);
      assert.ok(blog.meta_description.length <= BRAND_VOCABULARY.contentPolicy.limits.metaDescription);
      assert.ok(collection.seo_title.length <= BRAND_VOCABULARY.contentPolicy.limits.seoTitle);
      assert.equal(collection.seo_title.split(brand).length - 1, 1);
      assert.ok(collection.meta_description.length <= BRAND_VOCABULARY.contentPolicy.limits.metaDescription);
      if (previousCollection) assert.deepEqual(collection, previousCollection, "Shared collection copy must be stable across product events");
      previousCollection = collection;
      introductions.add(blog.introduction);
    }
    assert.ok(introductions.size >= 2, `Vary ${brand}/${category} introductions consistently`);
  }
}
assert.notEqual((record.content_suite.blog as any).introduction, (princessRecord.content_suite.blog as any).introduction);
assert.throws(() => buildAutomaticSurfaceRecord(richProduct, classification, content, "Unknown House"), /Unknown brand/);

console.log("automated content surface tests passed");
