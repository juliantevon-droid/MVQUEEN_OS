from pathlib import Path
import sys

CHECKS_DIR = Path(__file__).resolve().parent
AUDIT_PACKAGE = CHECKS_DIR.parent
AUDIT_ROOT = AUDIT_PACKAGE.parent

sys.path.insert(0, str(AUDIT_ROOT))

from mvqueen_audit.models import Finding


REPO_ROOT = AUDIT_ROOT.parent.parent

VAULT_FOLDERS = [
    "00_Doctrine",
    "01_Brand_Strategy",
]

BLOCKED_EXTENSIONS = {
    ".py",
    ".js",
    ".sh",
}


def check():
    findings = []

    for folder in VAULT_FOLDERS:
        path = REPO_ROOT / folder

        if not path.exists():
            findings.append(
                Finding(
                    "WARNING",
                    "VAULT_FOLDER_MISSING",
                    str(path),
                )
            )
            continue

        for file in path.rglob("*"):
            if file.is_file() and file.suffix in BLOCKED_EXTENSIONS:
                findings.append(
                    Finding(
                        "WARNING",
                        "ARCHITECTURE_VIOLATION",
                        str(file.relative_to(REPO_ROOT)),
                    )
                )

    if not findings:
        findings.append(
            Finding(
                "PASS",
                "ARCHITECTURE",
                "No blocked executable files found in protected vault folders",
            )
        )

    return findings


if __name__ == "__main__":
    for finding in check():
        print(finding.format())
