#!/usr/bin/env python3
"""Verify the MVQUEEN deployment target remains an unpublished Shopify theme.

Input: Shopify CLI `theme list --json` output file.
This intentionally fails if the target theme is missing or becomes MAIN/live.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "theme-list.json")
    if not path.is_file():
        print(f"THEME DEPLOYMENT VERIFY: FAIL — missing {path}")
        return 1

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"THEME DEPLOYMENT VERIFY: FAIL — invalid JSON: {exc}")
        return 1

    target = str(os.environ.get("SHOPIFY_THEME_ID", "")).split("/")[-1]
    if not target:
        print("THEME DEPLOYMENT VERIFY: FAIL — SHOPIFY_THEME_ID is not set")
        return 1

    themes = data.get("themes") or data.get("data", {}).get("themes", {}).get("nodes", [])
    found = None
    for theme in themes:
        theme_id = str(theme.get("id", "")).split("/")[-1]
        if theme_id == target:
            found = theme
            break

    if found is None:
        print(f"THEME DEPLOYMENT VERIFY: FAIL — target theme {target} not found")
        return 1

    role = str(found.get("role", "")).upper()
    name = found.get("name", "unknown")
    print(f"Target theme: {name}")
    print(f"Target role: {role or 'UNKNOWN'}")
    print(f"Target ID: {target}")

    if role == "MAIN":
        print("THEME DEPLOYMENT VERIFY: FAIL — target became the live theme")
        return 1

    print("THEME DEPLOYMENT VERIFY: PASS — target remains unpublished")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
