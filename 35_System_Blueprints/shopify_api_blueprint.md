# System Blueprint: Shopify Admin API Integration
## MVQUEEN_OS / 35_System_Blueprints

---

## 1. Purpose
This blueprint defines the technical architecture for the bidirectional synchronization between MVQUEEN_OS and the Shopify Admin API.

---

## 2. Dependencies
*   **Platform:** Shopify Admin API (REST & GraphQL).
*   **Auth:** Private App Access Token (Scoped to: Products, Orders, Customers, Inventory).
*   **Engine:** Omniluxe Engine (`mvqueen_engine.shopify_api`).

---

## 3. Data Flow

### Outbound (OS → Shopify)
1.  **Curation:** Omniluxe Engine processes raw product data.
2.  **Payload:** JSON object containing curated Title, Body, SEO Meta, and Metafields.
3.  **Transport:** `PUT` request to `/admin/api/2024-01/products/{id}.json`.

### Inbound (Shopify → OS)
1.  **Orders:** Webhook triggers on `orders/create`.
2.  **Inventory:** Daily sync of stock levels via `GET /admin/api/2024-01/inventory_levels.json`.
3.  **Analytics:** Weekly fetch of sales data for the `KPI_Dashboard.md`.

---

## 4. Safety & Rate Limiting
*   **Rate Limit:** Max 2 requests per second (standard Shopify REST limit).
*   **Retry Logic:** Exponential backoff on `429 Too Many Requests` errors.
*   **Dry Run:** All scripts must support a `--dry-run` flag to simulate changes without hitting the API.

---

## 5. Success Criteria
*   Zero manual data entry for product curation.
*   Real-time order visibility in `logs/`.
*   100% accuracy in stock level reporting.

---

## 6. Status
**Active** — Blueprint implemented in `mvqueen_engine/shopify_api/`.
