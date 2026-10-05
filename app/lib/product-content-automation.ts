import type { Classification, ProductSnapshot } from "./mvqueen-intelligence";
import { BRAND_VOCABULARY, removeForbiddenLanguage, type BrandVocabulary } from "./brand-vocabulary.server";

export type AutomatedProductContent = {
  title: string;
  shortDescription: string;
  descriptionHtml: string;
  highlights: string[];
  focusKeyword: string;
  secondaryKeywords: string[];
  longTailKeywords: string[];
  seoTitle: string;
  metaDescription: string;
  seoKeywords: string[];
};

const SPACE_RE = /\s+/g;
const HTML_RE = /<[^>]+>/g;
const TRAILING_CODE_RE = /\s*\(([A-Z0-9_-]{2,24})\)\s*$/i;

const CUSTOMER_FACING_BRAND_DENYLIST = [
  "OUHOE", "HOEGOA", "FANZHEN", "EELHOPE", "COLOR FIT", "WEST & MONTH",
  "EPROLO", "DROPSURE", "JAYSUING", "ROXELIS", "DESIRE GEM", "MIA JEWELRY",
  "SEPHORA", "VICTORIA'S SECRET", "VICTORIAS SECRET", "FENTY BEAUTY", "DIOR",
  "QIBEST", "QIBEST2", "HANDAIYAN", "O.TWO.O", "PUDAIER", "IMAGIC", "HOYGI",
  "ZEPHOCO", "NICEFACE", "OCEAURA", "CMAADU", "MENOW", "UCANBE", "CAKAILA",
  "FOCALLURE", "FOCALLUREL", "MISSROSE", "MISS ROSE", "ZEESEA", "BREYLEE",
  "KOEC", "BEAUTY GLAZED", "POPFEEL", "LANBENA", "DEROL", "HENGFEI", "LULAA",
  "MABREM", "WUWUVISTA", "COFULTIC", "GGDDSHA", "MEILIN OULIYUAN",
];

const CLAIM_REVIEW_RULES: Array<[string, RegExp]> = [
  ["medical_or_guaranteed", /\b(?:cures?|treats?|prevents?|clinically\s+proven|medical[- ]grade|guaranteed?|permanent)\b/i],
  ["hair_loss_or_regrowth", /\b(?:anti[- ]?hair\s+loss|hair\s+loss|hair\s+regrowth|regrowth)\b/i],
  ["scar_claim", /\bscar\b[\s\S]{0,30}\b(?:remov|repair|treat|cream|gel|desalination|fade)/i],
  ["body_enhancement", /\b(?:(?:breast|bust|butt|hip)\b[\s\S]{0,35}\b(?:enhanc(?:e|er|ement|ing)?|enlarg(?:e|ement|ing)?|lift(?:ing)?|growth|firm(?:ing|ness)?)|breast\s+(?:beauty|care)|bust\s+care)\b/i],
  ["fat_or_cellulite_claim", /\b(?:fat\s+burning|weight\s+loss|anti[- ]?cellulite|cellulite\s+(?:reduction|removal)|slimming(?:\s+(?:cream|oil|gel|massager|device))?|body\s+shaping)\b/i],
  ["wrinkle_treatment_claim", /\b(?:wrinkles?\b[\s\S]{0,25}\b(?:remove|flat|reduce|tighten)|tightening\s+cream[\s\S]{0,25}\bwrinkles?)\b/i],
  ["skin_lightening_claim", /\b(?:whiten(?:ing|s|ed)?|skin\s+lighten(?:ing|er)?|bleach(?:ing|es|ed)?|bright\s+white)\b/i],
  ["firming_tightening_claim", /(?:\b(?:skin|face|facial|body|cream|serum|lotion|roller|oil)\b[\s\S]{0,35}\b(?:firming|tightening|lifting)\b|\b(?:firming|tightening|lifting)\b[\s\S]{0,35}\b(?:skin|face|facial|body|cream|serum|lotion|roller|oil)\b)/i],
  ["wellness_health_claim", /\b(?:improv(?:e|ing)\s+insomnia|help\s+sleep|promot(?:e|es|ing)\s+blood\s+circulation|reliev(?:e|es|ing)\s+anxiety)\b/i],
  ["acne_treatment_claim", /\b(?:anti[- ]?acne|acne\s+(?:treatment|cure|remedy))\b/i],
];

