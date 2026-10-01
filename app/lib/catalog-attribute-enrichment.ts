import type { Classification, ProductSnapshot } from "./mvqueen-intelligence";

export type CatalogAttributeEnrichment = {
  colors: string[];
  sizes: string[];
  material: string | null;
  fabric: string | null;
  fit: string | null;
  occasions: string[];
  activities: string[];
  targetGender: "Women";
  ageGroup: "Adult";
  sizeType: string | null;
  features: string[];
  pattern: string | null;
  season: string | null;
  careInstructions: string | null;
  sourceAttributes: Record<string, string>;
  customProduct: boolean;
};

export type CatalogMetafieldInput = {
  namespace: string;
  key: string;
  type: string;
  value: string;
};

function cleanText(value: string): string {
  return value
    .replace(/&amp;/gi, "&")
    .replace(/&nbsp;/gi, " ")
    .replace(/&#39;/gi, "'")
    .replace(/&quot;/gi, '"')
    .replace(/\s+/g, " ")
    .trim();
}

function sourceLines(product: ProductSnapshot): string[] {
  const html = product.descriptionHtml ?? "";
  const text = html
    .replace(/<(?:br\s*\/?|\/p|\/li|\/tr|\/h[1-6])>/gi, "\n")
    .replace(/<[^>]+>/g, " ")
    .replace(/\r/g, "\n");

  return text
    .split(/\n+/)
    .map(cleanText)
    .filter(Boolean);
}

function existingSourceAttributes(product: ProductSnapshot): Record<string, string> {
  const raw = product.attributeMetafields?.nodes?.find(
    (item) => item.key === "source_attributes",
  )?.value;
  if (!raw) return {};
  try {
    const parsed = JSON.parse(raw) as Record<string, unknown>;
    return Object.fromEntries(
      Object.entries(parsed)
        .filter(([, value]) => value !== null && value !== undefined)
        .map(([key, value]) => [normalizedAttributeKey(key), cleanText(String(value))]),
    );
  } catch {
    return {};
  }
}

function variantGoogleValues(product: ProductSnapshot, key: string): string[] {
  return unique(
    (product.variants?.nodes ?? [])
      .map((variant) =>
        variant.googleMetafields?.nodes?.find((item) => item.key === key)?.value ?? "",
      )
      .filter(Boolean),
  );
}

function sourceText(product: ProductSnapshot): string {
  const sourceAttributes = existingSourceAttributes(product);
  return cleanText(
    [
      product.title ?? "",
      product.productType ?? "",
      product.seo?.title ?? "",
      product.seo?.description ?? "",
      ...sourceLines(product),
      ...(product.tags ?? []),
      ...Object.values(sourceAttributes),
      ...variantGoogleValues(product, "color"),
      ...variantGoogleValues(product, "material"),
    ].join(" "),
  );
}

function optionValues(product: ProductSnapshot, names: string[]): string[] {
  const wanted = new Set(names.map((name) => name.toLowerCase()));
  const productValues = (product.options ?? [])
    .filter((option) => wanted.has(option.name.trim().toLowerCase()))
    .flatMap((option) => option.values ?? []);
  const variantValues = (product.variants?.nodes ?? []).flatMap((variant) =>
    (variant.selectedOptions ?? [])
      .filter((option) => wanted.has(option.name.trim().toLowerCase()))
      .map((option) => option.value),
  );
  return unique([...productValues, ...variantValues].map(cleanText).filter(Boolean));
}

function unique(values: string[]): string[] {
  const seen = new Set<string>();
  const out: string[] = [];
  for (const value of values) {
    const cleaned = cleanText(value);
    const key = cleaned.toLowerCase();
    if (!cleaned || seen.has(key)) continue;
    seen.add(key);
    out.push(cleaned);
  }
  return out;
}

function splitValues(value: string): string[] {
  return unique(
    value
      .split(/\s*(?:,|\||\/)\s*/)
      .map((item) => item.trim())
      .filter(Boolean),
  );
}

function labeledValue(lines: string[], labels: string[]): string | null {
  const patterns = labels.map(
    (label) =>
      new RegExp(
        `^${label.replace(/[.*+?^${}()|[\\]\\]/g, "\\$&")}\\s*:\\s*(.+)$`,
        "i",
      ),
  );
  for (const line of lines) {
    for (const pattern of patterns) {
      const match = line.match(pattern);
      if (match?.[1]) return cleanText(match[1]);
    }
  }
  return null;
}

function normalizedAttributeKey(label: string): string {
  return label
    .toLowerCase()
    .replace(/&/g, " and ")
    .replace(/[^a-z0-9]+/g, "_")
    .replace(/^_+|_+$/g, "")
    .slice(0, 64);
}

function extractSourceAttributes(lines: string[]): Record<string, string> {
  const attributes: Record<string, string> = {};
  for (const line of lines) {
    const match = line.match(/^([A-Za-z][A-Za-z0-9 &/'()\-]{1,48})\s*:\s*(.+)$/);
    if (!match) continue;
    const key = normalizedAttributeKey(match[1]);
    const value = cleanText(match[2]);
    if (!key || !value || key === "http" || key === "https") continue;
    if (!(key in attributes)) attributes[key] = value;
  }
  return attributes;
}

const FEATURE_TERMS: Array<[RegExp, string]> = [
  [/\bhigh[- ]waisted\b/i, "High-waisted"],
  [/\bruched\b/i, "Ruched"],
  [/\bpleated\b/i, "Pleated"],
  [/\bribbed\b/i, "Ribbed"],
  [/\bsequined?\b/i, "Sequined"],
  [/\blace\b/i, "Lace detail"],
  [/\bmesh\b/i, "Mesh detail"],
  [/\bcut[- ]?out\b/i, "Cutout detail"],
  [/\bbackless\b/i, "Backless"],
  [/\bstrapless\b/i, "Strapless"],
  [/\badjustable straps?\b/i, "Adjustable straps"],
  [/\bpockets?\b/i, "Pockets"],
  [/\bzip(?:per)?(?: closure)?\b/i, "Zipper closure"],
  [/\bbutton(?: closure)?\b/i, "Button closure"],
  [/\bstretchy?\b/i, "Stretch"],
  [/\bwater[- ]?resistant\b/i, "Water-resistant"],
];

const FIT_TERMS: Array<[RegExp, string]> = [
  [/\bbodycon\b/i, "Bodycon"],
  [/\bslim(?:[- ]fit)?\b/i, "Slim"],
  [/\bfitted\b/i, "Fitted"],
  [/\brelaxed(?:[- ]fit)?\b/i, "Relaxed"],
  [/\boversized\b/i, "Oversized"],
  [/\bloose(?:[- ]fit)?\b/i, "Loose"],
  [/\bregular(?:[- ]fit)?\b/i, "Regular"],
  [/\btailored(?:[- ]fit)?\b/i, "Tailored"],
];

const OCCASIONS: Array<[RegExp, string]> = [
  [/\bcasual\b/i, "Casual"],
  [/\bparty\b/i, "Party"],
  [/\bwedding\b/i, "Wedding"],
  [/\bformal\b/i, "Formal"],
  [/\bevening\b/i, "Evening"],
  [/\bdate[- ]?night\b/i, "Date night"],
  [/\bworkwear\b|\boffice\b/i, "Work"],
  [/\bvacation\b|\bresort\b/i, "Vacation"],
  [/\bbeach\b/i, "Beach"],
  [/\blounge(?:wear)?\b/i, "Lounge"],
];

const ACTIVITIES: Array<[RegExp, string]> = [
  [/\byoga\b/i, "Yoga"],
  [/\brunn?ing\b|\bjogging\b/i, "Running"],
  [/\bgym\b|\bworkout\b|\btraining\b/i, "Workout"],
  [/\btennis\b/i, "Tennis"],
  [/\bwalking\b/i, "Walking"],
  [/\bhiking\b/i, "Hiking"],
  [/\bswimming\b|\bswimwear\b/i, "Swimming"],
  [/\bdance\b|\bdancing\b/i, "Dance"],
];

const PATTERNS: Array<[RegExp, string]> = [
  [/\bfloral\b/i, "Floral"],
  [/\bstriped?\b/i, "Striped"],
  [/\bpolka[- ]?dot\b/i, "Polka dot"],
  [/\bplaid\b|\btartan\b/i, "Plaid"],
  [/\bleopard\b/i, "Leopard"],
  [/\bzebra\b/i, "Zebra"],
  [/\banimal[- ]?print\b/i, "Animal print"],
  [/\bcolor[- ]?block(?:ed)?\b/i, "Colorblock"],
  [/\bcamouflage\b|\bcamo\b/i, "Camouflage"],
  [/\bgraphic\b/i, "Graphic"],
  [/\babstract\b/i, "Abstract"],
];

function firstMapped(text: string, patterns: Array<[RegExp, string]>): string | null {
  return patterns.find(([pattern]) => pattern.test(text))?.[1] ?? null;
}

function allMapped(text: string, patterns: Array<[RegExp, string]>): string[] {
  return unique(
    patterns
      .filter(([pattern]) => pattern.test(text))
      .map(([, value]) => value),
  );
}

function extractMaterial(lines: string[]): string | null {
  return labeledValue(lines, [
    "Material composition",
    "Material",
    "Materials",
    "Fabric content",
    "Fabric",
    "Metal",
  ]);
}

function extractCare(lines: string[]): string | null {
  const labeled = labeledValue(lines, ["Care instructions", "Care"]);
  if (labeled) return labeled;
  const line = lines.find((value) =>
    /\b(?:machine wash|hand wash|dry clean|spot clean|tumble dry|line dry)\b/i.test(value),
  );
  return line ? cleanText(line) : null;
}

function extractFeatures(product: ProductSnapshot, lines: string[]): string[] {
  const text = sourceText(product);
  const features: string[] = [];
  const labeled = labeledValue(lines, ["Features", "Feature"]);
  if (labeled) features.push(...splitValues(labeled));

  const stretch = labeledValue(lines, ["Stretch"]);
  if (stretch) features.push(stretch);

  const pieces = labeledValue(lines, ["Number of pieces", "Pieces"]);
  if (pieces) features.push(pieces);

  for (const [pattern, label] of FEATURE_TERMS) {
    if (pattern.test(text)) features.push(label);
  }
  return unique(features).slice(0, 12);
}

function extractSizeType(text: string, classification: Classification, sizes: string[]): string | null {
  if (classification.department !== "Fashion" || !sizes.length) return null;
  if (/\bplus[- ]?size\b/i.test(text)) return "plus";
  if (/\bpetite\b/i.test(text)) return "petite";
  if (/\bmaternity\b/i.test(text)) return "maternity";
  if (/\bbig\s*(?:&|and)\s*tall\b/i.test(text)) return "big and tall";
  return "regular";
}

function extractSeason(text: string): string | null {
  const values: Array<[RegExp, string]> = [
    [/\bspring\b/i, "Spring"],
    [/\bsummer\b/i, "Summer"],
    [/\bfall\b|\bautumn\b/i, "Fall"],
    [/\bwinter\b/i, "Winter"],
    [/\bholiday\b/i, "Holiday"],
  ];
  return firstMapped(text, values);
}

export function buildCatalogAttributeEnrichment(
  product: ProductSnapshot,
  classification: Classification,
): CatalogAttributeEnrichment {
  const lines = sourceLines(product);
  const text = sourceText(product);
  const sourceAttributes = {
    ...extractSourceAttributes(lines),
    ...existingSourceAttributes(product),
  };
  const colors = unique([
    ...optionValues(product, ["Color", "Colour"]),
    ...variantGoogleValues(product, "color"),
  ]);
  const sizes = unique([
    ...optionValues(product, ["Size"]),
    ...variantGoogleValues(product, "size"),
  ]);
  const material =
    extractMaterial(lines) ??
    sourceAttributes.material_composition ??
    sourceAttributes.material ??
    sourceAttributes.metal ??
    variantGoogleValues(product, "material")[0] ??
    null;
  const explicitFabric =
    labeledValue(lines, ["Fabric", "Fabric content"]) ??
    sourceAttributes.fabric ??
    sourceAttributes.fabric_content ??
    null;
  const fabric =
    explicitFabric ??
    (classification.department === "Fashion" ? material : null);

  const explicitFit = labeledValue(lines, ["Fit", "Fit type"]);
  const fit = explicitFit ?? firstMapped(text, FIT_TERMS);

  const occasions = allMapped(text, OCCASIONS);
  const activities = allMapped(text, ACTIVITIES);
  if (
    classification.family === "Activewear" &&
    !activities.some((value) => value.toLowerCase() === "workout")
  ) {
    activities.unshift("Workout");
  }

  const explicitPattern = labeledValue(lines, ["Pattern", "Pattern type"]);
  const pattern = explicitPattern ?? firstMapped(text, PATTERNS);

  return {
    colors,
    sizes,
    material,
    fabric,
    fit,
    occasions,
    activities: unique(activities),
    targetGender: "Women",
    ageGroup: "Adult",
    sizeType: extractSizeType(text, classification, sizes),
    features: extractFeatures(product, lines),
    pattern,
    season: extractSeason(text),
    careInstructions: extractCare(lines),
    sourceAttributes,
    customProduct: /\b(?:personalized|custom[- ]made|made[- ]to[- ]order|made to order)\b/i.test(text),
  };
}

function field(
  namespace: string,
  key: string,
  type: string,
  value: string | null | undefined,
): CatalogMetafieldInput[] {
  const cleaned = String(value ?? "").trim();
  return cleaned ? [{ namespace, key, type, value: cleaned }] : [];
}

function listField(
  namespace: string,
  key: string,
  values: string[],
): CatalogMetafieldInput[] {
  const cleaned = unique(values);
  return cleaned.length
    ? [{ namespace, key, type: "list.single_line_text_field", value: JSON.stringify(cleaned) }]
    : [];
}

export function buildCatalogAttributeMetafields(
  enrichment: CatalogAttributeEnrichment,
  classification: Classification,
  brandWorld: string | null,
): CatalogMetafieldInput[] {
  const fields: CatalogMetafieldInput[] = [
    ...field("attributes", "color", "single_line_text_field", enrichment.colors.join(" / ")),
    ...listField("attributes", "sizes", enrichment.sizes),
    ...field("attributes", "material", "single_line_text_field", enrichment.material),
    ...field("attributes", "fabric", "single_line_text_field", enrichment.fabric),
    ...field("attributes", "fit", "single_line_text_field", enrichment.fit),
    ...field("attributes", "occasion", "single_line_text_field", enrichment.occasions.join(" / ")),
    ...listField("attributes", "activity", enrichment.activities),
    ...field("attributes", "target_gender", "single_line_text_field", enrichment.targetGender),
    ...field("attributes", "age_group", "single_line_text_field", enrichment.ageGroup),
    ...field("attributes", "size_type", "single_line_text_field", enrichment.sizeType),
    ...listField("attributes", "features", enrichment.features),
    ...field("attributes", "pattern", "single_line_text_field", enrichment.pattern),
    ...field("attributes", "season", "single_line_text_field", enrichment.season),
    ...field("content", "care_instructions", "multi_line_text_field", enrichment.careInstructions),
  ];

  if (Object.keys(enrichment.sourceAttributes).length) {
    fields.push({
      namespace: "attributes",
      key: "source_attributes",
      type: "json",
      value: JSON.stringify(enrichment.sourceAttributes),
    });
  }

  const googleEligible =
    classification.department === "Fashion" || classification.department === "Jewelry";

  fields.push({
    namespace: "mm-google-shopping",
    key: "custom_product",
    type: "boolean",
    value: enrichment.customProduct ? "true" : "false",
  });
  fields.push({
    namespace: "mm-google-shopping",
    key: "condition",
    type: "single_line_text_field",
    value: "new",
  });
  fields.push({
    namespace: "mm-google-shopping",
    key: "product_type",
    type: "single_line_text_field",
    value: classification.productType,
  });

  if (googleEligible) {
    fields.push(
      {
        namespace: "mm-google-shopping",
        key: "gender",
        type: "single_line_text_field",
        value: "female",
      },
      {
        namespace: "mm-google-shopping",
        key: "age_group",
        type: "single_line_text_field",
        value: "adult",
      },
    );
  }

  if (enrichment.material) {
    fields.push({
      namespace: "mm-google-shopping",
      key: "material",
      type: "single_line_text_field",
      value: enrichment.material,
    });
  }
  if (enrichment.pattern) {
    fields.push({
      namespace: "mm-google-shopping",
      key: "pattern",
      type: "single_line_text_field",
      value: enrichment.pattern,
    });
  }
  if (googleEligible && enrichment.sizeType) {
    fields.push({
      namespace: "mm-google-shopping",
      key: "size_type",
      type: "single_line_text_field",
      value: enrichment.sizeType,
    });
  }

  // Shopify already exposes Color/Size product options to sales channels. Only
  // add a product-level Google value when the product has exactly one value so
  // multi-variant products do not receive an incorrect aggregate attribute.
  if (enrichment.colors.length === 1) {
    fields.push({
      namespace: "mm-google-shopping",
      key: "color",
      type: "single_line_text_field",
      value: enrichment.colors[0],
    });
  }
  if (enrichment.sizes.length === 1) {
    fields.push({
      namespace: "mm-google-shopping",
      key: "size",
      type: "single_line_text_field",
      value: enrichment.sizes[0],
    });
  }

  fields.push(
    {
      namespace: "mm-google-shopping",
      key: "custom_label_0",
      type: "single_line_text_field",
      value: brandWorld ?? "needs_review",
    },
    {
      namespace: "mm-google-shopping",
      key: "custom_label_1",
      type: "single_line_text_field",
      value: classification.department,
    },
    {
      namespace: "mm-google-shopping",
      key: "custom_label_2",
      type: "single_line_text_field",
      value: classification.family,
    },
    {
      namespace: "mm-google-shopping",
      key: "custom_label_3",
      type: "single_line_text_field",
      value: classification.subcollection,
    },
  );

  return fields;
}
