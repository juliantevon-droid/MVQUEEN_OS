export type ProductSnapshot = {
  id: string;
  title: string;
  handle?: string | null;
  descriptionHtml?: string | null;
  productType?: string | null;
  vendor?: string | null;
  tags?: string[];
  seo?: { title?: string | null; description?: string | null } | null;
  category?: { id?: string | null; fullName?: string | null } | null;
  options?: { name: string; values: string[] }[];
  media?: {
    nodes?: { id: string; alt?: string | null }[];
  };
  variants?: {
    nodes?: {
      id: string;
      price?: string | null;
      compareAtPrice?: string | null;
      sku?: string | null;
      barcode?: string | null;
      selectedOptions?: { name: string; value: string }[];
      googleMetafields?: {
        nodes?: { key: string; value?: string | null; type?: string | null }[];
      };
      unitCost?: string | null;
      costCurrency?: string | null;
    }[];
  };
  commercialMetafields?: {
    nodes?: { key: string; value?: string | null; type?: string | null }[];
  };
  shippingMetafields?: {
    nodes?: { key: string; value?: string | null; type?: string | null }[];
  };
  attributeMetafields?: {
    nodes?: { key: string; value?: string | null; type?: string | null }[];
  };
};

export type Classification = {
  department: string;
  family: string;
  subcollection: string;
  route: string;
  productType: string;
  confidence: "high" | "medium" | "review";
};


export function usableProductType(value?: string | null): boolean {
  const normalized = String(value ?? "").trim().toLowerCase();
  if (!normalized) return false;
  return !new Set([
    "0", "1", "2", "3", "4", "5",
    "n/a", "na", "none", "null", "undefined", "unknown", "other", "product",
  ]).has(normalized);
}

const COMPOUND_ROUTES: Array<[RegExp, Omit<Classification, "confidence">]> = [
  [
    /\b(?:active(?:wear)?\s*set|workout\s*set|sports?\s*bra\b[\s\S]*\bshorts?\b|shorts?\b[\s\S]*\bsports?\s*bra\b)/i,
    {
      department: "Fashion",
      family: "Activewear",
      subcollection: "Activewear Sets",
      route: "activewear-sets",
      productType: "Activewear Set",
    },
  ],
  [
    /\b(?:body\s+(?:lotion|cream|moisturizer|scrub|wash|butter)|bath\s+(?:salt|soak|oil))\b/i,
    {
      department: "Beauty",
      family: "Bath & Body",
      subcollection: "Bath & Body",
      route: "bath-body",
      productType: "Bath & Body",
    },
  ],
  [
    /\b(?:hair\s+(?:oil|serum|mask|treatment)|scalp\s+(?:oil|serum|treatment))\b/i,
    {
      department: "Beauty",
      family: "Hair Care",
      subcollection: "Hair Treatments",
      route: "hair-treatments",
      productType: "Hair Treatment",
    },
  ],
  [
    /\b(?:lip\s+(?:balm|gloss|oil|tint|liner)|lipstick)\b/i,
    {
      department: "Beauty",
      family: "Makeup",
      subcollection: "Makeup",
      route: "makeup",
      productType: "Makeup",
    },
  ],
  [
    /\b(?:face|facial|eye)\s+(?:cream|moisturizer|serum|mask|cleanser)|\bfacial\s+skin\s+care\b/i,
    {
      department: "Beauty",
      family: "Skincare",
      subcollection: "Skincare",
      route: "skincare",
      productType: "Skincare",
    },
  ],
];

