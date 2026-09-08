from pathlib import Path

VAULT_FOLDERS = ["00_Doctrine", "01_Brand_Strategy"]
BLOCKED = [".py", ".js", ".sh"]


def scan():
    violations = []
    for folder in VAULT_FOLDERS:
        path = Path(folder)
        if not path.exists():
            continue
        for file in path.rglob("*"):
            if file.suffix in BLOCKED:
                violations.append(str(file))
    return violations


if __name__ == "__main__":
    result = scan()
    if result:
        print("ARCHITECTURE VIOLATIONS:")
        for r in result:
            print(" ", r)
        raise SystemExit(1)
    else:
        print("ARCHITECTURE PASS")
