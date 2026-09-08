from pathlib import Path
import sys

CHECKS_DIR = Path(__file__).resolve().parent
AUDIT_PACKAGE = CHECKS_DIR.parent
AUDIT_ROOT = AUDIT_PACKAGE.parent

sys.path.insert(0, str(AUDIT_ROOT))

from mvqueen_audit.models import Finding


REPO_ROOT = AUDIT_ROOT.parent.parent

SYSTEM_ROOT = REPO_ROOT / "30_System_Infrastructure"

MODULE_LOADER = (
    SYSTEM_ROOT
    / "system"
    / "loader"
    / "module_loader.py"
)

ACTUAL_REGISTRY = (
    SYSTEM_ROOT
    / "system"
    / "registry"
    / "system.json"
)


def check():
    findings = []

    if not MODULE_LOADER.exists():
        findings.append(
            Finding(
                "ERROR",
                "MODULE_LOADER_MISSING",
                str(MODULE_LOADER.relative_to(REPO_ROOT)),
            )
        )
        return findings

    if ACTUAL_REGISTRY.exists():
        findings.append(
            Finding(
                "PASS",
                "MODULE_LOADER_REGISTRY_PATH",
                "Module loader registry path matches the "
                "MVQUEEN_OS system infrastructure layout",
            )
        )
    else:
        findings.append(
            Finding(
                "ERROR",
                "REGISTRY_MISSING",
                str(ACTUAL_REGISTRY.relative_to(REPO_ROOT)),
            )
        )

    return findings


if __name__ == "__main__":
    for finding in check():
        print(finding.format())