const TITLE_FIRST_ROUTES: Array<[RegExp, Omit<Classification, "confidence">]> = [
  [/\btoner\b/i, {department:"Beauty",family:"Skincare",subcollection:"Skincare",route:"skincare",productType:"Skincare"}],
  [/\bskin\s+care\s+oil\b/i, {department:"Beauty",family:"Skincare",subcollection:"Skincare",route:"skincare",productType:"Skincare"}],
  [/\byoga\s+(?:pants?|leggings?)\b/i, {department:"Fashion",family:"Bottoms",subcollection:"Pants",route:"pants",productType:"Pants"}],
  [/\banklet\b/i, {department:"Jewelry",family:"Anklets",subcollection:"Anklets",route:"anklets",productType:"Anklet"}],
  [/\bpress[- ]?on nails?\b|\bfake nails?\b|\bacrylic handmade nails?\b/i, {department:"Beauty",family:"Nails",subcollection:"Press-On Nails",route:"press-on-nails",productType:"Press-On Nails"}],
  [/\b(?:bb|cc)\s*cream\b/i, {department:"Beauty",family:"Makeup",subcollection:"Makeup",route:"makeup",productType:"Makeup"}],
  [/\b(?:hand|foot)\s*cream\b/i, {department:"Beauty",family:"Bath & Body",subcollection:"Hand & Body Care",route:"bath-body",productType:"Bath & Body"}],
  [/\bbody\s+(?:oil|treatment oil)\b/i, {department:"Beauty",family:"Bath & Body",subcollection:"Bath & Body",route:"bath-body",productType:"Bath & Body"}],
  [/\bbody\s+butter\b/i, {department:"Beauty",family:"Bath & Body",subcollection:"Bath & Body",route:"bath-body",productType:"Bath & Body"}],
  [/\b(?:beauty|skincare)\s+(?:box|boxes|set|kit)\b/i, {department:"Beauty",family:"Beauty Sets",subcollection:"Beauty Sets",route:"beauty-sets",productType:"Beauty Set"}],
  [/\bhair\s+mask\b/i, {department:"Beauty",family:"Hair Care",subcollection:"Hair Treatments",route:"hair-treatments",productType:"Hair Treatment"}],
  [/\b(?:hair remover|hair removal|lady shaver|waxing kit|wax kit)\b/i, {department:"Beauty",family:"Hair Removal",subcollection:"Hair Removal",route:"hair-removal",productType:"Hair Removal"}],
  [/\b(?:hair care solution|hair care essence|hair essence|hair care spray|hair spray)\b/i, {department:"Beauty",family:"Hair Care",subcollection:"Hair Treatments",route:"hair-treatments",productType:"Hair Treatment"}],
  [/\b(?:cupping massager|vacuum cupping|gua sha massager|massage cups?)\b/i, {department:"Beauty",family:"Beauty Tools",subcollection:"Beauty Tools",route:"beauty-tools",productType:"Beauty Tool"}],
  [/\b(?:massage cream|body care cream)\b/i, {department:"Beauty",family:"Bath & Body",subcollection:"Bath & Body",route:"bath-body",productType:"Bath & Body"}],
  [/\bskin\b[\s\S]{0,35}\b(?:cream|lotion)\b/i, {department:"Beauty",family:"Skincare",subcollection:"Skincare",route:"skincare",productType:"Skincare"}],
  [/\b(?:tightening|firming)\s+cream\b/i, {department:"Beauty",family:"Skincare",subcollection:"Skincare",route:"skincare",productType:"Skincare"}],
  [/\b(?:breast care|breast beauty|bust care|butt enhancer|hip enhancement)\b/i, {department:"Beauty",family:"Bath & Body",subcollection:"Body Care",route:"bath-body",productType:"Bath & Body"}],
  [/\b(?:hair|paddle|cushion)\s+(?:brush|comb)\b|\bwood comb\b/i, {department:"Beauty",family:"Hair Tools",subcollection:"Hair Tools",route:"hair-tools",productType:"Hair Tool"}],
  [/\b(?:jade|amethyst|facial)\s+(?:roller|massager)\b/i, {department:"Beauty",family:"Beauty Tools",subcollection:"Beauty Tools",route:"beauty-tools",productType:"Beauty Tool"}],
  [/\b(?:sportswear|tracksuit)\s+(?:set|suit)\b|\bhooded sportswear suit\b/i, {department:"Fashion",family:"Activewear",subcollection:"Activewear Sets",route:"activewear-sets",productType:"Activewear Set"}],
  [/\btop\b[\s\S]*\b(?:pants|skirt|shorts)\b[\s\S]*\b(?:set|suit)\b/i, {department:"Fashion",family:"Sets",subcollection:"Matching Sets",route:"matching-sets",productType:"Matching Set"}],
];

