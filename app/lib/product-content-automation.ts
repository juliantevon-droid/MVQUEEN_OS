import type { Classification, ProductSnapshot } from "./mvqueen-intelligence";

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
  "MABREM", "WUWUVISTA", "COFULTIC",
];

const CLAIM_REVIEW_RULES: Array<[string, RegExp]> = [
  ["medical_or_guaranteed", /\b(?:cures?|treats?|prevents?|clinically\s+proven|medical[- ]grade|guaranteed?|permanent)\b/i],
  ["hair_loss_or_regrowth", /\b(?:anti[- ]?hair\s+loss|hair\s+regrowth|regrowth)\b/i],
  ["scar_claim", /\bscar\b[\s\S]{0,30}\b(?:remov|repair|treat|cream|gel|desalination|fade)/i],
  ["body_enhancement", /\b(?:(?:breast|bust|butt|hip)\b[\s\S]{0,35}\b(?:enhanc(?:e|er|ement|ing)?|enlarg(?:e|ement|ing)?|lift(?:ing)?|growth|firm(?:ing|ness)?)|breast\s+(?:beauty|care)|bust\s+care)\b/i],
  ["fat_or_cellulite_claim", /\b(?:fat\s+burning|weight\s+loss|anti[- ]?cellulite|cellulite\s+(?:reduction|removal)|slimming\s+(?:cream|oil|gel|massager|device))\b/i],
  ["wrinkle_treatment_claim", /\b(?:wrinkles?\b[\s\S]{0,25}\b(?:remove|flat|reduce|tighten)|tightening\s+cream[\s\S]{0,25}\bwrinkles?)\b/i],
];

export function productClaimReviewReasons(
  product: Pick<ProductSnapshot, "title" | "descriptionHtml">,
): string[] {
  const text = [
    String(product.title ?? ""),
    String(product.descriptionHtml ?? "").replace(HTML_RE, " "),
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

function cleanCustomerText(value: string, vendor?: string | null): string {
  return stripKnownCustomerBrands(stripVendor(value, vendor))
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

function extractParagraphs(html?: string | null): string[] {
  const source = String(html ?? "");
  const matches = [...source.matchAll(/<p\b[^>]*>([\s\S]*?)<\/p>/gi)]
    .map((match) => cleanText(match[1]))
    .filter(Boolean);
  return unique(matches);
}

function extractHighlights(html?: string | null): string[] {
  const source = String(html ?? "");
  return unique(
    [...source.matchAll(/<li\b[^>]*>([\s\S]*?)<\/li>/gi)]
      .map((match) =>
        cleanText(match[1])
          .replace(/^[-•]\s*/, "")
          .replace(/\s*:\s*/g, ": "),
      )
      .filter(Boolean),
  ).slice(0, 6);
}

function humanizeAttributeKey(value: string): string {
  return value
    .replace(/[_-]+/g, " ")
    .replace(/\s+/g, " ")
    .trim()
    .replace(/^./, (char) => char.toUpperCase());
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
        if (!value) continue;
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

  return unique(highlights).slice(0, 6);
}

function valueAfterLabel(value: string): string {
  const cleaned = cleanText(value);
  const colon = cleaned.indexOf(":");
  return colon > 0 ? cleaned.slice(colon + 1).trim() : cleaned;
}

const DESCRIPTION_BOILERPLATE_RE =
  /^(?:product\s+(?:information|details|measurements?)|measurements?|size\s*(?:&|and)?\s*measurements?|size\s+(?:conversion|chart|guide)|packing\s+list|package\s+(?:list|includes?)|specifications?|notes?\s*:|\d+[.)]\s*)/i;

const KEYWORD_NOISE_RE =
  /^(?:general|standard\s+specifications?|standard|default|ordinary|as\s+shown|see\s+picture|product\s+information|specifications?|applicable\s+people)$/i;

function usefulKeywordDetail(value: string): boolean {
  const cleaned = cleanText(value);
  if (!cleaned || cleaned.length < 2 || cleaned.length > 70) return false;
  if (KEYWORD_NOISE_RE.test(cleaned)) return false;
  if ((cleaned.match(/,/g) ?? []).length > 3) return false;
  return true;
}

function sentenceFromDescription(html?: string | null): string {
  const paragraphs = extractParagraphs(html).filter(
    (paragraph) => !DESCRIPTION_BOILERPLATE_RE.test(paragraph),
  );
  const usable =
    paragraphs.find((paragraph) => paragraph.length >= 28) ??
    paragraphs[0] ??
    "";
  if (!usable) return "";
  const sentence =
    usable.match(/^(.{20,220}?[.!?])(?:\s|$)/)?.[1] ?? usable;
  return clip(sentence, 180);
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
  return clip(
    `${articleFor(type)[0].toUpperCase() + articleFor(type).slice(1)} ${type} with ${naturalList(details)}.`,
    180,
  );
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

  return (intro + details + measurements).trim();
}

function alignBrandLabel(value: string, brandLabel: string): string {
  const target = cleanText(brandLabel) || "MVQueen";
  return cleanText(value)
    .replace(/\bmiss\.?\s*princess\b/gi, target)
    .replace(/\bmvqueen\b/gi, target)
    .replace(SPACE_RE, " ")
    .trim();
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
): AutomatedProductContent {
  const sourceTitle = cleanText(product.title);
  const cleanedSourceTitle = cleanCustomerText(sourceTitle, product.vendor);
  const title = clipTitle(
    cleanedSourceTitle
      .replace(TRAILING_CODE_RE, "")
      .replace(SPACE_RE, " ")
      .trim() || cleanedSourceTitle || sourceTitle,
  );

  const highlights = unique([
    ...extractHighlights(product.descriptionHtml)
      .map((item) => cleanCustomerText(item, product.vendor))
      .filter(Boolean),
    ...structuredSourceHighlights(product),
  ]).slice(0, 6);

  const descriptionSentence = alignBrandLabel(
    cleanCustomerText(
      sentenceFromDescription(product.descriptionHtml),
      product.vendor,
    ),
    brandLabel,
  );
  const generatedIntro = groundedIntro(
    classification.productType,
    highlights,
  );
  const shortDescription = clip(
    descriptionSentence ||
      generatedIntro ||
      title + " — " + classification.productType + " from the " + brandLabel + " edit.",
    180,
  );

  const focusKeyword = cleanText(classification.productType).toLowerCase();
  const titleKeyword = keywordTitle(title, classification.productType);
  const detailValues = highlights
    .map(valueAfterLabel)
    .filter(usefulKeywordDetail);

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
    product.descriptionHtml,
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
