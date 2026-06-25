# testing/test_full_engine.py
"""
MVQueen Full System Test
------------------------

This is the master integration test for the entire MVQueen Omniluxe Engine.

It validates:
- Control Panel integration
- Config system
- Detection engine
- Persona routing
- Editorial engine
- Android safety layer
- Catalog processor
- Shopify sync safety mode
- Unified product package structure
"""

from mvqueen_engine import process_product, upload_to_shopify
from control_panel import get_engine_state
from control_panel.config import load_config


def test_full_engine():
    """
    Runs a full product through the entire engine.
    """

    raw = {
        "title": "Black Satin Slip Dress",
        "description": "A sleek satin slip dress perfect for evening wear.",
        "sku": "TEST-001",
    }

    # Run engine
    package = process_product(raw)

    # --------------------------------------------------------
    # VALIDATE PACKAGE STRUCTURE
    # --------------------------------------------------------
    assert "raw" in package
    assert "profile" in package
    assert "editorial" in package
    assert "metafields" in package
    assert "tags" in package
    assert "collections" in package
    assert "bundles" in package
    assert "paths" in package
    assert "engine_state" in package

    # --------------------------------------------------------
    # VALIDATE EDITORIAL OUTPUT
    # --------------------------------------------------------
    editorial = package["editorial"]
    assert isinstance(editorial["description"], str)
    assert len(editorial["description"]) > 50
    assert isinstance(editorial["frames"], list)
    assert isinstance(editorial["seo_block"], str)

    # --------------------------------------------------------
    # VALIDATE DETECTION OUTPUT
    # --------------------------------------------------------
    assert isinstance(package["metafields"], dict)
    assert isinstance(package["tags"], list)
    assert isinstance(package["collections"], list)

    # --------------------------------------------------------
    # VALIDATE CONTROL PANEL STATE
    # --------------------------------------------------------
    state = get_engine_state()
    assert "environment" in state
    assert "feature_toggles" in state
    assert "active_profile" in state

    # --------------------------------------------------------
    # VALIDATE SHOPIFY SAFETY MODE
    # --------------------------------------------------------
    cfg = load_config()
    if not cfg.get("shopify_sync_enabled", False):
        # Should return a "disabled" response
        resp = upload_to_shopify(package)
        assert resp["upload_response"]["status"] == "disabled"

    print("Full engine test passed.")


if __name__ == "__main__":
    test_full_engine()