const ROUTES: Array<[RegExp, Omit<Classification, "confidence">]> = [
  [/\b(pendant)\b/i, {department:"Jewelry",family:"Necklaces",subcollection:"Pendant Necklaces",route:"pendants",productType:"Pendant Necklace"}],
  [/\b(necklace|chain)\b/i, {department:"Jewelry",family:"Necklaces",subcollection:"Necklaces",route:"necklaces",productType:"Necklace"}],
  [/\b(earring|studs?)\b/i, {department:"Jewelry",family:"Earrings",subcollection:"Earrings",route:"earrings",productType:"Earrings"}],
  [/\b(bracelet|bangle)\b/i, {department:"Jewelry",family:"Bracelets",subcollection:"Bracelets",route:"bracelets",productType:"Bracelet"}],
  [/\b(ring)\b/i, {department:"Jewelry",family:"Rings",subcollection:"Rings",route:"rings",productType:"Ring"}],
  [/\b(sunglasses|shades)\b/i, {department:"Fashion",family:"Fashion Accessories",subcollection:"Sunglasses",route:"sunglasses",productType:"Sunglasses"}],
  [/\b(handbag|hand bag|purse|tote|clutch)\b/i, {department:"Fashion",family:"Handbags & Purses",subcollection:"Handbags & Purses",route:"handbags-purses",productType:"Handbag"}],
  [/\b(dress|gown)\b/i, {department:"Fashion",family:"Dresses",subcollection:"Dresses",route:"dresses",productType:"Dress"}],
  [/\b(jumpsuit|romper)\b/i, {department:"Fashion",family:"Jumpsuits & Rompers",subcollection:"Jumpsuits & Rompers",route:"jumpsuits-rompers",productType:"Jumpsuit"}],
  [/\b(bodysuit)\b/i, {department:"Fashion",family:"Bodysuits",subcollection:"Bodysuits",route:"bodysuits",productType:"Bodysuit"}],
  [/\b(t[- ]?shirt|tee)\b/i, {department:"Fashion",family:"Tops",subcollection:"T-Shirts",route:"t-shirts",productType:"T-Shirt"}],
  [/\b(blouse|button[- ]?down)\b/i, {department:"Fashion",family:"Tops",subcollection:"Blouses",route:"blouses",productType:"Blouse"}],
  [/\b(jean|denim)\b/i, {department:"Fashion",family:"Bottoms",subcollection:"Jeans & Denim",route:"jeans-denim",productType:"Jeans"}],
  [/\b(legging|pant|trouser)\b/i, {department:"Fashion",family:"Bottoms",subcollection:"Pants",route:"pants",productType:"Pants"}],
  [/\b(shorts?)\b/i, {department:"Fashion",family:"Bottoms",subcollection:"Shorts",route:"shorts",productType:"Shorts"}],
  [/\b(skirt)\b/i, {department:"Fashion",family:"Bottoms",subcollection:"Skirts",route:"skirts",productType:"Skirt"}],
  [/\b(makeup|foundation|concealer|mascara|lipstick|lip\s*balm|lip\s*gloss|lip\s*oil|lip\s*tint|lip\s*liner|eyeshadow|blush|bronzer|highlighter)\b/i, {department:"Beauty",family:"Makeup",subcollection:"Makeup",route:"makeup",productType:"Makeup"}],
  [/\b(cleanser|toner|serum|moisturizer|sunscreen|spf|exfoliator|skincare|skin\s*care|face\s*mask|face\s*cream|facial\s*cream|eye\s*cream)\b/i, {department:"Beauty",family:"Skincare",subcollection:"Skincare",route:"skincare",productType:"Skincare"}],
  [/\b(shampoo)\b/i, {department:"Beauty",family:"Hair Care",subcollection:"Shampoo",route:"shampoo",productType:"Shampoo"}],
  [/\b(conditioner)\b/i, {department:"Beauty",family:"Hair Care",subcollection:"Conditioner",route:"conditioner",productType:"Conditioner"}],
  [/\b(hair oil|hair serum|scalp oil|hair treatment)\b/i, {department:"Beauty",family:"Hair Care",subcollection:"Hair Treatments",route:"hair-treatments",productType:"Hair Treatment"}],
  [/\b(wig|wigs|extension|extensions)\b/i, {department:"Beauty",family:"Wigs & Extensions",subcollection:"Wigs & Extensions",route:"wigs-extensions",productType:"Wigs & Extensions"}],
  [/\b(flat iron|curling iron|hair dryer|blow dryer|hot comb|hair tool)\b/i, {department:"Beauty",family:"Hair Tools",subcollection:"Hair Tools",route:"hair-tools",productType:"Hair Tool"}],
  [/\b(beauty tool|makeup brush|makeup sponge|tweezer|facial roller)\b/i, {department:"Beauty",family:"Beauty Tools",subcollection:"Beauty Tools",route:"beauty-tools",productType:"Beauty Tool"}],
  [/\b(body\s*wash|body\s*lotion|body\s*cream|body\s*moisturizer|body\s*scrub|body\s*butter|bath|body\s*care)\b/i, {department:"Beauty",family:"Bath & Body",subcollection:"Bath & Body",route:"bath-body",productType:"Bath & Body"}],
  [/\b(fragrance|perfume|parfum|body mist)\b/i, {department:"Beauty",family:"Fragrance",subcollection:"Fragrance",route:"fragrance",productType:"Fragrance"}],
];