const HIGH_RISK_CLAIM_SANITIZERS: RegExp[] = [
  /\b(?:cures?|treats?|prevents?|clinically\s+proven|medical[- ]grade|guaranteed?|permanent)\b/gi,
  /\b(?:anti[- ]?hair\s+loss|hair\s+loss|hair\s+regrowth|regrowth)\b/gi,
  /\b(?:scar(?:s)?(?:\s+(?:removal|repair|treatment|fade|cream|gel))?|desalination)\b/gi,
  /\b(?:anti[- ]?cellulite|cellulite(?:\s+(?:reduction|removal))?|fat\s+burning|weight\s+loss|slimming|body\s+shaping)\b/gi,
  /\b(?:breast|bust|butt|hip)\s+(?:enhanc(?:e|er|ement|ing)?|enlarg(?:e|ement|ing)?|lift(?:ing)?|growth|firm(?:ing|ness)?)\b/gi,
  /\b(?:breast|bust)\s+(?:beauty|care)\b/gi,
  /\b(?:breast|bust|busty|butt|chest)\b/gi,
  /\b(?:wrinkles?|tightening|firming|lifting)\b/gi,
  /\b(?:whiten(?:ing|s|ed)?|skin\s+lighten(?:ing|er)?|bleach(?:ing|es|ed)?|bright\s+white)\b/gi,
  /\b(?:improv(?:e|ing)\s+insomnia|help\s+sleep|promot(?:e|es|ing)\s+blood\s+circulation|reliev(?:e|es|ing)\s+anxiety)\b/gi,
  /\b(?:anti[- ]?acne|acne\s+(?:treatment|cure|remedy))\b/gi,
  /\belasticity\b/gi,
  /\b(?:sexy|flat|strong)\b/gi,
];

export function removeHighRiskClaimLanguage(value: string): string {
  let output = String(value ?? "");
  for (const pattern of HIGH_RISK_CLAIM_SANITIZERS) {
    output = output.replace(pattern, " ");
  }
  return output
    .replace(/\b(?:and|or|with|for)\s+(?=(?:and|or|with|for)\b)/gi, " ")
    .replace(/\b(?:and|or|with|for)\s+(?=[,.;:!?])/gi, " ")
    .replace(/\s+([,.;:!?])/g, "$1")
    .replace(/([,.;:!?]){2,}/g, "$1")
    .replace(SPACE_RE, " ")
    .trim()
    .replace(/^(?:and|or|with|for)\s+/i, "")
    .replace(/\s+(?:and|or|with|for)$/i, "")
    .replace(/\b(?:and|or|with|for)\s+(?:and|or|with|for)\b/gi, " ")
    .replace(SPACE_RE, " ")
    .trim();
}

export function productClaimReviewReasons(
  product: {
    title?: string | null;
    descriptionHtml?: string | null;
    handle?: string | null;
    attributeMetafields?: ProductSnapshot["attributeMetafields"];
  },
): string[] {
  const sourceAttributes = product.attributeMetafields?.nodes?.find(
    (item) => item.key === "source_attributes",
  )?.value ?? "";
  const text = [
    String(product.title ?? ""),
    String(product.descriptionHtml ?? "").replace(HTML_RE, " "),
    String(product.handle ?? "").replace(/[-_]+/g, " "),
    String(sourceAttributes),
  ]
    .join(" ")
    .replace(SPACE_RE, " ")
    .trim();

  return CLAIM_REVIEW_RULES
    .filter(([, pattern]) => pattern.test(text))
    .map(([reason]) => reason);
}

export function shouldPublishAutomatedDescription(args: {
  topic?: string | null;
  currentDescriptionHtml?: string | null;
  allowExistingRewrite?: boolean;
}): boolean {
  const topic = String(args.topic ?? "").trim().toLowerCase().replace(/_/g, "/");
  const current = String(args.currentDescriptionHtml ?? "")
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ")
    .trim();

  // New Shopify products/imports may receive the governed MVQueen description.
  // Later update webhooks stay protected unless a separate, explicit
  // existing-description rewrite gate is enabled. Blank descriptions remain
  // repairable if a create webhook was missed.
  return (
    topic === "products/create" ||
    current.length === 0 ||
    args.allowExistingRewrite === true
  );
}

