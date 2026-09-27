import assert from "node:assert/strict";
import {
  buildAutomatedProductContent,
  needsMediaAltRepair,
  shouldPublishAutomatedDescription,
} from "./product-content-automation";
import {
  classifyBrandWorld,
  classifyProduct,
  type ProductSnapshot,
} from "./mvqueen-intelligence";

const product: ProductSnapshot = {
  id: "gid://shopify/Product/1",
  handle: "natural-pink-thulite-pendant",
  title: "SUPPLIER Natural Pink Thulite Pendant (ABC123)",
  vendor: "SUPPLIER",
  productType: "",
  descriptionHtml: [
    "<p>A soft natural pink thulite pendant set in sterling silver.</p>",
    "<ul>",
    "<li><strong>Stone:</strong> Natural Pink Thulite</li>",
    "<li><strong>Metal:</strong> 925 Sterling Silver</li>",
    "<li><strong>Stone size:</strong> 17 × 22 mm</li>",
    "</ul>",
  ].join(""),
  tags: [],
  variants: { nodes: [{ id: "gid://shopify/ProductVariant/1", price: "26.39" }] },
};

const classification = classifyProduct(
  product.title,
  product.descriptionHtml ?? "",
  product.productType ?? "",
);
const content = buildAutomatedProductContent(product, classification);

assert.equal(content.title, "Natural Pink Thulite Pendant");
assert.equal(content.focusKeyword, "pendant necklace");
assert.ok(content.shortDescription.toLowerCase().includes("pink thulite"));
assert.ok(content.descriptionHtml.includes("<p>"));
assert.ok(content.descriptionHtml.includes("<h3>Product Details</h3>"));
assert.ok(content.descriptionHtml.includes("925 Sterling Silver"));
assert.ok(!content.descriptionHtml.toLowerCase().includes("supplier"));
assert.ok(content.highlights.some((item) => item.includes("925 Sterling Silver")));
assert.ok(content.longTailKeywords.length > 0);
assert.ok(content.seoKeywords.includes("pendant necklace"));
assert.ok(content.seoTitle.endsWith("| MVQueen"));
assert.ok(content.seoTitle.length <= 60);
assert.ok(content.metaDescription.length <= 155);
assert.ok(!JSON.stringify(content).toLowerCase().includes("supplier"));

const pendantWithParentRoute = classifyProduct(
  "Pink Thulite Pendant in 925 Sterling Silver",
  "<p>Wear this pendant alone or layer it with your favorite necklaces.</p>",
  "Pendant Necklace",
);
assert.equal(pendantWithParentRoute.department, "Jewelry");
assert.equal(pendantWithParentRoute.family, "Necklaces");
assert.equal(pendantWithParentRoute.subcollection, "Pendant Necklaces");
assert.equal(pendantWithParentRoute.route, "pendants");
assert.equal(pendantWithParentRoute.productType, "Pendant Necklace");
assert.equal(pendantWithParentRoute.confidence, "high");

const unclassified: ProductSnapshot = {
  id: "gid://shopify/Product/2",
  title: "Mystery Item",
  descriptionHtml: "<p>Verified source description.</p>",
  tags: [],
  variants: { nodes: [{ id: "gid://shopify/ProductVariant/2", price: "10.00" }] },
};
assert.equal(classifyProduct(
  unclassified.title,
  unclassified.descriptionHtml ?? "",
  "",
).confidence, "review");


const activewear: ProductSnapshot = {
  id: "gid://shopify/Product/3",
  title: "Ruched Sports Bra and High-Waisted Shorts Active Set",
  descriptionHtml: [
    "<ul>",
    "<li>Features: Ruched</li>",
    "<li>Number of pieces: Two-piece</li>",
    "<li>Stretch: Moderate stretch</li>",
    "<li>Material composition: 94% polyester, 6% elastane</li>",
    "</ul>",
    "<p>Product Measurements (Measurements by inches) &amp; Size Conversion</p>",
    "<table><tr><th style=\"background-color: lightgray;\">Size</th><th>Bust</th></tr><tr><td>S</td><td>30.7</td></tr></table>",
  ].join(""),
  tags: [],
  options: [
    { name: "Color", values: ["Pink", "Black", "Yellow"] },
    { name: "Size", values: ["S", "M", "L", "XL"] },
  ],
  variants: { nodes: [{ id: "gid://shopify/ProductVariant/3", price: "39.24" }] },
};

const activewearClassification = classifyProduct(
  activewear.title,
  activewear.descriptionHtml ?? "",
  "",
);
assert.equal(activewearClassification.department, "Fashion");
assert.equal(activewearClassification.family, "Activewear");
assert.equal(activewearClassification.subcollection, "Activewear Sets");
assert.equal(activewearClassification.productType, "Activewear Set");
assert.equal(activewearClassification.confidence, "high");
const activewearBrand = classifyBrandWorld(activewear);
assert.equal(activewearBrand.brand, "miss-princess");
assert.equal(activewearBrand.tone, "soft-playful");
assert.equal(activewearBrand.reason, "color:pink");
const activewearContent = buildAutomatedProductContent(
  activewear,
  activewearClassification,
  "Miss.Princess",
);
assert.ok(activewearContent.seoTitle.endsWith("| Miss.Princess"));
assert.ok(activewearContent.seoTitle.length <= 60);
assert.ok(activewearContent.metaDescription.includes("at Miss.Princess."));
assert.ok(activewearContent.shortDescription.startsWith("An activewear set with"));
assert.ok(activewearContent.shortDescription.includes("two-piece design"));
assert.ok(activewearContent.shortDescription.includes("ruched detailing"));
assert.ok(activewearContent.shortDescription.includes("moderate stretch"));
assert.ok(!activewearContent.shortDescription.toLowerCase().startsWith("product measurements"));
assert.ok(activewearContent.descriptionHtml.includes("<table>"));
assert.ok(activewearContent.descriptionHtml.includes("Size &amp; Measurements"));
assert.ok(activewearContent.descriptionHtml.includes("Features: Ruched"));
assert.ok(!activewearContent.descriptionHtml.includes("style="));

assert.equal(needsMediaAltRepair(""), true);
assert.equal(
  needsMediaAltRepair("831d8f1bc6d34234ad68675383084a38-Max-Origin"),
  true,
);
assert.equal(needsMediaAltRepair("product-image.jpg"), true);
assert.equal(needsMediaAltRepair("IMG_1234"), true);
assert.equal(
  needsMediaAltRepair("Brown aventurine bead necklace, alternate product view"),
  false,
);

assert.equal(
  shouldPublishAutomatedDescription({
    topic: "PRODUCTS_CREATE",
    currentDescriptionHtml: "<p>Supplier copy already exists.</p>",
  }),
  true,
);
assert.equal(
  shouldPublishAutomatedDescription({
    topic: "products/update",
    currentDescriptionHtml: "",
  }),
  true,
);
assert.equal(
  shouldPublishAutomatedDescription({
    topic: "products/update",
    currentDescriptionHtml:
      "<p><strong>A Quiet Statement</strong></p><p>Curated MVQueen copy.</p>",
  }),
  false,
);

console.log("product content automation tests passed");
