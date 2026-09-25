#!/usr/bin/env python3
"""MVQUEEN enterprise integrity crawler.

Read-only scanner for repository/workspace content. It detects duplicate assets,
configuration drift, risky placeholders, syntax/JSON failures, legacy brands,
Shopify contract contradictions, unsafe write signals, and conversion/content
quality signals. It never publishes, deletes, merges, or changes Shopify data.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

EXCLUDED = {".git", ".venv", "__pycache__", "node_modules", "build", ".pytest_cache", ".trash", "_BACKUPS", "98_Archive"}
TEXT_EXT = {".py",".js",".jsx",".ts",".tsx",".json",".md",".txt",".html",".css",".liquid",".yml",".yaml",".toml",".ini",".cfg",".csv",".graphql",".gql",".sh"}
CANONICAL_BRAND = "MVQueen"
CANONICAL_STORE = "tsucu0-1i.myshopify.com"
CANONICAL_API = "2026-07"
LEGACY_BRANDS = (
    "OU" + "HOE",
    "MISS" + ".QUEEN",
    "Miss" + ". Queen",
    "Hoe" + "goa",
    "Fan" + "zhen",
    "eel" + "hope",
    "Color" + " Fit",
    "West" + " & Month",
)
# These files intentionally contain forbidden-brand strings as detection rules,
# test fixtures, or explicit historical/reference policy. Do not flag the rule
# itself as contamination.
BRAND_REFERENCE_ALLOWLIST = {
    "core/brand_linter.py",
    "15_Scripts_And_Code/mvqueen_engine/brand_governance.py",
    "30_System_Infrastructure/catalog/mvqueen_catalog_worker.py",
    "30_System_Infrastructure/automation/validate_theme_contract.py",
    "PRODUCTION_READINESS/MVQUEEN_CATALOG_CONTRACT_V1.md",
    "PRODUCTION_READINESS/UNIFIED_SYSTEM_CONTRACT.md",
    "PRODUCTION_READINESS/test_branch_consolidation.py",
    "PRODUCTION_READINESS/test_catalog_recovery_transform.py",
    "PRODUCTION_READINESS/test_catalog_recovery_controls.py",
    "PRODUCTION_READINESS/test_catalog_recovery_audit.py",
}
PROTECTED_TERMS = ("Variant SKU","Variant Inventory Qty","Variant Price","Variant Compare At Price","Handle")
API_RE = re.compile(r"\b20\d{2}-(?:01|04|07|10)\b")
STORE_RE = re.compile(r"\b[a-z0-9][a-z0-9-]*\.myshopify\.com\b", re.I)
TODO_RE = re.compile(r"\b(TODO|FIXME|HACK|XXX)\b")
SECRET_RE = re.compile(r"(?i)\b(api[_-]?key|access[_-]?token|client[_-]?secret|password|private[_-]?key)\b\s*[:=]\s*['\"]([^'\"\n]{8,})")
PLACEHOLDER_RE = re.compile(r"(?i)^(?:replace.*|change.*|example|placeholder|dummy|test|secret|token|<[^>]+>|\$\{[^}]+\})$")
WRITE_RE = re.compile(r"\b(requests\.(?:post|put|patch|delete)|productUpdate|productCreate|metafieldsSet|inventoryAdjustQuantities|inventorySetQuantities)\b")
CONVERSION_TERMS = ("add to cart","shipping","returns","size guide","reviews","related products","you may also like","email","newsletter")

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def add(findings, severity, category, path, message, confidence="verified", conversion="none"):
    findings.append({"severity":severity,"category":category,"path":path,"message":message,"confidence":confidence,"conversion_impact":conversion})

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--output", default="build/enterprise_crawler/report.json")
    ap.add_argument("--fail-on", choices=("blocker","critical","high","none"), default="critical")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    findings, records, by_hash = [], [], defaultdict(list)
    api_versions, stores = defaultdict(set), defaultdict(set)
    conversion_hits = Counter()

    for p in root.rglob("*"):
        if not p.is_file():
            continue
        relp = p.relative_to(root)
        if any(part in EXCLUDED for part in relp.parts):
            continue
        rel = relp.as_posix()
        digest = sha256(p)
        records.append({"path":rel,"sha256":digest,"size":p.stat().st_size})
        by_hash[digest].append(rel)

        if p.suffix.lower() not in TEXT_EXT and p.name not in {".env.example","Dockerfile","package.json"}:
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        if p.suffix == ".py":
            try: ast.parse(text, filename=rel)
            except SyntaxError as e: add(findings,"BLOCKER","syntax",rel,f"Python syntax error line {e.lineno}: {e.msg}")
        if p.suffix == ".json":
            try: json.loads(text)
            except json.JSONDecodeError as e: add(findings,"BLOCKER","syntax",rel,f"Invalid JSON line {e.lineno}: {e.msg}")

        for m in API_RE.finditer(text): api_versions[m.group(0)].add(rel)
        for m in STORE_RE.finditer(text): stores[m.group(0).lower()].add(rel)
        for m in TODO_RE.finditer(text): add(findings,"LOW","unfinished_work",rel,f"{m.group(1)} marker remains")
        if rel not in BRAND_REFERENCE_ALLOWLIST:
            for brand in LEGACY_BRANDS:
                if brand.lower() in text.lower():
                    add(findings,"MEDIUM","brand_drift",rel,f"Legacy/supplier brand reference: {brand}","review")
        for m in SECRET_RE.finditer(text):
            value=m.group(2).strip()
            if value and not PLACEHOLDER_RE.match(value):
                add(findings,"CRITICAL","security",rel,f"Possible committed credential assignment for {m.group(1)}")
        if WRITE_RE.search(text) and "dry_run" not in text.lower() and "MVQ_WRITE_ENABLED" not in text:
            add(findings,"HIGH","publishing_boundary",rel,"Write-capable signal without an obvious local dry-run/write-enable guard","review")
        for term in CONVERSION_TERMS:
            if term in text.lower(): conversion_hits[term]+=1

    for digest, paths in by_hash.items():
        if len(paths)>1:
            add(findings,"LOW","duplication",paths[0],f"Identical content appears in {len(paths)} paths","verified")

    noncanonical_api={v:sorted(paths) for v,paths in api_versions.items() if v != CANONICAL_API}
    noncanonical_store={v:sorted(paths) for v,paths in stores.items() if v != CANONICAL_STORE}
    for version, paths in noncanonical_api.items():
        add(findings,"HIGH","config_drift",paths[0],f"Non-canonical Shopify API version {version} appears in {len(paths)} file(s)")
    for domain, paths in noncanonical_store.items():
        add(findings,"CRITICAL","config_drift",paths[0],f"Non-canonical Shopify store domain {domain} appears in {len(paths)} file(s)")

    severity_order={"BLOCKER":5,"CRITICAL":4,"HIGH":3,"MEDIUM":2,"LOW":1,"INFO":0}
    counts=Counter(f["severity"] for f in findings)
    findings.sort(key=lambda x:(-severity_order[x["severity"]],x["category"],x["path"]))
    report={
      "schema_version":"2.0",
      "system":"MVQUEEN Enterprise Reliability & Conversion Overseer",
      "canonical":{"brand":CANONICAL_BRAND,"shopify_store":CANONICAL_STORE,"shopify_api_version":CANONICAL_API},
      "files_scanned":len(records),
      "duplicate_groups":sum(1 for x in by_hash.values() if len(x)>1),
      "severity_counts":dict(counts),
      "configuration":{"api_versions":{k:sorted(v) for k,v in api_versions.items()},"shopify_domains":{k:sorted(v) for k,v in stores.items()}},
      "conversion_signal_coverage":dict(conversion_hits),
      "findings":findings,
      "governance":"Discover → Correlate → Diagnose → Propose → Approve → Repair → Test → Verify → Log",
      "mutation_policy":"READ_ONLY: crawler never publishes, deletes, merges, changes inventory/pricing/variants, or mutates Shopify."
    }
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2),encoding="utf-8")
    md=out.with_suffix(".md")
    lines=["# MVQUEEN Enterprise Crawler Report","",f"- Files scanned: **{len(records)}**",f"- Duplicate groups: **{report['duplicate_groups']}**","", "## Severity"]
    for sev in ("BLOCKER","CRITICAL","HIGH","MEDIUM","LOW"): lines.append(f"- {sev}: **{counts.get(sev,0)}**")
    lines += ["","## Governance",report["governance"],"",report["mutation_policy"]]
    md.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps({"files_scanned":len(records),"severity_counts":dict(counts),"report":str(out)},indent=2))
    thresholds={"blocker":5,"critical":4,"high":3,"none":99}
    threshold=thresholds[args.fail_on]
    return 1 if any(severity_order[f["severity"]] >= threshold for f in findings) else 0

if __name__=="__main__":
    raise SystemExit(main())
