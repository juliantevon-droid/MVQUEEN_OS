import assert from "node:assert/strict";
import { selectTaxonomyValues } from "./shopify-category-enrichment";
import { classifyProduct, type ProductSnapshot } from "./mvqueen-intelligence";
import { buildCatalogAttributeEnrichment } from "./catalog-attribute-enrichment";

const product: ProductSnapshot = {
  id: "gid://shopify/Product/necklace",
  title: "Divine Radiance Cross Necklace",
  descriptionHtml: "<p>14K gold-plated cross with sparkling crystal details.</p>",
  productType: "Necklaces",
  seo: { title: "Divine Cross Necklace | 14K Gold Plated Crystal Pendant", description: "Adjustable chain with spiritual symbolism and sparkling details." },
  attributeMetafields: {
    nodes: [{
      key: "source_attributes",
      value: JSON.stringify({ chain_length: "440 - 490 mm, adjustable" }),
      type: "json",
    }],
  },
  variants: {
    nodes: [{
      id: "gid://shopify/ProductVariant/1",
      googleMetafields: {
        nodes: [
          { key: "color", value: "Gold", type: "single_line_text_field" },
          { key: "material", value: "Gold-plated", type: "single_line_text_field" },
        ],
      },
    }],
  },
};

const classification = classifyProduct(
  product.title,
  product.descriptionHtml ?? "",
  product.productType ?? "",
);
const enrichment = buildCatalogAttributeEnrichment(product, classification);

const value = (id: string, name: string) => ({ id, name });

assert.deepEqual(
  selectTaxonomyValues({
    attribute: {
      id: "color",
      name: "Color",
      values: [value("gold", "Gold"), value("silver", "Silver")],
    },
    product,
    enrichment,
    classification,
  }).map((item) => item.name),
  ["Gold"],
);

assert.deepEqual(
  selectTaxonomyValues({
    attribute: {
      id: "age",
      name: "Age group",
      values: [value("adult", "Adults"), value("kids", "Kids")],
    },
    product,
    enrichment,
    classification,
  }).map((item) => item.name),
  ["Adults"],
);

assert.deepEqual(
  selectTaxonomyValues({
    attribute: {
      id: "gender",
      name: "Target gender",
      values: [value("female", "Female"), value("male", "Male")],
    },
    product,
    enrichment,
    classification,
  }).map((item) => item.name),
  ["Female"],
);

assert.deepEqual(
  selectTaxonomyValues({
    attribute: {
      id: "material",
      name: "Jewelry material",
      values: [
        value("gold-plated", "Gold-plated"),
        value("gold", "Gold"),
      ],
    },
    product,
    enrichment,
    classification,
  }).map((item) => item.name),
  ["Gold-plated"],
);

assert.deepEqual(
  selectTaxonomyValues({
    attribute: {
      id: "design",
      name: "Necklace design",
      values: [value("pendant", "Pendant"), value("chain", "Chain")],
    },
    product,
    enrichment,
    classification,
  }).map((item) => item.name),
  ["Pendant"],
);

assert.deepEqual(
  selectTaxonomyValues({
    attribute: {
      id: "length",
      name: "Necklace length type",
      values: [
        value("choker", "Choker"),
        value("princess", "Princess"),
        value("matinee", "Matinee"),
      ],
    },
    product,
    enrichment,
    classification,
  }).map((item) => item.name),
  ["Princess"],
);

assert.deepEqual(
  selectTaxonomyValues({
    attribute: {
      id: "jewelry-type",
      name: "Jewelry type",
      values: [
        value("fine", "Fine jewelry"),
        value("imitation", "Imitation jewelry"),
      ],
    },
    product,
    enrichment,
    classification,
  }),
  [],
);

console.log("shopify category enrichment tests passed");
