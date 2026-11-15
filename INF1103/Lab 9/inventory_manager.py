"""
Main program (Lab 9: products are created through the ProductFactory).
Responsibilities:
  - Display the menu and get user input
  - Create Supplier objects and the Inventory object
  - Ask the ProductFactory for Product objects (it never names a subclass)
  - Call the appropriate Inventory methods
  - File handling: load / save inventory.json (including product type and supplier)
  - File handling: import products from products.csv, skipping invalid rows
"""

import csv
import json
import os

from inventory import Inventory
from product import Product
from supplier import Supplier
from product_factory import ProductFactory
from can_be_shipped import CanBeShipped


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_FILE = os.path.join(BASE_DIR, "inventory.json")
PRODUCTS_FILE = os.path.join(BASE_DIR, "products.csv")

# Used only for old inventory.json files saved before suppliers existed (Lab 7)
DEFAULT_SUPPLIER_DATA = {"id": "S000", "name": "Unknown Supplier",
                         "contact_email": "unknown@example.com"}

# Menu choice -> the type name the ProductFactory understands
PRODUCT_TYPES = {"1": "physical", "2": "digital"}

# The question to ask for the one value that differs between product types
SIZE_PROMPTS = {"physical": "Weight (kg): ", "digital": "Download Size (MB): "}

# ---------------------------------------------------------------------
# File Handling
# ---------------------------------------------------------------------
def get_or_create_supplier(data: dict, suppliers: dict[str, Supplier]) -> Supplier:
    """Returns the Supplier for this ID, creating it only the first time.
    Products from the same supplier therefore share ONE Supplier object."""
    supplier_id = data["id"]
    if supplier_id not in suppliers:
        suppliers[supplier_id] = Supplier(supplier_id, data["name"],
                                          data["contact_email"])
    return suppliers[supplier_id]


def create_product_from_dict(item: dict, suppliers: dict[str, Supplier]) -> Product:
    """Passes the saved 'type' identifier to the ProductFactory, which
    builds the correct Product subclass (or raises ValueError)."""
    supplier = get_or_create_supplier(item.get("supplier", DEFAULT_SUPPLIER_DATA),
                                      suppliers)
    # Physical products save a "weight", digital products a "download_size"
    size = item.get("weight", item.get("download_size", 0.0))

    return ProductFactory.create(item["type"], item["id"], item["name"],
                                 item["price"], item["stock"], supplier, size)


