import assert from "node:assert/strict";
import { editorialSourceFingerprint, reviewedEditorialState } from "./reviewed-product-content";
import type { ProductSnapshot } from "./mvqueen-intelligence";

const product: ProductSnapshot = {
  id: "gid://shopify/Product/1", title: "Reviewed necklace", productType: "Necklaces",
  attributeMetafields: { nodes: [{ key: "material", value: "Steel" }, { key: "shape", value: "Star" }] },
  variants: { nodes: [{ id: "v1", sku: "A", price: "29.00" }, { id: "v2", sku: "B" }] },
};
const marker = { version: 1, owner: "mvqueen-content", productId: product.id,
  sourceFingerprint: editorialSourceFingerprint(product), reviewedAt: "2026-10-11T00:00:00Z" };
const reviewed = { ...product, editorialApproval: { value: JSON.stringify(marker) } };
assert.deepEqual(reviewedEditorialState(product), { preserve: false, status: null });
assert.deepEqual(reviewedEditorialState(reviewed), { preserve: true, status: "reviewed" });
for (const value of ["{", "null", JSON.stringify({ ...marker, version: 2 }),
  JSON.stringify({ ...marker, owner: "foreign" }), JSON.stringify({ ...marker, productId: "other" }),
  JSON.stringify({ ...marker, sourceFingerprint: "invalid" }), JSON.stringify({ ...marker, reviewedAt: "invalid" })]) {
  assert.equal(reviewedEditorialState({ ...product, editorialApproval: { value } }).preserve, false);
}
const commerceChange = { ...reviewed, title: "Merchant revised title", descriptionHtml: "New copy",
  variants: { nodes: [...reviewed.variants!.nodes!].reverse().map(v => ({ ...v, price: "99.00" })) },
  attributeMetafields: { nodes: [...reviewed.attributeMetafields!.nodes!].reverse() } };
assert.equal(reviewedEditorialState(commerceChange).status, "reviewed");
for (const changed of [
  { ...reviewed, productType: "Bracelets" },
  { ...reviewed, attributeMetafields: { nodes: [{ key: "material", value: "Copper" }] } },
  { ...reviewed, variants: { nodes: [{ id: "v3", sku: "A" }] } },
]) assert.deepEqual(reviewedEditorialState(changed), { preserve: true, status: "source_changed" });
// Claim flags are independent of editorial ownership and remain on the source object.
const held = { ...reviewed, claimReviewReasons: { value: '["scar_claim"]' } };
assert.equal(reviewedEditorialState(held).preserve, true);
assert.equal(held.claimReviewReasons.value, '["scar_claim"]');
console.log("Reviewed editorial ownership checks passed");
