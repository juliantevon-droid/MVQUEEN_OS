import assert from "node:assert/strict";
import { BRAND_VOCABULARY, assertProductBrandStyle } from "./brand-vocabulary.server";
import { CURATED_PRODUCT_NAMES, matchingCuratedName } from "./curated-product-names";
import { brandedSeoTitle, buildAutomatedProductContent, productClaimReviewReasons } from "./product-content-automation";
import { classifyProduct, type ProductSnapshot } from "./mvqueen-intelligence";
import { buildAutomatedProductFaq } from "./automated-content-surfaces";

for (const entry of CURATED_PRODUCT_NAMES) {
  assert.ok(!/^(?:The|A|An)\s|\s—\s(?:The|A|An)\s/.test(entry.title), entry.title);
  assert.equal(matchingCuratedName(entry.productId, entry.title)?.title, entry.title);
  for (const alias of entry.sourceAliases) assert.equal(matchingCuratedName(entry.productId, alias)?.title, entry.title);
}
for (const [title, noun] of [
  ["Five-Step Play Electric Facial Cleansing Tool", "Facial Cleansing Tool"],
  ["Mirror Moment Ultrasonic Facial Cleansing Tool", "Facial Cleansing Tool"],
  ["Happy Little Break Heated Foot Massage Machine", "Foot Massage Machine"],
]) {
  const seo = brandedSeoTitle(title, "Miss.Princess", 60);
  assert.ok(seo.includes(noun), seo);
  assert.ok(seo.includes(title.split(" ")[0]), seo);
  assert.ok(seo.length <= 60);
}
assert.throws(() => assertProductBrandStyle("Face Cream", "Your own moment.", "<p>Refined polished elevated elegant.</p>"), /adjective limit/);
assert.throws(() => assertProductBrandStyle("Face Cream", "Your own moment.", "<p>micro-glows and feather-glows.</p>"), /sensory verb limit/);
assert.throws(() => assertProductBrandStyle("Face Cream", "Your own moment.", "<p>Intentional intentional intentional.</p>"), /repeats/);
assert.doesNotThrow(() => assertProductBrandStyle("Wood Paddle Hair Brush — In Good Order", "Your own moment.", "<p>Your own moment.</p>"));
assert.throws(() => assertProductBrandStyle("Face Cream", "Perfect products for you.", "<p>Perfect products for you.</p>"), /headline/);
assert.throws(() => assertProductBrandStyle("Face Cream", "Your own moment.", "<p>Your own moment.</p><p>Own your glow.</p>"), /Confidence phrases/);

const source: ProductSnapshot = { id: "new-anklet-review", title: "Crystal Heart Anklet", descriptionHtml: '<ul><li>Material: Crystal</li><li>Length: 22.2cm+9.1cm (12.3in)</li><li>Great Gift For: Your family will be proud of you.</li><li>Your item Ships Same Day to 1 Business Day from our California Location.</li></ul><table><tr><td><img src="https://supplier.invalid/photo.jpg"><p>Guaranteed results. Buy now.</p></td></tr></table>' };
const classification = classifyProduct(source.title, source.descriptionHtml ?? undefined);
const copy = buildAutomatedProductContent(source, classification);
assert.ok(copy.descriptionHtml.includes("22.2cm+9.1cm (12.3in)"));
assert.ok(!/family will|ships same|California|supplier.invalid|Guaranteed|<table>/i.test(copy.descriptionHtml));
const faq = buildAutomatedProductFaq(source, classification, copy);
assert.ok(faq.some(item => /materials or ingredients/.test(item.question) && item.answer.includes("Crystal")));
assert.ok(!/family will|ships same|California|Guaranteed/i.test(JSON.stringify(faq)));

const reviewed = Object.entries(BRAND_VOCABULARY.contentPolicy.claimReviews ?? {}).filter(([, review]) => review.disposition === "false_positive_corrected");
assert.equal(reviewed.length, 3);
for (const [id, review] of reviewed) {
  const product: ProductSnapshot = { id, title: review.allowedTitles[0], claimReviewReasons: {value:JSON.stringify(review.reviewedReasons)}, attributeMetafields:{nodes:[{key:"source_attributes",value:JSON.stringify(review.sourceAttributes)}]} };
  assert.deepEqual(productClaimReviewReasons(product), [], id);
  assert.ok(productClaimReviewReasons({...product,descriptionHtml:"Clinically proven to cure eczema."}).includes("medical_or_guaranteed"));
  assert.ok(productClaimReviewReasons({...product,attributeMetafields:{nodes:[{key:"source_attributes",value:JSON.stringify({...review.sourceAttributes,color:"changed source"})}]}}).length > 0);
  assert.ok(productClaimReviewReasons({...product,title:"A different product identity"}).length > 0);
}
console.log("canonical product language tests passed: article removal, SEO nouns, style budgets, supplier cleanup and evidence-bound claim review");
