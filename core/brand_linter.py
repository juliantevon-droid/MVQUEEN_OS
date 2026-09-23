#!/usr/bin/env python3
"""MVQUEEN product-content governance linter.

Deterministic rules are authoritative. Optional AI review is advisory only.
The linter never edits source product files.
"""
from __future__ import annotations

import argparse, json, os, re, sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

FORBIDDEN_BRANDS = {
    "ouhoe", "miss.queen", "miss queen", "hoegoa", "fanzhen",
    "eelhope", "color fit", "west & month",
}
PRIMARY_KEYWORDS = {
    "women's fashion", "luxury women's clothing", "elegant women's wear",
}
MAX_TITLE = 70
MAX_META_TITLE = 65
MAX_META_DESCRIPTION = 160
CANONICAL_BRAND = "MVQueen"

def normalize(value):
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value).strip()

def text_fields(record):
    keys = (
        "title", "product_title", "description", "body_html", "body",
        "seo_title", "meta_title", "seo_description", "meta_description",
        "short_description", "vendor", "brand", "product_type", "tags",
    )
    return {k: normalize(record.get(k)) for k in keys if k in record}

def forbidden_hits(text):
    low = text.lower()
    return sorted(x for x in FORBIDDEN_BRANDS if x in low)

def parse_json(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        return [data]
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    raise ValueError("JSON root must be an object or array of objects")

def parse_markdown(path):
    raw = path.read_text(encoding="utf-8")
    title = ""
    m = re.search(r"^#\s+(.+)$", raw, re.M)
    if m:
        title = m.group(1).strip()
    sections = {}
    current = None
    buf = []
    for line in raw.splitlines():
        hm = re.match(r"^#{1,3}\s+(.+)$", line)
        if hm:
            if current:
                sections[current] = "\n".join(buf).strip()
            current = hm.group(1).strip().lower().replace(" ", "_")
            buf = []
        elif current:
            buf.append(line)
    if current:
        sections[current] = "\n".join(buf).strip()
    return [{
        "title": title,
        "description": raw,
        "short_description": sections.get("short_description", ""),
        "seo_title": sections.get("seo_title", ""),
        "seo_description": sections.get("seo_description", ""),
    }]

def load_products(root):
    paths = [p for p in Path(root).rglob("*") if p.is_file() and p.suffix.lower() in {".json", ".md", ".markdown"}]
    for path in paths:
        try:
            records = parse_json(path) if path.suffix.lower() == ".json" else parse_markdown(path)
            for index, record in enumerate(records):
                yield path, index, record
        except Exception as exc:
            yield path, -1, {"__parse_error__": str(exc)}

def deterministic(record):
    issues, warnings = [], []
    if "__parse_error__" in record:
        return "HOLD", [f"Parse error: {record['__parse_error__']}"], warnings

    fields = text_fields(record)
    combined = "\n".join(fields.values())
    hits = forbidden_hits(combined)
    if hits:
        issues.append("Forbidden/supplier/legacy brand reference: " + ", ".join(hits))

    title = fields.get("title") or fields.get("product_title")
    if not title:
        issues.append("Missing product title")
    elif len(title) > MAX_TITLE:
        warnings.append(f"Title exceeds {MAX_TITLE} characters")

    meta_title = fields.get("seo_title") or fields.get("meta_title")
    if meta_title and len(meta_title) > MAX_META_TITLE:
        warnings.append(f"SEO title exceeds {MAX_META_TITLE} characters")

    meta_desc = fields.get("seo_description") or fields.get("meta_description")
    if meta_desc and len(meta_desc) > MAX_META_DESCRIPTION:
        warnings.append(f"Meta description exceeds {MAX_META_DESCRIPTION} characters")

    description = fields.get("description") or fields.get("body_html") or fields.get("body")
    if not description:
        issues.append("Missing product description")

    if re.search(r"(?i)\\b(?:cure|treats?|guaranteed|100% effective|clinically proven)\\b", combined):
        issues.append("Potential unsupported/high-risk product claim; verify against source facts")

    if re.search(r"(?i)(buy now|act now|limited time|only today){2,}", combined):
        warnings.append("Urgency language is repetitive")

    if title and title.upper().count(title.upper().split()[0]) > 2:
        warnings.append("Title may contain repetitive wording")

    brand = fields.get("brand")
    if brand and brand.casefold() != CANONICAL_BRAND.casefold():
        issues.append(f"Non-canonical product brand: {brand}")

    keyword_count = sum(combined.lower().count(k) for k in PRIMARY_KEYWORDS)
    if keyword_count > 8:
        issues.append("Potential keyword stuffing")

    status = "HOLD" if issues else ("WARN" if warnings else "PASS")
    return status, issues, warnings

def ollama_review(record, host, model):
    prompt = {
        "role": "system",
        "content": (
            "Audit MVQueen product copy. Do not invent facts. Return JSON only with "
            "status PASS/WARN/HOLD, issues[], warnings[], and rationale. Evaluate "
            "clarity, confident elegant tone, natural SEO, repetition, and unsupported claims."
        ),
    }
    payload = {"model": model, "messages": [prompt, {"role": "user", "content": json.dumps(record, ensure_ascii=False)}], "stream": False}
    req = Request(host.rstrip("/") + "/api/chat", data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(req, timeout=20) as response:
        data = json.loads(response.read().decode())
    content = data.get("message", {}).get("content", "{}")
    return json.loads(content)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="04_Products")
    ap.add_argument("--output", default="build/brand_lint_report.json")
    ap.add_argument("--provider", choices=["auto", "ollama", "none"], default="auto")
    ap.add_argument("--ollama-host", default=os.getenv("OLLAMA_HOST", "http://localhost:11434"))
    ap.add_argument("--ollama-model", default=os.getenv("OLLAMA_MODEL", "llama3.1:8b"))
    ap.add_argument("--fail-on", choices=["hold", "warn"], default="hold")
    args = ap.parse_args()

    results, counts = [], {"PASS": 0, "WARN": 0, "HOLD": 0}
    files_seen = 0
    for path, index, record in load_products(args.input):
        files_seen += 1
        status, issues, warnings = deterministic(record)
        ai = None
        if args.provider in {"auto", "ollama"} and status != "HOLD":
            try:
                ai = ollama_review(record, args.ollama_host, args.ollama_model)
                ai_status = str(ai.get("status", "")).upper()
                if ai_status == "HOLD":
                    status = "HOLD"
                elif ai_status == "WARN" and status == "PASS":
                    status = "WARN"
                issues.extend([str(x) for x in ai.get("issues", [])])
                warnings.extend([str(x) for x in ai.get("warnings", [])])
            except (URLError, HTTPError, TimeoutError, json.JSONDecodeError, OSError) as exc:
                warnings.append(f"AI review unavailable; deterministic rules used: {exc.__class__.__name__}")

        counts[status] += 1
        results.append({
            "file": str(path),
            "record_index": index,
            "status": status,
            "issues": issues,
            "warnings": warnings,
            "ai_review": ai,
        })

    report = {
        "schema_version": "1.1",
        "release_gate": {
            "eligible": counts["HOLD"] == 0 and not (args.fail_on == "warn" and counts["WARN"] > 0),
            "policy": "Deterministic HOLD findings block release; WARN findings block release when --fail-on warn is selected.",
        },
        "brand": "MVQUEEN",
        "input": args.input,
        "files_seen": files_seen,
        "counts": counts,
        "results": results,
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps({"files_seen": files_seen, "counts": counts, "report": str(out)}, indent=2))
    if counts["HOLD"] > 0 or (args.fail_on == "warn" and counts["WARN"] > 0):
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
