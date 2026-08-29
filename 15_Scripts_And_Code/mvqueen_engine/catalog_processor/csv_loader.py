"""MVQueen Shopify CSV loading and export helpers."""
from __future__ import annotations
import csv
import json
from pathlib import Path
from typing import Any
import pandas as pd
from mvqueen_engine.catalog_processor.schema import MVQUEEN_METAFIELDS, SHOPIFY_CORE_FIELDS, ProductRecord, ensure_columns


def _clean(value: Any) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    return str(value).strip()


def _float_or_none(value: Any) -> float | None:
    text = _clean(value).replace("$", "").replace(",", "")
    if not text:
        return None
    try:
        return float(text)
    except (TypeError, ValueError):
        return None


def _split_list(value: Any) -> list[str]:
    text = _clean(value)
    if not text:
        return []
    return [part.strip() for part in text.replace(";", ",").split(",") if part.strip()]


def records_from_dataframe(df: pd.DataFrame) -> list[ProductRecord]:
    """Normalize a dataframe into the engine's ProductRecord contract."""
    records: list[ProductRecord] = []
    for _, row in df.iterrows():
        metafields = {column: _clean(row.get(column, "")) for column in MVQUEEN_METAFIELDS if _clean(row.get(column, ""))}
        records.append(ProductRecord(
            handle=_clean(row.get("Handle")), title=_clean(row.get("Title")), body_html=_clean(row.get("Body (HTML)")),
            vendor=_clean(row.get("Vendor")) or "MVQueen", product_type=_clean(row.get("Type")) or _clean(row.get("Product Type")),
            tags=_split_list(row.get("Tags")), collections=_split_list(row.get("Collections")),
            price=_float_or_none(row.get("Variant Price")), compare_at_price=_float_or_none(row.get("Variant Compare At Price")),
            sku=_clean(row.get("Variant SKU")), barcode=_clean(row.get("Variant Barcode")), image_alt_text=_clean(row.get("Image Alt Text")),
            category=_clean(row.get("Category")) or "default", product_type_detailed=_clean(row.get("metafield.custom.product_type_detailed")),
            persona=_clean(row.get("Persona")) or _clean(row.get("metafield.custom.persona")), vibe=_clean(row.get("Vibe")) or _clean(row.get("metafield.custom.vibe")),
            trend=_clean(row.get("Trend")) or _clean(row.get("metafield.custom.trend")), season=_clean(row.get("Season")) or _clean(row.get("metafield.custom.seasonality")),
            material=_clean(row.get("Material")) or _clean(row.get("metafield.custom.material")), silhouette=_clean(row.get("Silhouette")) or _clean(row.get("metafield.custom.silhouette")),
            details=_split_list(row.get("Detail")) or _split_list(row.get("metafield.custom.details")), benefits=_split_list(row.get("metafield.custom.benefits")),
            ingredients=_split_list(row.get("metafield.custom.ingredients")), textures=_split_list(row.get("metafield.custom.texture")), finishes=_split_list(row.get("metafield.custom.finish")),
            occasion=_clean(row.get("metafield.custom.occasion")), fit=_clean(row.get("metafield.custom.fit")), voice=_clean(row.get("metafield.custom.voice")),
            intent=_clean(row.get("metafield.custom.intent")), collection=_clean(row.get("metafield.custom.collection")), target_audience=_clean(row.get("metafield.custom.target_audience")),
            who_its_for=_clean(row.get("metafield.custom.who_its_for")), results=_clean(row.get("metafield.custom.results")), mood=_clean(row.get("metafield.custom.mood")),
            key_benefits=_clean(row.get("metafield.custom.key_benefits")), short_description=_clean(row.get("metafield.custom.short_description")), long_description=_clean(row.get("metafield.custom.long_description")),
            seo_title=_clean(row.get("SEO Title")), seo_description=_clean(row.get("SEO Description")), alt_text=_clean(row.get("metafield.custom.alt_text")) or _clean(row.get("Image Alt Text")),
            prestige_score=_float_or_none(row.get("metafield.custom.prestige_score")), product_quality_score=_float_or_none(row.get("metafield.custom.product_quality_score")),
            shopify_bundle_safe=_clean(row.get("metafield.custom.shopify_bundle_safe")).lower() == "true", metafields=metafields, source=row.to_dict(), seed=_clean(row.get("seed"))
        ))
    return records


def load_shopify_csv(file_path: str | Path) -> tuple[pd.DataFrame, list[ProductRecord]]:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")
    if path.suffix.lower() != ".csv":
        raise ValueError(f"Expected a CSV file, received: {path.suffix}")
    df = pd.read_csv(path, dtype=object, keep_default_na=False)
    df = df.reindex(columns=ensure_columns(list(df.columns)), fill_value="")
    return df, records_from_dataframe(df)


def flatten_metafields(metafields: dict) -> dict:
    return {f"metafield.{key}": json.dumps(value, ensure_ascii=False) if isinstance(value, list) else value for key, value in metafields.items()}


def flatten_tags(tags: list) -> str:
    return ", ".join(sorted(str(tag).strip() for tag in tags if str(tag).strip()))


def flatten_collections(collections: list) -> str:
    return ", ".join(sorted(str(value).strip() for value in collections if str(value).strip()))


def convert_to_csv_row(product: dict) -> dict:
    row = {"Title": product.get("title", ""), "Handle": product.get("handle", ""), "Body (HTML)": product.get("editorial_long", ""), "Tags": flatten_tags(product.get("tags", [])), "Collections": flatten_collections(product.get("collections", [])), "SEO Title": product.get("seo_primary", ""), "SEO Description": product.get("seo_secondary", ""), "Image Alt Text": product.get("alt_text_long", ""), "Category": product.get("category", ""), "Product Type": product.get("product_type", ""), "Persona": product.get("persona", ""), "Trend": product.get("trend", ""), "Season": product.get("season", ""), "Vibe": product.get("vibe", ""), "Material": product.get("material", ""), "Silhouette": product.get("silhouette", ""), "Detail": product.get("detail", ""), "input_text": product.get("input_text", ""), "seed": product.get("seed", "")}
    row.update(flatten_metafields(product.get("metafields", {})))
    return row


def save_csv_from_texts(texts: list, filename: str = "mvqueen_output.csv"):
    from mvqueen_engine.catalog_processor.processor import process_product
    rows = [convert_to_csv_row(process_product(text)) for text in texts]
    if not rows:
        return
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys())); writer.writeheader(); writer.writerows(rows)


__all__ = ["load_shopify_csv", "records_from_dataframe", "flatten_metafields", "flatten_tags", "flatten_collections", "convert_to_csv_row", "save_csv_from_texts", "SHOPIFY_CORE_FIELDS", "MVQUEEN_METAFIELDS"]
