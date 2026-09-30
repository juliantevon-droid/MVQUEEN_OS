import assert from "node:assert/strict";
import {
  buildCatalogAttributeEnrichment,
  buildCatalogAttributeMetafields,
} from "./catalog-attribute-enrichment";
import {
  classifyProduct,
  type ProductSnapshot,
} from "./mvqueen-intelligence";

const activewear: ProductSnapshot = {
  id: "gid://shopify/Product/9087726584006",
  title: "Ruched Sports Bra and High-Waisted Shorts Active Set",
  productType: "Activewear Set",
  descriptionHtml: [
    "<p>Designed for the Miss.Princess edit.</p>",
    "<ul>",
    "<li>Number of pieces: Two-piece</li>",
    "<li>Features: Ruched</li>",
    "<li>Stretch: Moderate stretch</li>",
    "<li>Material composition: 94% polyester, 6% elastane</li>",
    "<li>Machine wash cold; tumble dry low</li>",
    "</ul>",
  ].join(""),
  tags: [],
  options: [
    { name: "Color", values: ["Pink", "Black", "Yellow"] },
    { name: "Size", values: ["S", "M", "L", "XL"] },
  ],
};

const classification = classifyProduct(
  activewear.title,
  activewear.descriptionHtml ?? "",
  activewear.productType ?? "",
);
const enrichment = buildCatalogAttributeEnrichment(activewear, classification);

assert.deepEqual(enrichment.colors, ["Pink", "Black", "Yellow"]);
assert.deepEqual(enrichment.sizes, ["S", "M", "L", "XL"]);
assert.equal(enrichment.material, "94% polyester, 6% elastane");
assert.equal(enrichment.fabric, "94% polyester, 6% elastane");
assert.equal(enrichment.targetGender, "Women");
assert.equal(enrichment.ageGroup, "Adult");
assert.equal(enrichment.sizeType, "regular");
assert.ok(enrichment.activities.includes("Workout"));
assert.ok(enrichment.features.includes("Ruched"));
assert.ok(enrichment.features.includes("Moderate stretch"));
assert.ok(enrichment.features.includes("High-waisted"));
assert.equal(enrichment.careInstructions, "Machine wash cold; tumble dry low");
assert.equal(enrichment.sourceAttributes.material_composition, "94% polyester, 6% elastane");

const metafields = buildCatalogAttributeMetafields(
  enrichment,
  classification,
  "miss-princess",
);
const byKey = new Map(
  metafields.map((item) => [`${item.namespace}.${item.key}`, item]),
);

assert.equal(byKey.get("attributes.color")?.value, "Pink / Black / Yellow");
assert.equal(
  byKey.get("attributes.sizes")?.value,
  JSON.stringify(["S", "M", "L", "XL"]),
);
assert.equal(byKey.get("attributes.material")?.value, "94% polyester, 6% elastane");
assert.equal(byKey.get("attributes.size_type")?.value, "regular");
assert.equal(byKey.get("mm-google-shopping.gender")?.value, "female");
assert.equal(byKey.get("mm-google-shopping.age_group")?.value, "adult");
assert.equal(byKey.get("mm-google-shopping.size_type")?.value, "regular");
assert.equal(byKey.get("mm-google-shopping.custom_label_0")?.value, "miss-princess");
assert.equal(byKey.get("mm-google-shopping.custom_label_1")?.value, "Fashion");
assert.equal(byKey.has("mm-google-shopping.color"), false);
assert.equal(byKey.has("mm-google-shopping.size"), false);

const singleVariant: ProductSnapshot = {
  id: "gid://shopify/Product/single",
  title: "Black Fitted Midi Dress",
  productType: "Dress",
  descriptionHtml: "<ul><li>Material: 95% polyester, 5% elastane</li><li>Occasion: Evening</li></ul>",
  options: [
    { name: "Color", values: ["Black"] },
    { name: "Size", values: ["M"] },
  ],
};
const singleClassification = classifyProduct(
  singleVariant.title,
  singleVariant.descriptionHtml ?? "",
  singleVariant.productType ?? "",
);
const singleEnrichment = buildCatalogAttributeEnrichment(
  singleVariant,
  singleClassification,
);
const singleFields = buildCatalogAttributeMetafields(
  singleEnrichment,
  singleClassification,
  "mvqueen",
);
const singleByKey = new Map(
  singleFields.map((item) => [`${item.namespace}.${item.key}`, item]),
);
assert.equal(singleEnrichment.fit, "Fitted");
assert.ok(singleEnrichment.occasions.includes("Evening"));
assert.equal(singleByKey.get("mm-google-shopping.color")?.value, "Black");
assert.equal(singleByKey.get("mm-google-shopping.size")?.value, "M");

console.log("catalog attribute enrichment tests passed");
