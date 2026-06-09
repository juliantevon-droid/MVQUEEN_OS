# mvqueen_engine/control_panel/control_panel.py
"""
PHASE 5 — CONTROL PANEL

This is the master controller for the entire MVQueen Engine.
It allows you to run:

1. CSV Mode (offline curation)
2. Shopify Mode (live updates)
3. Individual phases for debugging
4. Full pipeline

Everything is modular and uses:
- Phase 0 utilities
- Phase 1 brand brain
- Phase 2 metafields engine
- Phase 3 Shopify API engine
- Phase 4 catalog processor
"""

import os
from mvqueen_engine.catalog_processor.processor import (
    process_csv,
    process_shopify_catalog,
)
from mvqueen_engine.config import DEBUG


# ---------------------------------------------
# MENU DISPLAY
# ---------------------------------------------

def show_menu():
    print("\n==============================")
    print("     MVQUEEN ENGINE PANEL     ")
    print("==============================")
    print("1. Run CSV Mode (Offline Curation)")
    print("2. Run Shopify Mode (Live Updates)")
    print("3. Run Full Pipeline (CSV → Shopify)")
    print("4. Debug: Run CSV Only")
    print("5. Debug: Run Shopify Only")
    print("6. Exit")
    print("==============================\n")


# ---------------------------------------------
# MAIN CONTROL LOGIC
# ---------------------------------------------

def run_control_panel():
    while True:
        show_menu()
        choice = input("Select an option: ").strip()

        # ---------------------------------------------
        # OPTION 1 — CSV MODE
        # ---------------------------------------------
        if choice == "1":
            input_path = input("Enter input CSV path: ").strip()
            output_path = input("Enter output CSV path: ").strip()

            print("\nRunning CSV Mode...")
            result = process_csv(input_path, output_path)
            print(f"\nCSV Mode Complete. Output saved to: {result}")

        # ---------------------------------------------
        # OPTION 2 — SHOPIFY MODE
        # ---------------------------------------------
        elif choice == "2":
            print("\nRunning Shopify Mode...")
            process_shopify_catalog()
            print("\nShopify Mode Complete.")

        # ---------------------------------------------
        # OPTION 3 — FULL PIPELINE
        # ---------------------------------------------
        elif choice == "3":
            input_path = input("Enter input CSV path: ").strip()
            output_path = input("Enter output CSV path: ").strip()

            print("\nRunning CSV Mode...")
            result = process_csv(input_path, output_path)
            print(f"CSV Output saved to: {result}")

            print("\nRunning Shopify Mode...")
            process_shopify_catalog()

            print("\nFull Pipeline Complete.")

        # ---------------------------------------------
        # OPTION 4 — DEBUG CSV
        # ---------------------------------------------
        elif choice == "4":
            input_path = input("Enter input CSV path: ").strip()
            output_path = input("Enter output CSV path: ").strip()

            print("\nRunning CSV Debug Mode...")
            result = process_csv(input_path, output_path)
            print(f"CSV Debug Complete. Output saved to: {result}")

        # ---------------------------------------------
        # OPTION 5 — DEBUG SHOPIFY
        # ---------------------------------------------
        elif choice == "5":
            print("\nRunning Shopify Debug Mode...")
            process_shopify_catalog()
            print("\nShopify Debug Complete.")

        # ---------------------------------------------
        # OPTION 6 — EXIT
        # ---------------------------------------------
        elif choice == "6":
            print("\nExiting MVQueen Engine. Goodbye.")
            break

        else:
            print("\nInvalid option. Try again.\n")