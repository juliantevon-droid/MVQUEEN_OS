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

ALLOWED_LAYERS = {
    "engine",
    "operations",
    "memory",
}


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
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
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

    modules = data.get("modules")

    if not isinstance(modules, list):
        findings.append(
            Finding(
                "ERROR",
                "REGISTRY_MODULES_INVALID",
                "modules must be a list",
            )
        )
        return findings

    names = set()

    for index, module in enumerate(modules):
        prefix = f"MODULE_{index}"

        if not isinstance(module, dict):
            findings.append(
                Finding(
                    "ERROR",
                    f"{prefix}_INVALID",
                    "Module definition must be an object",
                )
            )
            continue

        name = module.get("name")

        if not isinstance(name, str) or not name.strip():
            findings.append(
                Finding(
                    "ERROR",
                    f"{prefix}_NAME_MISSING",
                    "Module must have a non-empty name",
                )
            )
        elif name in names:
            findings.append(
                Finding(
                    "ERROR",
                    f"{prefix}_DUPLICATE",
                    f"Duplicate module name: {name}",
                )
            )
        else:
            names.add(name)

        version = module.get("version")

        if not isinstance(version, str) or not version.strip():
            findings.append(
                Finding(
                    "ERROR",
                    f"{prefix}_VERSION_INVALID",
                    "Module must have a version",
                )
            )

        layer = module.get("layer")

        if layer not in ALLOWED_LAYERS:
            findings.append(
                Finding(
                    "ERROR",
                    f"{prefix}_LAYER_INVALID",
                    f"Invalid module layer: {layer!r}",
                )
            )

        path_value = module.get("path")
        entrypoint = module.get("entrypoint")

        if not isinstance(path_value, str) or not path_value:
            findings.append(
                Finding(
                    "ERROR",
                    f"{prefix}_PATH_MISSING",
                    "Module must define a path",
                )
            )
        elif not isinstance(entrypoint, str) or not entrypoint:
            findings.append(
                Finding(
                    "ERROR",
                    f"{prefix}_ENTRYPOINT_MISSING",
                    "Module must define an entrypoint",
                )
            )
        else:
            module_path = REPO_ROOT / path_value / entrypoint

            try:
                module_path.relative_to(REPO_ROOT)
            except ValueError:
                findings.append(
                    Finding(
                        "ERROR",
                        f"{prefix}_PATH_ESCAPE",
                        f"Module path escapes repository: {module_path}",
                    )
                )
                continue

            if not module_path.exists():
                findings.append(
                    Finding(
                        "ERROR",
                        f"{prefix}_ENTRYPOINT_NOT_FOUND",
                        str(module_path.relative_to(REPO_ROOT)),
                    )
                )

    if not findings:
        findings.append(
            Finding(
                "PASS",
                "REGISTRY_VALID",
                f"Valid MVQUEEN_OS registry; "
                f"{len(modules)} modules registered",
            )
        )

    return findings


if __name__ == "__main__":
    for finding in check():
        print(finding.format())
