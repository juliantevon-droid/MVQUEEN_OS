# ---------------------------------------------------------
# MVQUEEN OMNILUXE ENGINE — SHOPIFY SYNC LAYER (BLOCK O)
# Hybrid namespaces + auto-typed metafields + variants
# ---------------------------------------------------------

import time
import requests
import json


class ShopifySync:
    def __init__(
        self,
        shop_url: str,
        api_key: str,
        password: str,
        variant_mode: str = "full",  # "full" or "single"
        vendor: str = "MVQueen",
        api_version: str = "2024-01",
    ):
        """
        variant_mode:
            "full"   -> use product["variants"] from Omniluxe engine
            "single" -> create a single default variant using product["price"]
        """
        self.shop_url = shop_url.rstrip("/")
        self.api_key = api_key
        self.password = password
        self.vendor = vendor
        self.api_version = api_version
        self.variant_mode = variant_mode

    # ---------------------------------------------------------
    # INTERNAL REQUEST WRAPPER (RATE-LIMIT SAFE)
    # ---------------------------------------------------------

    def _request(self, method: str, endpoint: str, data: dict | None = None):
        url = f"{self.shop_url}/admin/api/{self.api_version}/{endpoint}"
        auth = (self.api_key, self.password)

        while True:
            response = requests.request(method, url, auth=auth, json=data)

            # Shopify rate limit handling
            if response.status_code == 429:
                time.sleep(1)
                continue

            response.raise_for_status()
            if response.text:
                return response.json()
            return {}

    # ---------------------------------------------------------
    # METAFIELD TYPE DETECTION
    # ---------------------------------------------------------

    def _detect_metafield_type(self, value):
        """
        Auto-detect Shopify metafield type based on Python value.
        """
        if isinstance(value, bool):
            # Shopify doesn't have a native boolean metafield type in older APIs;
            # store as JSON.
            return "json"
        if isinstance(value, int):
            return "number_integer"
        if isinstance(value, float):
            return "number_decimal"
        if isinstance(value, (list, dict)):
            return "json"
        if isinstance(value, str):
            # Heuristic: long strings -> multi-line
            if len(value) > 255:
                return "multi_line_text_field"
            return "single_line_text_field"
        # Fallback
        return "single_line_text_field"

    # ---------------------------------------------------------
    # HYBRID NAMESPACE MAPPING
    # ---------------------------------------------------------

    def _build_metafield_payloads(self, product: dict) -> list[dict]:
        """
        Build metafield payloads using hybrid namespaces:
        - editorial.* (short/medium/long)
        - seo.* (primary/secondary)
        - attributes.* (category, persona, etc.)
        - custom.* (extended metafields and everything else)
        """
        metafields = product.get("metafields", {}) or {}
        payloads: list[dict] = []

        # Helper to add a metafield
        def add_metafield(namespace: str, key: str, value):
            if value is None:
                return
            # Lists/dicts must be JSON-encoded for Shopify
            if isinstance(value, (list, dict)):
                stored_value = json.dumps(value)
            else:
                stored_value = value
            mtype = self._detect_metafield_type(value)
            payloads.append(
                {
                    "metafield": {
                        "namespace": namespace,
                        "key": key,
                        "value": stored_value,
                        "type": mtype,
                    }
                }
            )

        # --- EDITORIAL NAMESPACE ---
        add_metafield("editorial", "short", metafields.get("editorial_short"))
        add_metafield("editorial", "medium", metafields.get("editorial_medium"))
        add_metafield("editorial", "long", metafields.get("editorial_long"))

        # --- SEO NAMESPACE ---
        add_metafield("seo", "primary", metafields.get("seo_primary"))
        add_metafield("seo", "secondary", metafields.get("seo_secondary"))

        # --- ATTRIBUTES NAMESPACE ---
        # Prefer metafields if present, else fall back to top-level product keys.
        def attr(name: str):
            return metafields.get(name, product.get(name))

        add_metafield("attributes", "category", attr("category"))
        add_metafield("attributes", "product_type", attr("product_type"))
        add_metafield("attributes", "persona", attr("persona"))
        add_metafield("attributes", "trend", attr("trend"))
        add_metafield("attributes", "season", attr("season"))
        add_metafield("attributes", "vibe", attr("vibe"))
        add_metafield("attributes", "material", attr("material"))
        add_metafield("attributes", "silhouette", attr("silhouette"))
        add_metafield("attributes", "detail", attr("detail"))

        # --- CUSTOM NAMESPACE (extended metafields and everything else) ---
        extended_keys = {
            "emotional_axes",
            "seo_keywords",
            "care_instructions",
            "shipping_note",
            "size_guide",
            "trust_badges",
            "short_description",
            "focus_keyword",
            "faq",
            "ingredients",
            "how_to_use",
            "highlights",
            "badge",
        }

        for key, value in metafields.items():
            if key in {
                "editorial_short",
                "editorial_medium",
                "editorial_long",
                "seo_primary",
                "seo_secondary",
                "category",
                "product_type",
                "persona",
                "trend",
                "season",
                "vibe",
                "material",
                "silhouette",
                "detail",
            }:
                # Already mapped into editorial/seo/attributes
                continue

            namespace = "custom"
            if key in extended_keys:
                add_metafield(namespace, key, value)
            else:
                # Any other metafield also goes into custom.*
                add_metafield(namespace, key, value)

        return payloads

    # ---------------------------------------------------------
    # VARIANT BUILDING
    # ---------------------------------------------------------

    def _build_variants(self, product: dict) -> list[dict]:
        """
        Build Shopify variants payload from Omniluxe product dict.
        Supports:
        - full variant mode (use product["variants"])
        - single variant mode (use product["price"])
        """
        if self.variant_mode == "full" and product.get("variants"):
            variants_payload = []
            for v in product["variants"]:
                variant = {
                    "price": str(v.get("price", product.get("price", 0))),
                    "sku": v.get("sku", ""),
                    "inventory_management": "shopify",
                    "inventory_policy": "deny",
                    "requires_shipping": True,
                }
                # Map option fields if present
                # e.g., option1, option2, option3
                for opt_key in ("option1", "option2", "option3"):
                    if opt_key in v:
                        variant[opt_key] = v[opt_key]
                variants_payload.append(variant)
            return variants_payload

        # Fallback: single variant mode
        price = product.get("price", 0)
        return [
            {
                "price": str(price),
                "sku": product.get("sku", ""),
                "inventory_management": "shopify",
                "inventory_policy": "deny",
                "requires_shipping": True,
            }
        ]

    # ---------------------------------------------------------
    # PRODUCT CREATION
    # ---------------------------------------------------------

    def create_product(self, product_dict: dict) -> dict:
        """
        Create a Shopify product from the Omniluxe product dictionary.
        Uses:
        - title
        - handle
        - editorial_long as body_html
        - tags
        - product_type
        - vendor
        - seo_primary / seo_secondary
        - variants (full or single)
        """
        tags = product_dict.get("tags", [])
        if isinstance(tags, list):
            tags_str = ", ".join(sorted(tags))
        else:
            tags_str = str(tags)

        payload = {
            "product": {
                "title": product_dict.get("title", product_dict.get("editorial_short", "")),
                "body_html": product_dict.get("editorial_long", ""),
                "handle": product_dict.get("handle", ""),
                "tags": tags_str,
                "product_type": product_dict.get("product_type", ""),
                "vendor": self.vendor,
                "variants": self._build_variants(product_dict),
            }
        }

        # SEO fields
        seo_title = product_dict.get("seo_primary")
        seo_description = product_dict.get("seo_secondary")
        if seo_title or seo_description:
            payload["product"]["seo_title"] = seo_title or ""
            payload["product"]["seo_description"] = seo_description or ""

        return self._request("POST", "products.json", payload)

    # ---------------------------------------------------------
    # METAFIELD SYNC
    # ---------------------------------------------------------

    def update_metafields(self, product_id: int, product: dict):
        metafield_payloads = self._build_metafield_payloads(product)
        for payload in metafield_payloads:
            self._request("POST", f"products/{product_id}/metafields.json", payload)

    # ---------------------------------------------------------
    # COLLECTION SYNC (WITH DEDUPLICATION)
    # ---------------------------------------------------------

    def _find_collection_by_title(self, title: str) -> int | None:
        """
        Try to find an existing custom collection by title.
        This is a simple implementation; for large stores you might
        want pagination or a more targeted search.
        """
        result = self._request("GET", "custom_collections.json")
        collections = result.get("custom_collections", [])
        for c in collections:
            if c.get("title") == title:
                return c.get("id")
        return None

    def _ensure_collection(self, title: str) -> int:
        existing_id = self._find_collection_by_title(title)
        if existing_id:
            return existing_id
        payload = {"custom_collection": {"title": title}}
        result = self._request("POST", "custom_collections.json", payload)
        return result["custom_collection"]["id"]

    def add_to_collections(self, product_id: int, collections: list[str]):
        for c in collections or []:
            collection_id = self._ensure_collection(c)
            payload = {
                "collect": {
                    "product_id": product_id,
                    "collection_id": collection_id,
                }
            }
            self._request("POST", "collects.json", payload)

    # ---------------------------------------------------------
    # FULL SYNC PIPELINE
    # ---------------------------------------------------------

    def sync_product(self, product: dict) -> int:
        """
        Full sync pipeline:
        - create product
        - sync metafields (hybrid namespaces)
        - sync collections
        Returns Shopify product ID.
        """
        created = self.create_product(product)
        product_id = created["product"]["id"]

        self.update_metafields(product_id, product)
        self.add_to_collections(product_id, product.get("collections", []))

        return product_id