export function classifyProduct(title: string, description = "", productType = ""): Classification {
  const review = (): Classification => ({
    department: "Unclassified",
    family: "Unclassified",
    subcollection: "Needs Review",
    route: "needs-review",
    productType: "Needs Review",
    confidence: "review",
  });

  const classifyText = (
    text: string,
    existingType = "",
  ): Classification | null => {
    const clean = String(text ?? "").replace(/<[^>]+>/g, " ").trim();
    if (!clean) return null;

    const titleFirst = TITLE_FIRST_ROUTES.find(([pattern]) => pattern.test(clean));
    if (titleFirst) return { ...titleFirst[1], confidence: "high" };

    const compound = COMPOUND_ROUTES.find(([pattern]) => pattern.test(clean));
    if (compound) return { ...compound[1], confidence: "high" };

    const matches = ROUTES.filter(([pattern]) => pattern.test(clean));
    if (!matches.length) return null;

    const uniqueRoutes = Array.from(new Set(matches.map(([, route]) => route.route)));
    if (uniqueRoutes.length === 1) return { ...matches[0][1], confidence: "high" };

    const normalizedProductType = usableProductType(existingType)
      ? existingType.trim().toLowerCase()
      : "";
    const exactProductTypeMatch = normalizedProductType
      ? matches.find(([, route]) => route.productType.toLowerCase() === normalizedProductType)
      : undefined;
    if (exactProductTypeMatch) {
      return { ...exactProductTypeMatch[1], confidence: "high" };
    }

    const sameFamily = matches.every(
      ([, route]) =>
        route.department === matches[0][1].department &&
        route.family === matches[0][1].family,
    );
    if (sameFamily) return { ...matches[0][1], confidence: "high" };

    return review();
  };

  // Title is the strongest merchandising signal. A stale or supplier placeholder
  // product type must never override a clear current title.
  const fromTitle = classifyText(title, productType);
  if (fromTitle) return fromTitle;

  // Description is second because it can contain useful factual category terms,
  // but also supplier boilerplate that should not overpower a clear title.
  const fromDescription = classifyText(description, productType);
  if (fromDescription) return fromDescription;

  // Existing productType is only a final fallback and only if it is meaningful.
  if (usableProductType(productType)) {
    const fromType = classifyText(productType, productType);
    if (fromType) return fromType;
  }

  return review();
}


export function productTypeForWrite(
  existingProductType: string | null | undefined,
  classification: Classification,
): string {
  if (classification.confidence !== "review") {
    return classification.productType;
  }
  return usableProductType(existingProductType)
    ? String(existingProductType).trim()
    : classification.productType;
}


export type BrandWorld = "mvqueen" | "miss-princess";

export type BrandRouting = {
  brand: BrandWorld | null;
  confidence: "high" | "medium" | "review";
  tone: "bold-authoritative" | "vivid-youthful" | "review";
  reason: string;
};

const MVQUEEN_AUTHORITY_COLORS = new Set([
  "black", "charcoal", "gold", "rich-gold", "deep-gold", "metallic-gold",
  "burgundy", "wine", "oxblood", "espresso", "chocolate", "deep-brown",
  "navy", "midnight-blue", "royal-blue", "emerald", "forest-green",
  "deep-green", "plum", "aubergine", "royal-purple",
  "mustard",
  "silver", "bronze", "champagne",
]);

