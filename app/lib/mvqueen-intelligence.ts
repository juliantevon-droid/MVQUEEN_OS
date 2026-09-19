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
  [/\b(pendant|necklace)\b/i, {department:"Jewelry",family:"Necklaces",subcollection:"Pendant Necklaces",route:"pendants",productType:"Pendant Necklace"}],
  [/\b(earring|studs?)\b/i, {department:"Jewelry",family:"Earrings",subcollection:"Earrings",route:"earrings",productType:"Earrings"}],
  [/\b(bracelet|bangle)\b/i, {department:"Jewelry",family:"Bracelets",subcollection:"Bracelets",route:"bracelets",productType:"Bracelet"}],
  [/\b(ring)\b/i, {department:"Jewelry",family:"Rings",subcollection:"Rings",route:"rings",productType:"Ring"}],
  [/\b(dress|gown)\b/i, {department:"Fashion",family:"Dresses",subcollection:"Dresses",route:"dresses",productType:"Dress"}],
  [/\b(blouse|button[- ]?down|shirt)\b/i, {department:"Fashion",family:"Tops",subcollection:"Blouses",route:"blouses",productType:"Blouse"}],
  [/\b(t[- ]?shirt|tee)\b/i, {department:"Fashion",family:"Tops",subcollection:"T-Shirts",route:"t-shirts",productType:"T-Shirt"}],
  [/\b(skirt)\b/i, {department:"Fashion",family:"Bottoms",subcollection:"Skirts",route:"skirts",productType:"Skirt"}],
  [/\b(jean|denim)\b/i, {department:"Fashion",family:"Bottoms",subcollection:"Jeans & Denim",route:"jeans-denim",productType:"Jeans"}],
  [/\b(pant|trouser|legging)\b/i, {department:"Fashion",family:"Bottoms",subcollection:"Pants",route:"pants",productType:"Pants"}],
  [/\b(shorts?)\b/i, {department:"Fashion",family:"Bottoms",subcollection:"Shorts",route:"shorts",productType:"Shorts"}],
  [/\b(jumpsuit|romper)\b/i, {department:"Fashion",family:"Jumpsuits & Rompers",subcollection:"Jumpsuits & Rompers",route:"jumpsuits-rompers",productType:"Jumpsuit"}],
  [/\b(bodysuit)\b/i, {department:"Fashion",family:"Bodysuits",subcollection:"Bodysuits",route:"bodysuits",productType:"Bodysuit"}],
  [/\b(cosmetic|makeup|foundation|concealer|mascara|lipstick|eyeshadow)\b/i, {department:"Beauty",family:"Makeup",subcollection:"Makeup",route:"makeup",productType:"Makeup"}],
  [/\b(serum|moisturizer|cleanser|toner|sunscreen|mask|skincare)\b/i, {department:"Beauty",family:"Skincare",subcollection:"Skincare",route:"skincare",productType:"Skincare"}],
  [/\b(shampoo)\b/i, {department:"Beauty",family:"Hair Care",subcollection:"Shampoo",route:"shampoo",productType:"Shampoo"}],
  [/\b(conditioner)\b/i, {department:"Beauty",family:"Hair Care",subcollection:"Conditioner",route:"conditioner",productType:"Conditioner"}],
  [/\b(wig|extension)\b/i, {department:"Beauty",family:"Wigs & Extensions",subcollection:"Wigs & Extensions",route:"wigs-extensions",productType:"Wigs & Extensions"}],
  [/\b(hair tool|flat iron|curling iron|dryer|blow dryer)\b/i, {department:"Beauty",family:"Hair Tools",subcollection:"Hair Tools",route:"hair-tools",productType:"Hair Tool"}],
];

