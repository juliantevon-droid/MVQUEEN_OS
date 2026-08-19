"""
MVQUEEN OMNILUXE SUPREME v10.0
================================
Self-contained Shopify-safe catalog enrichment engine.

Extends the existing MVQueen architecture with:
- Universal brand/persona banks
- 1,000+ deterministic persona keywords
- Brand voice rotation
- Editorial SEO enrichment
- Multi-language SEO phrase variants
- Persona / collection / intent metadata
- Deterministic pricing suggestions
- Scalable bundle-neighbor generation
- Shopify Title and Status validation
- Protected operational-column preservation
- No Helper_Library.csv dependency

IMPORTANT:
This script is additive. It does not intentionally delete source columns and
never changes protected operational values. Status is copied exactly from the
source. Invalid status values are reported and block the final Shopify-safe
export rather than being silently changed.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import re
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import pandas as pd

from mvqueen_brand_banks import (
    BRAND_NAME,
    BRAND_VOICE_BANK,
    CATEGORY_BANKS,
    COLLECTION_BANK,
    INTENT_PHRASES,
    LUXURY_ADJECTIVES,
    LUXURY_MODIFIERS,
    PERSONA_PROFILES,
    PERSONA_KEYWORDS,
    PROTECTED_COLUMNS,
    SEO_LANGUAGE_BANK,
    SENSORY_VERBS,
    BENEFIT_SYNONYMS,
    assign_brand_voice,
    assign_keywords,
    assign_persona,
    compare_at_price,
    price_tier,
    stable_seed,
    validate_shopify_row,
)

VERSION = "10.0"
DEFAULT_INPUT = Path.cwd() / "shopify_input.csv"
DEFAULT_OUTPUT_DIR = Path.cwd() / "MVQ_Exports"

# -----------------------------------------------------------------------------
# COLUMN RESOLUTION
# -----------------------------------------------------------------------------
def find_col(columns: Sequence[str], *patterns: str) -> str | None:
    for column in columns:
        for pattern in patterns:
            if re.search(pattern, str(column), re.I):
                return column
    return None


def ensure_column(df: pd.DataFrame, name: str, default: str = "") -> str:
    if name not in df.columns:
        df[name] = default
    return name


# -----------------------------------------------------------------------------
# TEXT / CATEGORY HELPERS
# -----------------------------------------------------------------------------
def clean_text(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def product_category(title: str, product_type: str = "") -> str:
    text = f"{title} {product_type}".lower()
    if any(x in text for x in ("serum", "moisturizer", "cleanser", "retinol", "toner", "mask", "spf", "skin")):
        return "skincare"
    if any(x in text for x in ("foundation", "concealer", "lipstick", "lip gloss", "blush", "bronzer", "mascara", "eyeliner", "palette", "makeup")):
        return "makeup"
    if any(x in text for x in ("shampoo", "conditioner", "hair", "scalp", "styling", "curl", "edge")):
        return "haircare"
    if any(x in text for x in ("body", "lotion", "butter", "body oil", "scrub")):
        return "body"
    if any(x in text for x in ("dress", "blazer", "skirt", "top", "pants", "jacket", "coat", "fashion", "apparel")):
        return "fashion"
    return "beauty"


def safe_price(value: object) -> float:
    text = clean_text(value).replace(",", "")
    match = re.search(r"\d+(?:\.\d+)?", text)
    return float(match.group(0)) if match else 0.0


def generate_title(row: pd.Series, category: str, product_key: str) -> str:
    """Only used when the source Title is blank; existing titles are preserved."""
    seed = stable_seed(product_key)
    bank = CATEGORY_BANKS.get(category, CATEGORY_BANKS["beauty"])
    primary = bank["keywords"][seed[0] % len(bank["keywords"])]
    outcome = bank["outcomes"][seed[1] % len(bank["outcomes"])]
    adjective = LUXURY_ADJECTIVES[seed[2] % len(LUXURY_ADJECTIVES)]
    modifier = LUXURY_MODIFIERS[seed[3] % len(LUXURY_MODIFIERS)]

    product_type = clean_text(row.get("Type", ""))
    vendor = clean_text(row.get("Vendor", ""))
    base = product_type or primary
    prefix = vendor or BRAND_NAME
    title = f"{prefix} {adjective} {base} — {modifier} {outcome}"
    return clean_text(title)[:255]


def seo_phrase(language: str, key: str) -> str:
    return SEO_LANGUAGE_BANK.get(language, SEO_LANGUAGE_BANK["en"]).get(key, key)


def localized_seo(title: str, category: str, persona: str, language: str) -> Tuple[str, str]:
    # Controlled phrase translation keeps the title itself intact unless a
    # known controlled phrase is available; this avoids fake translations.
    lux = seo_phrase(language, "luxury")
    beauty = seo_phrase(language, "beauty")
    glow = seo_phrase(language, "glow")
    ritual = seo_phrase(language, "ritual")
    meta_title = f"{title} | {lux} {beauty}"[:70]
    meta_description = (
        f"{title}. A refined {beauty} ritual designed around {glow}, "
        f"performance and modern {lux}. Persona: {persona}."
    )[:320]
    if language != "en":
        meta_description = meta_description.replace("luxury", lux).replace("beauty", beauty).replace("glow", glow).replace("ritual", ritual)
    return meta_title, meta_description


# -----------------------------------------------------------------------------
# SCALABLE BUNDLE ENGINE
# -----------------------------------------------------------------------------
def nearest_bundle_neighbors(handles: List[str], limit: int = 20) -> Dict[str, List[str]]:
    """Generate deterministic nearest-hash neighbors without O(n²) comparisons."""
    if not handles:
        return {}

    records = sorted((stable_seed(h)[0], h) for h in handles)
    n = len(records)
    output: Dict[str, List[str]] = {}

    # A local ring of candidates gives deterministic, scalable neighbors. The
    # final candidate set is expanded slightly so ties do not produce poor
    # results at the edges of the sorted space.
    window = max(limit * 3, 60)
    for pos, (_, handle) in enumerate(records):
        candidates: List[Tuple[int, str]] = []
        lo = max(0, pos - window)
        hi = min(n, pos + window + 1)
        target = records[pos][0]
        for idx in range(lo, hi):
            if idx == pos:
                continue
            seed, other = records[idx]
            candidates.append((abs(target - seed), other))
        candidates.sort(key=lambda x: (x[0], x[1]))
        output[handle] = [h for _, h in candidates[:limit]]
    return output


# -----------------------------------------------------------------------------
# MAIN ENRICHMENT
# -----------------------------------------------------------------------------
def enrich_catalog(input_file: Path, output_dir: Path) -> Tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(input_file, dtype=str, keep_default_na=False).fillna("")
    original_columns = list(df.columns)

    title_col = find_col(df.columns, r"^title$")
    handle_col = find_col(df.columns, r"^handle$")
    status_col = find_col(df.columns, r"^status$")
    price_col = find_col(df.columns, r"^price$")
    type_col = find_col(df.columns, r"^type$", r"product.?type")
    body_col = find_col(df.columns, r"body", r"description")
    tags_col = find_col(df.columns, r"^tags$")
    vendor_col = find_col(df.columns, r"^vendor$")

    if title_col is None:
        title_col = "Title"
        df[title_col] = ""
    if handle_col is None:
        raise ValueError("Shopify-safe processing requires a Handle column.")
    if status_col is None:
        raise ValueError("Shopify-safe processing requires a Status column.")

    # Preserve every source column. Only add new columns after the source set.
    added_columns: List[str] = []

    def add(name: str, default: str = "") -> str:
        nonlocal df
        if name not in df.columns:
            df[name] = default
            added_columns.append(name)
        return name

    # Shopify title is required on every row. Existing titles are never changed.
    for idx in df.index:
        existing = clean_text(df.at[idx, title_col])
        if not existing:
            key = clean_text(df.at[idx, handle_col]) or f"row-{idx}"
            category = product_category(
                clean_text(df.at[idx, title_col]),
                clean_text(df.at[idx, type_col]) if type_col else "",
            )
            df.at[idx, title_col] = generate_title(df.loc[idx], category, key)

    # Product-level bundle map avoids repeating all-pairs calculations.
    handles = [clean_text(h) for h in df[handle_col].tolist()]
    unique_handles = list(dict.fromkeys(h for h in handles if h))
    bundle_map = nearest_bundle_neighbors(unique_handles, limit=20)

    # Additive fields.
    fields = [
        "metafield.custom.brand_version", "metafield.custom.brand_voice",
        "metafield.custom.persona", "metafield.custom.persona_axis",
        "metafield.custom.persona_emotion", "metafield.custom.persona_keywords",
        "metafield.custom.category", "metafield.custom.primary_keyword",
        "metafield.custom.secondary_keyword", "metafield.custom.long_tail_keyword",
        "metafield.custom.luxury_modifier", "metafield.custom.luxury_adjective",
        "metafield.custom.sensory_verb", "metafield.custom.benefit_synonym",
        "metafield.custom.intent_phrase", "metafield.custom.collection",
        "metafield.custom.price_psychology_tier", "metafield.custom.prestige_score",
        "metafield.custom.hero_probability", "metafield.custom.routine_integration_score",
        "metafield.custom.search_intent_match", "metafield.custom.conversion_index",
        "metafield.custom.bundle_affinity", "metafield.custom.bundle_candidates",
        "metafield.custom.editorial_short", "metafield.custom.editorial_medium",
        "metafield.custom.editorial_long", "metafield.custom.schema_ready",
        "metafield.custom.search_cluster", "metafield.custom.emotional_axis",
        "metafield.custom.performance_tier", "metafield.custom.aov_influence",
        "compare_at_price_suggestion",
    ]
    for field in fields:
        add(field)

    languages = ("en", "fr", "es", "de", "it", "pt")
    for lang in languages:
        add(f"metafield.custom.seo_title_{lang}")
        add(f"metafield.custom.seo_description_{lang}")

    campaign_rows: List[Dict[str, object]] = []

    for idx in df.index:
        key = clean_text(df.at[idx, handle_col]) or f"row-{idx}"
        title = clean_text(df.at[idx, title_col])
        category = product_category(title, clean_text(df.at[idx, type_col]) if type_col else "")
        price = safe_price(df.at[idx, price_col]) if price_col else 0.0
        seed = stable_seed(key)
        persona = assign_persona(key)
        voice = assign_brand_voice(key)
        persona_profile = PERSONA_PROFILES[persona]
        category_bank = CATEGORY_BANKS.get(category, CATEGORY_BANKS["beauty"])

        primary = category_bank["keywords"][seed[0] % len(category_bank["keywords"])]
        secondary = category_bank["keywords"][seed[1] % len(category_bank["keywords"])]
        long_tail = category_bank["outcomes"][seed[2] % len(category_bank["outcomes"])]
        luxury_modifier = LUXURY_MODIFIERS[seed[3] % len(LUXURY_MODIFIERS)]
        luxury_adjective = LUXURY_ADJECTIVES[seed[4] % len(LUXURY_ADJECTIVES)]
        sensory_verb = SENSORY_VERBS[seed[5] % len(SENSORY_VERBS)]
        benefit = BENEFIT_SYNONYMS[seed[6] % len(BENEFIT_SYNONYMS)]
        intent = INTENT_PHRASES[seed[7] % len(INTENT_PHRASES)]

        prestige = round(40 + (seed[0] % 61), 2)
        hero = round((seed[1] % 101) / 100, 2)
        routine = round((seed[2] % 101) / 100, 2)
        search = round((seed[3] % 101) / 100, 2)
        conversion = round((hero + routine + search) / 3, 4)
        bundle_affinity = round((seed[4] % 101) / 100, 2)
        aov = round((price / 100.0) + bundle_affinity, 4)
        performance = ("Elite" if prestige >= 90 else "Luxury" if prestige >= 75 else "Advanced" if prestige >= 55 else "Core")
        collection = COLLECTION_BANK[seed[6] % len(COLLECTION_BANK)]
        emotional_axis = persona_profile["axis"]
        bundles = ",".join(bundle_map.get(key, []))

        short = f"{luxury_adjective.capitalize()} {category} designed to {intent}."
        medium = f"{title} brings {luxury_modifier} {category} to a refined {persona.lower()} ritual, with {benefit}."
        long = (
            f"{title} is positioned within the MVQueen {collection} architecture. "
            f"Its {persona.lower()} language combines {luxury_adjective} presentation, "
            f"{sensory_verb} performance and a clear intent to {intent}."
        )

        values = {
            "metafield.custom.brand_version": VERSION,
            "metafield.custom.brand_voice": voice,
            "metafield.custom.persona": persona,
            "metafield.custom.persona_axis": persona_profile["axis"],
            "metafield.custom.persona_emotion": persona_profile["emotions"][seed[5] % len(persona_profile["emotions"])],
            "metafield.custom.persona_keywords": ", ".join(assign_keywords(key, 12)),
            "metafield.custom.category": category,
            "metafield.custom.primary_keyword": primary,
            "metafield.custom.secondary_keyword": secondary,
            "metafield.custom.long_tail_keyword": long_tail,
            "metafield.custom.luxury_modifier": luxury_modifier,
            "metafield.custom.luxury_adjective": luxury_adjective,
            "metafield.custom.sensory_verb": sensory_verb,
            "metafield.custom.benefit_synonym": benefit,
            "metafield.custom.intent_phrase": intent,
            "metafield.custom.collection": collection,
            "metafield.custom.price_psychology_tier": price_tier(price),
            "metafield.custom.prestige_score": prestige,
            "metafield.custom.hero_probability": hero,
            "metafield.custom.routine_integration_score": routine,
            "metafield.custom.search_intent_match": search,
            "metafield.custom.conversion_index": conversion,
            "metafield.custom.bundle_affinity": bundle_affinity,
            "metafield.custom.bundle_candidates": bundles,
            "metafield.custom.editorial_short": short,
            "metafield.custom.editorial_medium": medium,
            "metafield.custom.editorial_long": long,
            "metafield.custom.schema_ready": "true",
            "metafield.custom.search_cluster": f"{category}:{seed[0] % 1000:03d}",
            "metafield.custom.emotional_axis": emotional_axis,
            "metafield.custom.performance_tier": performance,
            "metafield.custom.aov_influence": aov,
            "compare_at_price_suggestion": compare_at_price(price),
        }

        for lang in languages:
            seo_title, seo_desc = localized_seo(title, category, persona, lang)
            values[f"metafield.custom.seo_title_{lang}"] = seo_title
            values[f"metafield.custom.seo_description_{lang}"] = seo_desc

        for column, value in values.items():
            df.at[idx, column] = value

        if tags_col:
            existing_tags = clean_text(df.at[idx, tags_col])
            additive_tags = ", ".join([primary, secondary, persona, collection, BRAND_NAME])
            df.at[idx, tags_col] = existing_tags if not additive_tags else \
                ", ".join(dict.fromkeys(filter(None, [existing_tags, additive_tags])))

        campaign_rows.append({
            "handle": key,
            "title": title,
            "category": category,
            "persona": persona,
            "brand_voice": voice,
            "collection": collection,
            "price_tier": price_tier(price),
            "prestige_score": prestige,
            "conversion_index": conversion,
            "hero_probability": hero,
            "bundle_affinity": bundle_affinity,
        })

    # -------------------------------------------------------------------------
    # FINAL SHOPIFY SAFETY GATE
    # -------------------------------------------------------------------------
    # Protected columns are compared to source values and restored if an
    # enrichment operation accidentally touched one. This is a defensive gate.
    source = pd.read_csv(input_file, dtype=str, keep_default_na=False).fillna("")
    for column in PROTECTED_COLUMNS:
        if column in source.columns and column in df.columns:
            df[column] = source[column]

    errors: List[Tuple[int, str]] = []
    for idx in df.index:
        row = {"Title": df.at[idx, title_col], "Status": df.at[idx, status_col]}
        row_errors = validate_shopify_row(row)
        for error in row_errors:
            errors.append((int(idx) + 2, error))

    # Title must never be blank anywhere in output.
    blank_titles = df[title_col].astype(str).str.strip().eq("")
    if blank_titles.any():
        errors.extend((int(i) + 2, "Title can't be blank") for i in df.index[blank_titles])

    # Status is never normalized. Any invalid source status blocks export.
    if errors:
        report = output_dir / "MVQ_SHOPIFY_VALIDATION_ERRORS.csv"
        pd.DataFrame(errors, columns=["source_row", "error"]).drop_duplicates().to_csv(report, index=False)
        raise ValueError(f"Shopify safety gate failed. See {report} — source Status values were not changed.")

    # Put Title first while retaining every original and added column.
    output_columns = list(df.columns)
    output_columns.remove(title_col)
    output_columns.insert(0, title_col)

    output_file = output_dir / "MVQUEEN_OMNILUXE_SUPREME_V10.csv"
    campaign_file = output_dir / "MVQUEEN_CAMPAIGN_SEGMENTS_V10.csv"
    df.to_csv(output_file, index=False, columns=output_columns)
    pd.DataFrame(campaign_rows).drop_duplicates(subset=["handle"]).to_csv(campaign_file, index=False)

    return output_file, campaign_file


def main() -> None:
    parser = argparse.ArgumentParser(description="MVQueen OmniLuxe Supreme v10 Shopify-safe catalog enrichment")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    output, campaign = enrich_catalog(args.input, args.output_dir)
    print(f"MVQueen OmniLuxe Supreme v{VERSION} complete")
    print(f"Shopify export: {output}")
    print(f"Campaign export: {campaign}")
    print(f"Persona bank size: {len(PERSONA_KEYWORDS)}")
    print("Protected columns preserved; source Status values were not normalized.")


if __name__ == "__main__":
    main()
