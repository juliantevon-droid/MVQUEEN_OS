import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

// These remain the editable source of truth. Both production images carry the
// same files; a vocabulary change changes the worker's automation version.
export const BRAND_VOCABULARY_SOURCES = [
  "06_Tone_And_Voice/Brand_Vocabulary_Banks.md",
  "06_Tone_And_Voice/Product_Description_Voice.md",
  "06_Tone_And_Voice/Forbidden_Words.md",
  "15_Scripts_And_Code/mvqueen_engine/brand_banks.py",
  "06_Tone_And_Voice/Product_Naming_Palette.json",
  "app/lib/curated-product-names.ts",
  "06_Tone_And_Voice/Brand_Content_Policy.json",
] as const;

export const PRODUCT_EDITORIAL_CATEGORIES = [
  "fashion", "jewelry", "skincare", "beauty", "fragrance", "haircare", "home", "tools", "general",
] as const;
export type ProductEditorialCategory = typeof PRODUCT_EDITORIAL_CATEGORIES[number];
export type BrandKey = "mvqueen" | "miss-princess";
export type BrandContentPolicy = {
  schemaVersion: 1;
  profiles: Record<BrandKey, {
    displayName: string;
    voice: string[];
    additionalAdjectives: string[];
    hooks: Record<ProductEditorialCategory, string[]>;
  }>;
  additionalForbidden: string[];
  limits: { shortDescription: number; title: number; seoTitle: number; metaDescription: number };
};

export type ProductNamingProfile = {
  evocative: { fragrance: string[]; general: string[] };
  "descriptive-poetic": string[];
  "identity-led": string[];
};

export type BrandVocabulary = {
  version: string;
  sources: readonly string[];
  forbidden: string[];
  profiles: Record<"mvqueen" | "miss-princess", { adjectives: string[] }>;
  naming: Record<"mvqueen" | "miss-princess", ProductNamingProfile>;
  contentPolicy: BrandContentPolicy;
};

// Lexical permission is separate from product evidence. Material, manufacture,
// texture and efficacy words in the larger banks cannot become random facts.
const EDITORIAL_ADJECTIVES = new Set([
  "refined", "polished", "elegant", "elevated", "intentional", "timeless",
  "understated", "curated", "distinctive", "modern", "considered", "composed",
  "deliberate", "restrained", "harmonious", "effortless", "precise", "playful",
  "chic", "lighthearted", "fresh", "fun", "clean", "easy", "sweet", "youthful",
]);

function words(value: string): string[] {
  return value.split(/,|\s+\/\s+/).map((word) => word.trim().toLowerCase()).filter(Boolean);
}

function unique(values: string[]): string[] {
  return [...new Set(values)];
}

function personaAdjectives(source: string, persona: string): string[] {
  const block = source.match(new RegExp(`"${persona}":\\s*\\{([\\s\\S]*?)\\n\\s*\\}`))?.[1];
  const list = block?.match(/"adjectives":\s*\[([\s\S]*?)\]/)?.[1];
  if (!list) throw new Error(`Missing canonical vocabulary persona: ${persona}`);
  const literals = list.match(/"(?:\\.|[^"\\])*"/g) ?? [];
  if (list.replace(/"(?:\\.|[^"\\])*"/g, "").replace(/[\s,]/g, "")) {
    throw new Error(`Unsupported vocabulary data in persona: ${persona}`);
  }
  return literals.map((literal) => String(JSON.parse(literal)).toLowerCase());
}

function forbiddenTerms(source: string): string[] {
  const section = source.split("## Tier 1", 2)[1]?.split("## Tier 2", 1)[0];
  if (!section) throw new Error("Canonical Tier 1 forbidden-language section is missing");
  return unique(section.split("\n").flatMap((line) => {
    if (!line.trim().startsWith("|")) return [];
    const phrase = line.split("|")[1]?.trim().replace(/\s*\([^)]*\)\s*$/, "") ?? "";
    if (!phrase || phrase === "Word / Phrase" || /^[-:]+$/.test(phrase)) return [];
    return phrase.split(/\s+\/\s+/).map((word) => word.trim());
  }));
}

function stringPool(value: unknown, field: string): string[] {
  if (!Array.isArray(value) || !value.length || value.some((item) => typeof item !== "string" || !item.trim())) {
    throw new Error(`Invalid brand content policy: ${field}`);
  }
  return unique(value.map((item: string) => item.trim()));
}

function contentPolicy(source: string): BrandContentPolicy {
  const policy = JSON.parse(source) as BrandContentPolicy;
  if (policy.schemaVersion !== 1) throw new Error("Unsupported brand content policy schema");
  for (const brand of ["mvqueen", "miss-princess"] as const) {
    const profile = policy.profiles?.[brand];
    const label = brand === "mvqueen" ? "MVQUEEN" : "Miss.Princess";
    if (profile?.displayName !== label) throw new Error(`Invalid canonical brand label: ${brand}`);
    profile.voice = stringPool(profile.voice, `${brand}.voice`);
    profile.additionalAdjectives = stringPool(profile.additionalAdjectives, `${brand}.additionalAdjectives`);
    for (const category of PRODUCT_EDITORIAL_CATEGORIES) {
      const hooks = stringPool(profile.hooks?.[category], `${brand}.hooks.${category}`);
      for (const hook of hooks) {
        if (/\{(?!brand\}|adjective\}|article\}|articleCapital\})/.test(hook)
          || /[{}]/.test(hook.replace(/\{(?:brand|adjective|article|articleCapital)\}/g, ""))
          || !hook.includes("{adjective}") || !hook.includes("{brand}") || hook.length > 120
          || /\b(?:clinically?|medical|dermatolog\w*|cures?|heals?|guaranteed?|vegan|cruelty|botanicals?|silk|cotton|stainless|handmade|hand.poured|formulated|engineered|longevity)\b/i.test(hook)) {
          throw new Error(`Invalid editorial hook: ${brand}.${category}`);
        }
      }
      profile.hooks[category] = hooks;
    }
  }
  policy.additionalForbidden = stringPool(policy.additionalForbidden, "additionalForbidden");
  for (const [field, ceiling] of Object.entries({ shortDescription: 180, title: 80, seoTitle: 60, metaDescription: 155 })) {
    const value = policy.limits?.[field as keyof BrandContentPolicy["limits"]];
    if (!Number.isInteger(value) || value < ceiling / 2 || value > ceiling) {
      throw new Error(`Invalid brand content limit: ${field}`);
    }
  }
  return policy;
}

