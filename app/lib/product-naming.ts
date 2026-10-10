import type { BrandVocabulary, ProductNamingProfile } from "./brand-vocabulary.server";
import { matchingCuratedName, normalizeProductName, type NamingRegister } from "./curated-product-names";
import type { Classification, ProductSnapshot } from "./mvqueen-intelligence";

export type ProductNamingDecision = {
  title: string;
  identity: string;
  register: NamingRegister;
  opening?: string;
  curated: boolean;
};

function identities(profile: ProductNamingProfile): string[] {
  return [...profile.evocative.fragrance, ...profile.evocative.general,
    ...profile["descriptive-poetic"], ...profile["identity-led"]];
}

// Recognize the writer's own formats before adding a new name. Hyphens in
// source silhouettes remain intact; only the explicit editorial dash separates
// a descriptive-poetic name from its source-backed product identity.
export function stripNamingDecoration(value: string, vocabulary: BrandVocabulary): string {
  const pool = Object.values(vocabulary.naming).flatMap(identities).sort((a, b) => b.length - a.length);
  const normalized = value.toLowerCase();
  for (const identity of pool) {
    const phrase = identity.toLowerCase();
    if (normalized.startsWith(phrase + " ")) return value.slice(identity.length).trim();
    if (normalized.endsWith(" — " + phrase)) return value.slice(0, -(identity.length + 3)).trim();
  }
  return value;
}

function seedFor(product: ProductSnapshot): number {
  let seed = 2166136261;
  for (const char of product.id || product.handle || product.title) seed = Math.imul(seed ^ char.charCodeAt(0), 16777619);
  return seed >>> 0;
}

function shorten(value: string, limit: number, noun: string): string {
  if (value.length <= limit) return value;
  const escaped = noun.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const withoutNoun = noun ? value.replace(new RegExp(`\\b${escaped}\\b`, "gi"), " ").replace(/\s+/g, " ").trim() : value;
  const ending = noun ? " " + noun : "";
  const words = withoutNoun.split(" ");
  while (words.length && words.join(" ").length + ending.length > limit) words.pop();
  while (/^(?:and|or|for|with|of|to|in|the|a|an)$/i.test(words.at(-1) ?? "")) words.pop();
  return (words.join(" ") + ending).trim();
}

export function buildProductName(
  product: ProductSnapshot,
  classification: Classification,
  factualName: string,
  brand: "mvqueen" | "miss-princess",
  vocabulary: BrandVocabulary,
  attempt = 0,
): ProductNamingDecision {
  const authored = matchingCuratedName(product.id, product.title) ?? matchingCuratedName(product.id, factualName);
  if (authored?.brand === brand) return {
    title: authored.title, identity: authored.title, register: authored.register,
    opening: authored.opening, curated: true,
  };

  const profile = vocabulary.naming[brand];
  const seed = seedFor(product);
  const register: NamingRegister = classification.productType === "Fragrance" ? "evocative"
    : (["evocative", "descriptive-poetic", "identity-led"] as const)[(seed + attempt) % 3];
  const pool = register === "evocative"
    ? profile.evocative[classification.productType === "Fragrance" ? "fragrance" : "general"]
    : profile[register];
  const identity = pool[((seed >>> 7) + attempt) % pool.length];
  const base = stripNamingDecoration(factualName, vocabulary);
  const noun = base.match(/\b(?:makeup brush(?:es)?|vanity mirror|makeup mirror|lip serum|hair straightener|facial roller|gua sha stone|body (?:moisturizer|scrub|cream|lotion|wash|oil|butter)|hair (?:oil|mask|serum|dryer|brush)|lip (?:balm|gloss|oil|liner)|waxing kit|face cream|facial cream|press[- ]on nails?|necklace|bracelet|earrings?|anklet|ring|dress|bodysuit|jumpsuit|romper|blouse|shorts|pants|skirt|shampoo|conditioner|foundation|concealer|mascara|lipstick|eyeliner|perfume|fragrance|serum|cream|comb|massager|tweezers?)\b/i)?.[0] ?? "";
  const subject = shorten(base, vocabulary.contentPolicy.limits.title - identity.length - (register === "descriptive-poetic" ? 3 : 1), noun);
  const title = register === "descriptive-poetic" ? `${subject} — ${identity}` : `${identity} ${subject}`;
  return { title, identity, register, curated: false };
}

export function usesNamingIdentity(title: string, identity: string): boolean {
  const normalized = " " + normalizeProductName(title) + " ";
  return normalized.includes(" " + normalizeProductName(identity) + " ");
}
