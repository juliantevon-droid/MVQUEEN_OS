# catalog_processor/schema.py
"""
MVQueen Catalog Schema — Enterprise Edition
-------------------------------------------

Defines and validates the schema for catalog items.

Ensures:
- Required fields exist
- Data types are correct
- Editorial + detection layers receive valid input
"""

from typing import Dict, List


# ------------------------------------------------------------
# EXPECTED SCHEMA
# ------------------------------------------------------------
REQUIRED_FIELDS = [
    "title",
    "description",
    "category",
    "product_type",
]


# ------------------------------------------------------------
# VALIDATE A SINGLE ITEM
# ------------------------------------------------------------
def validate_item(item: Dict) -> List[str]:
    """
    Validates a single catalog item.

    Returns:
        List[str] of errors (empty if valid)
    """

    errors = []

    for field in REQUIRED_FIELDS:
        if field not in item or not item[field]:
            errors.append(f"Missing required field: {field}")

    return errors


# ------------------------------------------------------------
# VALIDATE MULTIPLE ITEMS
# ------------------------------------------------------------
def validate_batch(items: List[Dict]) -> Dict[int, List[str]]:
    """
    Validates a list of catalog items.

    Returns:
        Dict[index, List[str]] of errors
    """

    results = {}

    for i, item in enumerate(items):
        errs = validate_item(item)
        if errs:
            results[i] = errs

    return results


__all__ = ["validate_item", "validate_batch", "REQUIRED_FIELDS"]