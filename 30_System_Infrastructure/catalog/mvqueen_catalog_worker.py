#!/usr/bin/env python3
"""MVQUEEN catalog governance worker.

This worker is validation/artifact-only. It never writes to Shopify.
Live Shopify mutations are owned exclusively by the authenticated React Router
application after explicit product approval.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE_ROOT = REPO_ROOT / "15_Scripts_And_Code"
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

import json
import sys
from pathlib import Path

FORBIDDEN = [
    "MISS.QUEEN", "MISS. QUEEN", "OUHOE", "HOEGOA", "FANZHEN", "EELHOPE",
    "COLOR FIT", "WEST & MONTH", "EPROLO", "DROPSURE", "JAYSUING",
    "ROXELIS", "DESIRE GEM", "MIA JEWELRY",
    "SEPHORA", "VICTORIA'S SECRET", "VICTORIAS SECRET", "FENTY BEAUTY", "DIOR",
]
PROTECTED = {"handle", "sku", "inventory", "variants", "variant", "images", "image"}
REQUIRED_FACTS = {"title", "description_html", "seo_title", "seo_description"}


def fail(msg: str) -> None:
    raise ValueError(msg)


def validate_record(record: dict, line: int) -> dict:
    if not isinstance(record, dict):
        fail(f"line {line}: record must be an object")
    pid = record.get("id")
    if not pid:
        fail(f"line {line}: missing Shopify product id")
    if not record.get("verified_facts"):
        fail(f"line {line}: HOLD — verified_facts is required")

    content = record.get("optimized", {})
    missing = REQUIRED_FACTS - set(content)
    if missing:
        fail(f"line {line}: HOLD — missing optimized fields: {sorted(missing)}")

    blob = json.dumps(content, ensure_ascii=False).upper()
    for brand in FORBIDDEN:
        if brand in blob:
            fail(f"line {line}: forbidden supplier/legacy brand found: {brand}")

    protected = set(record.get("protected_changes", [])) & PROTECTED
    if protected:
        fail(f"line {line}: protected field change requested: {sorted(protected)}")

    if not isinstance(content.get("tags", []), list):
        fail(f"line {line}: tags must be a list")

    return {"id": pid, **content}


def main() -> int:
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("12_Content_Assets/drive_inbox/catalog_ready.jsonl")
    output = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("build/catalog/validated_catalog.jsonl")

    if not source.exists():
        print(f"No catalog input found: {source}")
        return 0

    records = []
    for n, raw in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        records.append(validate_record(json.loads(raw), n))

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records), encoding="utf-8")

    print(f"VALIDATION PASS: {len(records)} candidate(s); artifact={output}; Shopify writes disabled in this worker.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"CATALOG PIPELINE: HOLD/FAIL — {exc}")
        raise SystemExit(1)
