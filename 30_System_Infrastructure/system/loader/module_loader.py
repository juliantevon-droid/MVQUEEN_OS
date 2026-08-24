import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path


SYSTEM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SYSTEM_ROOT.parent.parent
REGISTRY = SYSTEM_ROOT / "registry" / "system.json"
STATE = SYSTEM_ROOT / "state" / "system_state.json"
MODULE_ROOT = REPO_ROOT / "30_System_Infrastructure" / "modules"


def load_registry():
    with REGISTRY.open(encoding="utf-8") as f:
        return json.load(f)


def load_state():
    if not STATE.exists():
        return {
            "status": "unknown",
            "modules_loaded": [],
            "last_boot": None,
            "module_errors": [],
        }
    with STATE.open(encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def resolve_module_path(module_definition):
    path_value = module_definition.get("path")
    entrypoint = module_definition.get("entrypoint")
    if not isinstance(path_value, str) or not path_value:
        raise ValueError("Module definition must contain a valid path")
    if not isinstance(entrypoint, str) or not entrypoint:
        raise ValueError("Module definition must contain a valid entrypoint")

    module_path = (REPO_ROOT / path_value / entrypoint).resolve()
    module_root = MODULE_ROOT.resolve()
    try:
        module_path.relative_to(module_root)
    except ValueError as exc:
        raise ValueError(
            f"Module path escapes permitted module directory: {module_path}"
        ) from exc
    return module_path


def load_module(module_definition):
    name = module_definition.get("name")
    if not isinstance(name, str) or not name:
        raise ValueError("Module definition must contain a valid name")

    module_path = resolve_module_path(module_definition)
    if not module_path.is_file():
        raise FileNotFoundError(f"Module entrypoint not found: {module_path}")

    spec = importlib.util.spec_from_file_location(name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to create loader for module: {name}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def boot():
    system = load_registry()
    state = load_state()
    print("MVQUEEN_OS BOOT:", system.get("system", "UNKNOWN"))

    loaded = []
    failed = []
    state["status"] = "booting"
    state["modules_loaded"] = []
    state["last_boot"] = datetime.now(timezone.utc).isoformat()
    state["module_errors"] = []

    modules = system.get("modules", [])
    if not isinstance(modules, list):
        failed.append({"name": "<registry>", "error": "TypeError: modules must be a list"})
        modules = []

    for index, definition in enumerate(modules):
        name = f"<module-{index}>"
        try:
            if not isinstance(definition, dict):
                raise TypeError("Module definition must be an object")
            name = definition.get("name", name)
            if not isinstance(name, str) or not name:
                raise ValueError("Module definition must contain a valid name")
            if not definition.get("enabled", False):
                print("Skipping disabled module:", name)
                continue

            print("Loading:", name)
            module = load_module(definition)
            if not hasattr(module, "boot"):
                raise AttributeError(f"Module '{name}' has no boot() function")
            result = module.boot()
            if not isinstance(result, dict):
                raise TypeError(f"Module '{name}' boot() must return a dictionary")

            status = result.get("status", "unknown")
            print("  Status:", status)
            if status not in {"ready", "running", "healthy"}:
                raise RuntimeError(f"Module '{name}' returned non-ready status: {status}")
            loaded.append(name)
        except Exception as exc:
            print(f"  ERROR: {type(exc).__name__}: {exc}")
            failed.append({"name": name, "error": f"{type(exc).__name__}: {exc}"})

    state["modules_loaded"] = loaded
    state["module_errors"] = failed
    state["status"] = "degraded" if failed else "running"
    save_state(state)

    print("Loaded modules:", len(loaded))
    print("Failed modules:", len(failed))
    print("System status:", state["status"])
    return loaded


if __name__ == "__main__":
    boot()
