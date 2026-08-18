from datetime import datetime, timezone
from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = ROOT / "30_System_Infrastructure" / "overseer" / "reports"
REPORT = REPORT_DIR / "MVQUEEN_OS_CURRENT_AUDIT.md"


def run_audit():
    runner = ROOT / "30_System_Infrastructure" / "audit" / "mvqueen_audit" / "runner.py"
    result = subprocess.run(["python", str(runner)], cwd=ROOT, text=True, capture_output=True)
    return result.returncode, result.stdout, result.stderr


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    code, stdout, stderr = run_audit()
    now = datetime.now(timezone.utc).isoformat()
    status = "PASS" if code == 0 else "FAIL"

    report = f'''# MVQUEEN_OS CURRENT OVERSEER AUDIT\n\nGenerated: {now}\nStatus: **{status}**\nExit Code: `{code}`\n\n## Audit Output\n\n```text\n{stdout.rstrip()}\n```\n'''
    if stderr.strip():
        report += f'''\n## Errors\n\n```text\n{stderr.rstrip()}\n```\n'''

    REPORT.write_text(report, encoding="utf-8")
    print(f"OVERSEER_REPORT={REPORT}")
    print(f"OVERSEER_STATUS={status}")
    raise SystemExit(code)


if __name__ == "__main__":
    main()
