"""
main.py
-------
Main program (Lab 7: supports PhysicalProduct and DigitalProduct).
Responsibilities:
  - Display the menu and get user input
  - Create Product objects and the Inventory object
  - Call the appropriate Inventory methods
  - File handling: load / save inventory.json (including product type)
"""

import json
import os

from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_FILE = os.path.join(BASE_DIR, "inventory.json")


# ---------------------------------------------------------------------
# File Handling
# ---------------------------------------------------------------------
def create_product_from_dict(item):
    """Uses the 'type' identifier to build the correct Product subclass."""
    product_type = item["type"]

    if product_type == "physical":
        return PhysicalProduct(item["id"], item["name"], item["price"],
                               item["stock"], item["weight"])
    if product_type == "digital":
        return DigitalProduct(item["id"], item["name"], item["price"],
                              item["stock"], item["download_size"])

    raise ValueError(f"Unknown product type: {product_type}")


def load_inventory():
    """Loads inventory.json into an Inventory of Product objects."""
    inventory = Inventory()

    if not os.path.exists(INVENTORY_FILE):
        print(f"{INVENTORY_FILE} not found. Starting with an empty inventory.\n")
        return inventory

    print(f"{INVENTORY_FILE} found.")
    try:
        with open(INVENTORY_FILE, "r") as f:
            data = json.load(f)
        for item in data:
            inventory.add_product(create_product_from_dict(item))
        print("Inventory loaded successfully.\n")
    except (IOError, json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        print(f"  ⚠️  Could not read {INVENTORY_FILE} ({e}). Starting with an empty inventory.\n")
        return Inventory()

    return inventory


def save_inventory(inventory):
    """Converts every Product to a dictionary and saves to inventory.json."""
    print("Saving inventory...")
    try:
        data = [product.to_dict() for product in inventory.get_all_products()]
        with open(INVENTORY_FILE, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Inventory saved successfully to {INVENTORY_FILE}.\n")
    except IOError as e:
        print(f"  ⚠️  Warning: could not save inventory ({e})\n")


# ---------------------------------------------------------------------
# Menu actions (get input, call Inventory, print result)
# ---------------------------------------------------------------------
def add_product_action(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()

    if inventory.search_product(product_id) is not None:
        print(f"  ❌ A product with ID {product_id} already exists.\n")
        return

    print("Product Type:")
    print("  1. Physical")
    print("  2. Digital")
    type_choice = input("Choose type (1/2): ").strip()
    if type_choice not in ("1", "2"):
        print("  ❌ Invalid product type. Product not added.\n")
        return

    name = input("Product Name: ").strip()

    try:
        price = float(input("Price: ").strip())
        stock = int(input("Stock Quantity: ").strip())
    except ValueError:
        print("  ❌ Price must be a number and Stock Quantity must be a whole number. Product not added.\n")
        return

    if stock < 0:
        print("  ❌ Stock cannot be negative. Product not added.\n")
        return

    try:
        if type_choice == "1":
            weight = float(input("Weight (kg): ").strip())
            if weight < 0:
                print("  ❌ Weight cannot be negative. Product not added.\n")
                return
            product = PhysicalProduct(product_id, name, price, stock, weight)
        else:
            download_size = float(input("Download Size (MB): ").strip())
            if download_size < 0:
                print("  ❌ Download size cannot be negative. Product not added.\n")
                return
            product = DigitalProduct(product_id, name, price, stock, download_size)
    except ValueError:
        print("  ❌ Weight / Download Size must be a number. Product not added.\n")
        return

    inventory.add_product(product)
    print("\nProduct added successfully!\n")


def update_stock_action(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()

    product = inventory.search_product(product_id)
    if product is None:
        print("\nProduct not found.\n")
        return

    print("\nProduct Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}\n")

    try:
        new_stock = int(input("New Stock Quantity: ").strip())
    except ValueError:
        print("  ❌ Stock quantity must be a whole number. No changes made.\n")
        return

    if inventory.update_stock(product_id, new_stock):
        print("\nStock updated successfully!\n")
    else:
        print("  ❌ Stock cannot be negative. No changes made.\n")


def search_product_action(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()

    product = inventory.search_product(product_id)
    if product is None:
        print("\nProduct not found.\n")
        return

    print("\nProduct Found")
    print("-" * 50)
    product.display_information()
    print(f"Fulfilment: {product.get_fulfilment_info()}")
    if isinstance(product, CanBeShipped):
        print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
    print("-" * 50 + "\n")


# ---------------------------------------------------------------------
# Menu System
# ---------------------------------------------------------------------
def print_menu():
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("-" * 28)


def main():
    print("=" * 50)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 50 + "\n")

    inventory = load_inventory()

    while True:
        print_menu()
        choice = input("\nEnter option: ").strip()
        print()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product_action(inventory)
        elif choice == "3":
            update_stock_action(inventory)
        elif choice == "4":
            search_product_action(inventory)
        elif choice == "5":
            save_inventory(inventory)
        elif choice == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("  ❌ Invalid option. Please enter a number between 1 and 6.\n")


if __name__ == "__main__":
    main()