"""Benefit-copy utilities that only use supplied/detected benefits."""

from html import escape
from typing import Any, Mapping


def generate_benefit_copy(context: Mapping[str, Any] | None = None) -> str:
    data = dict(context or {})
    value = data.get("benefits", data.get("key_benefits", ""))
    if isinstance(value, (list, tuple, set)):
        items = [str(x).strip() for x in value if str(x).strip()]
        return "<ul>" + "".join(f"<li>{escape(x)}</li>" for x in items) + "</ul>" if items else ""
    value = str(value or "").strip()
    return f"<p>{escape(value)}</p>" if value else ""
