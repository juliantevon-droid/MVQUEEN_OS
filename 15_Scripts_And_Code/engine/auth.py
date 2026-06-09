# ---------------------------------------------------------
# MVQUEEN OMNILUXE ENGINE — SHOPIFY AUTH WRAPPER
# ---------------------------------------------------------

from mvqueen_engine.shopify_api.session_manager import SessionManager


class ShopifyAuth:
    """
    Simple authentication wrapper that returns a configured SessionManager.
    """

    def __init__(self, shop_url: str, api_key: str, password: str, api_version: str = "2024-01"):
        self.shop_url = shop_url
        self.api_key = api_key
        self.password = password
        self.api_version = api_version

    def get_session(self) -> SessionManager:
        return SessionManager(
            shop_url=self.shop_url,
            api_key=self.api_key,
            password=self.password,
            api_version=self.api_version,
        )