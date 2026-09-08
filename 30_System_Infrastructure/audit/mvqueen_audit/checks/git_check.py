from pathlib import Path
import subprocess
import sys

CHECKS_DIR = Path(__file__).resolve().parent
AUDIT_PACKAGE = CHECKS_DIR.parent
AUDIT_ROOT = AUDIT_PACKAGE.parent

sys.path.insert(0, str(AUDIT_ROOT))

from mvqueen_audit.models import Finding


REPO_ROOT = AUDIT_ROOT.parent.parent


def git(*args):
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def check():
    findings = []

    code, branch, _ = git("branch", "--show-current")

    if code != 0:
        findings.append(
            Finding(
                "ERROR",
                "GIT_BRANCH_CHECK_FAILED",
                "Unable to determine current branch",
            )
        )
        return findings

    findings.append(
        Finding(
            "INFO",
            "GIT_BRANCH",
            branch or "DETACHED",
        )
    )

    _, status, _ = git("status", "--short")

    if status:
        findings.append(
            Finding(
                "INFO",
                "GIT_WORKTREE",
                "Working tree contains changes",
            )
        )

        if "30_System_Infrastructure/audit/" in status:
            findings.append(
                Finding(
                    "INFO",
                    "AUDIT_WORKTREE",
                    "Current changes are inside the audit subsystem",
                )
            )
    else:
        findings.append(
            Finding(
                "PASS",
                "GIT_WORKTREE",
                "Working tree is clean",
            )
        )

    _, head, _ = git("log", "-1", "--oneline")

    findings.append(
        Finding(
            "INFO",
            "GIT_HEAD",
            head or "UNKNOWN",
        )
    )

    _, upstream, _ = git(
        "rev-parse",
        "--abbrev-ref",
        "--symbolic-full-name",
        "@{u}",
    )

    if upstream:
        findings.append(
            Finding(
                "PASS",
                "GIT_UPSTREAM",
                upstream,
            )
        )
    else:
        findings.append(
            Finding(
                "WARNING",
                "GIT_UPSTREAM_NOT_CONFIGURED",
                "Current branch has no upstream tracking branch",
            )
        )

    return findings


if __name__ == "__main__":
    for finding in check():
        print(finding.format())
