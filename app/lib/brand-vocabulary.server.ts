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
] as const;

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

export function loadBrandVocabulary(root = process.cwd()): BrandVocabulary {
  const texts = BRAND_VOCABULARY_SOURCES.map((file) => readFileSync(resolve(root, file), "utf8"));
  const [banks, voice, forbidden, personas] = texts;
  const luxury = banks.split("LUXURY ADJECTIVES", 2)[1]
    ?.replace(/^[\s━─]+/, "").split(/\n[━─]{3,}/, 1)[0];
  const adjectiveRow = voice.split("\n").find((line) => /^\|\s*Adjective range\s*\|/.test(line))?.split("|");
  if (!luxury || !adjectiveRow) throw new Error("Canonical product vocabulary sections are missing");
  const prohibited = forbiddenTerms(forbidden);
  const allowed = (pool: string[]) => unique(pool).filter((word) => EDITORIAL_ADJECTIVES.has(word) && !prohibited.some((term) => term.toLowerCase() === word));
  const mvqueen = allowed([
    ...personaAdjectives(personas, "mvqueen_signature"),
    ...words(adjectiveRow[2] ?? ""),
    ...words(luxury),
  ]);
  const princess = allowed([
    ...personaAdjectives(personas, "miss_princess_style"),
    ...words(adjectiveRow[3] ?? ""),
  ]);
  if (!mvqueen.length || !princess.length) throw new Error("A brand's approved vocabulary pool is empty");
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
  };
}

export const BRAND_VOCABULARY = loadBrandVocabulary();

export function removeForbiddenLanguage(value: string, vocabulary: Pick<BrandVocabulary, "forbidden"> = BRAND_VOCABULARY): string {
  let output = value;
  for (const term of [...vocabulary.forbidden].sort((a, b) => b.length - a.length)) {
    const escaped = term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    output = output.replace(new RegExp(`(?<!\\w)${escaped}(?!\\w)`, "gi"), " ");
  }
  return output.replace(/\s+/g, " ").replace(/\s+([,.;:!?])/g, "$1").trim();
}
