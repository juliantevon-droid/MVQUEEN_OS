import json
from pathlib import Path


SYSTEM_ROOT = Path(__file__).resolve().parents[1]
REGISTRY = SYSTEM_ROOT / "registry" / "system.json"


def load_registry():
    with REGISTRY.open(encoding="utf-8") as f:
        return json.load(f)


def boot():
    system = load_registry()

    print("MVQUEEN_OS BOOT:", system["system"])

    for module in system.get("modules", []):
        print("Loading:", module["name"])


if __name__ == "__main__":
    boot()
