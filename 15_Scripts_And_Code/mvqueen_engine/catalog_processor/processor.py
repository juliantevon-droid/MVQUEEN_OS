"""MVQueen catalog orchestration layer.

The processor is the integration point between CSV input, brand intelligence,
editorial generation, metafields, tags, collections, bundles, and Shopify.
Live Shopify writes remain an explicit downstream concern.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping
import pandas as pd

from .csv_loader import load_shopify_csv
from mvqueen_engine.brand_brain.editorial.titles import generate_title
from mvqueen_engine.brand_brain.editorial.descriptions import generate_description
from mvqueen_engine.brand_brain.editorial.seo import generate_seo
from mvqueen_engine.brand_brain.editorial.frames import select_frame
from mvqueen_engine.brand_brain.editorial.persona_voice import build_voice_context
from mvqueen_engine.brand_brain.editorial.benefit_copy import generate_benefit_copy
from mvqueen_engine.brand_brain.editorial.ingredient_copy import generate_ingredient_copy


def _value(row: pd.Series, *names: str) -> str:
    for name in names:
        value = str(row.get(name, "") or "").strip()
        if value:
            return value
    return ""


def build_context(row: pd.Series) -> dict[str, Any]:
    return {
        "persona": _value(row, "metafield.custom.persona", "Persona"),
        "voice": _value(row, "metafield.custom.voice"),
        "tone": _value(row, "metafield.custom.tone"),
        "benefits": _value(row, "metafield.custom.key_benefits", "Benefits"),
        "ingredients": _value(row, "metafield.custom.ingredients", "Ingredients"),
        "target_audience": _value(row, "metafield.custom.target_audience"),
        "who_its_for": _value(row, "metafield.custom.who_its_for"),
        "mood": _value(row, "metafield.custom.mood"),
        "occasion": _value(row, "metafield.custom.occasion"),
        "frame": _value(row, "metafield.custom.editorial_frame"),
        "seo_keywords": _value(row, "metafield.custom.seo_keywords"),
    }


def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Process an already-loaded Shopify DataFrame without touching Shopify."""
    if "Handle" not in df.columns or "Title" not in df.columns:
        raise ValueError("Catalog must contain Handle and Title columns")

    result = df.copy()
    for column in ("Body (HTML)", "SEO Title", "SEO Description", "Tags", "Image Alt Text"):
        if column not in result.columns:
            result[column] = ""

    for index, row in result.iterrows():
        handle = str(row["Handle"]).strip()
        base_title = str(row["Title"]).strip()
        context = build_context(row)
        context["frame"] = select_frame(context)

        title = generate_title(base_title, handle, context)
        body = generate_description(base_title, handle, str(row.get("Body (HTML)", "")), context)
        seo = generate_seo(title, context)

        result.at[index, "Title"] = title
        result.at[index, "Body (HTML)"] = body
        result.at[index, "SEO Title"] = seo["seo_title"]
        result.at[index, "SEO Description"] = seo["seo_description"]

        existing_tags = str(row.get("Tags", "") or "").strip()
        result.at[index, "Tags"] = existing_tags

        # Keep generated editorial intelligence available to downstream processors.
        result.at[index, "metafield.custom.editorial_frame"] = context["frame"]
        result.at[index, "metafield.custom.persona_voice"] = str(build_voice_context(context))
        result.at[index, "metafield.custom.benefit_copy"] = generate_benefit_copy(context)
        result.at[index, "metafield.custom.ingredient_copy"] = generate_ingredient_copy(context)

    return result


def process_csv(input_path: str | Path, output_path: str | Path) -> Path:
    """Load, curate, and export a Shopify-compatible CSV."""
    df = load_shopify_csv(input_path)
    result = process_dataframe(df)
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(destination, index=False)
    return destination
