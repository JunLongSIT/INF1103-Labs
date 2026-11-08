"""
lab8_tests.py
-------------
Test script for Lab 8: association, aggregation, composition, LSP, polymorphism.

BEFORE you run each section, write your "Predict first" answer in your Word
document. Run one section at a time by commenting out the others in the
__main__ block at the bottom.
"""

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order


def heading(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# ---------------------------------------------------------------------
# Section 2: Association (Supplier - Product)
# ---------------------------------------------------------------------
def test_association() -> None:
    heading("SECTION 2: ASSOCIATION (Supplier - Product)")
    # >>> PREDICT FIRST (Section 2.2): what happens after `del supplier`?
    supplier = Supplier("S001", "Acme Supplies", "sales@acme.com")
    laptop = PhysicalProduct("P001", "Laptop", 1200.00, 10, supplier, 2.5)
    ebook = DigitalProduct("P002", "Python eBook", 25.00, 100, supplier, 15.0)

    print("Supplier info through each Product:")
    laptop.get_supplier().display_information()
    ebook.get_supplier().display_information()
    print("Same Supplier object shared by both products:",
          laptop.get_supplier() is ebook.get_supplier())

    del supplier
    print("\nAfter `del supplier`:")
    laptop.get_supplier().display_information()
    ebook.get_supplier().display_information()


# ---------------------------------------------------------------------
# Section 3: Aggregation (Inventory - Product)
# ---------------------------------------------------------------------
def test_aggregation() -> None:
    heading("SECTION 3: AGGREGATION (Inventory - Product)")
    supplier = Supplier("S001", "Acme Supplies", "sales@acme.com")
    # The product exists BEFORE any inventory holds it
    mouse = PhysicalProduct("P003", "Wireless Mouse", 29.90, 50, supplier, 0.2)
    inventory_a = Inventory()
    inventory_b = Inventory()

    inventory_a.add_product(mouse)
    print("Added to Inventory A:", inventory_a.find_product("P003") is mouse)

    # >>> PREDICT FIRST (Section 3.2): will the Product still work after removal?
    inventory_a.remove_product("P003")
    print("Still in Inventory A:", inventory_a.find_product("P003") is not None)
    print("\nProduct after removal from Inventory A:")
    mouse.display_information()
    print("Stock update still works:", mouse.update_stock(45))

    inventory_b.add_product(mouse)
    print("\nSame object now in Inventory B:", inventory_b.find_product("P003") is mouse)
    inventory_b.display_all()


# ---------------------------------------------------------------------
# Section 4: Composition (Order - OrderLine)
# ---------------------------------------------------------------------
def test_composition() -> None:
    heading("SECTION 4: COMPOSITION (Order - OrderLine)")
    supplier = Supplier("S001", "Acme Supplies", "sales@acme.com")
    laptop = PhysicalProduct("P001", "Laptop", 1200.00, 10, supplier, 2.5)
    ebook = DigitalProduct("P002", "Python eBook", 25.00, 100, supplier, 15.0)

    order_1 = Order("O001")
    order_1.add_order_line(laptop, 1)
    order_1.add_order_line(ebook, 2)
    order_1.display_information()

    # >>> PREDICT FIRST (Section 4.3): same Product in two Orders -
    #     how many OrderLine objects and how many Product objects?
    order_2 = Order("O002")
    order_2.add_order_line(laptop, 3)
    order_2.display_information()

    line_1 = order_1.get_order_lines()[0]
    line_2 = order_2.get_order_lines()[0]
    print("\nSame OrderLine object in both orders:", line_1 is line_2)
    print("Same Product object in both lines:   ",
          line_1.get_product() is line_2.get_product())
    print("id(line_1), id(line_2):", id(line_1), id(line_2))
    print("id(product via line_1), id(product via line_2):",
          id(line_1.get_product()), id(line_2.get_product()))

    print("\nRemove the eBook line from Order O001 (through the Order):")
    print("Removed:", order_1.remove_order_line("P002"))
    order_1.display_information()


# ---------------------------------------------------------------------
# Sections 6 and 7: LSP and polymorphism
# ---------------------------------------------------------------------
def show_product_details(product: Product) -> None:
    """Works for ANY Product: it only uses what Product promises."""
    product.display_information()
    print(product.get_fulfilment_info())


def test_lsp_and_polymorphism() -> None:
    heading("SECTIONS 6-7: LSP AND POLYMORPHISM")
    supplier = Supplier("S001", "Acme Supplies", "sales@acme.com")
    laptop = PhysicalProduct("P001", "Laptop", 1200.00, 10, supplier, 2.5)
    ebook = DigitalProduct("P002", "Python eBook", 25.00, 100, supplier, 15.0)

    print("--- show_product_details() with each subclass ---")
    show_product_details(laptop)
    show_product_details(ebook)

    print("\n--- Both types in ONE Inventory, ONE loop ---")
    # >>> PREDICT FIRST (Section 7.2): what will get_fulfilment_info() print for each?
    inventory = Inventory()
    inventory.add_product(laptop)
    inventory.add_product(ebook)
    for product in inventory.get_all_products():
        show_product_details(product)

    print("\n--- Normal Product operations on both types ---")
    print("update_stock on physical:", inventory.update_stock("P001", 8))
    print("update_stock on digital: ", inventory.update_stock("P002", 90))
    print("negative stock rejected by both:",
          inventory.update_stock("P001", -1), inventory.update_stock("P002", -1))


if __name__ == "__main__":
    test_association()
    test_aggregation()
    test_composition()
    test_lsp_and_polymorphism()