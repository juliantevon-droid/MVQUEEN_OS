#!/usr/bin/env python3
"""Portable MVQueen asset crawler for local and CI environments."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

EXCLUDED = {".git", ".venv", "__pycache__", "node_modules", "build", ".pytest_cache"}

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--output", default="build/vault_index.json")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    records, by_hash = [], {}
    for p in root.rglob("*"):
        if not p.is_file() or any(part in EXCLUDED for part in p.relative_to(root).parts):
            continue
        digest = sha256(p)
        rel = str(p.relative_to(root))
        records.append({"path": rel, "sha256": digest, "size": p.stat().st_size})
        by_hash.setdefault(digest, []).append(rel)
    duplicates = {k:v for k,v in by_hash.items() if len(v)>1}
    report = {"schema_version":"1.0","root":str(root),"files":len(records),"duplicates":duplicates,"assets":records}
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Indexed {len(records)} files; duplicate groups: {len(duplicates)}")
if __name__ == "__main__":
    main()
