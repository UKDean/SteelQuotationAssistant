from pathlib import Path

from services.price_service import get_price
from models.item import Item
from models.quotation import Quotation
from database import (
    create_database,
    get_next_quotation_number,
    save_customer,
    save_project,
    save_quotation as save_quotation_db,
    save_items,
)

QUOTATIONS_DIRECTORY = Path("quotations")
VALID_GRADES = ("60", "80")
VALID_SIZES = ("10", "12", "14", "16", "18", "20", "25", "32")


def ensure_directory_exists(path: Path) -> None:
    """Create a directory if it does not already exist."""
    path.mkdir(parents=True, exist_ok=True)


def get_next_quotation_filename() -> Path:
    """Return the next available quotation file path."""
    ensure_directory_exists(QUOTATIONS_DIRECTORY)
    file_count = len(list(QUOTATIONS_DIRECTORY.glob("*.txt")))
    return QUOTATIONS_DIRECTORY / f"quotation_{file_count + 1}.txt"


def save_text_file(text: str) -> None:
    """Save the quotation text to a numbered file."""
    quotation_path = get_next_quotation_filename()
    with quotation_path.open("w", encoding="utf-8") as file:
        file.write(text)

    print("\nQuotation saved successfully.")
    print(f"File Name: {quotation_path.name}")


def show_menu() -> None:
    """Display the main application menu."""
    print("\n======================================")
    print("      Steel Quotation Assistant")
    print("======================================")
    print("1. Create New Quotation")
    print("2. View Quotations")
    print("3. Exit")


def get_saved_quotation_files() -> list[Path]:
    """Return a list of saved quotation text files."""
    if not QUOTATIONS_DIRECTORY.exists():
        return []
    return sorted(QUOTATIONS_DIRECTORY.glob("*.txt"))


def display_saved_quotations() -> None:
    """Display saved quotation filenames to the user."""
    quotation_files = get_saved_quotation_files()
    if not quotation_files:
        print("\nNo quotations found.")
        return

    print("\nSaved Quotations:\n")
    for quotation_file in quotation_files:
        print(quotation_file.name)


def input_item() -> Item:
    """Prompt the user for item details and return a new Item."""
    print("\nAdd New Item")
    grade = input("Steel Grade (60/80): ")
    steel_size = input("Steel Size (10,12,14,16,18,20,25,32): ")
    quantity = float(input("Quantity (Ton): "))

    unit_price = get_price(grade, steel_size)
    if unit_price is None:
        raise ValueError("Invalid grade or size.")

    return Item(grade, steel_size, quantity, unit_price)


def create_new_quotation() -> Quotation:
    """Collect quotation metadata and items from the user."""
    customer_name = input("Customer Name: ")
    project_name = input("Project Name: ")
    quotation_number = get_next_quotation_number()

    quotation = Quotation(customer_name, project_name, quotation_number)
    while True:
        try:
            item = input_item()
        except ValueError:
            print("\nInvalid Grade or Size.")
            continue

        quotation.add_item(item)
        answer = input("\nAdd another item? (y/n): ").lower()
        if answer != "y":
            break

    return quotation


def persist_quotation(quotation: Quotation) -> None:
    """Save quotation data to SQLite and export the text file."""
    quotation_text = quotation.to_text()
    customer_id = save_customer(quotation.customer_name)
    project_id = save_project(customer_id, quotation.project_name)
    quotation_id = save_quotation_db(customer_id, project_id, quotation)
    save_items(quotation_id, quotation.items)

    print(quotation_text)
    save_text_file(quotation_text)


def main() -> None:
    """Run the main program loop."""
    create_database()

    while True:
        show_menu()
        choice = input("Select an option: ")

        if choice == "1":
            quotation = create_new_quotation()
            persist_quotation(quotation)
        elif choice == "2":
            display_saved_quotations()
        elif choice == "3":
            print("\nGoodbye.")
            break
        else:
            print("\nInvalid option.")


if __name__ == "__main__":
    main()
