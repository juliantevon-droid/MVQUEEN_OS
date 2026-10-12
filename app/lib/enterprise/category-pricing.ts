/**
 * MVQUEEN category-specific retail guardrails.
 *
 * These are merchandising targets, NOT proof of market value or permission to
 * disregard the financial floor. Unknown, multipack and specialty variants
 * require separate review. Organic/add-on suggestions are advisory only.
 */
export type CategoryPriceBand = {
  key: string;
  label: string;
  min: number;
  max: number;
  preferred: number;
};

export type CategoryPriceAssessment = {
  state: "unclassified" | "multipack_review" | "within_band" | "above_band" |
    "below_band" | "paid_cost_conflict" | "organic_cost_conflict";
  band: CategoryPriceBand | null;
  suggestedOrganicPrice: number | null;
  paidFloor: number | null;
  organicFloor: number | null;
  rationale: string;
};

const bands: Record<string, CategoryPriceBand> = {
  scalp_brush: { key: "scalp_brush", label: "Single silicone scalp/shampoo brush", min: 12.99, max: 17.99, preferred: 16.99 },
  small_beauty_tool: { key: "small_beauty_tool", label: "Simple beauty accessories", min: 7.99, max: 17.99, preferred: 14.99 },
  eyeliner: { key: "eyeliner", label: "Everyday eyeliner", min: 6.99, max: 19.99, preferred: 14.99 },
  brow_makeup: { key: "brow_makeup", label: "Basic brow makeup", min: 8.99, max: 19.99, preferred: 15.99 },
  lip_makeup: { key: "lip_makeup", label: "Everyday lip makeup", min: 6.99, max: 19.99, preferred: 13.99 },
  single_soap: { key: "single_soap", label: "Single soap bar", min: 6.99, max: 17.99, preferred: 12.99 },
  basic_jewelry: { key: "basic_jewelry", label: "Everyday jewelry", min: 9.99, max: 39.99, preferred: 24.99 },
  basic_top: { key: "basic_top", label: "Tops and everyday basics", min: 14.99, max: 29.99, preferred: 24.99 },
  dress: { key: "dress", label: "Everyday dress", min: 24.99, max: 49.99, preferred: 39.99 },
  skirt: { key: "skirt", label: "Skirts and bodysuits", min: 19.99, max: 39.99, preferred: 29.99 },
  pants: { key: "pants", label: "Jeans and everyday pants", min: 29.99, max: 59.99, preferred: 44.99 },
  skincare: { key: "skincare", label: "Basic skincare", min: 12.99, max: 29.99, preferred: 22.99 },
};

function multipack(text: string): boolean {
  // 1PCS is an ordinary single item. 2PCS, 25pcs and kits deserve their
  // own pricing logic; never force them into a single-item ceiling.
  return /\b(?:[2-9]|[1-9]\d+)\s*(?:pcs?|pieces?|pairs?|packs?|sets?)\b/i.test(text) ||
    /\b(?:bundle|kit|multi-?pack|gift set|matching set)\b/i.test(text);
}

export function getCategoryPriceBand(args: {
  title: string;
  productType?: string | null;
  variantTitle?: string | null;
}): { band: CategoryPriceBand | null; multipackReview: boolean } {
  const title = args.title.toLowerCase();
  const type = (args.productType ?? "").toLowerCase();
  const variant = args.variantTitle ?? "";
  if (multipack(title + " " + variant) ||
      /\b(?:spray bottle.*comb|brush.*comb|microcurrent|electric|rechargeable|heated|premium|luxury|professional)\b/i.test(title)) {
    return { band: null, multipackReview: true };
  }
  let band: CategoryPriceBand | null = null;
  if (/\b(shampoo|scalp)(?:\s+massage)?\s+brush\b|\bscalp\s+massager\b/.test(title)) band = bands.scalp_brush;
  else if (/\b(eyeliner|eye liner)\b/.test(title)) band = bands.eyeliner;
  else if (/\b(eyebrow|brow)\b/.test(title) && /\b(cream|gel|pencil|pomade|powder|makeup)\b/.test(title)) band = bands.brow_makeup;
  else if (/\b(lip gloss|lipstick|lip tint|lip liner)\b/.test(title)) band = bands.lip_makeup;
  else if (/\b(soap|soap bar)\b/.test(title) && !/\bset\b/.test(title)) band = bands.single_soap;
  else if (/\b(tweezers?|lash comb|beauty sponge|makeup sponge|eyebrow knife)\b/.test(title)) band = bands.small_beauty_tool;
  else if (/\b(earrings?|necklace|bracelet|rings?)\b/.test(title) || /\b(jewelry|jewellery)\b/.test(type)) band = bands.basic_jewelry;
  else if (/\b(dress)\b/.test(type) || /\bcasual dress\b/.test(title)) band = bands.dress;
  else if (/\b(t-?shirt|tank top|basic top|crop top)\b/.test(title) || /\b(tops?)\b/.test(type)) band = bands.basic_top;
  else if (/\b(skirt|bodysuit)\b/.test(type + " " + title)) band = bands.skirt;
  else if (/\b(jeans|pants|trousers)\b/.test(type + " " + title)) band = bands.pants;
  else if (/\b(cleanser|toner|moisturizer|serum|face cream)\b/.test(title) && !/\bset\b/.test(title)) band = bands.skincare;
  return { band, multipackReview: false };
}

function atOrAbove99(value: number): number {
  // A .99 recommendation may never round down through the cost floor.
  return Math.round((Math.ceil(value + 0.01 - Number.EPSILON) - 0.01) * 100) / 100;
}

export function assessCategoryPrice(args: {
  title: string;
  productType?: string | null;
  variantTitle?: string | null;
  currentPrice: number | null;
  paidFloor: number | null;
  organicFloor: number | null;
}): CategoryPriceAssessment {
  const { band, multipackReview } = getCategoryPriceBand(args);
  const base = { band, suggestedOrganicPrice: null, paidFloor: args.paidFloor, organicFloor: args.organicFloor };
  if (multipackReview) return { ...base, state: "multipack_review", rationale: "Bundle, multi-unit or specialized item needs an item-specific pricing review." };
  if (!band) return { ...base, state: "unclassified", rationale: "No evidence-based simple-item price band is assigned." };
  const proposed = args.organicFloor === null ? null : atOrAbove99(Math.max(band.preferred, args.organicFloor, band.min));
  const suggestedOrganicPrice = proposed !== null && proposed <= band.max ? proposed : null;
  const withSuggestion = { ...base, suggestedOrganicPrice };
  if (args.organicFloor !== null && args.organicFloor > band.max)
    return { ...withSuggestion, state: "organic_cost_conflict", rationale: "Even the organic/add-on contribution floor exceeds the category ceiling; review sourcing and costs." };
  if (args.paidFloor !== null && args.paidFloor > band.max)
    return { ...withSuggestion, state: "paid_cost_conflict", rationale: "Paid-acquisition economics exceed the category ceiling; avoid inflating this item to recover ad spend." };
  if (args.currentPrice !== null && args.currentPrice > band.max)
    return { ...withSuggestion, state: "above_band", rationale: "Current price exceeds the usual simple-item merchandising range." };
  if (args.currentPrice !== null && args.currentPrice < band.min)
    return { ...withSuggestion, state: "below_band", rationale: "Current price is below the merchandising range; verify costs and item details." };
  return { ...withSuggestion, state: "within_band", rationale: "The item falls within its approximate category merchandising range." };
}
