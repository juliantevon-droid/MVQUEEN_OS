"""Ingredient/material copy utilities with claim-safe handling."""

from html import escape
from typing import Any, Mapping


def generate_ingredient_copy(context: Mapping[str, Any] | None = None) -> str:
    data = dict(context or {})
    value = data.get("ingredients", data.get("ingredient", ""))
    if isinstance(value, (list, tuple, set)):
        items = [str(x).strip() for x in value if str(x).strip()]
        return "<ul>" + "".join(f"<li>{escape(x)}</li>" for x in items) + "</ul>" if items else ""
    value = str(value or "").strip()
    return f"<p>{escape(value)}</p>" if value else ""