def load_inventory() -> Inventory:
    """Loads inventory.json into an Inventory of Product objects."""
    inventory = Inventory()
    suppliers: dict[str, Supplier] = {}

    if not os.path.exists(INVENTORY_FILE):
        print(f"{INVENTORY_FILE} not found. Starting with an empty inventory.\n")
        return inventory

    print(f"{INVENTORY_FILE} found.")
    try:
        with open(INVENTORY_FILE, "r") as f:
            data = json.load(f)
        for item in data:
            inventory.add_product(create_product_from_dict(item, suppliers))
        print("Inventory loaded successfully.\n")
    except (IOError, json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        print(f"  ⚠️  Could not read {INVENTORY_FILE} ({e}). Starting with an empty inventory.\n")
        return Inventory()

    return inventory


def save_inventory(inventory: Inventory) -> None:
    """Converts every Product to a dictionary and saves to inventory.json."""
    print("Saving inventory...")
    try:
        data = [product.to_dict() for product in inventory.get_all_products()]
        with open(INVENTORY_FILE, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Inventory saved successfully to {INVENTORY_FILE}.\n")
    except IOError as e:
        print(f"  ⚠️  Warning: could not save inventory ({e})\n")


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Reads products from a CSV file and adds them to the inventory.
    Every product is created through the ProductFactory and given `supplier`.

    try     : open the file
    except  : the file does not exist -> simple message, no crash
    else    : the file opened -> read the rows; one invalid row is reported
              and skipped, and loading carries on
    finally : always runs, whether the file was found or not"""
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip the header row
            loaded = 0
            # The header is line 1, so the first product is on line 2
            for line_number, row in enumerate(reader, start=2):
                if not row:
                    continue  # ignore blank lines
                try:
                    product_type, product_id, name, price, stock = row
                    product = ProductFactory.create(product_type, product_id, name,
                                                    float(price), int(stock), supplier)
                except ValueError as e:
                    # Unknown product type, a price/stock that is not a number,
                    # a value that fails validation, or the wrong number of columns
                    print(f"Skipped line {line_number} {row}: {e}")
                    continue

                if inventory.add_product(product):
                    loaded += 1
                else:
                    print(f"Skipped line {line_number} {row}: "
                          f"product ID {product_id} already exists.")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


# ---------------------------------------------------------------------
# Input helpers (keep asking until the value is usable)
# ---------------------------------------------------------------------
def get_positive_float(prompt: str) -> float:
    """Asks until the user enters a number greater than zero.
    float() raises ValueError for text such as "abc" (exception handling);
    the if statement rejects zero and negatives (validation)."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def get_non_negative_int(prompt: str) -> int:
    """Asks until the user enters a whole number that is zero or more."""
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Please enter a whole number that is zero or more.")
                continue
            return value
        except ValueError:
            print("Please enter a valid whole number, e.g. 10")


# ---------------------------------------------------------------------
# Menu actions (get input, call Inventory, print result)
# ---------------------------------------------------------------------
def find_existing_supplier(inventory: Inventory, supplier_id: str) -> Supplier | None:
    """Looks through the products for a Supplier with this ID."""
    for product in inventory.get_all_products():
        if product.get_supplier().get_supplier_id() == supplier_id:
            return product.get_supplier()
    return None


def ask_for_supplier(inventory: Inventory) -> Supplier | None:
    """Reuses a known supplier, or asks for the details of a new one.
    Returns None if the input is not usable."""
    supplier_id = input("Supplier ID: ").strip()
    if supplier_id == "":
        print("  ❌ Supplier ID cannot be empty. Product not added.\n")
        return None

    supplier = find_existing_supplier(inventory, supplier_id)
    if supplier is not None:
        print("  Using existing supplier:")
        print("  ", end="")
        supplier.display_information()
        return supplier

    name = input("Supplier Name: ").strip()
    email = input("Supplier Contact Email: ").strip()
    if name == "" or "@" not in email:
        print("  ❌ Supplier needs a name and a valid email. Product not added.\n")
        return None
    return Supplier(supplier_id, name, email)


def add_product_action(inventory: Inventory) -> None:
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()

    if inventory.find_product(product_id) is not None:
        print(f"  ❌ A product with ID {product_id} already exists.\n")
        return

    print("Product Type:")
    print("  1. Physical")
    print("  2. Digital")
    type_choice = input("Choose type (1/2): ").strip()
    if type_choice not in PRODUCT_TYPES:
        print("  ❌ Invalid product type. Product not added.\n")
        return
    product_type = PRODUCT_TYPES[type_choice]

    name = input("Product Name: ").strip()

    # Do not carry on with incomplete data: ask again until both are valid
    price = get_positive_float("Price: ")
    stock = get_non_negative_int("Stock Quantity: ")

    supplier = ask_for_supplier(inventory)
    if supplier is None:
        return

    try:
        size = float(input(SIZE_PROMPTS[product_type]).strip())
    except ValueError:
        print("  ❌ Weight / Download Size must be a number. Product not added.\n")
        return
    if size < 0:
        print("  ❌ Weight / Download Size cannot be negative. Product not added.\n")
        return

    # The factory decides which Product subclass to build. The Product
    # validates its own price and stock and raises ValueError if a rule is broken.
    try:
        product = ProductFactory.create(product_type, product_id, name, price,
                                        stock, supplier, size)
    except ValueError as e:
        print(f"  ❌ {e} Product not added.\n")
        return

    inventory.add_product(product)
    print("\nProduct added successfully!\n")


def update_stock_action(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()

    product = inventory.find_product(product_id)
    if product is None:
        print("\nProduct not found.\n")
        return

    print("\nProduct Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}\n")

    new_stock = get_non_negative_int("New Stock Quantity: ")

    if inventory.update_stock(product_id, new_stock):
        print("\nStock updated successfully!\n")
    else:
        print("  ❌ Stock cannot be negative. No changes made.\n")


def search_product_action(inventory: Inventory) -> None:
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()

    product = inventory.find_product(product_id)
    if product is None:
        print("\nProduct not found.\n")
        return

    print("\nProduct Found")
    print("-" * 50)
    product.display_information()
    product.get_supplier().display_information()
    print(f"Fulfilment: {product.get_fulfilment_info()}")
    if isinstance(product, CanBeShipped):
        print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
    print("-" * 50 + "\n")


def import_products_action(inventory: Inventory) -> None:
    print("\nImport Products from CSV")
    print(f"File: {PRODUCTS_FILE}")
    print("Every imported product is given the same supplier.")

    supplier = ask_for_supplier(inventory)
    if supplier is None:
        return

    print()
    load_products(PRODUCTS_FILE, inventory, supplier)
    print()


# ---------------------------------------------------------------------
# Menu System
# ---------------------------------------------------------------------
def print_menu() -> None:
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Import Products from CSV")
    print("7. Exit")
    print("-" * 28)


def main() -> None:
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
            import_products_action(inventory)
        elif choice == "7":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("  ❌ Invalid option. Please enter a number between 1 and 7.\n")


if __name__ == "__main__":
    main()