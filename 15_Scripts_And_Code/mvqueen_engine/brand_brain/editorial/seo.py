"""SEO metadata generation for MVQueen products."""

from typing import Any, Mapping


def _clean(value: Any) -> str:
    return " ".join(str(value or "").split()).strip()


def generate_seo(title: str, context: Mapping[str, Any] | None = None, max_title: int = 60, max_description: int = 155) -> dict[str, str]:
    data = dict(context or {})
    product_title = _clean(title)
    keywords = _clean(data.get("seo_keywords") or data.get("keywords"))
    seo_title = product_title
    if keywords and len(seo_title) < max_title:
        candidate = f"{seo_title} | {keywords.split(',')[0].strip()}"
        seo_title = candidate[:max_title].rstrip(" |,-")
    description = _clean(data.get("seo_description") or data.get("short_description") or data.get("benefits") or product_title)
    return {"seo_title": seo_title[:max_title].rstrip(), "seo_description": description[:max_description].rstrip()}
