import assert from "node:assert/strict";
import { copyFileSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { BRAND_VOCABULARY, BRAND_VOCABULARY_SOURCES, canonicalBrandLabel, loadBrandVocabulary, PRODUCT_EDITORIAL_CATEGORIES } from "./brand-vocabulary.server";
import { buildAutomatedProductContent, productEditorialCategory } from "./product-content-automation";
import type { Classification, ProductSnapshot } from "./mvqueen-intelligence";

assert.equal(canonicalBrandLabel("MvQueen"), "MVQUEEN");
assert.equal(canonicalBrandLabel("MV QUEEN"), "MVQUEEN");
const historicalSisterBrand = ["MISS", "QUEEN"].join(".");
assert.equal(canonicalBrandLabel(historicalSisterBrand), "Miss.Princess");
assert.equal(canonicalBrandLabel("Miss Princess"), "Miss.Princess");

const cases = [
  ["fashion", "Fashion", "Dress"], ["jewelry", "Jewelry", "Necklace"],
  ["skincare", "Beauty", "Face Cream"], ["beauty", "Beauty", "Lipstick"],
  ["fragrance", "Beauty", "Fragrance"], ["haircare", "Hair", "Shampoo"],
  ["home", "Home", "Candle"], ["tools", "Beauty", "Makeup Brush"],
  ["general", "Lifestyle Accessories", "Pouch"],
] as const;
for (const [category, department, productType] of cases) {
  const classification: Classification = { department, productType, family: productType, route: productType.toLowerCase().replace(/ /g, "-"), subcollection: productType, confidence: "high" };
  assert.equal(productEditorialCategory(classification), category);
  for (const label of ["MVQueen", historicalSisterBrand]) {
    const brand = label === "MVQueen" ? "mvqueen" : "miss-princess";
    const openings = new Set<string>();
    for (let index = 0; index < 80; index++) {
      const product: ProductSnapshot = { id: `brand-policy-${brand}-${category}-${index}`, title: productType, handle: "unchanged-handle", variants: { nodes: [{ id: "unchanged-variant", sku: "KEEP-SKU", price: "29.00" }] } };
      const before = structuredClone(product);
      const content = buildAutomatedProductContent(product, classification, label);
      assert.deepEqual(product, before);
      assert.ok(content.shortDescription.includes(canonicalBrandLabel(label)));
      assert.ok(content.shortDescription.includes(content.title));
      assert.ok(content.shortDescription.length <= 180);
      assert.ok(!/\b(?:silk|cotton|stainless|vegan|cruelty|clinical|heals|longevity|sephora|victoria|opulent)\b/i.test(content.descriptionHtml));
      assert.ok(!/\b[Aa] (?:elegant|elevated|intentional|understated|effortless)\b/.test(content.shortDescription));
      assert.ok(!/[{}]/.test(content.shortDescription));
      assert.equal(buildAutomatedProductContent({ ...product, title: content.title, descriptionHtml: content.descriptionHtml }, classification, label).descriptionHtml, content.descriptionHtml);
      openings.add(content.shortDescription.split(". ")[0]);
    }
    assert.ok(openings.size >= 12, `${brand}/${category} needs varied openings`);
  }
}

const root = mkdtempSync(join(tmpdir(), "mvqueen-brand-policy-"));
try {
  for (const source of BRAND_VOCABULARY_SOURCES) {
    const destination = join(root, source);
    mkdirSync(dirname(destination), { recursive: true });
    copyFileSync(source, destination);
  }
  const file = join(root, "06_Tone_And_Voice/Brand_Content_Policy.json");
  const original = JSON.parse(readFileSync(file, "utf8"));
  original.profiles.mvqueen.hooks.jewelry = ["Your {brand} jewelry edit begins with {article} {adjective} choice."];
  writeFileSync(file, JSON.stringify(original));
  const updated = loadBrandVocabulary(root);
  assert.notEqual(updated.version, BRAND_VOCABULARY.version);
  const c: Classification = { department: "Jewelry", family: "Necklaces", subcollection: "Necklaces", route: "necklaces", productType: "Necklace", confidence: "high" };
  assert.ok(buildAutomatedProductContent({ id: "policy-edited-future", title: "Necklace" }, c, "MVQUEEN", updated).shortDescription.includes("begins with"));
  for (const category of PRODUCT_EDITORIAL_CATEGORIES) assert.ok(updated.contentPolicy.profiles["miss-princess"].hooks[category].length);
  original.profiles.mvqueen.hooks.jewelry = ["Your {brand} clinically proven {adjective} silk choice."];
  writeFileSync(file, JSON.stringify(original));
  assert.throws(() => loadBrandVocabulary(root), /Invalid editorial hook/);
  original.profiles.mvqueen.hooks.jewelry = ["Your {brand} {adjective} {ingredient} choice."];
  writeFileSync(file, JSON.stringify(original));
  assert.throws(() => loadBrandVocabulary(root), /Invalid editorial hook/);
  rmSync(file);
  assert.throws(() => loadBrandVocabulary(root), /ENOENT/);
} finally { rmSync(root, { recursive: true, force: true }); }

console.log("brand content policy tests passed: both brands, nine categories, source edits and claim rejection");
