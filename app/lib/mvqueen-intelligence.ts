export type ProductSnapshot = {
  id: string;
  title: string;
  handle?: string | null;
  descriptionHtml?: string | null;
  productType?: string | null;
  vendor?: string | null;
  tags?: string[];
  media?: {
    nodes?: { id: string; alt?: string | null }[];
  };
  variants?: {
    nodes?: {
      id: string;
      price?: string | null;
      compareAtPrice?: string | null;
      unitCost?: string | null;
      costCurrency?: string | null;
    }[];
  };
  commercialMetafields?: {
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
  [/\b(makeup|foundation|concealer|mascara|lipstick|eyeshadow|blush|bronzer|highlighter)\b/i, {department:"Beauty",family:"Makeup",subcollection:"Makeup",route:"makeup",productType:"Makeup"}],
  [/\b(cleanser|toner|serum|moisturizer|sunscreen|spf|exfoliator|skincare|face mask)\b/i, {department:"Beauty",family:"Skincare",subcollection:"Skincare",route:"skincare",productType:"Skincare"}],
  [/\b(shampoo)\b/i, {department:"Beauty",family:"Hair Care",subcollection:"Shampoo",route:"shampoo",productType:"Shampoo"}],
  [/\b(conditioner)\b/i, {department:"Beauty",family:"Hair Care",subcollection:"Conditioner",route:"conditioner",productType:"Conditioner"}],
  [/\b(hair oil|hair serum|scalp oil|hair treatment)\b/i, {department:"Beauty",family:"Hair Care",subcollection:"Hair Treatments",route:"hair-treatments",productType:"Hair Treatment"}],
  [/\b(wig|wigs|extension|extensions)\b/i, {department:"Beauty",family:"Wigs & Extensions",subcollection:"Wigs & Extensions",route:"wigs-extensions",productType:"Wigs & Extensions"}],
  [/\b(flat iron|curling iron|hair dryer|blow dryer|hot comb|hair tool)\b/i, {department:"Beauty",family:"Hair Tools",subcollection:"Hair Tools",route:"hair-tools",productType:"Hair Tool"}],
  [/\b(beauty tool|makeup brush|makeup sponge|tweezer|facial roller)\b/i, {department:"Beauty",family:"Beauty Tools",subcollection:"Beauty Tools",route:"beauty-tools",productType:"Beauty Tool"}],
  [/\b(body wash|body lotion|body scrub|bath|body care)\b/i, {department:"Beauty",family:"Bath & Body",subcollection:"Bath & Body",route:"bath-body",productType:"Bath & Body"}],
  [/\b(fragrance|perfume|parfum|body mist)\b/i, {department:"Beauty",family:"Fragrance",subcollection:"Fragrance",route:"fragrance",productType:"Fragrance"}],
];

export function classifyProduct(title: string, description = "", productType = ""): Classification {
  const text = `${title} ${productType} ${description.replace(/<[^>]+>/g, " ")}`;
  const matches = ROUTES.filter(([pattern]) => pattern.test(text));

  if (!matches.length) {
    return {department:"Unclassified", family:"Unclassified", subcollection:"Needs Review", route:"needs-review", productType:"Needs Review", confidence:"review"};
  }

  const uniqueRoutes = Array.from(new Set(matches.map(([, route]) => route.route)));
  if (uniqueRoutes.length > 1) {
    return {department:"Unclassified", family:"Unclassified", subcollection:"Needs Review", route:"needs-review", productType:"Needs Review", confidence:"review"};
  }

  return {...matches[0][1], confidence:"high"};
}


export type BrandWorld = "mvqueen" | "miss-princess";

export type BrandRouting = {
  brand: BrandWorld | null;
  confidence: "high" | "medium" | "review";
  tone: "neutral-mature" | "soft-playful" | "review";
  reason: string;
};

const MISS_PRINCESS_COLORS = new Set([
  "pink", "blush", "rose", "baby-pink", "hot-pink", "coral", "peach",
  "lavender", "lilac", "mint", "aqua", "turquoise", "sky-blue",
  "yellow", "lemon", "orange", "lime", "rainbow", "multicolor", "pastel",
]);

const MVQUEEN_COLORS = new Set([
  "black", "white", "ivory", "cream", "beige", "nude", "tan", "camel",
  "brown", "taupe", "khaki", "gray", "grey", "charcoal", "navy",
  "burgundy", "wine", "olive", "gold", "silver", "bronze", "champagne",
]);

const PRINCESS_STYLE_HINTS = [
  "playful", "soft", "sweet", "romantic", "cute", "pastel", "bright",
  "colorful", "youthful", "fun", "floral", "sparkle",
];

const MVQUEEN_STYLE_HINTS = [
  "luxury", "elegant", "refined", "bold", "mature", "sleek", "tailored",
  "minimal", "structured", "classic", "polished", "statement",
];

function normalizedColorSignals(tags: string[] = [], title = ""): string[] {
  const fromTags = tags
    .filter((tag) => tag.toLowerCase().startsWith("mvq:color:"))
    .map((tag) => tag.toLowerCase().replace("mvq:color:", "").trim())
    .filter(Boolean);

  const titleTokens = title
    .toLowerCase()
    .replace(/[^a-z0-9 -]+/g, " ")
    .split(/\s+/)
    .filter(Boolean);

  return Array.from(new Set([...fromTags, ...titleTokens]));
}

export function classifyBrandWorld(product: Pick<ProductSnapshot, "title" | "tags" | "descriptionHtml">): BrandRouting {
  const signals = normalizedColorSignals(product.tags ?? [], product.title ?? "");
  const text = [
    product.title ?? "",
    product.descriptionHtml?.replace(/<[^>]+>/g, " ") ?? "",
    ...(product.tags ?? []),
  ].join(" ").toLowerCase();

  const princessColors = signals.filter((signal) => MISS_PRINCESS_COLORS.has(signal));
  if (princessColors.length) {
    return {
      brand: "miss-princess",
      confidence: "high",
      tone: "soft-playful",
      reason: `color:${princessColors[0]}`,
    };
  }

  const mvqueenColors = signals.filter((signal) => MVQUEEN_COLORS.has(signal));
  if (mvqueenColors.length) {
    return {
      brand: "mvqueen",
      confidence: "high",
      tone: "neutral-mature",
      reason: `color:${mvqueenColors[0]}`,
    };
  }

  const princessStyle = PRINCESS_STYLE_HINTS.find((hint) => text.includes(hint));
  const mvqueenStyle = MVQUEEN_STYLE_HINTS.find((hint) => text.includes(hint));

  if (princessStyle && !mvqueenStyle) {
    return {
      brand: "miss-princess",
      confidence: "medium",
      tone: "soft-playful",
      reason: `style:${princessStyle}`,
    };
  }

  if (mvqueenStyle && !princessStyle) {
    return {
      brand: "mvqueen",
      confidence: "medium",
      tone: "neutral-mature",
      reason: `style:${mvqueenStyle}`,
    };
  }

  return {
    brand: null,
    confidence: "review",
    tone: "review",
    reason: "ambiguous-color-or-style",
  };
}

export function brandRoutingTags(route: BrandRouting): string[] {
  if (!route.brand) return ["mvq:brand:needs-review"];
  return [
    `mvq:brand:${route.brand}`,
    `mvq:tone:${route.tone}`,
  ];
}
