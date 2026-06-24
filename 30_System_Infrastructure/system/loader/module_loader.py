import json
from pathlib import Path

REGISTRY = Path("system/registry/system.json")


def load_registry():
    with open(REGISTRY) as f:
        return json.load(f)


def boot():
    system = load_registry()
    print("MVQUEEN_OS BOOT:", system["system"])
    for module in system["modules"]:
        print("Loading:", module["name"])


if __name__ == "__main__":
    boot()
