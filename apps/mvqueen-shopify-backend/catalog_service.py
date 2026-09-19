from __future__ import annotations

from typing import Any

from shopify_graphql_client import ShopifyGraphQLClient


PRODUCT_FIELDS = """
id
title
handle
status
vendor
productType
tags
descriptionHtml
createdAt
updatedAt
"""


def preview_products(
    client: ShopifyGraphQLClient,
    *,
    first: int = 25,
) -> dict[str, Any]:
    first = max(1, min(first, 50))
    query = f"""
        query MVQueenCatalogPreview($first: Int!, $after: String) {{
          products(first: $first, after: $after) {{
            nodes {{
              {PRODUCT_FIELDS}
            }}
            pageInfo {{
              hasNextPage
              endCursor
            }}
          }}
        }}
        """
    body = client.execute(query, {"first": first, "after": None})
    connection = ((body.get("data") or {}).get("products") or {})
    nodes = connection.get("nodes", [])
    # Preview intentionally reads one bounded page only; full catalog reads
    # remain available through read_all_products().
    return {
        "count_returned": len(nodes),
        "products": [normalize_product(node) for node in nodes],
        "read_only": True,
    }


def read_all_products(
    client: ShopifyGraphQLClient,
    *,
    page_size: int = 100,
) -> list[dict[str, Any]]:
    """Read the full Shopify product catalog without changing Shopify."""
    page_size = max(1, min(page_size, 250))
    query = f"""
        query MVQueenCatalogSnapshot($first: Int!, $after: String) {{
          products(first: $first, after: $after) {{
            nodes {{
              {PRODUCT_FIELDS}
            }}
            pageInfo {{
              hasNextPage
              endCursor
            }}
          }}
        }}
        """
    return [
        normalize_product(node)
        for node in client.query_all(
            query,
            ("products",),
            first=page_size,
        )
    ]


def normalize_product(product: dict[str, Any]) -> dict[str, Any]:
    """Return a stable MVQUEEN catalog shape without changing Shopify data."""
    return {
        "id": product.get("id"),
        "title": product.get("title") or "",
        "handle": product.get("handle") or "",
        "status": product.get("status"),
        "vendor": product.get("vendor") or "",
        "product_type": product.get("productType") or "",
        "tags": list(product.get("tags") or []),
        "description_html": product.get("descriptionHtml") or "",
        "created_at": product.get("createdAt"),
        "updated_at": product.get("updatedAt"),
    }
