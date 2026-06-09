import sys
sys.path.insert(0, "/storage/emulated/0")

from mvqueen_engine.catalog_processor.processor import process_csv

process_csv(
    input_path="/storage/emulated/0/mvqueen_engine/products.csv",
    output_path="/storage/emulated/0/mvqueen_engine/output/products_final.csv",
    overwrite_mode="balanced"
)