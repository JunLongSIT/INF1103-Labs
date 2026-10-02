"""
Inventory Management System
----------------------------
1. Data Representation: each product is a dictionary (id, name, price, stock)
   stored inside a list.
2. Data Manipulation: add_product(), update_stock(), search_product(),
   display_all() operate on that list.
3. Data Persistence: load_inventory() / save_inventory() read and write
   inventory.json.
4. Menu System: Display, Add, Update, Search, Save, Exit.
"""

import json
import os

INVENTORY_FILE = "inventory.json"


# ---------------------------------------------------------------------
# Data Persistence
# ---------------------------------------------------------------------
def load_inventory():
    """
    Loads the product list from inventory.json if it exists.
    Otherwise, begins with an empty inventory.
    """
    if os.path.exists(INVENTORY_FILE):
        print(f"{INVENTORY_FILE} found.")
        try:
            with open(INVENTORY_FILE, "r") as f:
                inventory = json.load(f)
            print("Inventory loaded successfully.\n")
            return inventory
        except (IOError, json.JSONDecodeError) as e:
            print(f"  ⚠️  Could not read {INVENTORY_FILE} ({e}). Starting with an empty inventory.\n")
            return []
    else:
        print(f"{INVENTORY_FILE} not found. Starting with an empty inventory.\n")
        return []


def save_inventory(inventory):
    """Saves the current inventory list to inventory.json."""
    print("Saving inventory...")
    try:
        with open(INVENTORY_FILE, "w") as f:
            json.dump(inventory, f, indent=4)
        print(f"Inventory saved successfully to {INVENTORY_FILE}.\n")
    except IOError as e:
        print(f"  ⚠️  Warning: could not save inventory ({e})\n")


# ---------------------------------------------------------------------
# Data Manipulation
# ---------------------------------------------------------------------
def display_all(inventory):
    """Prints every product currently in the inventory list."""
    print("\nCurrent Inventory")
    print("-" * 50)
    if not inventory:
        print("No products in inventory.")
    for product in inventory:
        print(f"ID: {product['id']} | Name: {product['name']} | "
              f"Price: ${product['price']:.2f} | Stock: {product['stock']}")
    print("-" * 50 + "\n")


def add_product(inventory):
    """Prompts for new product details and appends a dictionary to the inventory list."""
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()

    if any(p["id"] == product_id for p in inventory):
        print(f"  ❌ A product with ID {product_id} already exists.\n")
        return

    name = input("Product Name: ").strip()

    try:
        price = float(input("Price: ").strip())
        stock = int(input("Stock Quantity: ").strip())
    except ValueError:
        print("  ❌ Price must be a number and Stock Quantity must be a whole number. Product not added.\n")
        return

    inventory.append({"id": product_id, "name": name, "price": price, "stock": stock})
    print("\nProduct added successfully!\n")


def update_stock(inventory):
    """Finds a product by ID and updates its stock quantity."""
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()

    for product in inventory:
        if product["id"] == product_id:
            print("\nProduct Found:")
            print(f"Name: {product['name']}")
            print(f"Current Stock: {product['stock']}\n")

            try:
                new_stock = int(input("New Stock Quantity: ").strip())
            except ValueError:
                print("  ❌ Stock quantity must be a whole number. No changes made.\n")
                return

            product["stock"] = new_stock
            print("\nStock updated successfully!\n")
            return

    print("\nProduct not found.\n")


def search_product(inventory):
    """Finds and displays a single product by ID."""
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()

    for product in inventory:
        if product["id"] == product_id:
            print("\nProduct Found")
            print("-" * 50)
            print(f"ID: {product['id']}")
            print(f"Name: {product['name']}")
            print(f"Price: ${product['price']:.2f}")
            print(f"Stock: {product['stock']}")
            print("-" * 50 + "\n")
            return

    print("\nProduct not found.\n")


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
            display_all(inventory)
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
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