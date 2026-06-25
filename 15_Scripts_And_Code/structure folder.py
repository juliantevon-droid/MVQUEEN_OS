from pathlib import Path

structure = [
    "mvqueen_engine",
    "mvqueen_engine/utils",
    "mvqueen_engine/brand_brain/brand_banks",
    "mvqueen_engine/brand_brain/detection",
    "mvqueen_engine/brand_brain/persona",
    "mvqueen_engine/brand_brain/editorial",
    "mvqueen_engine/catalog_processor",
    "mvqueen_engine/shopify",
    "mvqueen_engine/control_panel",
    "mvqueen_engine/android",
    "mvqueen_engine/testing",
]

for folder in structure:
    Path(folder).mkdir(parents=True, exist_ok=True)

print("Structure created.")