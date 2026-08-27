"""Description generation and HTML-safe editorial assembly."""

from html import escape
from typing import Any, Mapping


def generate_description(base_title: str, handle: str = "", supplier_body_html: str = "", context: Mapping[str, Any] | None = None) -> str:
    """Generate factual-first product copy from supplied product intelligence."""
    data = dict(context or {})
    title = escape(" ".join(str(base_title or "").split()))
    paragraphs: list[str] = []
    if title:
        paragraphs.append(f"<p>{title}</p>")

    benefit = str(data.get("benefits") or data.get("key_benefits") or "").strip()
    if benefit:
        paragraphs.append(f"<p>{escape(benefit)}</p>")

    audience = str(data.get("target_audience") or data.get("who_its_for") or "").strip()
    if audience:
        paragraphs.append(f"<p>Designed for {escape(audience)}.</p>")

    source = str(supplier_body_html or "").strip()
    if source:
        paragraphs.append(source)
    return "".join(paragraphs)