export function needsMediaAltRepair(value?: string | null): boolean {
  const alt = String(value ?? "").trim();
  if (!alt) return true;

  const lower = alt.toLowerCase();
  if (
    lower.includes("max-origin") ||
    /\.(?:jpe?g|png|webp|gif|avif)(?:\?|$)/i.test(alt) ||
    /^(?:img|image|photo|pic)[-_ ]?\d+\b/i.test(alt)
  ) {
    return true;
  }

  const compact = alt.replace(/[^a-z0-9]/gi, "");
  if (compact.length >= 20 && /^[a-f0-9]+$/i.test(compact)) return true;

  return false;
}

function cleanText(value?: string | null): string {
  return String(value ?? "")
    .replace(/&nbsp;/gi, " ")
    .replace(/&amp;/gi, "&")
    .replace(/&quot;/gi, '"')
    .replace(/&#39;|&apos;/gi, "'")
    .replace(/&times;/gi, "×")
    .replace(HTML_RE, " ")
    .replace(SPACE_RE, " ")
    .trim();
}

function stripVendor(value: string, vendor?: string | null): string {
  const rawVendor = String(vendor ?? "").trim();
  if (!rawVendor || /^mvqueen$/i.test(rawVendor)) return value.trim();
  const escaped = rawVendor.replace(/[.*+?^$(){}|[\]\\]/g, "\\$&");
  return value
    .replace(new RegExp("\\b" + escaped + "\\b", "gi"), " ")
    .replace(SPACE_RE, " ")
    .trim();
}

function stripKnownCustomerBrands(value: string): string {
  let output = value;
  for (const brand of CUSTOMER_FACING_BRAND_DENYLIST) {
    const escaped = brand.replace(/[.*+?^$(){}|[\]\\]/g, "\\$&");
    output = output.replace(new RegExp("\\b" + escaped + "\\b", "gi"), " ");
  }
  return output.replace(SPACE_RE, " ").trim();
}

function cleanCustomerText(
  value: string,
  vendor?: string | null,
  vocabulary = BRAND_VOCABULARY,
  sanitizeClaims = false,
): string {
  const cleaned = removeForbiddenLanguage(
    stripKnownCustomerBrands(stripVendor(value, vendor)),
    vocabulary,
  );
  return (sanitizeClaims ? removeHighRiskClaimLanguage(cleaned) : cleaned)
    .replace(SPACE_RE, " ")
    .trim();
}

function unique(values: string[]): string[] {
  const seen = new Set<string>();
  const out: string[] = [];
  for (const raw of values) {
    const value = cleanText(raw).replace(/^[-–—|,:;]+|[-–—|,:;]+$/g, "").trim();
    const key = value.toLowerCase();
    if (!value || seen.has(key)) continue;
    seen.add(key);
    out.push(value);
  }
  return out;
}

function clip(value: string, max: number): string {
  const text = cleanText(value);
  if (text.length <= max) return text;
  const cut = text.slice(0, Math.max(1, max - 1)).replace(/\s+\S*$/, "").trim();
  return (cut || text.slice(0, max - 1).trim()) + "…";
}

function clipTitle(value: string, max = 80): string {
  const text = cleanText(value);
  if (text.length <= max) return text;
  return (
    text.slice(0, max + 1).replace(/\s+\S*$/, "").trim() ||
    text.slice(0, max).trim()
  );
}

function extractHighlights(html?: string | null): string[] {
  const source = String(html ?? "");
  const labeledLines = source
    .replace(/<table\b[^>]*>[\s\S]*?<\/table>/gi, "")
    .replace(/<(?:br\s*\/?|\/p|\/li)>/gi, "\n")
    .split(/\n+/)
    .map(cleanText)
    .filter((line) => /^[A-Za-z][A-Za-z0-9 &/'()\-]{1,48}\s*:\s*\S/.test(line));
  return unique(
    [
      ...[...source.matchAll(/<li\b[^>]*>([\s\S]*?)<\/li>/gi)].map((match) => match[1]),
      ...labeledLines,
    ].map((line) =>
        cleanText(line)
          .replace(/^[-•]\s*/, "")
          .replace(/\s*:\s*/g, ": "),
      )
      .filter(Boolean),
  );
}

function humanizeAttributeKey(value: string): string {
  return value
    .replace(/[_-]+/g, " ")
    .replace(/\s+/g, " ")
    .trim()
    .replace(/^./, (char) => char.toUpperCase());
}

const CUSTOMER_HIGHLIGHT_SKIP_KEYS = new Set([
  "brand",
  "key_words",
  "keywords",
  "product_name",
  "slogan",
  "shelf_life",
  "purpose",
  "applicable_people",
  "applicable_object",
  "special_purpose_cosmetics",
  "cosmetic_efficacy",
  "skin_effect_of_essential_oil",
  "psychological_effect_of_essential_oil",
  "effect",
  "function",
  "product_features",
  "how_to_use",
  "category",
]);

function usefulSourceHighlight(key: string, value: string): boolean {
  const normalizedKey = key.toLowerCase().trim().replace(/[\s-]+/g, "_");
  const normalizedValue = cleanText(value).toLowerCase();
  if (CUSTOMER_HIGHLIGHT_SKIP_KEYS.has(normalizedKey)) return false;
  if (!normalizedValue) return false;
  if (/^(?:other|other effects?|general|standard|default|no|yes|n\/a|none|ordinary)$/i.test(normalizedValue)) {
    return false;
  }
  if (normalizedValue.length > 180) return false;
  return true;
}

function structuredSourceHighlights(product: ProductSnapshot): string[] {
  const highlights: string[] = [];
  const sourceRaw = product.attributeMetafields?.nodes?.find(
    (item) => item.key === "source_attributes",
  )?.value;

  if (sourceRaw) {
    try {
      const parsed = JSON.parse(sourceRaw) as Record<string, unknown>;
      for (const [key, rawValue] of Object.entries(parsed)) {
        if (rawValue === null || rawValue === undefined) continue;
        const value = cleanText(String(rawValue));
        if (!usefulSourceHighlight(key, value)) continue;
        highlights.push(`${humanizeAttributeKey(key)}: ${value}`);
      }
    } catch {
      // Preserve the product job if a legacy source_attributes value is invalid.
    }
  }

  const variantValues = (key: string) =>
    unique(
      (product.variants?.nodes ?? [])
        .map((variant) =>
          variant.googleMetafields?.nodes?.find((item) => item.key === key)?.value ?? "",
        )
        .filter(Boolean),
    );

  const materials = variantValues("material");
  const colors = variantValues("color");
  if (materials.length) highlights.unshift(`Material: ${materials.join(" / ")}`);
  if (colors.length) highlights.unshift(`Color: ${colors.join(" / ")}`);

  return unique(highlights);
}

function valueAfterLabel(value: string): string {
  const cleaned = cleanText(value);
  const colon = cleaned.indexOf(":");
  return colon > 0 ? cleaned.slice(colon + 1).trim() : cleaned;
}

function uniqueHighlights(values: string[], productType: string): string[] {
  const type = cleanText(productType).toLowerCase();
  const comparison = (value: string) => {
    let text = cleanText(value).toLowerCase().replace(/\s+(?:design|detailing)$/, "");
    if (type && text.endsWith(" " + type)) text = text.slice(0, -type.length).trimEnd();
    return text;
  };
  const label = (value: string) => value.includes(":") ? value.split(":", 1)[0].toLowerCase().trim() : "";
  const canonicalLabel = (value: string) => /^(?:material(?: composition)?|metal|pendant material)$/.test(value) ? "material" : value;
  const score = (value: string) => /^material composition\s*:/i.test(value) ? 3 : label(value) ? 2 : 1;
  const out: string[] = [];
  // Older descriptions contain natural bullets alongside the same structured
  // attributes. Keep one fact, preferring its more precise label. Distinct
  // labeled quantities (for example length and weight) stay separate.
  for (const value of unique(values)) {
    const identity = comparison(valueAfterLabel(value));
    const index = out.findIndex((existing) => {
      if (comparison(valueAfterLabel(existing)) !== identity) return false;
      const first = label(existing);
      const second = label(value);
      return !first || !second || canonicalLabel(first) === canonicalLabel(second);
    });
    if (index < 0) out.push(value);
    else if (score(value) > score(out[index])) out[index] = value;
  }
  return out;
}

const DESCRIPTION_BOILERPLATE_RE =
  /^(?:product\s+(?:information|details|measurements?)|measurements?|size\s*(?:&|and)?\s*measurements?|size\s+(?:conversion|chart|guide)|packing\s+list|package\s+(?:list|includes?)|specifications?|notes?\s*:|\d+[.)]\s*)/i;

const KEYWORD_NOISE_RE =
  /^(?:general|standard\s+specifications?|standard|default|ordinary|as\s+shown|see\s+picture|product\s+information|specifications?|applicable\s+people|brand|other|other effects?|other functions?)$/i;

const SEO_DETAIL_LABEL_RE =
  /^(?:material(?:\s+composition)?|metal|stone|color|shade|size|stone\s+size|net\s+content|capacity|length|weight|finish|texture|number\s+of\s+pieces|features?|stretch)\s*:/i;

function usefulKeywordDetail(value: string): boolean {
  const cleaned = cleanText(value);
  if (!cleaned || cleaned.length < 2 || cleaned.length > 70) return false;
  if (KEYWORD_NOISE_RE.test(cleaned)) return false;
  if ((cleaned.match(/,/g) ?? []).length > 3) return false;
  return true;
}

function usefulSeoDetailValues(highlights: string[]): string[] {
  return highlights
    .filter((item) => SEO_DETAIL_LABEL_RE.test(item))
    .map(valueAfterLabel)
    .filter(usefulKeywordDetail);
}

function highlightValue(
  highlights: string[],
  label: RegExp,
): string {
  const item = highlights.find((value) => label.test(value));
  return item ? valueAfterLabel(item) : "";
}

function naturalList(values: string[]): string {
  const cleaned = values.map(cleanText).filter(Boolean);
  if (cleaned.length <= 1) return cleaned[0] ?? "";
  if (cleaned.length === 2) return cleaned.join(" and ");
  return cleaned.slice(0, -1).join(", ") + ", and " + cleaned.at(-1);
}

function articleFor(value: string): string {
  return /^[aeiou]/i.test(value.trim()) ? "an" : "a";
}

function groundedIntro(
  productType: string,
  highlights: string[],
): string {
  const type = cleanText(productType).toLowerCase();
  if (!type) return "";

  const pieces = highlightValue(highlights, /^number of pieces\s*:/i);
  const feature = highlightValue(highlights, /^features?\s*:/i);
  const stretch = highlightValue(highlights, /^stretch\s*:/i);
  const material = highlightValue(highlights, /^material composition\s*:/i);

  const details = [
    pieces ? pieces.toLowerCase() + " design" : "",
    feature ? feature.toLowerCase() + " detailing" : "",
    stretch ? stretch.toLowerCase() : "",
    material ? material + " composition" : "",
  ].filter(Boolean);

  if (!details.length) return "";
  return `${articleFor(type)[0].toUpperCase() + articleFor(type).slice(1)} ${type} with ${naturalList(details)}.`;
}

function productSeed(product: ProductSnapshot): number {
  const key = product.id || product.handle || product.title;
  let seed = 2166136261;
  for (const char of key) seed = Math.imul(seed ^ char.charCodeAt(0), 16777619);
  return seed >>> 0;
}

function titleCase(value: string): string {
  return value.split(" ").map((word) => {
    if (/^(?:\d.*|SPF|BB|CC|UV|USB)$/i.test(word)) return word;
    return word.split("-").map((part) => part.charAt(0).toUpperCase() + part.slice(1).toLowerCase()).join("-");
  }).join(" ");
}

function factualProductName(
  product: ProductSnapshot,
  classification: Classification,
  highlights: string[],
  vocabulary: BrandVocabulary,
  sanitizeClaims = false,
): string {
  let name = cleanCustomerText(
    cleanText(product.title),
    product.vendor,
    vocabulary,
    sanitizeClaims,
  )
    .replace(TRAILING_CODE_RE, "")
    .replace(/^beauty\s+(?=\S)/i, "")
    .replace(/\b(?:european\s+and\s+american|european|american|special[- ]interest|light\s+luxury|design\s+sense|exquisite|fashion|ornament|hot\s+sale|new\s+arrival|high[- ]quality|top\s+quality|women'?s?\s+cosmetics|new|pma)\b/gi, " ")
    .replace(/\bcolor(?=\s+zircon)\b/gi, " ")
    .replace(/\s+/g, " ")
    .trim();

  // Remove a prior editorial prefix, so processing our own output is stable.
  const modifiers = new Set(Object.values(vocabulary.profiles).flatMap((profile) => profile.adjectives));
  while (modifiers.has(name.split(" ")[0]?.toLowerCase())) name = name.split(" ").slice(1).join(" ");

  const seen = new Set<string>();
  name = name.split(" ").filter((word) => {
    const key = word.toLowerCase();
    if (/^(?:and|with|for|of|in|the|a|an)$/.test(key)) return true;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  }).join(" ").trim();

  if (classification.department === "Jewelry") {
    const material = highlightValue(highlights, /^(?:material|metal|pendant material)\s*:/i);
    if (material && material.length <= 30) {
      const escaped = material.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      name = material + " " + name.replace(new RegExp(`\\b${escaped}\\b`, "gi"), " ").replace(SPACE_RE, " ").trim();
    }
    if (classification.family === "Necklaces" && !/\bnecklace\b/i.test(name)) name += " Necklace";
  }
  name = name
    .replace(/\bwithdiamonds\b/gi, "with diamonds")
    .replace(/^care\s+hair\s+oil\b/i, "hair care oil")
    .replace(/\bcream\s+hand\b/i, "hand cream")
    .replace(/\b(?:and|or|for|with|of|to|in|the|a|an)\s*$/i, "")
    .replace(SPACE_RE, " ")
    .trim();
  return titleCase(name || classification.productType);
}

function brandedProductCopy(
  product: ProductSnapshot,
  classification: Classification,
  highlights: string[],
  brandLabel: string,
  vocabulary: BrandVocabulary,
  sanitizeClaims = false,
): { title: string; shortDescription: string } {
  const princess = /miss\.?\s*princess/i.test(brandLabel);
  const profile = vocabulary.profiles[princess ? "miss-princess" : "mvqueen"];
  const seed = productSeed(product);
  const adjective = profile.adjectives[seed % profile.adjectives.length];
  const base = factualProductName(
    product,
    classification,
    highlights,
    vocabulary,
    sanitizeClaims,
  );

  // Product titles are factual/search-first. Brand vocabulary belongs in
  // editorial copy, not as a random adjective prefix on every title.
  const sourceNoun = base.match(/\b(?:body (?:moisturizer|scrub|cream|lotion|wash|oil|butter)|hair (?:oil|mask|serum|dryer|brush)|lip (?:balm|gloss|oil|liner)|waxing kit|face cream|facial cream|skin care|necklace|bracelet|earrings?|anklet|ring|dress|bodysuit|jumpsuit|romper|blouse|shorts|pants|skirt|shampoo|conditioner|foundation|concealer|mascara|lipstick|perfume|fragrance)\b/i)?.[0];
  const endNoun = classification.family === "Necklaces" ? "Necklace" : sourceNoun ?? "";
  let title = base;
  if (title.length > 80) {
    const escaped = endNoun.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const head = endNoun
      ? title.replace(new RegExp(`\\b${escaped}\\b`, "gi"), " ").replace(SPACE_RE, " ").trim()
      : title;
    const ending = endNoun ? " " + endNoun : "";
    title = clipTitle(head, 80 - ending.length) + ending;
  }
  title = title
    .replace(/\b(?:and|or|for|with|of|to|in|the|a|an)\s*$/i, "")
    .replace(SPACE_RE, " ")
    .trim();
  if (classification.productType === "Press-On Nails" && /press\s+on\s+nails?/i.test(title)) {
    const long = /\blong\b/i.test(title) ? "Long " : "";
    const crystal = /\bcrystal\b/i.test(title) ? "Crystal " : "";
    title = `${long}${crystal}Press-On Nails`.trim();
  }
  if (classification.productType === "Bath & Body" && /^cream\s+\d+(?:\.\d+)?\s*g$/i.test(title)) {
    title = "Body " + title;
  }

  const type = cleanText(classification.productType).toLowerCase() || "piece";
  const detailValues = usefulSeoDetailValues(highlights).slice(0, 2);
  const detailPhrase = naturalList(detailValues);
  const style = adjective.toLowerCase();

  const factualTemplates = princess
    ? [
        `${titleCase(type)} with ${detailPhrase}, styled with a ${style}, expressive ${brandLabel} point of view.`,
        `Built around ${detailPhrase}, this ${type} keeps the ${brandLabel} presentation ${style}, fresh, and clear.`,
        `${detailPhrase} define this ${type}, finished with ${style} ${brandLabel} styling and straightforward details.`,
        `${articleFor(style)[0].toUpperCase() + articleFor(style).slice(1)} ${style} ${brandLabel} take on ${type}, grounded in ${detailPhrase}.`,
      ]
    : [
        `${titleCase(type)} with ${detailPhrase}, presented through a ${style} ${brandLabel} point of view.`,
        `Built around ${detailPhrase}, this ${type} keeps the ${brandLabel} presentation ${style}, polished, and clear.`,
        `${detailPhrase} define this ${type}, with ${style} ${brandLabel} styling and straightforward details.`,
        `${articleFor(style)[0].toUpperCase() + articleFor(style).slice(1)} ${style} ${brandLabel} take on ${type}, grounded in ${detailPhrase}.`,
      ];

  const fallbackTemplates = princess
    ? [
        `${articleFor(style)[0].toUpperCase() + articleFor(style).slice(1)} ${style} ${brandLabel} ${type} with clear product details and an expressive point of view.`,
        `This ${type} brings a ${style} ${brandLabel} perspective while keeping the product details clear.`,
        `${title} is presented with ${style} ${brandLabel} styling and straightforward product information.`,
      ]
    : [
        `${articleFor(style)[0].toUpperCase() + articleFor(style).slice(1)} ${style} ${brandLabel} ${type} with clear product details and a polished point of view.`,
        `This ${type} brings a ${style} ${brandLabel} perspective while keeping the product details clear.`,
        `${title} is presented with ${style} ${brandLabel} styling and straightforward product information.`,
      ];

  const pool = detailPhrase ? factualTemplates : fallbackTemplates;
  let shortDescription = cleanText(pool[(seed >>> 8) % pool.length]);
  if (shortDescription.length > 180) {
    shortDescription = clipTitle(
      detailPhrase
        ? `${titleCase(type)} with ${detailPhrase}, presented with ${style} ${brandLabel} styling.`
        : `${title} with ${style} ${brandLabel} styling.`,
      179,
    ).replace(/[,:;\-]+$/, "").trim();
    if (!/[.!?]$/.test(shortDescription)) shortDescription += ".";
  }

  return { title, shortDescription };
}

function escapeHtml(value: string): string {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function preservedTables(html?: string | null): string[] {
  const source = String(html ?? "");
  return [...source.matchAll(/<table\b[^>]*>[\s\S]*?<\/table>/gi)]
    .map((match) =>
      match[0]
        .replace(/\sstyle=(["'])[^"']*\1/gi, "")
        .replace(/\sclass=(["'])[^"']*\1/gi, "")
        .trim(),
    )
    .filter(Boolean);
}

function buildDescriptionHtml(
  shortDescription: string,
  highlights: string[],
  sourceDescriptionHtml?: string | null,
  factualIntro = "",
): string {
  const intro = shortDescription
    ? `<p>${escapeHtml(shortDescription)}</p>`
    : "";

  const details = highlights.length
    ? `<h3>Product Details</h3><ul>${highlights
        .map((item) => `<li>${escapeHtml(item)}</li>`)
        .join("")}</ul>`
    : "";

  const tables = preservedTables(sourceDescriptionHtml);
  const measurements = tables.length
    ? `<h3>Size &amp; Measurements</h3>${tables.join("")}`
    : "";

  const facts = factualIntro ? `<p>${escapeHtml(factualIntro)}</p>` : "";
  return (intro + facts + details + measurements).trim();
}

function brandedSeoTitle(title: string, brandLabel: string): string {
  const suffix = " | " + cleanText(brandLabel);
  if (suffix.length >= 60) return cleanText(brandLabel).slice(0, 60).trim();
  const available = 60 - suffix.length;
  const cleanTitle = cleanText(title);
  const base =
    cleanTitle.length <= available
      ? cleanTitle
      : cleanTitle.slice(0, available).replace(/\s+\S*$/, "").trim() ||
        cleanTitle.slice(0, available).trim();
  return base + suffix;
}

function keywordTitle(title: string, productType: string): string {
  const lower = cleanText(title).toLowerCase();
  const type = cleanText(productType).toLowerCase();
  if (!lower) return type;
  const words = lower.split(" ").filter(Boolean);
  if (words.length <= 6) return lower;
  const typeWords = new Set(type.split(" ").filter(Boolean));
  const selected: string[] = [];
  for (const word of words) {
    if (selected.length >= 6) break;
    if (!selected.includes(word) || typeWords.has(word)) selected.push(word);
  }
  return selected.join(" ");
}

function keywordTokenSet(value: string): Set<string> {
  return new Set(
    cleanText(value)
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, " ")
      .split(SPACE_RE)
      .filter(Boolean),
  );
}

function composeKeywordParts(parts: string[]): string {
  const candidates = unique(parts)
    .map((value) => value.toLowerCase())
    .filter(Boolean);
  const tokenSets = candidates.map(keywordTokenSet);

  return candidates
    .filter((_value, index) => {
      const current = tokenSets[index];
      if (!current.size) return false;
      return !tokenSets.some((other, otherIndex) => {
        if (index === otherIndex || !other.size) return false;
        const contained = [...current].every((token) => other.has(token));
        if (!contained) return false;
        return current.size < other.size ||
          (current.size === other.size && index < otherIndex);
      });
    })
    .join(" ")
    .replace(SPACE_RE, " ")
    .trim();
}

export function buildAutomatedProductContent(
  product: ProductSnapshot,
  classification: Classification,
  brandLabel = "MVQueen",
  vocabulary = BRAND_VOCABULARY,
): AutomatedProductContent {
  const sanitizeClaims = productClaimReviewReasons(product).length > 0;
  const sourceHighlights = uniqueHighlights([
    ...extractHighlights(product.descriptionHtml),
    ...structuredSourceHighlights(product),
  ].map((item) =>
      cleanCustomerText(item, product.vendor, vocabulary, sanitizeClaims),
    )
    .filter((item) => Boolean(item) && !DESCRIPTION_BOILERPLATE_RE.test(item)), classification.productType);
  const highlights = sourceHighlights.length
    ? sourceHighlights
    : [`Product type: ${classification.productType}`];

  // Karat "purity" cannot describe stainless steel. Keep that supplier field
  // in the source metadata and variant options, without presenting it as a
  // solid-gold composition claim in the customer-facing details.
  if (classification.department === "Jewelry" && /stainless steel/i.test(highlightValue(highlights, /^(?:material|metal|pendant material)\s*:/i))) {
    for (let index = highlights.length - 1; index >= 0; index--) {
      if (/^purity\s*:/i.test(highlights[index])) highlights.splice(index, 1);
    }
  }

  const generatedIntro = groundedIntro(
    classification.productType,
    highlights,
  );
  const { title, shortDescription } = brandedProductCopy(
    product,
    classification,
    highlights,
    brandLabel,
    vocabulary,
    sanitizeClaims,
  );

  const focusKeyword = cleanText(classification.productType).toLowerCase();
  const titleKeyword = keywordTitle(title, classification.productType);
  const detailValues = usefulSeoDetailValues(highlights);

  const secondaryKeywords = unique([
    cleanText(classification.subcollection).toLowerCase(),
    cleanText(classification.family).toLowerCase(),
    titleKeyword,
  ])
    .map((value) => value.toLowerCase())
    .filter((value) => value !== focusKeyword)
    .slice(0, 4);

  const longTailKeywords = unique([
    title.toLowerCase(),
    composeKeywordParts([titleKeyword, detailValues[0] ?? ""]),
    composeKeywordParts([titleKeyword, detailValues[1] ?? ""]),
    composeKeywordParts([detailValues[0] ?? "", focusKeyword]),
    composeKeywordParts([detailValues[1] ?? "", focusKeyword]),
    composeKeywordParts([
      detailValues[0] ?? "",
      detailValues[1] ?? "",
      focusKeyword,
    ]),
  ])
    .filter((value) => {
      const words = value.split(/\s+/).filter(Boolean).length;
      return words >= 4 && words <= 12;
    })
    .slice(0, 5);

  const descriptionHtml = buildDescriptionHtml(
    shortDescription,
    highlights,
    sanitizeClaims ? undefined : product.descriptionHtml,
    generatedIntro,
  );

  const seoTitle = brandedSeoTitle(title, brandLabel);
  const metaDescription = clip(
    "Shop " + title + " at " + brandLabel + ". " + shortDescription,
    155,
  );

  const seoKeywords = unique([
    focusKeyword,
    ...secondaryKeywords,
    ...longTailKeywords,
  ]).map((value) => value.toLowerCase());

  return {
    title,
    shortDescription,
    descriptionHtml,
    highlights,
    focusKeyword,
    secondaryKeywords,
    longTailKeywords,
    seoTitle,
    metaDescription,
    seoKeywords,
  };
}
