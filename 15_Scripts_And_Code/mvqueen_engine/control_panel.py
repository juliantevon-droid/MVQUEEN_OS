"""MVQUEEN offline catalog control panel.

The historical direct-Shopify menu has been retired. Production Shopify writes
must flow through the authenticated React application and explicit approval
boundary. This controller remains useful only for offline CSV curation.
"""
from __future__ import annotations

from mvqueen_engine.catalog_processor.processor import process_csv
from mvqueen_engine.config import DEBUG


def show_menu() -> None:
    print("\n==============================")
    print("     MVQUEEN ENGINE PANEL     ")
    print("==============================")
    print("1. Run CSV Mode (Offline Curation)")
    if DEBUG:
        print("2. Run CSV Debug Mode")
    print("0. Exit")
    print("==============================\n")


def run_control_panel() -> None:
    while True:
        show_menu()
        choice = input("Select an option: ").strip()

        if choice == "1" or (choice == "2" and DEBUG):
            input_path = input("Enter input CSV path: ").strip()
            output_path = input("Enter output CSV path: ").strip()
            result = process_csv(input_path, output_path)
            print(f"CSV curation complete: {result}")
        elif choice == "0":
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    run_control_panel()
