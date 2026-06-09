# ============================================================
# BLOCK 31 — ENGINE CORE (engine_core.py)
# ============================================================

from __future__ import annotations
import json
import random
from pathlib import Path
from typing import Any, Dict, List, Optional

# Adjust this import to your actual config module path
from .config import MASTER_CONFIG


# -----------------------------
# CORE: MASTER CONFIG ACCESS
# -----------------------------

def get_master_config() -> Dict[str, Any]:
    return MASTER_CONFIG


def get_block(name: str) -> Optional[Dict[str, Any]]:
    return MASTER_CONFIG.get("blocks", {}).get(name)


def get_engine(name: str) -> Optional[Dict[str, Any]]:
    return get_block(name)


# -----------------------------
# CORE: DETERMINISTIC SEEDING
# -----------------------------

def build_seed(*components: Any, fallback: int = 42) -> int:
    parts = [str(c) for c in components if c is not None]
    if not parts:
        return fallback
    return abs(hash("::".join(parts))) % (2**31 - 1)


def with_seed(*components: Any, fallback: int = 42):
    seed = build_seed(*components, fallback=fallback)
    random.seed(seed)
    return seed


# -----------------------------
# CORE: SAFE HELPERS
# -----------------------------

def safe_get(d: Dict[str, Any], key: str, default: Any = None) -> Any:
    if not isinstance(d, dict):
        return default
    return d.get(key, default)


def ensure_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def sanitize_text(value: Optional[str]) -> str:
    if value is None:
        return ""
    return str(value).strip()


# -----------------------------
# CORE: SELECTORS (HOOKS)
# -----------------------------

def select_persona(product: Dict[str, Any]) -> str:
    persona = product.get("persona")
    if persona:
        return persona

    personas_engine = get_engine("personas") or {}
    fallback = personas_engine.get("fallback_persona", "MVQueen Core")
    return fallback


def select_editorial_length(product: Dict[str, Any]) -> str:
    editorial_engine = get_engine("editorial") or {}
    lengths = editorial_engine.get("lengths", {})
    if "medium" in lengths:
        return "medium"
    return next(iter(lengths.keys()), "medium")


def select_primary_keyword(product: Dict[str, Any]) -> str:
    if "primary_keyword" in product:
        return product["primary_keyword"]

    seo_engine = get_engine("seo") or {}
    pools = seo_engine.get("keyword_pools", {})
    default_pool = ensure_list(pools.get("default"))
    if default_pool:
        with_seed(product.get("handle"), product.get("title"))
        return random.choice(default_pool)

    return "luxury"


def select_vocabulary_pool(persona: str) -> Dict[str, List[str]]:
    vocab_engine = get_engine("vocab") or {}
    persona_pools = vocab_engine.get("persona_pools", {})
    return persona_pools.get(persona, vocab_engine.get("default_pools", {}))


# -----------------------------
# CORE: METAFIELD + TITLE HOOKS
# -----------------------------

def build_metafields(product: Dict[str, Any]) -> Dict[str, Any]:
    metafields_engine = get_engine("metafields") or {}
    # placeholder: later use metafields_engine rules
    return product.get("metafields", {})


def build_title(product: Dict[str, Any]) -> str:
    if product.get("title"):
        return product["title"]

    title_engine = get_engine("title") or {}
    patterns = ensure_list(title_engine.get("patterns", []))
    base = sanitize_text(
        product.get("base_title")
        or product.get("handle")
        or "MVQueen Product"
    )

    if not patterns:
        return base

    with_seed(product.get("handle"), base)
    pattern = random.choice(patterns)
    return pattern.format(base=base)


# -----------------------------
# CORE: IO HELPERS
# -----------------------------

def load_json(path: str | Path) -> Any:
    p = Path(path)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def save_json(path: str | Path, data: Any) -> None:
    p = Path(path)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")