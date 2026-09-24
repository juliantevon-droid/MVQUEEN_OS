export type ProductSnapshot = {
  id: string;
  title: string;
  descriptionHtml?: string | null;
  productType?: string | null;
  vendor?: string | null;
  tags?: string[];
  media?: { id: string; alt?: string | null }[];
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

  const first = matches[0][1];
  return {...first, confidence:"high"};
}


export type CatalogPackage = {
  title: string;
  descriptionHtml: string;
  shortDescription: string;
  seoTitle: string;
  seoDescription: string;
  keywords: string[];
  tags: string[];
  c: Classification;
  attributes: {
    material: string | null;
    color: string | null;
    fit: string | null;
    occasion: string | null;
  };
};

const SUPPLIER_TERMS = /\b(OUHOE|MISS\.?\s*QUEEN|HOEGOA|FANZHEN|EELHOPE|COLOR\s*FIT|WEST\s*&\s*MONTH)\b/gi;

function plainText(value = ""): string {
  return value.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
}

function safeTitle(value: string): string {
  const cleaned = value.replace(SUPPLIER_TERMS, "").replace(/\s+/g, " ").replace(/^[-–—|,:\s]+|[-–—|,:\s]+$/g, "").trim();
  return cleaned || value.trim() || "MVQueen Edit";
}

function clip(value: string, limit: number): string {
  const clean = value.replace(/\s+/g, " ").trim();
  if (clean.length <= limit) return clean;
  return clean.slice(0, Math.max(0, limit - 1)).trimEnd() + "…";
}

function escapeHtml(value: string): string {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function findAttribute(text: string, values: string[]): string | null {
  const lower = text.toLowerCase();
  return values.find((value) => lower.includes(value.toLowerCase())) ?? null;
}

function slug(value: string): string {
  return value
    .toLowerCase()
    .replace(/&/g, "and")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

export function generateCatalogPackage(product: ProductSnapshot): CatalogPackage {
  const title = safeTitle(product.title ?? "");
  const existingDescriptionHtml = product.descriptionHtml?.trim() ?? "";
  const sourceText = plainText(`${title} ${existingDescriptionHtml} ${product.productType ?? ""}`);
  const c = classifyProduct(title, existingDescriptionHtml, product.productType ?? "");

  const material = findAttribute(sourceText, [
    "sterling silver", "gold filled", "gold plated", "stainless steel", "gold", "silver",
    "satin", "silk", "cotton", "denim", "leather", "lace", "mesh", "knit",
  ]);
  const color = findAttribute(sourceText, [
    "black", "white", "ivory", "cream", "pink", "red", "burgundy", "purple", "lilac",
    "blue", "navy", "green", "brown", "beige", "gold", "silver",
  ]);
  const fit = findAttribute(sourceText, [
    "bodycon", "oversized", "relaxed", "tailored", "slim fit", "wide leg", "straight leg",
  ]);
  const occasion = findAttribute(sourceText, [
    "evening", "date night", "work", "office", "wedding", "party", "vacation", "everyday",
  ]);

  const fallbackSentence = `${title} from the MVQueen edit.`;
  const sourceDescription = plainText(existingDescriptionHtml);
  const shortDescription = clip(sourceDescription || fallbackSentence, 155);
  const descriptionHtml = existingDescriptionHtml || `<p>${escapeHtml(fallbackSentence)}</p>`;

  const seoTitle = clip(`${title} | MVQueen`, 60);
  const seoDescription = clip(sourceDescription || fallbackSentence, 155);

  const tags = [
    "mvq:catalog",
    `mvq:department:${slug(c.department)}`,
    `mvq:family:${slug(c.family)}`,
    `mvq:collection:${slug(c.route)}`,
    ...(c.confidence === "review" ? ["mvq:needs-review"] : []),
  ];

  const keywords = Array.from(new Set([
    title.toLowerCase(),
    c.productType.toLowerCase(),
    c.family.toLowerCase(),
    c.department.toLowerCase(),
  ].filter((value) => value && value !== "unclassified" && value !== "needs review")));

  return {
    title,
    descriptionHtml,
    shortDescription,
    seoTitle,
    seoDescription,
    keywords,
    tags,
    c,
    attributes: { material, color, fit, occasion },
  };
}
