from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parent
CHECKS = ROOT / "checks"

AUDIT_ROOT = ROOT.parent
REPO_ROOT = AUDIT_ROOT.parent.parent

sys.path.insert(0, str(AUDIT_ROOT))


def load_check(path):
    module_name = path.stem
    spec = importlib.util.spec_from_file_location(module_name, path)

    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def normalize_finding(finding):
    if hasattr(finding, "format"):
        return finding.format()

    return str(finding)


def run():
    check_files = sorted(
        p for p in CHECKS.glob("*_check.py")
        if p.is_file()
    )

    print("=" * 60)
    print("MVQUEEN_OS STABILIZATION AUDIT")
    print("=" * 60)
    print(f"Repository: {REPO_ROOT}")
    print(f"Checks: {len(check_files)}")

    total = 0

    for path in check_files:
        print()
        print(f"[CHECK] {path.stem}")

        try:
            module = load_check(path)

            if not hasattr(module, "check"):
                print("  [ERROR] CHECK_FUNCTION_MISSING")
                total += 1
                continue

            findings = module.check()

            if findings is None:
                print("  [PASS] NO_FINDINGS")
                continue

            findings = list(findings)

            if not findings:
                print("  [PASS] NO_FINDINGS")
                continue

            for finding in findings:
                print(f"  {normalize_finding(finding)}")
                total += 1

        except Exception as exc:
            print(
                f"  [ERROR] CHECK_EXECUTION_FAILED: "
                f"{type(exc).__name__}: {exc}"
            )
            total += 1

    print()
    print("=" * 60)
    print(f"Audit findings reported: {total}")
    print("=" * 60)

    # A finding must fail the process so CI/Overseer can detect it.
    if total > 0:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(run())
