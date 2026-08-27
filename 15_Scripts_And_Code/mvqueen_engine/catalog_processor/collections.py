"""Collection rule/value generation for MVQueen catalogs."""
from __future__ import annotations

import re
from collections.abc import Mapping


def slugify(value: object) -> str:
    text = str(value or "").lower().strip()
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def build_collection_values(data: Mapping[str, object]) -> list[str]:
    values: list[str] = []
    for key in ("collection", "category", "persona", "intent", "season", "vibe", "trend"):
        value = str(data.get(key) or "").strip()
        if value and value not in values:
            values.append(value)
    return values


def build_collection_rules(data: Mapping[str, object]) -> list[dict[str, str]]:
    rules: list[dict[str, str]] = []
    for key, column in (("collection", "Product metafield: custom.collection"), ("persona", "Product metafield: custom.persona"), ("intent", "Product metafield: custom.intent"), ("season", "Product metafield: custom.seasonality"), ("vibe", "Product metafield: custom.vibe")):
        value = str(data.get(key) or "").strip()
        if value:
            rules.append({"column": column, "relation": "equals", "condition": value})
    return rules
