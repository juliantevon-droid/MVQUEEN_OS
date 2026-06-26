# MVQueen Omniluxe Engine
## Enterprise Automation Layer

---

## 1. Overview
The Omniluxe Engine is the core automation system for MVQueen. It handles product curation, Shopify synchronization, and data processing while ensuring strict adherence to brand doctrine.

---

## 2. Architecture
The engine is structured as a modular Python package:
*   `catalog_processor/`: Logic for CSV and Live Shopify processing.
*   `brand_brain/`: AI-driven editorial and asset generation.
*   `shopify_api/`: Hardened client for Shopify Admin API interactions.
*   `metafields/`: Custom data mapping engine.
*   `utils/`: Shared helper functions for text and pricing logic.

---

## 3. Configuration
The engine uses a tiered configuration system:
1.  `.env`: Local environment variables (ignored by Git).
2.  `config.py`: Global constants and safety toggles.
3.  `env.py`: Environment profile management (Dev/Staging/Prod).

---

## 4. Usage
### Batch CSV Processing
```python
from mvqueen_engine.batch_processor import process_csv
process_csv("input.csv", "output.csv")
```

### Shopify Live Sync
```python
from mvqueen_engine.catalog_processor.processor import process_shopify_catalog
process_shopify_catalog()
```

---

## 5. Maintenance
*   **Logs:** All actions are logged to the `logs/` directory.
*   **Validation:** Every code change must be validated against the `00_Doctrine` standards.
