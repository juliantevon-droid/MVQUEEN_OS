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

function valueAfterLabel(value: string): string {
  const cleaned = cleanText(value);
  const colon = cleaned.indexOf(":");
  return colon > 0 ? cleaned.slice(colon + 1).trim() : cleaned;
}

const DESCRIPTION_BOILERPLATE_RE =
  /^(?:product\s+measurements?|measurements?|size\s*(?:&|and)?\s*measurements?|size\s+(?:conversion|chart|guide))/i;

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

export function buildAutomatedProductContent(
  product: ProductSnapshot,
  classification: Classification,
): AutomatedProductContent {
  const sourceTitle = cleanText(product.title);
  const title = stripVendor(sourceTitle, product.vendor)
    .replace(TRAILING_CODE_RE, "")
    .replace(SPACE_RE, " ")
    .trim() || sourceTitle;

  const highlights = extractHighlights(product.descriptionHtml)
    .map((item) => stripVendor(item, product.vendor))
    .filter(Boolean);

  const descriptionSentence = stripVendor(
    sentenceFromDescription(product.descriptionHtml),
    product.vendor,
  );
  const generatedIntro = groundedIntro(
    classification.productType,
    highlights,
  );
  const shortDescription = clip(
    descriptionSentence ||
      generatedIntro ||
      title + " — " + classification.productType + " from the MVQueen edit.",
    180,
  );

  const focusKeyword = cleanText(classification.productType).toLowerCase();
  const titleKeyword = keywordTitle(title, classification.productType);
  const detailValues = highlights.map(valueAfterLabel).filter(Boolean);

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
    detailValues[0] ? (detailValues[0] + " " + focusKeyword).toLowerCase() : "",
    detailValues[1] ? (detailValues[1] + " " + focusKeyword).toLowerCase() : "",
    detailValues[0] && detailValues[1]
      ? (detailValues[0] + " " + detailValues[1] + " " + focusKeyword).toLowerCase()
      : "",
  ])
    .filter((value) => value.split(" ").length >= 4)
    .slice(0, 5);

  const descriptionHtml = buildDescriptionHtml(
    shortDescription,
    highlights,
    product.descriptionHtml,
  );

  const seoTitle = clip(title + " | MVQueen", 60);
  const descriptionPlain = stripVendor(cleanText(product.descriptionHtml), product.vendor);
  const metaDescription = clip(
    descriptionPlain
      ? "Shop " + title + " at MVQueen. " + descriptionPlain
      : "Shop " + title + " at MVQueen. Explore verified product details, imagery, shipping and returns.",
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
