#!/usr/bin/env python3
"""Execute MVQUEEN specialist-agent analysis over routed Overseer findings.

This runtime is intentionally fail-closed. It turns routed findings into
specialist analysis, QA requirements, and release dispositions. It never
mutates Shopify, GitHub, Railway, credentials, inventory, pricing, variants,
handles, or theme publication state.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BLOCKING = {"BLOCKER", "CRITICAL", "HIGH"}

CATEGORY_PLAYBOOKS = {
    "syntax": {
        "diagnosis": "Code/configuration cannot be trusted until the parser or contract failure is corrected.",
        "recommendation": "Repair the smallest invalid syntax surface, then rerun syntax, unit, and affected integration checks.",
        "checks": ["syntax_validation", "targeted_unit_tests", "overseer_rerun"],
    },
    "duplication": {
        "diagnosis": "Identical content exists in multiple active paths and may create source-of-truth ambiguity.",
        "recommendation": "Classify each duplicate as canonical, generated, historical, or redundant before any consolidation.",
        "checks": ["source_of_truth_review", "reference_check", "regression_tests"],
    },
    "config_drift": {
        "diagnosis": "A runtime or Shopify configuration reference differs from the canonical system contract.",
        "recommendation": "Align only the active configuration path to the canonical value and preserve historical evidence where appropriate.",
        "checks": ["configuration_contract_test", "runtime_preflight", "integration_smoke_test"],
    },
    "unfinished_work": {
        "diagnosis": "An unfinished-work marker remains in an active path.",
        "recommendation": "Determine whether the marker represents required production work, intentional documentation, or removable technical debt.",
        "checks": ["owner_review", "targeted_tests"],
    },
    "brand_drift": {
        "diagnosis": "Non-canonical brand language appears in an active file.",
        "recommendation": "Replace operational contamination with canonical MVQueen language while preserving explicit fixtures and historical references.",
        "checks": ["brand_linter", "content_truth_review", "regression_tests"],
    },
    "security": {
        "diagnosis": "A security-sensitive pattern requires immediate review before production promotion.",
        "recommendation": "Contain exposure, remove unsafe committed material, rotate/revoke affected credentials outside this agent, and verify history plus permissions.",
        "checks": ["secret_scan", "credential_rotation_confirmation", "permission_review", "overseer_rerun"],
    },
    "publishing_boundary": {
        "diagnosis": "Write-capable code lacks an obvious local production safety boundary.",
        "recommendation": "Add or verify dry-run/write-enable gating and ensure the authenticated React app remains the only live Shopify writer.",
        "checks": ["write_gate_test", "shopify_transport_boundary_test", "release_review"],
    },
    "catalog": {
        "diagnosis": "Catalog evidence indicates a normalization, completeness, or taxonomy issue.",
        "recommendation": "Prepare a source-truth-preserving catalog correction and validate protected product fields before release.",
        "checks": ["catalog_contract_test", "protected_field_test", "sample_product_review"],
    },
    "seo": {
        "diagnosis": "Search-readiness evidence indicates metadata, linking, or structured-content work.",
        "recommendation": "Prepare factual SEO changes, then validate indexability and canonical brand/product truth.",
        "checks": ["seo_contract_review", "structured_data_validation", "content_truth_review"],
    },
    "conversion": {
        "diagnosis": "A conversion surface needs evidence-driven UX or merchandising review.",
        "recommendation": "Prepare the smallest measurable UX change and define the event or metric that will verify the outcome.",
        "checks": ["mobile_ux_review", "funnel_event_validation", "regression_tests"],
    },
    "accessibility": {
        "diagnosis": "An accessibility surface requires semantic, keyboard, or assistive-technology verification.",
        "recommendation": "Correct the smallest accessibility defect without reducing functionality or visual clarity.",
        "checks": ["semantic_check", "keyboard_check", "screen_reader_review"],
    },
    "performance": {
        "diagnosis": "A performance surface requires measured payload or rendering investigation.",
        "recommendation": "Profile first, change the verified bottleneck only, then compare before/after measurements.",
        "checks": ["performance_measurement", "mobile_performance_review", "regression_tests"],
    },
    "theme": {
        "diagnosis": "Theme evidence requires Liquid/storefront contract review.",
        "recommendation": "Prepare changes against the verified unpublished theme target and run theme checks before any publication.",
        "checks": ["theme_check", "mobile_render_review", "release_review"],
    },
    "mobile_ux": {
        "diagnosis": "The mobile purchase path requires interaction or responsive-layout review.",
        "recommendation": "Prioritize the smallest-screen purchase journey, then validate touch, layout, and checkout handoff.",
        "checks": ["mobile_viewport_test", "touch_target_review", "purchase_path_smoke_test"],
    },
    "merchandising": {
        "diagnosis": "Product discovery, collection, or recommendation evidence needs merchandising review.",
        "recommendation": "Prepare collection/navigation changes from verified catalog attributes and preserve dual-brand routing rules.",
        "checks": ["collection_membership_review", "navigation_test", "product_discovery_review"],
    },
    "metafields": {
        "diagnosis": "Structured product data needs schema or completeness review.",
        "recommendation": "Map only evidence-backed values into approved metafield definitions and leave unknown facts blank.",
        "checks": ["schema_validation", "factual_truth_review", "protected_field_test"],
    },
}

DEFAULT_PLAYBOOK = {
    "diagnosis": "The routed finding requires specialist review in its assigned domain.",
    "recommendation": "Inspect the cited evidence, propose the smallest reversible change, and verify it before release.",
    "checks": ["specialist_review", "qa_verification", "release_review"],
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def registry_index(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    agents = registry.get("agents", [])
    index = {a["id"]: a for a in agents}
    if len(index) != len(agents):
        raise ValueError("Agent registry contains duplicate ids")
    for required in ("qa", "release"):
        if required not in index:
            raise ValueError(f"Agent registry missing required agent: {required}")
    if any(a.get("can_mutate_production") for a in agents):
        raise ValueError("Fail-closed contract violated: production mutation authority detected")
    return index


def execute_assignment(item: dict[str, Any], agents: dict[str, dict[str, Any]]) -> dict[str, Any]:
    owner = item.get("owner", "qa")
    if owner not in agents:
        raise ValueError(f"Unknown routed owner: {owner}")
    reviewers = item.get("reviewers") or ["qa"]
    unknown = [r for r in reviewers if r not in agents]
    if unknown:
        raise ValueError(f"Unknown routed reviewers: {unknown}")

    category = item.get("category", "unknown")
    playbook = CATEGORY_PLAYBOOKS.get(category, DEFAULT_PLAYBOOK)
    severity = str(item.get("severity", "INFO")).upper()
    production_blocking = bool(item.get("production_blocking")) or severity in BLOCKING

    return {
        "finding_id": item.get("finding_id"),
        "owner": owner,
        "owner_name": agents[owner]["name"],
        "reviewers": reviewers,
        "severity": severity,
        "category": category,
        "path": item.get("path"),
        "evidence": {
            "message": item.get("message"),
            "confidence": item.get("confidence", "review"),
            "conversion_impact": item.get("conversion_impact", "none"),
        },
        "specialist_analysis": {
            "state": "completed",
            "diagnosis": playbook["diagnosis"],
            "recommendation": playbook["recommendation"],
            "proposed_change_authority": "recommend_only",
            "automatic_production_mutation": False,
        },
        "qa_verification": {
            "state": "pending_change" if production_blocking else "pending_review",
            "required_checks": playbook["checks"],
            "verifier": "qa",
            "automatic_pass_allowed": False,
        },
        "release_disposition": {
            "state": "HOLD" if production_blocking else "REVIEW",
            "production_blocking": production_blocking,
            "release_owner": "release",
            "reason": (
                "Blocking finding requires an approved change and verified QA evidence."
                if production_blocking
                else "Non-blocking finding remains tracked until reviewed or explicitly dispositioned."
            ),
        },
        "learning": {
            "candidate_allowed": True,
            "promotion_allowed_without_verification": False,
            "authority_growth_allowed": False,
        },
    }


def execute(assignments: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    agents = registry_index(registry)
    runs = [execute_assignment(item, agents) for item in assignments.get("assignments", [])]
    owner_counts = Counter(r["owner"] for r in runs)
    release_counts = Counter(r["release_disposition"]["state"] for r in runs)
    return {
        "schema_version": "1.0",
        "system": "MVQUEEN_OS Specialist Agent Execution Layer",
        "generated_at": utc_now(),
        "source": assignments.get("source"),
        "execution_mode": registry.get("execution_policy", {}).get("default_mode", "analysis_and_recommendation"),
        "registered_agents": sorted(agents),
        "registered_agent_count": len(agents),
        "run_count": len(runs),
        "owner_counts": dict(owner_counts),
        "release_counts": dict(release_counts),
        "production_mutation_performed": False,
        "approval_boundary": "Protected or production-changing actions require explicit approval and verified QA evidence.",
        "runs": runs,
    }


def write_markdown(report: dict[str, Any], path: str | Path) -> None:
    lines = [
        "# MVQUEEN Specialist Agent Execution Report",
        "",
        f"- Registered agents: **{report['registered_agent_count']}**",
        f"- Findings executed: **{report['run_count']}**",
        f"- Production mutation performed: **{str(report['production_mutation_performed']).lower()}**",
        "",
        "## Release disposition",
    ]
    if report["release_counts"]:
        for state, count in sorted(report["release_counts"].items()):
            lines.append(f"- {state}: **{count}**")
    else:
        lines.append("- CLEAR: **0 routed findings**")
    lines += [
        "",
        "## Approval boundary",
        report["approval_boundary"],
        "",
        "Specialist execution produces analysis and verification requirements; it does not silently change production.",
    ]
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="build/agents/assignments.json")
    ap.add_argument("--registry", default="30_System_Infrastructure/overseer/agent_registry.json")
    ap.add_argument("--output", default="build/agents/execution.json")
    args = ap.parse_args()

    assignments = load_json(args.input)
    registry = load_json(args.registry)
    report = execute(assignments, registry)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report, out.with_suffix(".md"))

    print(json.dumps({
        "registered_agents": report["registered_agent_count"],
        "runs": report["run_count"],
        "release_counts": report["release_counts"],
        "output": str(out),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