export function classifyProduct(title: string, description = ""): Classification {
  const text = `${title} ${description.replace(/<[^>]+>/g, " ")}`;
  const matches = ROUTES.filter(([pattern]) => pattern.test(text));
  if (!matches.length) {
    return {department:"Unclassified", family:"Unclassified", subcollection:"Needs Review", route:"needs-review", productType:"Needs Review", confidence:"review"};
  }
  const first = matches[0][1];
  return {...first, confidence: matches.length === 1 ? "high" : "medium"};
}

function cleanTitle(title: string) {
  return title
    .replace(/\b(ouhoe|miss\.?\s*queen|hoegoa|fanzhen|eelhope|color fit|west & month)\b/gi, "")
    .replace(/\b(p\.?\s*\d+|sdp\d+)\b/gi, "")
    .replace(/\s{2,}/g, " ")
    .replace(/^\s*[|,-]+|[|,-]+\s*$/g, "")
    .trim();
}

function plainText(html = "") {
  return html.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
}

function extractValue(text: string, patterns: RegExp[]): string | null {
  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match?.[1]) return match[1].trim();
  }
  return null;
}

export function extractAttributes(product: ProductSnapshot) {
  const text = plainText(`${product.title} ${product.descriptionHtml ?? ""}`);
  return {
    material: extractValue(text, [/\b(925\s+sterling\s+silver|sterling\s+silver|gold[- ]?plated|stainless steel|cotton|linen|silk|polyester|nylon|leather)\b/i]),
    color: extractValue(text, [/\b(black|white|pink|red|blue|green|brown|beige|cream|gold|silver|purple|yellow|orange|nude|multicolor)\b/i]),
    fit: extractValue(text, [/\b(slim fit|regular fit|relaxed fit|oversized|loose fit|bodycon|fitted)\b/i]),
    occasion: extractValue(text, [/\b(everyday|casual|formal|office|work|party|evening|vacation|wedding|bridal|active)\b/i]),
  };
}

export function generateCatalogPackage(product: ProductSnapshot) {
  const clean = cleanTitle(product.title);
  const c = classifyProduct(clean, product.descriptionHtml ?? "");
  const attributes = extractAttributes(product);
  const title = clean || product.title;
  const shortDescription = `A thoughtfully selected ${title.toLowerCase()}, curated for modern style and effortless everyday confidence.`;
  const source = plainText(product.descriptionHtml ?? "");
  const descriptionHtml = [
    "<p><strong>Made to be part of your own edit.</strong></p>",
    `<p>${shortDescription}</p>`,
    "<h3>The Details</h3>",
    `<ul><li><strong>Category:</strong> ${c.family}</li><li><strong>Collection:</strong> ${c.subcollection}</li>${attributes.material ? `<li><strong>Material:</strong> ${attributes.material}</li>` : ""}${attributes.color ? `<li><strong>Color:</strong> ${attributes.color}</li>` : ""}${attributes.fit ? `<li><strong>Fit:</strong> ${attributes.fit}</li>` : ""}${attributes.occasion ? `<li><strong>Occasion:</strong> ${attributes.occasion}</li>` : ""}</ul>`,
    source ? `<p><strong>Product information:</strong> ${source}</p>` : "",
  ].join("");
  const keywords = Array.from(new Set([title.toLowerCase(), c.family.toLowerCase(), c.subcollection.toLowerCase(), "women's style"]));
  const routeSlug = c.route;
  const routingTags = [
    "mvq:catalog",
    `mvq:collection:${routeSlug}`,
    `mvq:department:${c.department.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`,
    `mvq:family:${c.family.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`,
    ...(c.confidence === "review" ? ["mvq:needs-review"] : []),
  ];
  const existingOperationalTags = (product.tags ?? []).filter(t => !t.startsWith("mvq:"));
  return {
    title, c, attributes, shortDescription, descriptionHtml, keywords,
    seoTitle: `${title} | MVQueen`.slice(0, 70),
    seoDescription: `Shop ${title.toLowerCase()} from MVQueen, curated for modern feminine style and effortless everyday elegance.`.slice(0, 320),
    tags: Array.from(new Set([...existingOperationalTags, ...routingTags])),
  };
}
