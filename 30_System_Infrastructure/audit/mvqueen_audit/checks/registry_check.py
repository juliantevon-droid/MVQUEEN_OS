from pathlib import Path
import json
import sys

CHECKS_DIR = Path(__file__).resolve().parent
AUDIT_PACKAGE = CHECKS_DIR.parent
AUDIT_ROOT = AUDIT_PACKAGE.parent

sys.path.insert(0, str(AUDIT_ROOT))

from mvqueen_audit.models import Finding


REPO_ROOT = AUDIT_ROOT.parent.parent

REGISTRY = (
    REPO_ROOT
    / "30_System_Infrastructure"
    / "system"
    / "registry"
    / "system.json"
)


def check():
    findings = []

    if not REGISTRY.exists():
        return [
            Finding(
                "ERROR",
                "REGISTRY_MISSING",
                str(REGISTRY.relative_to(REPO_ROOT)),
            )
        ]

    try:
        data = json.loads(REGISTRY.read_text())
    except json.JSONDecodeError as exc:
        return [
            Finding(
                "ERROR",
                "REGISTRY_INVALID_JSON",
                str(exc),
            )
        ]

    if data.get("system") != "MVQUEEN_OS":
        findings.append(
            Finding(
                "ERROR",
                "REGISTRY_SYSTEM_ID",
                f"Expected MVQUEEN_OS, got {data.get('system')!r}",
            )
        )

    if "version" not in data:
        findings.append(
            Finding(
                "WARNING",
                "REGISTRY_VERSION_MISSING",
                "Registry has no version field",
            )
        )

    if "architecture" not in data:
        findings.append(
            Finding(
                "ERROR",
                "REGISTRY_ARCHITECTURE_MISSING",
                "Registry has no architecture definition",
            )
        )

    if not isinstance(data.get("modules"), list):
        findings.append(
            Finding(
                "ERROR",
                "REGISTRY_MODULES_INVALID",
                "modules must be a list",
            )
        )

    if not findings:
        findings.append(
            Finding(
                "PASS",
                "REGISTRY_VALID",
                f"Valid MVQUEEN_OS registry; "
                f"{len(data.get('modules', []))} modules registered",
            )
        )

    return findings


if __name__ == "__main__":
    for finding in check():
        print(finding.format())