const MVQUEEN_LUXE_NEUTRALS = new Set([
  "white", "ivory", "cream", "beige", "nude", "tan", "camel",
  "brown", "taupe", "khaki", "gray", "grey", "olive",
]);

const MISS_PRINCESS_VIVID_COLORS = new Set([
  "sky-blue", "baby-blue", "powder-blue", "electric-blue",
  "aqua", "turquoise", "mint", "seafoam",
  "lavender", "lilac", "periwinkle",
  "pink", "baby-pink", "blush", "soft-pink", "light-pink", "bubblegum-pink",
  "fuchsia", "magenta", "hot-pink", "bold-pink",
  "yellow", "sun-yellow", "sunflower-yellow", "golden-yellow",
  "coral", "peach", "lime", "lemon", "pastel-yellow", "light-yellow",
  "blue", "orange", "tangerine", "bright-orange", "rainbow", "multicolor", "pastel",
]);

// Bright/colorful base colors route to Miss.Princess by default. Deep,
// neutral, metallic, and explicitly refined shades remain MVQueen signals.
const SHARED_BASE_COLORS = new Set<string>();

const MVQUEEN_STYLE_HINTS = [
  "bold", "rich", "deep", "saturated", "authority", "authoritative",
  "luxury", "luxe", "elegant", "refined", "dramatic", "sleek", "tailored",
  "minimal", "structured", "classic", "polished", "statement", "jewel-tone",
  "jewel toned", "metallic",
];

const PRINCESS_STYLE_HINTS = [
  "bright", "vivid", "high-light", "high light", "light-intensity",
  "spring", "summer", "energetic", "energy", "youthful", "playful",
  "fresh", "airy", "soft", "sweet", "cute", "pastel", "colorful",
  "romantic", "fun", "floral", "sparkle",
];

// Refined metallic jewelry materials are an MVQueen tie-breaker when a
// product has no stronger vivid/playful palette signal. This keeps neutral
// luxury jewelry out of manual review without stealing colorful pieces from
// Miss.Princess.
const MVQUEEN_JEWELRY_MATERIAL_HINTS: Array<[RegExp, string]> = [
  [/\bgold[- ]plated\b/i, "gold-plated"],
  [/\bgold[- ]filled\b/i, "gold-filled"],
  [/\b(?:9|10|14|18|22|24)k\s+gold\b/i, "gold"],
  [/\bsterling\s+silver\b/i, "sterling-silver"],
  [/\bstainless\s+steel\b/i, "stainless-steel"],
  [/\brhodium[- ]plated\b/i, "rhodium-plated"],
  [/\bplatinum\b/i, "platinum"],
];

