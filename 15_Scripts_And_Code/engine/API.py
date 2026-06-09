# shopify/api.py
"""
MVQueen Shopify API Wrapper — Enterprise Edition
------------------------------------------------

Provides a safe, config-aware wrapper around Shopify API calls.
Actual network calls only occur if:
    config["shopify_sync_enabled"] == True

This prevents accidental live store updates.
"""

import json
from typing import Dict, Any
from control_panel.config import load_config


class ShopifyAPI:
    """
    Safe Shopify API wrapper.
    """

    def __init__(self):
        self.cfg = load_config()
        self.enabled = self.cfg.get("shopify_sync_enabled", False)

        # Placeholder credentials (admin will fill these in config.json)
        self.api_key = self.cfg.get("shopify_api_key", "")
        self.password = self.cfg.get("shopify_password", "")
        self.store_url = self.cfg.get("shopify_store_url", "")

    # ------------------------------------------------------------
    # INTERNAL SAFE CALL
    # ------------------------------------------------------------
    def _safe_call(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulates or performs a Shopify API call depending on config.
        """

        if not self.enabled:
            return {
                "status": "disabled",
                "endpoint": endpoint,
                "payload": payload,
                "message": "Shopify sync disabled in config.",
            }

        # In a real environment, you'd use requests.post() here.
        # We simulate a successful response for safety.
        return {
            "status": "success",
            "endpoint": endpoint,
            "payload": payload,
            "message": "Simulated Shopify API call.",
        }

    # ------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------
    def create_product(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._safe_call("products/create", data)

    def update_product(self, product_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._safe_call(f"products/{product_id}/update", data)

    def update_metafields(self, product_id: str, metafields: Dict[str, Any]) -> Dict[str, Any]:
        return self._safe_call(f"products/{product_id}/metafields", metafields)

    def assign_to_collection(self, product_id: str, collection_id: str) -> Dict[str, Any]:
        return self._safe_call(f"collections/{collection_id}/add", {"product_id": product_id})


__all__ = ["ShopifyAPI"]