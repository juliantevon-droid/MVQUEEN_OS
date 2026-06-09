# ---------------------------------------------------------
# MVQUEEN OMNILUXE ENGINE — SHOPIFY PRODUCT UPDATER
# ---------------------------------------------------------

from typing import Optional

from mvqueen_engine.shopify.sync import ShopifySync


class ProductUpdater:
    """
    Thin wrapper around ShopifySync that updates existing products
    using the same schema, variant model, and metafield logic as
    the create flow.

    - Overwrites core fields (title, body_html, handle, tags, product_type)
    - Rebuilds variants (honors ShopifySync.variant_mode: "full" or "single")
    - Optionally updates metafields (hybrid namespaces)
    - Optionally updates collections
    """

    def __init__(self, sync: ShopifySync):
        self.sync = sync

    # ---------------------------------------------------------
    # CORE PRODUCT UPDATE
    # ---------------------------------------------------------

    def update_product(
        self,
        product_id: int,
        product: dict,
        update_metafields: bool = True,
        update_collections: bool = True,
    ) -> dict:
        """
        Update an existing Shopify product to match the Omniluxe product dict.

        Args:
            product_id: Shopify product ID to update.
            product:    Omniluxe product dictionary (same schema as create).
            update_metafields: If True, re-sync metafields (hybrid namespaces).
            update_collections: If True, re-sync collections.
        """

        tags = product.get("tags", [])
        if isinstance(tags, list):
            tags_str = ", ".join(sorted(tags))
        else:
            tags_str = str(tags)

        payload = {
            "product": {
                "id": product_id,
                "title": product.get("title", product.get("editorial_short", "")),
                "body_html": product.get("editorial_long", ""),
                "handle": product.get("handle", ""),
                "tags": tags_str,
                "product_type": product.get("product_type", ""),
                "vendor": self.sync.vendor,
                "variants": self.sync._build_variants(product),
            }
        }

        # SEO fields
        seo_title = product.get("seo_primary")
        seo_description = product.get("seo_secondary")
        if seo_title or seo_description:
            payload["product"]["seo_title"] = seo_title or ""
            payload["product"]["seo_description"] = seo_description or ""

        # PUT update
        updated = self.sync._request("PUT", f"products/{product_id}.json", payload)

        # Metafields (hybrid namespaces)
        if update_metafields:
            self.sync.update_metafields(product_id, product)

        # Collections
        if update_collections:
            self.sync.add_to_collections(product_id, product.get("collections", []))

        return updated

    # ---------------------------------------------------------
    # CONVENIENCE: UPSERT BY HANDLE (OPTIONAL)
    # ---------------------------------------------------------

    def upsert_by_handle(
        self,
        product: dict,
        update_metafields: bool = True,
        update_collections: bool = True,
    ) -> dict:
        """
        Convenience method:
        - If a product with this handle exists, update it.
        - Otherwise, create a new product via ShopifySync and return it.
        """

        handle = product.get("handle")
        if not handle:
            # No handle: just create a new product
            created = self.sync.create_product(product)
            product_id = created["product"]["id"]
            if update_metafields:
                self.sync.update_metafields(product_id, product)
            if update_collections:
                self.sync.add_to_collections(product_id, product.get("collections", []))
            return created

        # Try to find existing product by handle
        result = self.sync._request(
            "GET", f"products.json?handle={handle}"
        )
        products = result.get("products", [])
        if products:
            existing = products[0]
            product_id = existing["id"]
            return self.update_product(
                product_id,
                product,
                update_metafields=update_metafields,
                update_collections=update_collections,
            )

        # No existing product: create new
        created = self.sync.create_product(product)
        product_id = created["product"]["id"]
        if update_metafields:
            self.sync.update_metafields(product_id, product)
        if update_collections:
            self.sync.add_to_collections(product_id, product.get("collections", []))
        return created