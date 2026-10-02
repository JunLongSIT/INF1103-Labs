"""
Inventory Management System
----------------------------
Data representation: each product is stored as a dictionary with keys
(id, name, price, stock). All products are kept in a list of dictionaries.
Inventory is persisted to inventory.json between runs.
"""

import json
import os

INVENTORY_FILE = "inventory.json"


# ---------------------------------------------------------------------
# Data representation
# ---------------------------------------------------------------------
def default_inventory():
    """Returns a starting list of at least three product dictionaries."""
    return [
        {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
        {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
        {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25},
    ]


def load_inventory():
    """
    Loads the product list from inventory.json.
    Falls back to the default inventory if the file is missing or corrupt.
    """
    if os.path.exists(INVENTORY_FILE):
        print(f"{INVENTORY_FILE} found.")
        try:
            with open(INVENTORY_FILE, "r") as f:
                products = json.load(f)
            print("Inventory loaded successfully.\n")
            return products
        except (IOError, json.JSONDecodeError) as e:
            print(f"  ⚠️  Could not read {INVENTORY_FILE} ({e}). Starting with default inventory.\n")
            return default_inventory()
    else:
        print(f"{INVENTORY_FILE} not found. Starting with default inventory.\n")
        return default_inventory()


def save_inventory(products):
    """Writes the current product list to inventory.json."""
    try:
        with open(INVENTORY_FILE, "w") as f:
            json.dump(products, f, indent=4)
        print("Inventory saved successfully.\n")
    except IOError as e:
        print(f"  ⚠️  Warning: could not save inventory ({e})\n")


# ---------------------------------------------------------------------
# Menu actions
# ---------------------------------------------------------------------
def display_all_products(products):
    print("\nCurrent Inventory")
    print("-" * 70)
    if not products:
        print("No products in inventory.")
    for p in products:
        print(f"ID: {p['id']} | Name: {p['name']} | Price: ${p['price']:.2f} | Stock: {p['stock']}")
    print("-" * 70 + "\n")


def add_product(products):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()

    if any(p["id"] == product_id for p in products):
        print(f"  ❌ A product with ID {product_id} already exists.\n")
        return

    name = input("Product Name: ").strip()

    try:
        price = float(input("Price: ").strip())
        stock = int(input("Stock Quantity: ").strip())
    except ValueError:
        print("  ❌ Price must be a number and Stock Quantity must be a whole number. Product not added.\n")
        return

    products.append({"id": product_id, "name": name, "price": price, "stock": stock})
    print("\nProduct added successfully!\n")


def update_stock(products):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID to update: ").strip()

    for p in products:
        if p["id"] == product_id:
            try:
                new_stock = int(input(f"Enter new stock quantity for {p['name']}: ").strip())
            except ValueError:
                print("  ❌ Stock quantity must be a whole number. No changes made.\n")
                return
            p["stock"] = new_stock
            print(f"\nStock updated successfully! {p['name']} now has {p['stock']} units.\n")
            return

    print(f"  ❌ No product found with ID {product_id}.\n")


def search_product(products):
    print("\nSearch Product")
    query = input("Enter Product ID or Name: ").strip().lower()

    matches = [p for p in products if query == p["id"].lower() or query in p["name"].lower()]

    if matches:
        print("\nMatching Products")
        print("-" * 70)
        for p in matches:
            print(f"ID: {p['id']} | Name: {p['name']} | Price: ${p['price']:.2f} | Stock: {p['stock']}")
        print("-" * 70 + "\n")
    else:
        print(f"  ❌ No product found matching '{query}'.\n")


# ---------------------------------------------------------------------
# Main program loop
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

    products = load_inventory()

    while True:
        print_menu()
        choice = input("\nEnter option: ").strip()
        print()

        if choice == "1":
            display_all_products(products)
        elif choice == "2":
            add_product(products)
        elif choice == "3":
            update_stock(products)
        elif choice == "4":
            search_product(products)
        elif choice == "5":
            save_inventory(products)
        elif choice == "6":
            save_inventory(products)
            print("Exiting Inventory Management System. Goodbye!")
            break
        else:
            print("  ❌ Invalid option. Please enter a number between 1 and 6.\n")


if __name__ == "__main__":
    main()