function normalizeColor(value: string): string {
  return value
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

function normalizedColorSignals(
  tags: string[] = [],
  title = "",
  options: ProductSnapshot["options"] = [],
): string[] {
  const fromTags = tags
    .filter((tag) => tag.toLowerCase().startsWith("mvq:color:"))
    .map((tag) => normalizeColor(tag.replace(/^mvq:color:/i, "")))
    .filter(Boolean);

  const fromOptions = (options ?? [])
    .filter((option) => option.name.trim().toLowerCase() === "color")
    .flatMap((option) => option.values ?? [])
    .map(normalizeColor)
    .filter(Boolean);

  const phraseSignals = [
    "bold pink", "hot pink", "baby pink", "soft pink", "light pink",
    "sun yellow", "sunflower yellow", "golden yellow", "pastel yellow", "light yellow",
    "sky blue", "baby blue", "powder blue", "electric blue", "midnight blue", "royal blue",
    "rich gold", "deep gold", "metallic gold", "deep brown", "forest green",
    "deep green", "royal purple", "bright orange",
  ]
    .filter((phrase) => title.toLowerCase().includes(phrase))
    .map(normalizeColor);

  const titleTokens = title
    .toLowerCase()
    .replace(/[^a-z0-9 -]+/g, " ")
    .split(/\s+/)
    .map(normalizeColor)
    .filter(Boolean);

  return Array.from(new Set([...fromOptions, ...fromTags, ...phraseSignals, ...titleTokens]));
}

function paletteScores(signals: string[], text: string) {
  let mvqueen = 0;
  let princess = 0;
  const mvqueenReasons: string[] = [];
  const princessReasons: string[] = [];

  for (const signal of signals) {
    if (MVQUEEN_AUTHORITY_COLORS.has(signal)) {
      mvqueen += 3;
      mvqueenReasons.push(`color:${signal}`);
      continue;
    }
    if (MVQUEEN_LUXE_NEUTRALS.has(signal)) {
      mvqueen += 2;
      mvqueenReasons.push(`color:${signal}`);
      continue;
    }
    if (MISS_PRINCESS_VIVID_COLORS.has(signal)) {
      princess += 3;
      princessReasons.push(`color:${signal}`);
      continue;
    }
    if (SHARED_BASE_COLORS.has(signal)) {
      // Shared base colors need a shade, companion color, or style context.
      continue;
    }
  }

  const mvqueenStyle = MVQUEEN_STYLE_HINTS.find((hint) => text.includes(hint));
  const princessStyle = PRINCESS_STYLE_HINTS.find((hint) => text.includes(hint));

  if (mvqueenStyle) {
    mvqueen += 1;
    mvqueenReasons.push(`style:${mvqueenStyle}`);
  }
  if (princessStyle) {
    princess += 1;
    princessReasons.push(`style:${princessStyle}`);
  }

  const jewelryMaterial = MVQUEEN_JEWELRY_MATERIAL_HINTS.find(([pattern]) =>
    pattern.test(text),
  );
  if (jewelryMaterial) {
    mvqueen += 2;
    mvqueenReasons.push(`material:${jewelryMaterial[1]}`);
  }

  return { mvqueen, princess, mvqueenReasons, princessReasons };
}

export function classifyBrandWorld(
  product: Pick<
    ProductSnapshot,
    "title" | "tags" | "descriptionHtml" | "options" | "variants"
  >,
): BrandRouting {
  const variantColors = (product.variants?.nodes ?? [])
    .map(
      (variant) =>
        variant.googleMetafields?.nodes?.find((item) => item.key === "color")?.value ??
        "",
    )
    .filter(Boolean);
  const signals = normalizedColorSignals(
    product.tags ?? [],
    product.title ?? "",
    [
      ...(product.options ?? []),
      ...(variantColors.length
        ? [{ name: "Color", values: variantColors }]
        : []),
    ],
  );
  const variantMaterials = (product.variants?.nodes ?? [])
    .map(
      (variant) =>
        variant.googleMetafields?.nodes?.find((item) => item.key === "material")?.value ??
        "",
    )
    .filter(Boolean);
  const text = [
    product.title ?? "",
    product.descriptionHtml?.replace(/<[^>]+>/g, " ") ?? "",
    ...(product.tags ?? []),
    ...(product.options ?? []).flatMap((option) => option.values ?? []),
    ...variantColors,
    ...variantMaterials,
  ].join(" ").toLowerCase();

  const scores = paletteScores(signals, text);

  if (scores.mvqueen > scores.princess) {
    const confidence = scores.mvqueen - scores.princess >= 2 ? "high" : "medium";
    return {
      brand: "mvqueen",
      confidence,
      tone: "bold-authoritative",
      reason: scores.mvqueenReasons[0] ?? "palette:deep-saturated-authority",
    };
  }

  if (scores.princess > scores.mvqueen) {
    const confidence = scores.princess - scores.mvqueen >= 2 ? "high" : "medium";
    return {
      brand: "miss-princess",
      confidence,
      tone: "vivid-youthful",
      reason: scores.princessReasons[0] ?? "palette:vivid-high-light-youthful",
    };
  }

  // MVQueen is the primary store brand. When a product has no decisive
  // Miss.Princess palette/style signal, route it to MVQueen rather than
  // freezing otherwise-safe automation. Keep medium confidence and an
  // explicit reason so the fallback remains auditable.
  return {
    brand: "mvqueen",
    confidence: "medium",
    tone: "bold-authoritative",
    reason: scores.mvqueen || scores.princess
      ? "balanced-signals-primary-brand-fallback"
      : "default-primary-brand",
  };
}

export function brandRoutingTags(route: BrandRouting): string[] {
  if (!route.brand) return ["mvq:brand:needs-review"];
  return [
    `mvq:brand:${route.brand}`,
    `mvq:tone:${route.tone}`,
  ];
}
