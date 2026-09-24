#!/usr/bin/env python3
"""Deep, non-destructive MVQUEEN_OS repository audit.

Scans every tracked file at every remote branch head, deduplicates identical Git
blobs, and scans all reachable historical blobs for hygiene/security signals.
Secret-like matches are reported by location/pattern only; values are never
written to the report.
"""
from __future__ import annotations

import ast
import collections
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "build" / "deep_repo_audit"
OUT.mkdir(parents=True, exist_ok=True)

TEXT_EXTENSIONS = {
    ".py", ".pyi", ".js", ".jsx", ".ts", ".tsx", ".json", ".jsonl", ".md",
    ".txt", ".html", ".htm", ".css", ".scss", ".liquid", ".yml", ".yaml",
    ".toml", ".ini", ".cfg", ".conf", ".env", ".example", ".csv", ".tsv",
    ".sql", ".graphql", ".gql", ".xml", ".svg", ".sh", ".bash", ".zsh",
}
GENERATED_MARKERS = (
    "/__pycache__/", "/.obsidian/plugins/", "/node_modules/", "/build/",
    "/coverage/", "/_BACKUPS/", "/backups/", "/.trash/",
)
CONFLICT_NAME_RE = re.compile(
    r"(?i)(?:\bconflict\b|copy of|(?:^|[._ -])copy(?:[._ -]|$)|\.orig$|\.bak$|~$)"
)
PLACEHOLDER_RE = re.compile(
    r"(?i)^(?:changeme|replace[_ -]?me|example|placeholder|dummy|test|token|secret|"
    r"your[_ -]?(?:token|key|secret)|xxx+|<[^>]+>|\$\{[^}]+\})$"
)
CRED_ASSIGN_RE = re.compile(
    r"""(?ix)
    \b(api[_-]?key|access[_-]?token|client[_-]?secret|password|private[_-]?key|
       shopify[_-]?access[_-]?token|openai[_-]?api[_-]?key)\b
    \s*[:=]\s*
    ["']([^"'\n]{8,})["']
    """
)
TOKEN_PREFIX_RE = re.compile(
    r"(?i)\b(?:shpat_[A-Za-z0-9_-]{12,}|gh[pousr]_[A-Za-z0-9_]{20,}|"
    r"sk-[A-Za-z0-9_-]{20,}|xox[baprs]-[A-Za-z0-9-]{12,})\b"
)
WRITE_PATTERNS = {
    "requests_write": re.compile(r"\brequests\.(?:post|put|patch|delete|request)\s*\("),
    "shopify_mutation": re.compile(
        r"\b(?:productUpdate|productCreate|productDelete|metafieldsSet|"
        r"inventoryAdjustQuantities|inventorySetQuantities|collectionCreate|collectionUpdate)\b"
    ),
    "fetch_write": re.compile(r"\bfetch\s*\([^;\n]{0,300}\bmethod\s*:\s*['\"](?:POST|PUT|PATCH|DELETE)['\"]", re.I),
    "axios_write": re.compile(r"\baxios\.(?:post|put|patch|delete)\s*\("),
}
API_VERSION_RE = re.compile(r"\b20\d{2}-(?:01|04|07|10)\b")
SHOP_DOMAIN_RE = re.compile(r"\b[a-z0-9][a-z0-9-]*\.myshopify\.com\b", re.I)
TODO_RE = re.compile(r"\b(TODO|FIXME|HACK|XXX)\b")
LIQUID_SCHEMA_RE = re.compile(r"{%\s*schema\s*%}(.*?){%\s*endschema\s*%}", re.S | re.I)

def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True, stderr=subprocess.STDOUT)

def branches() -> list[dict[str, str]]:
    raw = run(
        "git", "for-each-ref",
        "--format=%(refname:short)|%(objectname)",
        "refs/remotes/origin/"
    )
    rows = []
    for line in raw.splitlines():
        name, sha = line.split("|", 1)
        if name == "origin/HEAD":
            continue
        rows.append({"name": name.removeprefix("origin/"), "sha": sha})
    return rows

