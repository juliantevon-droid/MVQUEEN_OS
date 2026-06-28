# SOP: Product Upload & Curation
## MVQUEEN_OS / 39_SOP_Library

---

## 1. Purpose
This SOP defines the process for adding new products to the MVQueen Shopify store, ensuring they are doctrine-aligned and optimized for luxury positioning.

---

## 2. Prerequisites
*   Access to Shopify Admin.
*   Supplier product data (CSV or Link).
*   Omniluxe Engine environment configured.

---

## 3. Step-by-Step Process

### Step 1: Data Preparation
1.  Obtain the supplier CSV.
2.  Ensure the CSV contains a `Handle` and `input_text` column.
3.  Save the file to `15_Scripts_And_Code/data/raw/`.

### Step 2: Omniluxe Processing
1.  Run the batch processor:
    ```bash
    python3 -c "from mvqueen_engine.batch_processor import process_csv; process_csv('data/raw/supplier.csv', 'data/processed/curated.csv')"
    ```
2.  Verify the `data/processed/curated.csv` for brand voice alignment.

### Step 3: Shopify Import
1.  Log in to Shopify Admin > Products > Import.
2.  Upload the `curated.csv`.
3.  Select "Overwrite any current products that have the same handle" if updating existing items.

### Step 4: Visual Review
1.  Check the live product page.
2.  Ensure images are high-quality and alt text is present.
3.  Verify that the "MVQueen | [Title]" format is correct.

---

## 4. Success Criteria
*   Product is live on Shopify.
*   Description is sensory and emotional.
*   Price includes the standard luxury markup.
*   SEO metadata is populated.

---

## 5. Status
**Active** — Published June 25, 2026.
