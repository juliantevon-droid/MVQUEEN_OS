import type { Classification, ProductSnapshot } from "./mvqueen-intelligence";
import type { CatalogAttributeEnrichment } from "./catalog-attribute-enrichment";

export type TaxonomyValueCandidate = {
  id: string;
  name: string;
};

export type TaxonomyAttributeCandidate = {
  id: string;
  name: string;
  values: TaxonomyValueCandidate[];
};

function normalize(value: string): string {
  return value
    .toLowerCase()
    .replace(/&/g, " and ")
    .replace(/\bcolour\b/g, "color")
    .replace(/\bwomen'?s\b/g, "women")
    .replace(/[^a-z0-9]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function unique<T>(values: T[], key: (value: T) => string): T[] {
  const seen = new Set<string>();
  const out: T[] = [];
  for (const value of values) {
    const id = key(value);
    if (seen.has(id)) continue;
    seen.add(id);
    out.push(value);
  }
  return out;
}

function sourceText(
  product: ProductSnapshot,
  enrichment: CatalogAttributeEnrichment,
): string {
  return normalize(
    [
      product.title ?? "",
      product.productType ?? "",
      product.descriptionHtml?.replace(/<[^>]+>/g, " ") ?? "",
      product.seo?.title ?? "",
      product.seo?.description ?? "",
      ...(product.tags ?? []),
      enrichment.material ?? "",
      enrichment.fabric ?? "",
      enrichment.fit ?? "",
      enrichment.pattern ?? "",
      enrichment.season ?? "",
      ...enrichment.colors,
      ...enrichment.sizes,
      ...enrichment.occasions,
      ...enrichment.activities,
      ...enrichment.features,
      ...Object.entries(enrichment.sourceAttributes).flatMap(([key, value]) => [
        key,
        value,
      ]),
    ].join(" "),
  );
}

function candidateByName(
  candidates: TaxonomyValueCandidate[],
  name: string,
): TaxonomyValueCandidate | null {
  const target = normalize(name);
  return (
    candidates.find((candidate) => normalize(candidate.name) === target) ??
    null
  );
}

function colorBaseName(value: string): string {
  const n = normalize(value);
  const direct = [
    "black",
    "white",
    "gray",
    "silver",
    "gold",
    "rose gold",
    "red",
    "pink",
    "purple",
    "blue",
    "navy",
    "green",
    "yellow",
    "orange",
    "brown",
    "beige",
    "bronze",
    "clear",
    "multicolor",
  ];
  const exact = direct.find((name) => n === name);
  if (exact) return exact;
  if (/\brose gold\b/.test(n)) return "rose gold";
  if (/\bgold\b/.test(n)) return "gold";
  if (/\bsilver\b/.test(n)) return "silver";
  if (/\bnavy\b/.test(n)) return "navy";
  if (/\bsky blue\b|\belectric blue\b|\blight blue\b|\bdark blue\b/.test(n)) return "blue";
  if (/\bhot pink\b|\bblush\b|\bfuchsia\b/.test(n)) return "pink";
  if (/\bivory\b|\bcream\b/.test(n)) return "white";
  if (/\bcharcoal\b/.test(n)) return "gray";
  if (/\bmulti(?:color|colored)?\b|\brainbow\b/.test(n)) return "multicolor";
  for (const name of direct) {
    if (new RegExp(`\\b${name.replace(/ /g, "\\s+")}\\b`).test(n)) return name;
  }
  return n;
}

function materialAliases(value: string): string[] {
  const n = normalize(value);
  const out = [n];
  if (/\belastane\b/.test(n)) out.push("spandex");
  if (/\bpu leather\b|\bvegan leather\b/.test(n)) out.push("faux leather");
  if (/\b14k gold plated\b|\b18k gold plated\b|\bgold plated\b/.test(n)) {
    out.push("gold plated");
  }
  if (/\brose gold plated\b/.test(n)) out.push("rose gold plated");
  if (/\bsilver plated\b/.test(n)) out.push("silver plated");
  if (/\bstainless steel\b/.test(n)) out.push("stainless steel");
  return unique(out, (item) => item);
}

function parseLengthInches(value: string): number | null {
  const n = value.toLowerCase().replace(/,/g, ".");
  const numbers = [...n.matchAll(/(\d+(?:\.\d+)?)/g)].map((match) =>
    Number(match[1]),
  );
  if (!numbers.length) return null;
  let average =
    numbers.length >= 2 ? (numbers[0] + numbers[1]) / 2 : numbers[0];

  if (/\bmm\b/.test(n)) average /= 25.4;
  else if (/\bcm\b/.test(n)) average /= 2.54;
  else if (/\b(?:in|inch|inches)\b|["″]/.test(n)) {
    // already inches
  } else {
    return null;
  }
  return Number.isFinite(average) ? average : null;
}

function necklaceLengthType(
  enrichment: CatalogAttributeEnrichment,
  product: ProductSnapshot,
): string | null {
  const raw =
    enrichment.sourceAttributes.chain_length ??
    enrichment.sourceAttributes.necklace_length ??
    enrichment.sourceAttributes.length ??
    "";
  const inches = parseLengthInches(raw);
  if (inches !== null) {
    if (inches <= 14) return "Collar";
    if (inches <= 16.5) return "Choker";
    if (inches <= 19.5) return "Princess";
    if (inches <= 24.5) return "Matinee";
    if (inches <= 36.5) return "Opera";
    return "Rope";
  }

  const text = sourceText(product, enrichment);
  for (const name of [
    "Choker",
    "Collar",
    "Lariat",
    "Matinee",
    "Opera",
    "Princess",
    "Rope",
    "Y-shaped",
  ]) {
    if (text.includes(normalize(name))) return name;
  }
  return null;
}

function explicitJewelryType(
  product: ProductSnapshot,
  enrichment: CatalogAttributeEnrichment,
): string | null {
  const text = sourceText(product, enrichment);
  if (text.includes("fine jewelry")) return "Fine jewelry";
  if (text.includes("imitation jewelry") || text.includes("costume jewelry")) {
    return "Imitation jewelry";
  }
  return null;
}

function necklaceDesign(
  product: ProductSnapshot,
  enrichment: CatalogAttributeEnrichment,
  classification: Classification,
): string | null {
  const text = sourceText(product, enrichment);
  const values = [
    "Beaded",
    "Chain",
    "Choker",
    "Cord",
    "Cuff",
    "Lariat",
    "Pendant",
    "Riviera",
    "Statement",
    "Strand",
    "Y-shaped",
  ];
  for (const value of values) {
    if (text.includes(normalize(value))) return value;
  }
  if (classification.route === "pendants") return "Pendant";
  if (/\bcross necklace\b/.test(text)) return "Pendant";
  return null;
}

function directDesiredValues(
  attributeName: string,
  product: ProductSnapshot,
  enrichment: CatalogAttributeEnrichment,
  classification: Classification,
): string[] {
  const name = normalize(attributeName);

  if (name === "color") return enrichment.colors.map(colorBaseName);
  if (name === "age group") {
    return enrichment.ageGroup.toLowerCase() === "adult"
      ? ["Adults"]
      : [enrichment.ageGroup];
  }
  if (name === "target gender") {
    return enrichment.targetGender.toLowerCase() === "women"
      ? ["Female"]
      : [enrichment.targetGender];
  }
  if (name === "pattern" && enrichment.pattern) return [enrichment.pattern];
  if (name.includes("size type") && enrichment.sizeType) return [enrichment.sizeType];
  if (name.includes("fit") && enrichment.fit) return [enrichment.fit];
  if (name.includes("occasion")) return enrichment.occasions;
  if (name.includes("activity") || name.includes("training usage")) {
    return enrichment.activities;
  }
  if (name.includes("feature")) return enrichment.features;
  if (name.includes("size") && !name.includes("size type")) return enrichment.sizes;
  if (name === "jewelry type") {
    const value = explicitJewelryType(product, enrichment);
    return value ? [value] : [];
  }
  if (name === "necklace design") {
    const value = necklaceDesign(product, enrichment, classification);
    return value ? [value] : [];
  }
  if (name === "necklace length type") {
    const value = necklaceLengthType(enrichment, product);
    return value ? [value] : [];
  }
  if (name.includes("material")) {
    return [
      ...materialAliases(enrichment.material ?? ""),
      ...materialAliases(enrichment.fabric ?? ""),
    ].filter(Boolean);
  }

  return [];
}

function fuzzyMatch(
  desired: string,
  candidates: TaxonomyValueCandidate[],
): TaxonomyValueCandidate | null {
  const normalizedDesired = normalize(desired);
  const direct = candidateByName(candidates, normalizedDesired);
  if (direct) return direct;

  const aliases = materialAliases(normalizedDesired);
  for (const alias of aliases) {
    const exact = candidateByName(candidates, alias);
    if (exact) return exact;
  }

  const contained = candidates.find((candidate) => {
    const n = normalize(candidate.name);
    if (!n || ["other", "universal", "all ages"].includes(n)) return false;
    return (
      normalizedDesired.includes(n) ||
      n.includes(normalizedDesired)
    );
  });
  return contained ?? null;
}

export function selectTaxonomyValues(args: {
  attribute: TaxonomyAttributeCandidate;
  product: ProductSnapshot;
  enrichment: CatalogAttributeEnrichment;
  classification: Classification;
}): TaxonomyValueCandidate[] {
  const { attribute, product, enrichment, classification } = args;
  const desired = directDesiredValues(
    attribute.name,
    product,
    enrichment,
    classification,
  );

  const matches = desired
    .map((value) => fuzzyMatch(value, attribute.values))
    .filter((value): value is TaxonomyValueCandidate => Boolean(value));

  if (matches.length) return unique(matches, (value) => value.id).slice(0, 12);

  const text = sourceText(product, enrichment);
  const explicit = attribute.values.filter((candidate) => {
    const name = normalize(candidate.name);
    if (!name || ["other", "universal", "all ages"].includes(name)) return false;
    if (name.length < 3) return false;
    const escaped = name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&").replace(/\s+/g, "\\s+");
    return new RegExp(`(?:^|\\b)${escaped}(?:$|\\b)`, "i").test(text);
  });

  return unique(explicit, (value) => value.id).slice(0, 8);
}
