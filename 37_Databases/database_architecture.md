# Database & Intelligence Architecture
## MVQUEEN_OS / 37_Databases

---

## 1. Purpose
This document defines how MVQUEEN_OS stores, retrieves, and processes data. We favor a "Git-as-a-Database" approach for doctrine and a structured relational approach for transactional data.

---

## 2. Data Storage Tiers

### Tier 1: Semantic Database (Obsidian/Git)
*   **Content:** Doctrine, SOPs, Brand Bible, Strategy.
*   **Format:** Markdown.
*   **Storage:** GitHub Repository.
*   **Purpose:** Long-term memory and AI context.

### Tier 2: Transactional Database (Shopify)
*   **Content:** Orders, Customers, Products, Inventory.
*   **Format:** Relational (Shopify Internal).
*   **Storage:** Shopify Cloud.
*   **Purpose:** Live business operations.

### Tier 3: Analytics Warehouse (Planned)
*   **Content:** Aggregated KPIs, Ad Spend, LTV data.
*   **Format:** BigQuery or Snowflake.
*   **Purpose:** Business intelligence and scaling decisions.

---

## 3. Data Integrity Rules
1.  **Source of Truth:** Shopify is the source of truth for all transactional data.
2.  **Doctrine Priority:** `00_Doctrine` is the source of truth for all AI behavior and brand voice.
3.  **No Silos:** All data must be accessible via the Omniluxe Engine for cross-functional analysis.

---

## 4. Status
**Active** — Published June 25, 2026.