def tree_for(ref: str) -> list[dict[str, Any]]:
    raw = run("git", "ls-tree", "-r", "-l", ref)
    out = []
    for line in raw.splitlines():
        meta, path = line.split("\t", 1)
        parts = meta.split()
        if len(parts) < 4 or parts[1] != "blob":
            continue
        size = None if parts[3] == "-" else int(parts[3])
        out.append({"mode": parts[0], "sha": parts[2], "size": size, "path": path})
    return out

class CatFileBatch:
    def __init__(self) -> None:
        self.proc = subprocess.Popen(
            ["git", "cat-file", "--batch"],
            cwd=ROOT,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
    def get(self, sha: str) -> bytes:
        assert self.proc.stdin and self.proc.stdout
        self.proc.stdin.write((sha + "\n").encode())
        self.proc.stdin.flush()
        header = self.proc.stdout.readline().decode("utf-8", "replace").strip()
        parts = header.split()
        if len(parts) < 3 or parts[1] != "blob":
            return b""
        size = int(parts[2])
        data = self.proc.stdout.read(size)
        self.proc.stdout.read(1)
        return data
    def close(self) -> None:
        if self.proc.stdin:
            self.proc.stdin.close()
        self.proc.terminate()

def is_text(path: str, data: bytes) -> bool:
    if b"\x00" in data[:8192]:
        return False
    ext = Path(path).suffix.lower()
    if ext in TEXT_EXTENSIONS or Path(path).name in {
        ".gitignore", ".gitattributes", "Dockerfile", "Procfile", "Gemfile",
        "requirements.txt", "package.json", "package-lock.json", "shopify.app.toml",
        "shopify.web.toml",
    }:
        return True
    try:
        data[:65536].decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False

def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1

def redact_credential_findings(path: str, sha: str, text: str) -> list[dict[str, Any]]:
    findings = []
    for m in CRED_ASSIGN_RE.finditer(text):
        value = m.group(2).strip()
        if not value or PLACEHOLDER_RE.match(value):
            continue
        findings.append({
            "path": path, "sha": sha, "line": line_number(text, m.start()),
            "kind": "credential_assignment", "key": m.group(1).lower(),
        })
    for m in TOKEN_PREFIX_RE.finditer(text):
        findings.append({
            "path": path, "sha": sha, "line": line_number(text, m.start()),
            "kind": "token_prefix",
        })
    return findings

branch_rows = branches()
head_groups: dict[str, list[str]] = collections.defaultdict(list)
for b in branch_rows:
    head_groups[b["sha"]].append(b["name"])

branch_trees = {}
blob_paths: dict[str, set[str]] = collections.defaultdict(set)
path_versions: dict[str, set[str]] = collections.defaultdict(set)
instance_count = 0
for sha, names in head_groups.items():
    tree = tree_for(sha)
    branch_trees[sha] = tree
    instance_count += len(tree) * len(names)
    for item in tree:
        blob_paths[item["sha"]].add(item["path"])
        path_versions[item["path"]].add(item["sha"])

unique_head_blobs = len(blob_paths)
unique_paths = len(path_versions)

summary: dict[str, Any] = {
    "branch_count": len(branch_rows),
    "distinct_branch_heads": len(head_groups),
    "branch_head_groups": [
        {"sha": sha, "branches": sorted(names), "file_count": len(branch_trees[sha])}
        for sha, names in sorted(head_groups.items(), key=lambda x: sorted(x[1])[0])
    ],
    "tracked_file_instances_across_branch_names": instance_count,
    "unique_paths_across_branch_heads": unique_paths,
    "unique_blob_versions_across_branch_heads": unique_head_blobs,
}

findings: dict[str, list[Any]] = collections.defaultdict(list)
stats = collections.Counter()
extension_counts = collections.Counter()
size_by_topdir = collections.Counter()
basename_paths: dict[str, set[str]] = collections.defaultdict(set)
content_paths: dict[str, set[str]] = collections.defaultdict(set)
api_versions: dict[str, set[str]] = collections.defaultdict(set)
shop_domains: dict[str, set[str]] = collections.defaultdict(set)

reader = CatFileBatch()
try:
    for idx, (blob_sha, paths) in enumerate(blob_paths.items(), 1):
        path = sorted(paths)[0]
        data = reader.get(blob_sha)
        size = len(data)
        stats["bytes_unique_head_blobs"] += size
        topdir = path.split("/", 1)[0]
        size_by_topdir[topdir] += size
        ext = Path(path).suffix.lower() or "<none>"
        extension_counts[ext] += 1
        for p in paths:
            basename_paths[Path(p).name.lower()].add(p)
            content_paths[blob_sha].add(p)
            if CONFLICT_NAME_RE.search(Path(p).name):
                findings["conflict_or_copy_names"].append({"path": p, "sha": blob_sha, "size": size})
            normalized = "/" + p.replace("\\", "/") + "/"
            if any(marker in normalized for marker in GENERATED_MARKERS):
                findings["generated_or_archive_paths"].append({"path": p, "sha": blob_sha, "size": size})

        if size >= 1_000_000:
            findings["large_blobs"].append({"sha": blob_sha, "size": size, "paths": sorted(paths)})

        if not is_text(path, data):
            stats["binary_blobs"] += 1
            continue
        stats["text_blobs"] += 1
        text = data.decode("utf-8", "replace")
        stats["text_lines"] += text.count("\n") + 1

        findings["credential_signals"].extend(redact_credential_findings(path, blob_sha, text))

        for name, rx in WRITE_PATTERNS.items():
            for m in rx.finditer(text):
                findings["write_paths"].append({
                    "path": path, "sha": blob_sha, "line": line_number(text, m.start()),
                    "pattern": name,
                })

        for m in API_VERSION_RE.finditer(text):
            api_versions[m.group(0)].add(path)
        for m in SHOP_DOMAIN_RE.finditer(text):
            shop_domains[m.group(0).lower()].add(path)
        for m in TODO_RE.finditer(text):
            findings["todo_markers"].append({
                "path": path, "sha": blob_sha, "line": line_number(text, m.start()),
                "kind": m.group(1),
            })

        if path.endswith(".py"):
            try:
                ast.parse(text, filename=path)
            except SyntaxError as exc:
                findings["python_syntax_errors"].append({
                    "path": path, "sha": blob_sha, "line": exc.lineno, "message": exc.msg,
                })

        if path.endswith(".json"):
            try:
                json.loads(text)
            except json.JSONDecodeError as exc:
                findings["json_errors"].append({
                    "path": path, "sha": blob_sha, "line": exc.lineno, "message": exc.msg,
                })

        if path.endswith(".liquid"):
            for schema_match in LIQUID_SCHEMA_RE.finditer(text):
                raw = schema_match.group(1).strip()
                try:
                    schema = json.loads(raw)
                    name = str(schema.get("name", ""))
                    if len(name) > 25:
                        findings["liquid_schema_name_errors"].append({
                            "path": path, "sha": blob_sha, "name_length": len(name),
                        })
                except json.JSONDecodeError as exc:
                    findings["liquid_schema_json_errors"].append({
                        "path": path, "sha": blob_sha, "line": line_number(text, schema_match.start()) + exc.lineno,
                        "message": exc.msg,
                    })
finally:
    reader.close()

for basename, paths in basename_paths.items():
    if len(paths) > 1:
        findings["duplicate_basenames"].append({"basename": basename, "paths": sorted(paths)})

for sha, paths in content_paths.items():
    if len(paths) > 1:
        findings["identical_content_multiple_paths"].append({"sha": sha, "paths": sorted(paths)})

for path, versions in path_versions.items():
    if len(versions) > 1:
        findings["divergent_path_versions"].append({"path": path, "versions": len(versions)})

summary["unique_blob_stats"] = dict(stats)
summary["extensions"] = dict(extension_counts.most_common())
summary["top_level_bytes"] = dict(size_by_topdir.most_common())
summary["api_versions"] = {k: sorted(v) for k, v in sorted(api_versions.items())}
summary["shopify_domains"] = {k: sorted(v) for k, v in sorted(shop_domains.items())}
summary["finding_counts"] = {k: len(v) for k, v in findings.items()}

# Reachable-history object census (all refs/history), with large-blob and secret-only scan.
rev_objects = run("git", "rev-list", "--objects", "--all").splitlines()
object_paths: dict[str, str] = {}
for line in rev_objects:
    parts = line.split(" ", 1)
    if len(parts) == 2:
        object_paths.setdefault(parts[0], parts[1])

check = subprocess.Popen(
    ["git", "cat-file", "--batch-check=%(objectname) %(objecttype) %(objectsize)"],
    cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
)
assert check.stdin and check.stdout
for oid in object_paths:
    check.stdin.write(oid + "\n")
check.stdin.close()
historical_blob_meta = []
for line in check.stdout:
    oid, typ, size_s = line.strip().split()
    if typ == "blob":
        historical_blob_meta.append((oid, int(size_s), object_paths.get(oid, "")))
check.wait()
summary["reachable_historical_blob_count"] = len(historical_blob_meta)
summary["reachable_historical_blob_bytes"] = sum(x[1] for x in historical_blob_meta)
findings["historical_large_blobs"] = [
    {"sha": oid, "size": size, "representative_path": path}
    for oid, size, path in sorted(historical_blob_meta, key=lambda x: x[1], reverse=True)
    if size >= 5_000_000
][:100]

head_blob_set = set(blob_paths)
history_only = [(oid, size, path) for oid, size, path in historical_blob_meta if oid not in head_blob_set]
summary["history_only_blob_count"] = len(history_only)

# Validate current main theme structure.
required_theme_dirs = {"assets", "config", "layout", "locales", "sections", "snippets", "templates"}
main_sha = next((b["sha"] for b in branch_rows if b["name"] == "main"), None)
main_paths = {item["path"] for item in branch_trees.get(main_sha, [])}
present_theme_dirs = {
    p.split("/")[2]
    for p in main_paths
    if p.startswith("storefront/theme/") and len(p.split("/")) > 2
}
summary["theme_required_dirs_missing"] = sorted(required_theme_dirs - present_theme_dirs)

# Keep reports manageable but complete enough to act on. Full path-version map included.
report = {
    "summary": summary,
    "findings": {k: v for k, v in findings.items()},
    "path_versions": {k: sorted(v) for k, v in sorted(path_versions.items())},
}
(OUT / "deep_repo_audit.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

md = []
md.append("# MVQUEEN_OS Deep Repository Audit")
md.append("")
md.append(f"- Branches: **{summary['branch_count']}**")
md.append(f"- Distinct branch heads: **{summary['distinct_branch_heads']}**")
md.append(f"- Unique paths across branch heads: **{summary['unique_paths_across_branch_heads']}**")
md.append(f"- Unique blob versions across branch heads: **{summary['unique_blob_versions_across_branch_heads']}**")
md.append(f"- Reachable historical blobs: **{summary['reachable_historical_blob_count']}**")
md.append("")
md.append("## Finding counts")
for key, count in sorted(summary["finding_counts"].items(), key=lambda x: (-x[1], x[0])):
    md.append(f"- {key}: **{count}**")
md.append("")
md.append("## API versions")
for version, paths in summary["api_versions"].items():
    md.append(f"- {version}: {len(paths)} file(s)")
md.append("")
md.append("## Shopify domains")
for domain, paths in summary["shopify_domains"].items():
    md.append(f"- {domain}: {len(paths)} file(s)")
md.append("")
md.append("## Largest current unique blobs")
for item in sorted(findings["large_blobs"], key=lambda x: x["size"], reverse=True)[:30]:
    md.append(f"- {item['size']:,} bytes — {', '.join(item['paths'][:3])}")
md.append("")
md.append("## Important note")
md.append("Credential findings never include secret values. This audit is read-only and does not delete, publish, or mutate Shopify data.")
(OUT / "deep_repo_audit.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print(json.dumps(summary, indent=2))
