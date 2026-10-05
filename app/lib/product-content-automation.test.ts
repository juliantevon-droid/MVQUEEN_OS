import assert from "node:assert/strict";
import { copyFileSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { tmpdir } from "node:os";
import { BRAND_VOCABULARY, BRAND_VOCABULARY_SOURCES, loadBrandVocabulary } from "./brand-vocabulary.server";
import {
  buildAutomatedProductContent,
  needsMediaAltRepair,
  productClaimReviewReasons,
  removeHighRiskClaimLanguage,
  shouldPublishAutomatedDescription,
} from "./product-content-automation";
import {
  classifyBrandWorld,
  classifyProduct,
  productTypeForWrite,
  type ProductSnapshot,
  usableProductType,
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

assert.match(content.title, /Natural Pink Thulite Pendant Necklace$/);
assert.ok(BRAND_VOCABULARY.profiles.mvqueen.adjectives.includes(content.title.split(" ")[0].toLowerCase()));
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
assert.equal(activewearBrand.tone, "vivid-youthful");
assert.equal(activewearBrand.reason, "color:pink");
const activewearContent = buildAutomatedProductContent(
  activewear,
  activewearClassification,
  "Miss.Princess",
);
assert.ok(activewearContent.seoTitle.endsWith("| Miss.Princess"));
assert.ok(activewearContent.seoTitle.length <= 60);
assert.ok(!activewearContent.seoTitle.includes("…"));
assert.ok(activewearContent.metaDescription.includes("at Miss.Princess."));
assert.ok(activewearContent.shortDescription.includes("Miss.Princess"));
assert.ok(activewearContent.descriptionHtml.includes("two-piece design"));
assert.ok(activewearContent.descriptionHtml.includes("ruched detailing"));
assert.ok(activewearContent.descriptionHtml.includes("moderate stretch"));
assert.ok(BRAND_VOCABULARY.profiles["miss-princess"].adjectives.includes(activewearContent.title.split(" ")[0].toLowerCase()));
assert.ok(!activewearContent.shortDescription.toLowerCase().startsWith("product measurements"));
assert.ok(activewearContent.descriptionHtml.includes("<table>"));
assert.ok(activewearContent.descriptionHtml.includes("Size &amp; Measurements"));
assert.ok(activewearContent.descriptionHtml.includes("Features: Ruched"));
assert.ok(!activewearContent.descriptionHtml.includes("style="));
assert.ok(
  activewearContent.longTailKeywords.every(
    (value) => !value.includes("activewear set activewear set"),
  ),
);

const previouslyMvqueenBrandedActivewear: ProductSnapshot = {
  ...activewear,
  id: "gid://shopify/Product/brand-copy-alignment",
  vendor: "MVQueen",
  descriptionHtml: [
    "<p>Designed for the MVQueen edit, this two-piece active set pairs a ruched sports bra with high-waisted shorts for a streamlined look.</p>",
    "<ul>",
    "<li>Features: Ruched</li>",
    "<li>Number of pieces: Two-piece</li>",
    "<li>Stretch: Moderate stretch</li>",
    "<li>Material composition: 94% polyester, 6% elastane</li>",
    "</ul>",
  ].join(""),
};
const alignedPrincessContent = buildAutomatedProductContent(
  previouslyMvqueenBrandedActivewear,
  activewearClassification,
  "Miss.Princess",
);
assert.ok(alignedPrincessContent.shortDescription.includes("Miss.Princess"));
assert.ok(!alignedPrincessContent.shortDescription.includes("MVQueen"));
assert.ok(alignedPrincessContent.descriptionHtml.includes("Miss.Princess"));
assert.ok(!alignedPrincessContent.descriptionHtml.includes("MVQueen"));
assert.ok(alignedPrincessContent.metaDescription.includes("Miss.Princess"));
assert.ok(!alignedPrincessContent.metaDescription.includes("MVQueen"));
assert.ok(alignedPrincessContent.seoTitle.endsWith("| Miss.Princess"));


const princessPaletteProduct: ProductSnapshot = {
  id: "gid://shopify/Product/princess-palette",
  title: "Summer Mini Dress",
  tags: [],
  options: [{ name: "Color", values: ["Sky Blue", "Electric Blue", "Lilac"] }],
  variants: { nodes: [{ id: "gid://shopify/ProductVariant/princess", price: "48.00" }] },
};
const princessPaletteRoute = classifyBrandWorld(princessPaletteProduct);
assert.equal(princessPaletteRoute.brand, "miss-princess");
assert.equal(princessPaletteRoute.tone, "vivid-youthful");
assert.equal(princessPaletteRoute.reason, "color:sky-blue");

const mvqueenPaletteProduct: ProductSnapshot = {
  id: "gid://shopify/Product/mvqueen-palette",
  title: "Statement Set",
  tags: [],
  options: [{ name: "Color", values: ["Gold", "Charcoal", "Burgundy"] }],
  variants: { nodes: [{ id: "gid://shopify/ProductVariant/mvqueen", price: "58.00" }] },
};
const mvqueenPaletteRoute = classifyBrandWorld(mvqueenPaletteProduct);
assert.equal(mvqueenPaletteRoute.brand, "mvqueen");
assert.equal(mvqueenPaletteRoute.tone, "bold-authoritative");
assert.equal(mvqueenPaletteRoute.reason, "color:gold");

const divineRadianceCross: ProductSnapshot = {
  id: "gid://shopify/Product/divine-radiance-cross",
  title: "Divine Radiance Cross Necklace",
  descriptionHtml:
    "<p>14K gold-plated cross with sparkling crystal details channels confidence and warmth.</p>",
  tags: [],
  variants: {
    nodes: [{ id: "gid://shopify/ProductVariant/divine-radiance-cross", price: "37.99" }],
  },
};
const divineRadianceRoute = classifyBrandWorld(divineRadianceCross);
assert.equal(divineRadianceRoute.brand, "mvqueen");
assert.equal(divineRadianceRoute.tone, "bold-authoritative");
assert.equal(divineRadianceRoute.reason, "material:gold-plated");

const divineSeoProduct: ProductSnapshot = {
  ...divineRadianceCross,
  attributeMetafields: {
    nodes: [
      {
        key: "source_attributes",
        value: JSON.stringify({ color: "Gold", material: "Gold-plated" }),
      },
    ],
  },
};
const divineSeoClassification = classifyProduct(
  divineSeoProduct.title,
  divineSeoProduct.descriptionHtml ?? "",
  "Necklace",
);
const divineSeoContent = buildAutomatedProductContent(
  divineSeoProduct,
  divineSeoClassification,
  "MVQueen",
);
assert.ok(
  divineSeoContent.longTailKeywords.every(
    (value) => !value.includes("gold gold-plated"),
  ),
);
assert.ok(
  divineSeoContent.longTailKeywords.every(
    (value) => !value.includes("necklace necklace"),
  ),
);

const playfulGoldPlatedJewelry: ProductSnapshot = {
  id: "gid://shopify/Product/playful-gold-plated",
  title: "Pink Crystal Cross Necklace",
  descriptionHtml: "<p>Gold-plated necklace with playful pink crystal details.</p>",
  tags: [],
  variants: {
    nodes: [{ id: "gid://shopify/ProductVariant/playful-gold-plated", price: "32.00" }],
  },
};
const playfulGoldPlatedRoute = classifyBrandWorld(playfulGoldPlatedJewelry);
assert.equal(playfulGoldPlatedRoute.brand, "miss-princess");
assert.equal(playfulGoldPlatedRoute.reason, "color:pink");

const sharedPinkOnly: ProductSnapshot = {
  id: "gid://shopify/Product/shared-pink",
  title: "Pink Top",
  tags: [],
  options: [{ name: "Color", values: ["Pink"] }],
  variants: { nodes: [{ id: "gid://shopify/ProductVariant/shared-pink", price: "30.00" }] },
};
assert.equal(classifyBrandWorld(sharedPinkOnly).brand, "miss-princess");

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

assert.equal(
  shouldPublishAutomatedDescription({
    topic: "products/update",
    currentDescriptionHtml:
      "<p>Existing supplier-style product description with useful source facts.</p>",
    allowExistingRewrite: true,
  }),
  true,
);


const lipBalmClassification = classifyProduct(
  "4-color Brightening Lip Balm Moisturizing Lip Gloss Women Cosmetics",
  "",
  "0",
);
assert.equal(lipBalmClassification.department, "Beauty");
assert.equal(lipBalmClassification.family, "Makeup");
assert.equal(lipBalmClassification.route, "makeup");
assert.equal(lipBalmClassification.confidence, "high");

const faceCreamClassification = classifyProduct(
  "Face Firming Cream",
  "<p>Facial skin care cream.</p>",
  "0",
);
assert.equal(faceCreamClassification.family, "Skincare");
assert.equal(faceCreamClassification.route, "skincare");
assert.equal(faceCreamClassification.confidence, "high");

const centellaClassification = classifyProduct(
  "Beauty Madagascar Centella Asiatica Facial Skin Care",
  "",
  "0",
);
assert.equal(centellaClassification.family, "Skincare");
assert.equal(centellaClassification.route, "skincare");

const hairOilClassification = classifyProduct(
  "Rosemary Coconut Hair Oil Nourishing Moisturizing Fragrance Care Hair Care",
  "",
  "0",
);
assert.equal(hairOilClassification.family, "Hair Care");
assert.equal(hairOilClassification.route, "hair-treatments");
assert.equal(hairOilClassification.confidence, "high");

const bodyMoisturizerClassification = classifyProduct(
  "Body Moisturizer Hydrating Skin Care",
  "",
  "0",
);
assert.equal(bodyMoisturizerClassification.family, "Bath & Body");
assert.equal(bodyMoisturizerClassification.route, "bath-body");

assert.equal(usableProductType("0"), false);
assert.equal(usableProductType("unknown"), false);
assert.equal(usableProductType("Necklace"), true);


const ankletWithBadOldType = classifyProduct(
  "Double Heart Anklet Bracelet Love Barefoot Chain Bling Crystal Ankle Bracelet",
  "<p>Jewelry chain with crystal details.</p>",
  "Activewear Set",
);
assert.equal(ankletWithBadOldType.department, "Jewelry");
assert.equal(ankletWithBadOldType.family, "Anklets");
assert.equal(ankletWithBadOldType.productType, "Anklet");
assert.equal(ankletWithBadOldType.confidence, "high");
assert.equal(productTypeForWrite("Activewear Set", ankletWithBadOldType), "Anklet");

const pressOnNails = classifyProduct(
  "Long Press On Nails With Diamonds Reusable Acrylic Handmade Nails",
  "",
  "5",
);
assert.equal(pressOnNails.department, "Beauty");
assert.equal(pressOnNails.family, "Nails");
assert.equal(pressOnNails.productType, "Press-On Nails");

const bodyOil = classifyProduct("Vitamin E Body Oil", "", "0");
assert.equal(bodyOil.family, "Bath & Body");

const beautyBox = classifyProduct("Mystery Beauty Boxes", "", "0");
assert.equal(beautyBox.family, "Beauty Sets");

const hairMask = classifyProduct("Smooth And Sleek Hair Mask", "", "0");
assert.equal(hairMask.route, "hair-treatments");

const hairRemoval = classifyProduct(
  "Waxing Kit With Wax Warmer And Hair Removal Beads",
  "",
  "4",
);
assert.equal(hairRemoval.family, "Hair Removal");

assert.deepEqual(
  productClaimReviewReasons({
    title: "Herbal Hair Care Solution Anti-hair Loss And Strong",
    descriptionHtml: "<p>Hair care product.</p>",
  }),
  ["hair_loss_or_regrowth"],
);
assert.ok(
  productClaimReviewReasons({
    title: "Light Scar Cream Scar Fine Grain Desalination",
    descriptionHtml: "",
  }).includes("scar_claim"),
);
assert.ok(
  productClaimReviewReasons({
    title: "Electric Cupping Massager Fat Burning Slimming Device",
    descriptionHtml: "",
  }).includes("fat_or_cellulite_claim"),
);
assert.ok(
  productClaimReviewReasons({
    title: "Big Breast Butt Enhancer Skin Firming Cream",
    descriptionHtml: "",
  }).includes("body_enhancement"),
);
assert.deepEqual(
  productClaimReviewReasons({
    title: "Watermelon Body Cream",
    descriptionHtml: "<p>Ingredients: water, watermelon extract, glycerin.</p>",
  }),
  [],
);

assert.equal(
  removeHighRiskClaimLanguage(
    "Electric Vacuum Cupping Massager Anti-Cellulite Fat Burning Slimming Device",
  ).toLowerCase().includes("fat burning"),
  false,
);

const claimReviewProduct: ProductSnapshot = {
  id: "gid://shopify/Product/claim-review",
  title: "Electric Vacuum Cupping Massager Anti-Cellulite Fat Burning Slimming Device",
  vendor: "MVQueen",
  productType: "Beauty Tool",
  descriptionHtml:
    "<p>Vacuum cupping massager for body care.</p><ul><li>Function: Fat burning</li><li>Color: Black</li></ul>",
  tags: [],
  variants: { nodes: [{ id: "gid://shopify/ProductVariant/claim-review", price: "39.00" }] },
};
const claimReviewClassification = classifyProduct(
  claimReviewProduct.title,
  claimReviewProduct.descriptionHtml ?? "",
  claimReviewProduct.productType ?? "",
);
const claimReviewContent = buildAutomatedProductContent(
  claimReviewProduct,
  claimReviewClassification,
  "MVQueen",
);
const claimReviewSerialized = JSON.stringify(claimReviewContent).toLowerCase();
assert.ok(!claimReviewSerialized.includes("anti-cellulite"));
assert.ok(!claimReviewSerialized.includes("fat burning"));
assert.ok(!claimReviewSerialized.includes("slimming"));
assert.ok(claimReviewContent.title.toLowerCase().includes("cupping"));
assert.ok(claimReviewContent.seoTitle.endsWith("| MVQueen"));

const defaultBrandProduct: ProductSnapshot = {
  id: "gid://shopify/Product/default-brand",
  title: "Hydrating Body Serum",
  descriptionHtml: "<p>Body serum.</p>",
  tags: [],
  variants: { nodes: [{ id: "gid://shopify/ProductVariant/default-brand", price: "24.00" }] },
};
const defaultBrandRoute = classifyBrandWorld(defaultBrandProduct);
assert.equal(defaultBrandRoute.brand, "mvqueen");
assert.equal(defaultBrandRoute.confidence, "medium");
assert.equal(defaultBrandRoute.reason, "default-primary-brand");

const tonerPriority = classifyProduct("Pre Makeup Mousse Toner", "", "Needs Review");
assert.equal(tonerPriority.family, "Skincare");
assert.equal(tonerPriority.confidence, "high");

const skinCareOilPriority = classifyProduct(
  "Deep Moisturizing Fragrance Brightening Skin Care Oil",
  "",
  "Needs Review",
);
assert.equal(skinCareOilPriority.family, "Skincare");
assert.equal(skinCareOilPriority.confidence, "high");

const yogaPantsPriority = classifyProduct(
  "Elastic High Waist Slightly Flared Yoga Pants",
  "",
  "Needs Review",
);
assert.equal(yogaPantsPriority.family, "Bottoms");
assert.equal(yogaPantsPriority.productType, "Pants");
assert.equal(yogaPantsPriority.confidence, "high");

const supplierBrandedWaxKit: ProductSnapshot = {
  id: "gid://shopify/Product/supplier-brand-title",
  title: "WUWUVISTA Waxing Kit With Wax Warmer And Hair Removal Beads",
  vendor: "MVQueen",
  productType: "Hair Removal",
  descriptionHtml: [
    "<p>Product information: Applicable people: Ladies Specifications: Standard specifications</p>",
    "<ul>",
    "<li>Specifications: Standard specifications</li>",
    "<li>Net content: 500g</li>",
    "</ul>",
  ].join(""),
  tags: [],
  variants: { nodes: [{ id: "gid://shopify/ProductVariant/supplier-brand-title", price: "32.00" }] },
};
const supplierWaxClassification = classifyProduct(
  supplierBrandedWaxKit.title,
  supplierBrandedWaxKit.descriptionHtml ?? "",
  supplierBrandedWaxKit.productType ?? "",
);
const supplierWaxContent = buildAutomatedProductContent(
  supplierBrandedWaxKit,
  supplierWaxClassification,
  "MVQueen",
);
assert.ok(!supplierWaxContent.title.includes("WUWUVISTA"));
assert.ok(supplierWaxContent.title.length <= 80);
assert.ok(!supplierWaxContent.shortDescription.toLowerCase().startsWith("product information"));
assert.ok(!supplierWaxContent.metaDescription.toLowerCase().includes("standard specifications"));
assert.ok(
  supplierWaxContent.longTailKeywords.every(
    (value) => !value.includes("standard specifications") && !value.includes(" general "),
  ),
);

const attributeDumpProduct: ProductSnapshot = {
  id: "gid://shopify/Product/attribute-dump",
  title: "Hair Removal Cream",
  vendor: "MVQueen",
  productType: "Hair Removal",
  descriptionHtml: [
    "<p>Brand: Shelf life: three years Efficacy: other effects Special purpose cosmetics: Yes Net content: 40g</p>",
    "<ul>",
    "<li>Brand: Generic</li>",
    "<li>Shelf life: three years</li>",
    "<li>Net content: 40g</li>",
    "<li>Specifications: Standard specifications</li>",
    "</ul>",
  ].join(""),
  tags: [],
  variants: { nodes: [{ id: "gid://shopify/ProductVariant/attribute-dump", price: "19.00" }] },
};
const attributeDumpClassification = classifyProduct(
  attributeDumpProduct.title,
  attributeDumpProduct.descriptionHtml ?? "",
  attributeDumpProduct.productType ?? "",
);
const attributeDumpContent = buildAutomatedProductContent(
  attributeDumpProduct,
  attributeDumpClassification,
  "MVQueen",
);
assert.ok(!attributeDumpContent.shortDescription.toLowerCase().startsWith("brand:"));
assert.ok(!attributeDumpContent.metaDescription.toLowerCase().includes("shelf life"));
assert.ok(
  attributeDumpContent.longTailKeywords.every(
    (value) =>
      !value.includes("standard specifications") &&
      !value.includes("brand") &&
      !value.includes("other effects"),
  ),
);

const supplierNecklace: ProductSnapshot = {
  id: "gid://shopify/Product/9100059869382",
  handle: "european-and-american-fashion-special-interest-color-zircon-star-pendant-stainless-steel-necklace",
  title: "European And American Fashion Special-interest Color Zircon Star Pendant Stainless Steel Necklace",
  vendor: "MVQueen",
  productType: "Pendant Necklace",
  descriptionHtml: "<p>Product information: Treatment process: Electroplating</p><ul><li>Material: Stainless steel</li><li>Treatment process: Electroplating</li></ul>",
  tags: ["mvq:brand:mvqueen"],
  variants: { nodes: [{ id: "gid://shopify/ProductVariant/48246503669958", price: "34.29", sku: "CJLX244727201AZ" }] },
};
const necklaceClassification = classifyProduct(supplierNecklace.title, supplierNecklace.descriptionHtml ?? "", supplierNecklace.productType ?? "");
const necklaceBefore = structuredClone(supplierNecklace);
const necklaceCopy = buildAutomatedProductContent(supplierNecklace, necklaceClassification);
assert.match(necklaceCopy.title, /Stainless Steel Zircon Star Pendant Necklace$/);
assert.ok(!/european|american|special-interest|fashion/i.test(necklaceCopy.title));
assert.ok(necklaceCopy.title.length <= 80);
assert.ok(necklaceCopy.shortDescription.length <= 180);
assert.ok(!necklaceCopy.shortDescription.includes("…"));
assert.ok(!necklaceCopy.shortDescription.includes("Product information"));
assert.match(necklaceCopy.shortDescription, /[.!?]$/);
assert.ok(necklaceCopy.descriptionHtml.includes("Stainless steel"));
assert.ok(necklaceCopy.descriptionHtml.includes("Electroplating"));
assert.ok(!/solid gold|handmade|waterproof|hypoallergenic|50\s*cm/i.test(JSON.stringify(necklaceCopy)));
assert.deepEqual(supplierNecklace, necklaceBefore);
const repeatedNecklace = buildAutomatedProductContent({ ...supplierNecklace, title: necklaceCopy.title, descriptionHtml: necklaceCopy.descriptionHtml }, necklaceClassification);
assert.equal(repeatedNecklace.title, necklaceCopy.title);
assert.equal(repeatedNecklace.shortDescription, necklaceCopy.shortDescription);

const extraLongNecklace = buildAutomatedProductContent({ ...supplierNecklace, title: "Natural Pink Crystal Pearl Beaded Delicate Star Pendant Stainless Steel Layered Necklace ".repeat(3) }, necklaceClassification);
assert.ok(extraLongNecklace.title.length <= 80);
assert.match(extraLongNecklace.title, /Necklace$/);
assert.ok(extraLongNecklace.shortDescription.length <= 180);
assert.ok(!extraLongNecklace.shortDescription.includes("…"));
const repeatedLongNecklace = buildAutomatedProductContent({ ...supplierNecklace, title: extraLongNecklace.title, descriptionHtml: extraLongNecklace.descriptionHtml }, necklaceClassification);
assert.equal(repeatedLongNecklace.title, extraLongNecklace.title);
assert.equal(repeatedLongNecklace.shortDescription, extraLongNecklace.shortDescription);

const paragraphFacts = buildAutomatedProductContent({ ...activewear, descriptionHtml: "<p>Fabric: 94% polyester, 6% elastane<br>Care: Machine wash cold; tumble dry low</p>" }, activewearClassification, "Miss.Princess");
assert.ok(paragraphFacts.descriptionHtml.includes("94% polyester, 6% elastane"));
assert.ok(paragraphFacts.descriptionHtml.includes("Machine wash cold; tumble dry low"));
const repeatedActivewear = buildAutomatedProductContent({ ...activewear, title: activewearContent.title, descriptionHtml: activewearContent.descriptionHtml }, activewearClassification, "Miss.Princess");
assert.equal(repeatedActivewear.title, activewearContent.title);
assert.equal(repeatedActivewear.shortDescription, activewearContent.shortDescription);
assert.equal(repeatedActivewear.descriptionHtml, activewearContent.descriptionHtml);

const manyFacts = buildAutomatedProductContent({ ...activewear, descriptionHtml: "<ul>" + ["Features: Ruched", "Number of pieces: Two-piece", "Stretch: Moderate stretch", "Material composition: 94% polyester, 6% elastane", "Color: Pink", "Fit: Fitted", "Care: Machine wash cold", "Origin: Imported"].map((fact) => `<li>${fact}</li>`).join("") + "</ul>" }, activewearClassification, "Miss.Princess");
assert.ok(manyFacts.descriptionHtml.includes("Care: Machine wash cold"));
assert.ok(manyFacts.descriptionHtml.includes("Origin: Imported"));

const legacyStructuredFacts: ProductSnapshot = {
  ...activewear,
  descriptionHtml: "<ul><li>Two-piece activewear set</li><li>Ruched detailing</li><li>Moderate stretch</li><li>94% polyester, 6% elastane</li><li>Machine wash cold; tumble dry low</li><li>Imported</li></ul>",
  attributeMetafields: { nodes: [{ key: "source_attributes", value: JSON.stringify({ features: "Ruched", number_of_pieces: "Two-piece", stretch: "Moderate stretch", material_composition: "94% polyester, 6% elastane" }) }] },
  variants: { nodes: [{ id: "gid://shopify/ProductVariant/3", googleMetafields: { nodes: [{ key: "material", value: "94% polyester, 6% elastane" }] } }] },
};
const deduplicatedCopy = buildAutomatedProductContent(legacyStructuredFacts, activewearClassification, "Miss.Princess");
assert.equal(deduplicatedCopy.highlights.filter((detail) => /94% polyester/.test(detail)).length, 1);
assert.equal(deduplicatedCopy.highlights.filter((detail) => /ruched/i.test(detail)).length, 1);
assert.equal(deduplicatedCopy.highlights.filter((detail) => /two-piece/i.test(detail)).length, 1);
assert.equal(deduplicatedCopy.highlights.filter((detail) => /moderate stretch/i.test(detail)).length, 1);
assert.ok(deduplicatedCopy.descriptionHtml.includes("Machine wash cold; tumble dry low"));
assert.ok(deduplicatedCopy.descriptionHtml.includes("Imported"));
const deduplicatedRepeat = buildAutomatedProductContent({ ...legacyStructuredFacts, title: deduplicatedCopy.title, descriptionHtml: deduplicatedCopy.descriptionHtml }, activewearClassification, "Miss.Princess");
assert.equal(deduplicatedRepeat.descriptionHtml, deduplicatedCopy.descriptionHtml);
const distinctNumericDetails = buildAutomatedProductContent({ ...supplierNecklace, descriptionHtml: "<ul><li>Length: 45</li><li>Weight: 45</li></ul>" }, necklaceClassification);
assert.ok(distinctNumericDetails.highlights.includes("Length: 45"));
assert.ok(distinctNumericDetails.highlights.includes("Weight: 45"));
const platedSteelSource = { ...supplierNecklace, attributeMetafields: { nodes: [{ key: "source_attributes", value: JSON.stringify({ material: "Stainless steel", treatment_process: "Electroplating", purity: "18K" }) }] } };
const platedSteelBefore = structuredClone(platedSteelSource);
const platedSteelCopy = buildAutomatedProductContent(platedSteelSource, necklaceClassification);
assert.ok(platedSteelCopy.descriptionHtml.includes("Stainless steel"));
assert.ok(platedSteelCopy.descriptionHtml.includes("Electroplating"));
assert.ok(!/purity|solid gold/i.test(platedSteelCopy.descriptionHtml));
assert.deepEqual(platedSteelSource, platedSteelBefore);

const cleanUnspecified = buildAutomatedProductContent({ ...supplierNecklace, title: "Star Pendant", descriptionHtml: "", variants: { nodes: [] } }, necklaceClassification);
assert.ok(!/silk|velvet|satin|gold|silver|stainless|cruelty|vegan|artisan/i.test(cleanUnspecified.descriptionHtml));
const noisyCopy = buildAutomatedProductContent({ ...supplierNecklace, title: "Amazing Stunning OUHOE Zircon Star Pendant" }, necklaceClassification);
assert.ok(!/amazing|stunning|ouhoe/i.test(JSON.stringify(noisyCopy)));

// Prove the writer consumes the files, including an edited persona adjective,
// and that source edits invalidate the automation fingerprint.
const vocabularyRoot = mkdtempSync(join(tmpdir(), "mvqueen-vocabulary-test-"));
try {
  for (const source of BRAND_VOCABULARY_SOURCES) {
    const destination = join(vocabularyRoot, source);
    mkdirSync(dirname(destination), { recursive: true });
    copyFileSync(source, destination);
  }
  const personaFile = join(vocabularyRoot, BRAND_VOCABULARY_SOURCES[3]);
  const original = readFileSync(personaFile, "utf8");
  const changed = original.replace('"elevated", "polished", "luxurious", "refined", "timeless", "intentional"', '"considered", "polished", "luxurious", "refined", "timeless", "intentional"');
  assert.notEqual(changed, original);
  writeFileSync(personaFile, changed);
  const revisedVocabulary = loadBrandVocabulary(vocabularyRoot);
  assert.notEqual(revisedVocabulary.version, BRAND_VOCABULARY.version);
  assert.ok(revisedVocabulary.profiles.mvqueen.adjectives.includes("considered"));
  const names = Array.from({ length: 100 }, (_, index) => buildAutomatedProductContent({ ...supplierNecklace, id: "gid://shopify/Product/test-vocabulary-" + index }, necklaceClassification, "MVQueen", revisedVocabulary).title);
  assert.ok(names.some((name) => name.startsWith("Considered ")));
  const forbiddenFile = join(vocabularyRoot, BRAND_VOCABULARY_SOURCES[2]);
  const forbiddenSource = readFileSync(forbiddenFile, "utf8");
  writeFileSync(forbiddenFile, forbiddenSource.replace("## Tier 2", "| Considered | Editorial review |\n\n## Tier 2"));
  const restrictedVocabulary = loadBrandVocabulary(vocabularyRoot);
  assert.ok(!restrictedVocabulary.profiles.mvqueen.adjectives.includes("considered"));
  assert.notEqual(restrictedVocabulary.version, revisedVocabulary.version);
  rmSync(personaFile);
  assert.throws(() => loadBrandVocabulary(vocabularyRoot), /ENOENT/);
} finally {
  rmSync(vocabularyRoot, { recursive: true, force: true });
}

console.log("product content automation tests passed");
