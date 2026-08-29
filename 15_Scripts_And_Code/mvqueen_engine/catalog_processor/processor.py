"""MVQueen catalog orchestration layer."""
from __future__ import annotations

from pathlib import Path
from typing import Any
import pandas as pd

from .csv_loader import load_shopify_csv
from .schema import ProductRecord
from mvqueen_engine.brand_brain.detection import detect_all
from mvqueen_engine.brand_brain.persona.router import route_profile
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
    context = {
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
    if not context["persona"]:
        profile = route_profile(context)
        context["persona"] = profile["persona"]
        context["voice"] = context["voice"] or profile["voice"]
        context["tone"] = context["tone"] or profile["tone"]
    return context


def process_record(record: ProductRecord) -> ProductRecord:
    """Enrich one normalized ProductRecord while preserving source data."""
    source_text = " ".join(filter(None, [record.title, record.body_html, record.product_type, record.category, record.material, " ".join(record.details), " ".join(record.benefits), " ".join(record.ingredients), " ".join(record.textures), " ".join(record.finishes)]))
    detected = detect_all(source_text, seed=record.handle)

    record.category = record.category or detected.get("category", "default")
    record.product_type_detailed = record.product_type_detailed or detected.get("product_type", "")
    record.persona = record.persona or detected.get("persona", "")
    record.vibe = record.vibe or detected.get("vibe", "")
    record.trend = record.trend or detected.get("trend", "")
    record.season = record.season or detected.get("season", "")
    record.material = record.material or detected.get("material", "")
    record.silhouette = record.silhouette or detected.get("silhouette", "")
    record.details = record.details or detected.get("details", [])
    record.benefits = record.benefits or detected.get("benefits", [])
    record.ingredients = record.ingredients or detected.get("ingredients", [])
    record.textures = record.textures or detected.get("textures", [])
    record.finishes = record.finishes or detected.get("finishes", [])

    raw_context = {
        "persona": record.persona,
        "voice": record.voice,
        "tone": "",
        "benefits": record.key_benefits or ", ".join(record.benefits),
        "ingredients": record.ingredients,
        "target_audience": record.target_audience,
        "who_its_for": record.who_its_for,
        "mood": record.mood,
        "occasion": record.occasion,
        "frame": "",
        "seo_keywords": "",
        "title": record.title,
        "description": record.body_html,
        "category": record.category,
        "product_type": record.product_type_detailed,
        "vibe": record.vibe,
        "trend": record.trend,
    }
    profile = route_profile(raw_context)
    record.persona = record.persona or profile["persona"]
    raw_context["persona"] = record.persona
    raw_context["voice"] = record.voice or profile["voice"]
    raw_context["tone"] = profile["tone"]
    raw_context["frame"] = select_frame(raw_context)

    record.generated_title = generate_title(record.title, record.handle, raw_context)
    record.long_description = generate_description(record.title, record.handle, record.body_html, raw_context)
    record.short_description = record.long_description[:155]
    seo = generate_seo(record.generated_title, raw_context)
    record.seo_title = seo["seo_title"]
    record.seo_description = seo["seo_description"]
    record.alt_text = record.alt_text or record.image_alt_text or record.generated_title
    record.metafields.update({
        "custom.category": record.category,
        "custom.product_type_detailed": record.product_type_detailed,
        "custom.persona": record.persona,
        "custom.vibe": record.vibe,
        "custom.trend": record.trend,
        "custom.seasonality": record.season,
        "custom.material": record.material,
        "custom.silhouette": record.silhouette,
        "custom.details": record.details,
        "custom.benefits": record.benefits,
        "custom.ingredients": record.ingredients,
        "custom.texture": record.textures,
        "custom.finish": record.finishes,
        "custom.editorial_frame": raw_context["frame"],
        "custom.persona_voice": str(build_voice_context(raw_context)),
        "custom.benefit_copy": generate_benefit_copy(raw_context),
        "custom.ingredient_copy": generate_ingredient_copy(raw_context),
    })
    return record


def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Process a Shopify DataFrame without touching Shopify."""
    if "Handle" not in df.columns or "Title" not in df.columns:
        raise ValueError("Catalog must contain Handle and Title columns")
    result = df.copy()
    for column in ("Body (HTML)", "SEO Title", "SEO Description", "Tags", "Image Alt Text"):
        if column not in result.columns:
            result[column] = ""
    _, records = load_shopify_csv_from_dataframe(result)
    processed = [process_record(record) for record in records]
    for index, record in enumerate(processed):
        result.at[index, "Title"] = record.generated_title or record.title
        result.at[index, "Body (HTML)"] = record.long_description
        result.at[index, "SEO Title"] = record.seo_title
        result.at[index, "SEO Description"] = record.seo_description
        result.at[index, "Image Alt Text"] = record.alt_text
        for key, value in record.metafields.items():
            result.at[index, f"metafield.{key}"] = value
    return result


def load_shopify_csv_from_dataframe(df: pd.DataFrame):
    from .csv_loader import records_from_dataframe
    return df, records_from_dataframe(df)


def process_csv(input_path: str | Path, output_path: str | Path) -> Path:
    df, records = load_shopify_csv(input_path)
    processed = [process_record(record) for record in records]
    result = df.copy()
    for index, record in enumerate(processed):
        result.at[index, "Title"] = record.generated_title or record.title
        result.at[index, "Body (HTML)"] = record.long_description
        result.at[index, "SEO Title"] = record.seo_title
        result.at[index, "SEO Description"] = record.seo_description
        result.at[index, "Image Alt Text"] = record.alt_text
        for key, value in record.metafields.items():
            result.at[index, f"metafield.{key}"] = value
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(destination, index=False)
    return destination


def process_product(text: str | dict[str, Any]) -> dict[str, Any]:
    """Legacy compatibility adapter retained for existing exporters."""
    if isinstance(text, dict):
        return dict(text)
    return {"title": str(text), "description": str(text), "category": "default", "product_type": "default"}
