#!/usr/bin/env python3
"""Continuous read-only MVQUEEN Overseer + specialist-agent worker."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTERVAL_SECONDS = max(300, int(os.environ.get("MVQ_AGENT_WORKER_INTERVAL_SECONDS", "900")))
RUN_ONCE = os.environ.get("MVQ_AGENT_WORKER_ONCE", "false").lower() == "true"


def stamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, cwd=ROOT, check=True)


def cycle() -> dict:
    with tempfile.TemporaryDirectory(prefix="mvq-agent-") as td:
        base = Path(td)
        crawler = base / "report.json"
        assignments = base / "assignments.json"
        execution = base / "execution.json"

        run([sys.executable, "core/vault_crawler.py", "--root", ".", "--output", str(crawler), "--fail-on", "none"])
        run([
            sys.executable,
            "30_System_Infrastructure/overseer/route_findings.py",
            "--input", str(crawler),
            "--output", str(assignments),
        ])
        run([
            sys.executable,
            "30_System_Infrastructure/overseer/agent_executor.py",
            "--input", str(assignments),
            "--registry", "30_System_Infrastructure/overseer/agent_registry.json",
            "--output", str(execution),
        ])

        report = json.loads(execution.read_text(encoding="utf-8"))
        return {
            "timestamp": stamp(),
            "registered_agents": report["registered_agent_count"],
            "runs": report["run_count"],
            "release_counts": report["release_counts"],
            "production_mutation_performed": report["production_mutation_performed"],
        }


def main() -> int:
    print(json.dumps({
        "event": "mvqueen_agent_worker_started",
        "timestamp": stamp(),
        "interval_seconds": INTERVAL_SECONDS,
        "run_once": RUN_ONCE,
        "mutation_policy": "read_only_analysis_and_recommendation",
    }))
    while True:
        started = time.monotonic()
        try:
            summary = cycle()
            summary["event"] = "mvqueen_agent_cycle_completed"
            summary["duration_seconds"] = round(time.monotonic() - started, 3)
            print(json.dumps(summary), flush=True)
        except Exception as exc:
            print(json.dumps({
                "event": "mvqueen_agent_cycle_failed",
                "timestamp": stamp(),
                "error_type": type(exc).__name__,
                "error": str(exc),
            }), file=sys.stderr, flush=True)
        if RUN_ONCE:
            return 0
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    raise SystemExit(main())
