import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path


SYSTEM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SYSTEM_ROOT.parent.parent

REGISTRY = SYSTEM_ROOT / "registry" / "system.json"
STATE = SYSTEM_ROOT / "state" / "system_state.json"


def load_registry():
    with REGISTRY.open(encoding="utf-8") as f:
        return json.load(f)


def load_state():
    with STATE.open(encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    STATE.write_text(
        json.dumps(state, indent=2) + "\n",
        encoding="utf-8",
    )


def load_module(module_definition):
    name = module_definition["name"]

    module_path = (
        REPO_ROOT
        / module_definition["path"]
        / module_definition["entrypoint"]
    )

    if not module_path.exists():
        raise FileNotFoundError(
            f"Module entrypoint not found: {module_path}"
        )

    spec = importlib.util.spec_from_file_location(
        name,
        module_path,
    )

    if spec is None or spec.loader is None:
        raise ImportError(
            f"Unable to create loader for module: {name}"
        )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def boot():
    system = load_registry()
    state = load_state()

    print("MVQUEEN_OS BOOT:", system["system"])

    loaded = []
    failed = []

    state["status"] = "booting"
    state["modules_loaded"] = []
    state["last_boot"] = datetime.now(timezone.utc).isoformat()
    state["module_errors"] = []

    for definition in system.get("modules", []):
        name = definition["name"]

        if not definition.get("enabled", False):
            print("Skipping disabled module:", name)
            continue

        print("Loading:", name)

        try:
            module = load_module(definition)

            if not hasattr(module, "boot"):
                raise AttributeError(
                    f"Module '{name}' has no boot() function"
                )

            result = module.boot()

            if not isinstance(result, dict):
                raise TypeError(
                    f"Module '{name}' boot() must return a dictionary"
                )

            status = result.get("status", "unknown")

            print("  Status:", status)

            loaded.append(name)

        except Exception as exc:
            print(
                f"  ERROR: {type(exc).__name__}: {exc}"
            )

            failed.append(
                {
                    "name": name,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )

    state["modules_loaded"] = loaded
    state["module_errors"] = failed

    if failed:
        state["status"] = "degraded"
    else:
        state["status"] = "running"

    save_state(state)

    print("Loaded modules:", len(loaded))
    print("Failed modules:", len(failed))
    print("System status:", state["status"])

    return loaded


if __name__ == "__main__":
    boot()