export function loadBrandVocabulary(root = process.cwd()): BrandVocabulary {
  const texts = BRAND_VOCABULARY_SOURCES.map((file) => readFileSync(resolve(root, file), "utf8"));
  const [banks, voice, forbidden, personas] = texts;
  const policy = contentPolicy(texts[6]);
  const luxury = banks.split("LUXURY ADJECTIVES", 2)[1]
    ?.replace(/^[\s━─]+/, "").split(/\n[━─]{3,}/, 1)[0];
  const adjectiveRow = voice.split("\n").find((line) => /^\|\s*Adjective range\s*\|/.test(line))?.split("|");
  if (!luxury || !adjectiveRow) throw new Error("Canonical product vocabulary sections are missing");
  const prohibited = unique([...forbiddenTerms(forbidden), ...policy.additionalForbidden]);
  const allowed = (pool: string[]) => unique(pool).filter((word) => EDITORIAL_ADJECTIVES.has(word) && !prohibited.some((term) => term.toLowerCase() === word));
  const mvqueen = allowed([
    ...personaAdjectives(personas, "mvqueen_signature"),
    ...words(adjectiveRow[2] ?? ""),
    ...words(luxury),
    ...policy.profiles.mvqueen.additionalAdjectives,
  ]);
  const princess = allowed([
    ...personaAdjectives(personas, "miss_princess_style"),
    ...words(adjectiveRow[3] ?? ""),
    ...policy.profiles["miss-princess"].additionalAdjectives,
  ]);
  if (!mvqueen.length || !princess.length) throw new Error("A brand's approved vocabulary pool is empty");
  for (const brand of ["mvqueen", "miss-princess"] as const) {
    for (const category of PRODUCT_EDITORIAL_CATEGORIES) {
      const hooks = policy.profiles[brand].hooks[category].filter((hook) =>
        removeForbiddenLanguage(hook, { forbidden: prohibited }) === hook,
      );
      if (!hooks.length) throw new Error(`No approved editorial hooks: ${brand}.${category}`);
      policy.profiles[brand].hooks[category] = hooks;
    }
  }
  const palette = JSON.parse(texts[4]) as {
    profiles: Record<"mvqueen" | "miss-princess", ProductNamingProfile>;
  };
  const namingPool = (values: unknown): string[] => {
    if (!Array.isArray(values) || values.some((value) => typeof value !== "string" || !value.trim())) {
      throw new Error("Invalid canonical product naming pool");
    }
    const names = unique(values as string[]).filter((name) =>
      removeForbiddenLanguage(name, { forbidden: prohibited }) === name,
    );
    if (!names.length) throw new Error("A brand's canonical naming pool is empty");
    return names;
  };
  const naming = Object.fromEntries((["mvqueen", "miss-princess"] as const).map((brand) => {
    const profile = palette.profiles?.[brand];
    if (!profile) throw new Error(`Missing canonical naming persona: ${brand}`);
    return [brand, {
      evocative: {
        fragrance: namingPool(profile.evocative?.fragrance),
        general: namingPool(profile.evocative?.general),
      },
      "descriptive-poetic": namingPool(profile["descriptive-poetic"]),
      "identity-led": namingPool(profile["identity-led"]),
    }];
  })) as BrandVocabulary["naming"];
  return {
    version: createHash("sha256").update(JSON.stringify(BRAND_VOCABULARY_SOURCES.map((path, index) => [path, texts[index]]))).digest("hex").slice(0, 16),
    sources: BRAND_VOCABULARY_SOURCES,
    forbidden: prohibited,
    profiles: { mvqueen: { adjectives: mvqueen }, "miss-princess": { adjectives: princess } },
    naming,
    contentPolicy: policy,
  };
}

export const BRAND_VOCABULARY = loadBrandVocabulary();

export function canonicalBrandLabel(value: string, vocabulary = BRAND_VOCABULARY): string {
  if (/^mv\s*queen$/i.test(value.trim())) return vocabulary.contentPolicy.profiles.mvqueen.displayName;
  if (/^miss[.\s]*(?:princess|queen)$/i.test(value.trim())) return vocabulary.contentPolicy.profiles["miss-princess"].displayName;
  return value.trim();
}

export function removeForbiddenLanguage(value: string, vocabulary: Pick<BrandVocabulary, "forbidden"> = BRAND_VOCABULARY): string {
  let output = value;
  for (const term of [...vocabulary.forbidden].sort((a, b) => b.length - a.length)) {
    const escaped = term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    output = output.replace(new RegExp(`(?<!\\w)${escaped}(?!\\w)`, "gi"), " ");
  }
  return output.replace(/\s+/g, " ").replace(/\s+([,.;:!?])/g, "$1").trim();
}
