"""MVQUEEN CSV safety validation. Editorial-only mutations; 850 is per-file batch limit."""
from typing import Dict, Iterable, List
from .config import MAX_PRODUCTS_PER_IMPORT_FILE, ONLY_EDIT_IMAGE_FIELD, SHOPIFY_EDITORIAL_COLUMNS, SHOPIFY_PROTECTED_COLUMNS, PRESERVE_SOURCE_COLUMN_ORDER

def validate_columns(headers: List[str]) -> List[str]:
    return [f"missing-required-column:{x}" for x in ("Title",) if x not in headers]

def validate_import_size(product_count: int) -> List[str]:
    return [] if product_count <= MAX_PRODUCTS_PER_IMPORT_FILE else [f"batch-exceeds-limit:{MAX_PRODUCTS_PER_IMPORT_FILE}"]

def protected_changes(before: Dict[str,str], after: Dict[str,str]) -> List[str]:
    return [k for k in SHOPIFY_PROTECTED_COLUMNS if str(before.get(k,"")) != str(after.get(k,""))]

def validate_editorial_changes(before: Dict[str,str], after: Dict[str,str]) -> List[str]:
    changed=[k for k in after if str(before.get(k,"")) != str(after.get(k,""))]
    return [k for k in changed if k not in SHOPIFY_EDITORIAL_COLUMNS]
