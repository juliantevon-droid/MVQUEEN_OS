# ---------------------------------------------------------
# MVQUEEN OMNILUXE ENGINE — SHOPIFY SESSION MANAGER
# ---------------------------------------------------------

import time
import requests


class SessionManager:
    """
    Low-level HTTP client for Shopify API.
    Handles:
    - Base URL construction
    - Auth
    - Rate limits (429)
    - Retries
    - GET/POST/PUT/DELETE wrappers
    """

    def __init__(self, shop_url: str, api_key: str, password: str, api_version: str = "2024-01"):
        self.shop_url = shop_url.rstrip("/")
        self.api_key = api_key
        self.password = password
        self.api_version = api_version

    # ---------------------------------------------------------
    # INTERNAL REQUEST WRAPPER
    # ---------------------------------------------------------

    def request(self, method: str, endpoint: str, data=None):
        url = f"{self.shop_url}/admin/api/{self.api_version}/{endpoint}"
        auth = (self.api_key, self.password)

        while True:
            response = requests.request(method, url, auth=auth, json=data)

            # Rate limit handling
            if response.status_code == 429:
                time.sleep(1)
                continue

            response.raise_for_status()
            if response.text:
                return response.json()
            return {}

    # ---------------------------------------------------------
    # CONVENIENCE WRAPPERS
    # ---------------------------------------------------------

    def get(self, endpoint: str):
        return self.request("GET", endpoint)

    def post(self, endpoint: str, data=None):
        return self.request("POST", endpoint, data)

    def put(self, endpoint: str, data=None):
        return self.request("PUT", endpoint, data)

    def delete(self, endpoint: str):
        return self.request("DELETE", endpoint)