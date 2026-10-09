import assert from "node:assert/strict";
import { copyFileSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { tmpdir } from "node:os";
import { BRAND_VOCABULARY, BRAND_VOCABULARY_SOURCES, loadBrandVocabulary } from "./brand-vocabulary.server";
import { CURATED_PRODUCT_NAMES, matchingCuratedName, normalizeProductName } from "./curated-product-names";
import { stripNamingDecoration } from "./product-naming";
import {
  buildAutomatedProductContent,
  needsMediaAltRepair,
  productClaimReviewReasons,
  removeHighRiskClaimLanguage,
  resolveUniqueAutomatedProductContent,
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

assert.match(content.title, /Natural Pink Thulite Pendant Necklace\b/);
assert.ok(["evocative", "descriptive-poetic", "identity-led"].includes(content.namingRegister));
assert.ok(BRAND_VOCABULARY.profiles.mvqueen.adjectives.some((word) => content.shortDescription.toLowerCase().includes(word)));
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
assert.ok(["evocative", "descriptive-poetic", "identity-led"].includes(activewearContent.namingRegister));
assert.ok(activewearContent.seoTitle.length <= 60);
assert.ok(!activewearContent.seoTitle.includes("…"));
assert.ok(activewearContent.metaDescription.includes("at Miss.Princess."));
assert.ok(activewearContent.shortDescription.includes("Miss.Princess"));
assert.ok(activewearContent.descriptionHtml.includes("two-piece design"));
assert.ok(activewearContent.descriptionHtml.includes("ruched detailing"));
assert.ok(activewearContent.descriptionHtml.includes("moderate stretch"));
assert.ok(BRAND_VOCABULARY.profiles["miss-princess"].adjectives.some((word) => activewearContent.shortDescription.toLowerCase().includes(word)));
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

assert.deepEqual(
  productClaimReviewReasons({
    title: "Wood Comb Professional Hair Loss Massage Brush",
    descriptionHtml: "<p>Wood paddle brush.</p>",
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

assert.ok(
  productClaimReviewReasons({
    title: "Skin Moisturizing Whitening Repair Cream",
    descriptionHtml: "<p>Body cream.</p>",
  }).includes("skin_lightening_claim"),
);

assert.ok(
  productClaimReviewReasons({
    title: "Skin Moisturizing Repair Cream",
    descriptionHtml: "<p>Body cream.</p>",
    handle: "skin-moisturizing-whitening-repair-whitening-cream",
    attributeMetafields: {
      nodes: [{
        key: "source_attributes",
        value: JSON.stringify({ key_words: "bright white cream", cosmetic_efficacy: "firming" }),
      }],
    },
  }).includes("skin_lightening_claim"),
);
assert.ok(
  productClaimReviewReasons({
    title: "Essential Oil",
    descriptionHtml: "<p>Body oil.</p>",
    handle: "breast-care-essential-oil",
  }).includes("body_enhancement"),
);
assert.ok(
  !removeHighRiskClaimLanguage("Skin Moisturizing Whitening Repair Cream")
    .toLowerCase()
    .includes("whitening"),
);

assert.ok(
  productClaimReviewReasons({
    title: "Turmeric Firming Care Face Cream",
    descriptionHtml: "<p>Face cream.</p>",
  }).includes("firming_tightening_claim"),
);
assert.ok(
  !removeHighRiskClaimLanguage("Turmeric Firming Care Face Cream")
    .toLowerCase()
    .includes("firming"),
);

assert.ok(
  productClaimReviewReasons({
    title: "Lavender Essential Oil",
    descriptionHtml: "<p>Helps sleep and improve insomnia.</p>",
  }).includes("wellness_health_claim"),
);
assert.ok(
  !removeHighRiskClaimLanguage("Lavender oil helps sleep and improve insomnia")
    .toLowerCase()
    .includes("insomnia"),
);

assert.ok(
  productClaimReviewReasons({
    title: "Anti Acne Moisturizer Cream",
    descriptionHtml: "<p>Moisturizer.</p>",
  }).includes("acne_treatment_claim"),
);
assert.ok(
  !removeHighRiskClaimLanguage("Anti Acne Moisturizer Cream")
    .toLowerCase()
    .includes("anti acne"),
);
assert.ok(
  productClaimReviewReasons({
    title: "Body Shaping Care Bath Oil",
    descriptionHtml: "<p>Bath oil.</p>",
  }).includes("fat_or_cellulite_claim"),
);
assert.ok(
  !removeHighRiskClaimLanguage("Body Shaping Care Bath Oil")
    .toLowerCase()
    .includes("body shaping"),
);

assert.equal(
  removeHighRiskClaimLanguage(
    "Electric Vacuum Cupping Massager Anti-Cellulite Fat Burning Slimming Device",
  ).toLowerCase().includes("fat burning"),
  false,
);

const polishedClaimText = removeHighRiskClaimLanguage(
  "Big Breast Butt Enhancer Elasticity Chest Hip Enhancement Skin Firming And Lifting Cream Busty Sexy Body Massage Care Creams",
).toLowerCase();
for (const forbidden of ["breast", "butt", "enhancer", "enhancement", "firming", "lifting", "busty", "sexy"]) {
  assert.ok(!polishedClaimText.includes(forbidden));
}
assert.ok(
  !removeHighRiskClaimLanguage("Herbal Hair Care Solution Anti-hair Loss And Strong")
    .toLowerCase()
    .includes("strong"),
);
assert.ok(
  !removeHighRiskClaimLanguage("Night Sleep Tightening Cream Flat Wrinkles")
    .toLowerCase()
    .includes("flat"),
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

const lighteningProduct: ProductSnapshot = {
  id: "gid://shopify/Product/lightening-review",
  title: "Skin Moisturizing Whitening Repair Cream",
  vendor: "MVQueen",
  productType: "Skincare",
  descriptionHtml: "<p>Body cream.</p><ul><li>Net weight: 100g</li></ul>",
  tags: [],
  variants: { nodes: [{ id: "gid://shopify/ProductVariant/lightening-review", price: "18.00" }] },
};
const lighteningClassification = classifyProduct(
  lighteningProduct.title,
  lighteningProduct.descriptionHtml ?? "",
  lighteningProduct.productType ?? "",
);
const lighteningContent = buildAutomatedProductContent(
  lighteningProduct,
  lighteningClassification,
  "MVQueen",
);
assert.ok(!JSON.stringify(lighteningContent).toLowerCase().includes("whitening"));
assert.ok(lighteningContent.title.toLowerCase().includes("moisturizing"));

const firmingProduct: ProductSnapshot = {
  id: "gid://shopify/Product/firming-review",
  title: "Turmeric Firming Care Face Cream",
  vendor: "MVQueen",
  productType: "Skincare",
  descriptionHtml: "<p>Face cream.</p><ul><li>Net weight: 50g</li></ul>",
  tags: [],
  variants: { nodes: [{ id: "gid://shopify/ProductVariant/firming-review", price: "18.00" }] },
};
const firmingClassification = classifyProduct(
  firmingProduct.title,
  firmingProduct.descriptionHtml ?? "",
  firmingProduct.productType ?? "",
);
const firmingContent = buildAutomatedProductContent(
  firmingProduct,
  firmingClassification,
  "MVQueen",
);
assert.ok(!JSON.stringify(firmingContent).toLowerCase().includes("firming"));
assert.ok(firmingContent.title.toLowerCase().includes("face cream"));

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

const defaultBrandClassification = classifyProduct(
  defaultBrandProduct.title,
  defaultBrandProduct.descriptionHtml ?? "",
  "",
);
const defaultBrandContent = buildAutomatedProductContent(
  defaultBrandProduct,
  defaultBrandClassification,
  "MVQueen",
);
assert.deepEqual(
  defaultBrandContent.highlights,
  [`Product type: ${defaultBrandClassification.productType}`],
);

const metadataHeavyProduct: ProductSnapshot = {
  ...defaultBrandProduct,
  id: "gid://shopify/Product/metadata-heavy",
  attributeMetafields: {
    nodes: [{
      key: "source_attributes",
      value: JSON.stringify({
        brand: "Generic",
        shelf_life: "3 years",
        key_words: "bright white",
        cosmetic_efficacy: "firming",
        material: "Glass",
        color: "Amber",
        net_content: "30ml",
      }),
    }],
  },
};
const metadataHeavyContent = buildAutomatedProductContent(
  metadataHeavyProduct,
  defaultBrandClassification,
  "MVQueen",
);
assert.ok(metadataHeavyContent.highlights.includes("Material: Glass"));
assert.ok(metadataHeavyContent.highlights.includes("Color: Amber"));
assert.ok(metadataHeavyContent.highlights.includes("Net content: 30ml"));
assert.ok(!metadataHeavyContent.highlights.some((value) => /brand|shelf life|key words|cosmetic efficacy/i.test(value)));

const grammarSamples = Array.from({ length: 80 }, (_, index) =>
  buildAutomatedProductContent(
    { ...defaultBrandProduct, id: `gid://shopify/Product/grammar-${index}` },
    defaultBrandClassification,
    "MVQueen",
  ).shortDescription,
);
assert.ok(grammarSamples.every((value) => !/\bA (?:elevated|elegant|understated|intentional|effortless)\b/.test(value)));

const pressOnProduct: ProductSnapshot = {
  id: "gid://shopify/Product/press-on-cleanup",
  title: "GGDDSHA New Shiny Crystal Long Press On Nails Withdiamonds Reusable PMA",
  vendor: "MVQueen",
  productType: "Press-On Nails",
  descriptionHtml: "<p>Reusable press-on nails.</p>",
  tags: [],
  variants: { nodes: [{ id: "gid://shopify/ProductVariant/press-on-cleanup", price: "12.00" }] },
};
const pressOnClass = classifyProduct(
  pressOnProduct.title,
  pressOnProduct.descriptionHtml ?? "",
  pressOnProduct.productType ?? "",
);
const pressOnContent = buildAutomatedProductContent(pressOnProduct, pressOnClass, "MVQueen");
assert.match(pressOnContent.title, /\bLong Crystal Press-On Nails\b/);
assert.ok(!/ggddsha|\bnew\b|\bpma\b|withdiamonds/i.test(pressOnContent.title));

const creamBrandProduct: ProductSnapshot = {
  id: "gid://shopify/Product/cream-brand-cleanup",
  title: "Meilin Ouliyuan Cream 40g",
  vendor: "MVQueen",
  productType: "Bath & Body",
  descriptionHtml: "<p>Body cream, 40g.</p>",
  tags: [],
  variants: { nodes: [{ id: "gid://shopify/ProductVariant/cream-brand-cleanup", price: "12.00" }] },
};
const creamBrandClass = classifyProduct(
  creamBrandProduct.title,
  creamBrandProduct.descriptionHtml ?? "",
  creamBrandProduct.productType ?? "",
);
const creamBrandContent = buildAutomatedProductContent(creamBrandProduct, creamBrandClass, "MVQueen");
assert.match(creamBrandContent.title, / Body Cream 40g$/);

assert.equal(
  classifyProduct("Baby Hair Gel Fluffy Fixed And Anti Manic", "", "").productType,
  "Hair Styling",
);
assert.equal(
  classifyProduct("Silky Hair Essential Oil", "", "").productType,
  "Hair Treatment",
);

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
assert.equal(necklaceCopy.title, "True North Zircon Star Pendant Necklace");
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
assert.match(extraLongNecklace.title, /\bNecklace\b/);
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
  const namingFile = join(vocabularyRoot, BRAND_VOCABULARY_SOURCES[4]);
  const namingPalette = JSON.parse(readFileSync(namingFile, "utf8"));
  namingPalette.profiles.mvqueen.evocative.general.push("Considered Hour");
  writeFileSync(namingFile, JSON.stringify(namingPalette));
  const revisedVocabulary = loadBrandVocabulary(vocabularyRoot);
  assert.notEqual(revisedVocabulary.version, BRAND_VOCABULARY.version);
  assert.ok(revisedVocabulary.profiles.mvqueen.adjectives.includes("considered"));
  const generated = Array.from({ length: 100 }, (_, index) => buildAutomatedProductContent({ ...supplierNecklace, id: "gid://shopify/Product/test-vocabulary-" + index }, necklaceClassification, "MVQueen", revisedVocabulary));
  assert.ok(generated.some((item) => item.shortDescription.toLowerCase().includes("considered")));
  assert.ok(generated.some((item) => item.title.includes("Considered Hour")));
  const forbiddenFile = join(vocabularyRoot, BRAND_VOCABULARY_SOURCES[2]);
  const forbiddenSource = readFileSync(forbiddenFile, "utf8");
  writeFileSync(forbiddenFile, forbiddenSource.replace("## Tier 2", "| Considered | Editorial review |\n\n## Tier 2"));
  const restrictedVocabulary = loadBrandVocabulary(vocabularyRoot);
  assert.ok(!restrictedVocabulary.profiles.mvqueen.adjectives.includes("considered"));
  assert.ok(!restrictedVocabulary.naming.mvqueen.evocative.general.includes("Considered Hour"));
  assert.notEqual(restrictedVocabulary.version, revisedVocabulary.version);
  rmSync(personaFile);
  assert.throws(() => loadBrandVocabulary(vocabularyRoot), /ENOENT/);
} finally {
  rmSync(vocabularyRoot, { recursive: true, force: true });
}

// Real October 5 imports: a clear tool noun must resolve the cosmetics overlap.
for (const [title, existingType] of [
  ["Student Dormitory Fill-light Desktop Vanity Mirror With Charging Function", "Needs Review"],
  ["Rose Loose Powder Makeup Brush Beauty Tool", "Needs Review"],
  ["Portable Foldable Led Makeup Mirror With Built-In Lights", "Makeup"],
  ["Foundation Brush", "Makeup"],
  ["Makeup Brushes", ""],
  ["Makeup Sponges", ""],
] as const) {
  const tool = classifyProduct(title, "", existingType);
  assert.equal(tool.productType, "Beauty Tool", title);
  assert.equal(tool.route, "beauty-tools", title);
  assert.equal(tool.confidence, "high", title);
  assert.equal(productTypeForWrite(existingType, tool), "Beauty Tool", title);
}
assert.equal(classifyProduct("Anti-Chapping Mirror-Like Hydrating Lip Serum", "", "Skincare").productType, "Skincare");
assert.equal(classifyProduct("Mirror Finish Ring", "", "Ring").productType, "Ring");
assert.equal(classifyProduct("Wood Paddle Hair Brush", "", "").productType, "Hair Tool");
assert.equal(classifyProduct("Liquid Foundation Makeup", "", "").productType, "Makeup");

const liveLipSerum: ProductSnapshot = {
  id: "gid://shopify/Product/9100794560710",
  title: "Anti-Chapping Mirror-Like Hydrating Lip Serum",
  productType: "Skincare",
  descriptionHtml: "<ul><li>Capacity: 7.5 ml</li><li>Color: Color01 / Color02 / Color03 / Color04 / Color05 / Color06</li></ul>",
};
const liveBatana: ProductSnapshot = {
  id: "gid://shopify/Product/9100793741510",
  title: "Batana Oil Hair Care Essential",
  productType: "Hair Treatment",
  descriptionHtml: "<ul><li>Net content: Batana essential oil 118ml, Batana essential oil 60ml</li></ul>",
};
for (const fixture of [liveLipSerum, liveBatana]) {
  const before = structuredClone(fixture);
  const route = classifyProduct(fixture.title, fixture.descriptionHtml ?? "", fixture.productType ?? "");
  const copy = buildAutomatedProductContent(fixture, route);
  assert.ok(copy.shortDescription.includes(copy.title));
  assert.ok(!/define this|built around|point of view|presentation|straightforward details/i.test(copy.shortDescription));
  assert.ok(copy.shortDescription.length <= 180);
  assert.ok(!copy.shortDescription.includes("…"));
  assert.deepEqual(fixture, before);
  const repeated = buildAutomatedProductContent({ ...fixture, title: copy.title, descriptionHtml: copy.descriptionHtml }, route);
  assert.equal(repeated.shortDescription, copy.shortDescription);
}
const lipSerumCopy = buildAutomatedProductContent(liveLipSerum, classifyProduct(liveLipSerum.title, "", "Skincare"));
assert.match(lipSerumCopy.shortDescription, /7\.5 ml/);
assert.ok(!/Color0[1-6]/.test(lipSerumCopy.shortDescription));
assert.ok(lipSerumCopy.descriptionHtml.includes("Color06"));
const batanaCopy = buildAutomatedProductContent(liveBatana, classifyProduct(liveBatana.title, "", "Hair Treatment"));
assert.match(batanaCopy.shortDescription, /118 ml and 60 ml/);
assert.ok(batanaCopy.descriptionHtml.includes("Batana essential oil 118ml, Batana essential oil 60ml"));
const unspecifiedCapacity = buildAutomatedProductContent({ ...liveLipSerum, descriptionHtml: "<ul><li>Capacity: 30</li></ul>" }, classifyProduct(liveLipSerum.title, "", "Skincare"));
assert.ok(!/30\s*(?:ml|g|oz)/i.test(unspecifiedCapacity.descriptionHtml));
const foldingMirrorCopy = buildAutomatedProductContent({
  id: "gid://shopify/Product/9100794429638",
  title: "Portable Foldable Led Makeup Mirror With Built-In Lights",
  productType: "Makeup",
  descriptionHtml: "<ul><li>Colors: White - 14.5 x 19.5 cm - Tricolor illumination; Black - 14.5 x 19.5 cm - Tricolor illumination; Pink - 14.5 x 19.5 cm - Tricolor illumination</li><li>Color: White / Black / Pink</li></ul>",
}, classifyProduct("Portable Foldable Led Makeup Mirror With Built-In Lights", "", "Makeup"));
assert.match(foldingMirrorCopy.shortDescription, /White, Black, and Pink/);
assert.ok(foldingMirrorCopy.title.includes("LED Makeup Mirror"));

const longBrushSource: ProductSnapshot = {
  id: "gid://shopify/Product/brand-title-long-brush",
  title: "Portable Travel Professional Cosmetic Makeup Brush Loose Powder Foundation Blush Eye Shadow Beauty Tool Makeup",
  productType: "Beauty Tool",
};
const brushRoute = classifyProduct(longBrushSource.title, "", "Beauty Tool");
const brandedBrush = buildAutomatedProductContent(longBrushSource, brushRoute);
assert.ok(brandedBrush.title.length <= 80);
assert.match(brandedBrush.title, /\bMakeup Brush\b/);
assert.equal(buildAutomatedProductContent({ ...longBrushSource, title: brandedBrush.title, descriptionHtml: brandedBrush.descriptionHtml }, brushRoute).title, brandedBrush.title);

const repeatedPrefix = buildAutomatedProductContent({ ...product, title: "Refined Polished " + content.title }, classification);
assert.equal(repeatedPrefix.title, content.title);

const fragranceSource: ProductSnapshot = { id: "gid://shopify/Product/9100065996998", title: "Osmanthus Peony Pomegranate Fragrance Crystal Diamond Series Perfume", productType: "Fragrance" };
const fragranceRoute = classifyProduct(fragranceSource.title, "", "Fragrance");
const fragranceCopy = buildAutomatedProductContent(fragranceSource, fragranceRoute, "Miss.Princess");
assert.equal(fragranceCopy.title, "Petal Dream Perfume");
assert.equal(buildAutomatedProductContent({ ...fragranceSource, title: fragranceCopy.title }, fragranceRoute, "Miss.Princess").title, fragranceCopy.title);

const supplierWordSource: ProductSnapshot = { id: "gid://shopify/Product/title-source-repair", title: "Vitamin C Serum Facial Amazon", productType: "Skincare" };
const supplierWordCopy = buildAutomatedProductContent(supplierWordSource, classifyProduct(supplierWordSource.title, "", "Skincare"));
assert.match(supplierWordCopy.title, /Vitamin C Facial Serum\b/);
assert.ok(!supplierWordCopy.title.includes("Amazon"));

const sprayBottleSource: ProductSnapshot = { id: "gid://shopify/Product/9100793938118", title: "High Pressure Spray Bottle Cleaning Silicone Brush Hollow Comb Hair Care Shampoo", productType: "Shampoo" };
const sprayBottleRoute = classifyProduct(sprayBottleSource.title, "", "Shampoo");
assert.equal(sprayBottleRoute.productType, "Hair Tool");
const sprayBottleCopy = buildAutomatedProductContent(sprayBottleSource, sprayBottleRoute);
assert.equal(sprayBottleCopy.title, "The Wash-Day Edit Spray Bottle, Silicone Brush & Hair Comb");
assert.equal(classifyProduct(sprayBottleCopy.title, "", "Shampoo").productType, "Hair Tool");
assert.equal(buildAutomatedProductContent({ ...sprayBottleSource, title: sprayBottleCopy.title }, sprayBottleRoute).title, sprayBottleCopy.title);
assert.equal(classifyProduct("Hair Care Spray", "", "Hair Treatment").productType, "Hair Treatment");

// Naming philosophy: different registers, distinct authored names, stable
// category/review decisions, and no ID-only override after a source change.
assert.equal(CURATED_PRODUCT_NAMES.length, 181);
assert.equal(new Set(CURATED_PRODUCT_NAMES.map((entry) => normalizeProductName(entry.title))).size, 181);
assert.equal(new Set(CURATED_PRODUCT_NAMES.map((entry) => entry.register)).size, 3);
assert.ok(CURATED_PRODUCT_NAMES.filter((entry) => /^The\s/.test(entry.title)).length < CURATED_PRODUCT_NAMES.length / 4);
for (const entry of CURATED_PRODUCT_NAMES) {
  assert.ok(entry.title.length <= 80);
  assert.ok(entry.opening.length < 90);
  const route = classifyProduct(entry.sourceTitle);
  assert.deepEqual(classifyProduct(entry.title), route, entry.title);
  const fixture = { id: entry.productId, title: entry.sourceTitle };
  const label = entry.brand === "mvqueen" ? "MVQueen" : "Miss.Princess";
  const named = buildAutomatedProductContent(fixture, route, label);
  assert.equal(named.title, entry.title);
  assert.equal(named.curatedName, true);
  assert.equal(buildAutomatedProductContent({ ...fixture, title: named.title, descriptionHtml: named.descriptionHtml }, route, label).title, named.title);
  assert.equal(matchingCuratedName(entry.productId, "A completely different source item"), undefined);
}
const futureCream: ProductSnapshot = { id: "gid://shopify/Product/new-curated-cream", title: "Moisturizing Face Cream", productType: "Skincare" };
const futureCreamRoute = classifyProduct(futureCream.title, "", "Skincare");
const futureNames = Array.from({ length: 90 }, (_, i) => buildAutomatedProductContent({ ...futureCream, id: futureCream.id + i }, futureCreamRoute));
assert.equal(new Set(futureNames.map((named) => named.namingRegister)).size, 3);
assert.ok(new Set(futureNames.map((named) => named.namingIdentity)).size > 20);
for (const named of futureNames) assert.ok(/Moisturizing Face Cream\b/.test(named.title));
const primaryFutureName = buildAutomatedProductContent(futureCream, futureCreamRoute);
const resolvedName = await resolveUniqueAutomatedProductContent(futureCream, futureCreamRoute, "MVQueen", async (identity) =>
  identity === primaryFutureName.namingIdentity ? [{ id: "gid://shopify/Product/another", title: identity + " Body Scrub" }] : [],
);
assert.notEqual(resolvedName.namingIdentity, primaryFutureName.namingIdentity);
assert.equal(stripNamingDecoration(resolvedName.title, BRAND_VOCABULARY), "Moisturizing Face Cream");
const resolvedRepeat = await resolveUniqueAutomatedProductContent({ ...futureCream, title: resolvedName.title }, futureCreamRoute, "MVQueen", async (identity) =>
  identity === primaryFutureName.namingIdentity ? [{ id: "gid://shopify/Product/another", title: identity + " Body Scrub" }]
    : [{ id: futureCream.id, title: resolvedName.title }],
);
assert.equal(resolvedRepeat.title, resolvedName.title);
assert.equal((await resolveUniqueAutomatedProductContent(futureCream, futureCreamRoute, "MVQueen", async () => [{ id: futureCream.id, title: primaryFutureName.title }])).title, primaryFutureName.title);
await assert.rejects(resolveUniqueAutomatedProductContent(futureCream, futureCreamRoute, "MVQueen", async (identity) => [{ id: "another", title: identity + " Face Cream" }]), /editorial review/);
await assert.rejects(resolveUniqueAutomatedProductContent(supplierNecklace, necklaceClassification, "MVQueen", async () => [{ id: "another", title: necklaceCopy.title }]), /editorial review/);
assert.notEqual(buildAutomatedProductContent({ ...supplierNecklace, title: "A completely different source item" }, necklaceClassification).title, necklaceCopy.title);

console.log("product content automation tests passed");

