"""MVQueen canonical product schema validator V1.

This intentionally implements the JSON-Schema keywords used by
PRODUCT_SCHEMA_V1.json so CI can validate records without a third-party
runtime dependency.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SCHEMA_PATH = Path(__file__).with_name("PRODUCT_SCHEMA_V1.json")


def load_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "null":
        return value is None
    return True


def validate(instance: Any, schema: dict[str, Any], path: str = "$", errors: list[str] | None = None) -> list[str]:
    """Validate the schema subset used by the MVQueen production contract."""
    errors = [] if errors is None else errors

    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: expected const {schema['const']!r}")
        return errors

    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: value {instance!r} is not in enum")
        return errors

    expected = schema.get("type")
    if expected:
        types = expected if isinstance(expected, list) else [expected]
        if not any(_type_matches(instance, item) for item in types):
            errors.append(f"{path}: expected type {types}, got {type(instance).__name__}")
            return errors

    if isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0):
            errors.append(f"{path}: string is shorter than minLength")
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            errors.append(f"{path}: string exceeds maxLength")

    if isinstance(instance, dict):
        for required in schema.get("required", []):
            if required not in instance:
                errors.append(f"{path}: missing required property {required!r}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in instance:
                if key not in properties:
                    errors.append(f"{path}: unexpected property {key!r}")
        for key, value in instance.items():
            if key in properties:
                validate(value, properties[key], f"{path}.{key}", errors)

    if isinstance(instance, list) and "items" in schema:
        for index, value in enumerate(instance):
            validate(value, schema["items"], f"{path}[{index}]", errors)

    return errors


def validate_record(record: dict[str, Any]) -> list[str]:
    return validate(record, load_schema())


if __name__ == "__main__":
    import sys

    payload = json.load(sys.stdin)
    problems = validate_record(payload)
    if problems:
        for problem in problems:
            print(problem)
        raise SystemExit(1)
    print("SCHEMA_VALID")
