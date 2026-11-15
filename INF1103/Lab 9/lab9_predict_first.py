"""
Run script for the Lab 9 "Predict first" questions.
Write your prediction down first, then run:  python3 lab9_predict_first.py

The LAST section (3.2) crashes on purpose, to show what an uncaught
exception does to a program.
"""

from discount_strategy import BulkDiscount, PercentageDiscount, StudentDiscount
from inventory import Inventory
from inventory_manager import PRODUCTS_FILE, get_positive_float, load_products
from order import Order
from product_factory import ProductFactory
from supplier import Supplier


def heading(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# ---------------------------------------------------------------------
# Section 2.3: swapping the strategy on one order
# ---------------------------------------------------------------------
def predict_strategy(supplier: Supplier) -> None:
    heading("SECTION 2.3: STRATEGY (order lines add up to 250)")
    chair = ProductFactory.create("physical", "P001", "Office Chair",
                                  125.00, 10, supplier, 8.5)
    order = Order("O001", BulkDiscount(200, 20))
    order.add_order_line(chair, 2)

    # >>> PREDICT FIRST (Section 2.3): what does calculate_total() return?
    print("With BulkDiscount(200, 20):          ", order.calculate_total())

    order.set_discount(PercentageDiscount(10))
    print("After set_discount(Percentage(10)):  ", order.calculate_total())

    # Section 2.4: a fourth strategy, with no change to order.py
    order.set_discount(StudentDiscount())
    print("After set_discount(StudentDiscount()):", order.calculate_total())


# ---------------------------------------------------------------------
# Section 2.4: Order - DiscountStrategy relationship
# ---------------------------------------------------------------------
def predict_relationship(supplier: Supplier) -> None:
    heading("SECTION 2.4: CAN TWO ORDERS SHARE ONE STRATEGY?")
    ebook = ProductFactory.create("digital", "D001", "Python eBook",
                                  25.00, 100, supplier, 15.0)
    # >>> PREDICT FIRST (Section 2.4): association, aggregation or composition?
    shared = PercentageDiscount(10)
    order_1 = Order("O001", shared)
    order_2 = Order("O002", shared)
    order_1.add_order_line(ebook, 4)
    order_2.add_order_line(ebook, 8)

    print("Same strategy object in both orders:",
          order_1.get_discount() is order_2.get_discount())
    print("Order O001 total:", order_1.calculate_total())
    print("Order O002 total:", order_2.calculate_total())

    del order_1
    print("After `del order_1`, the strategy still works:", shared.apply(100.0))


# ---------------------------------------------------------------------
# Section 4: validation
# ---------------------------------------------------------------------
def predict_validation(supplier: Supplier) -> None:
    heading("SECTION 4: VALIDATION (same rules for both product types)")
    # >>> PREDICT FIRST (Section 4): may DigitalProduct skip the stock rule?
    attempts = [("physical", 25.00, -1), ("digital", 25.00, -1),
                ("physical", 0, 5), ("digital", -9.99, 5)]
    for product_type, price, stock in attempts:
        try:
            ProductFactory.create(product_type, "X001", "Test", price, stock, supplier)
            print(f"{product_type:9} price={price} stock={stock} -> created")
        except ValueError as e:
            print(f"{product_type:9} price={price} stock={stock} -> ValueError: {e}")

    lamp = ProductFactory.create("physical", "P002", "Desk Lamp", 25.00, 10, supplier)
    try:
        Order("O003").add_order_line(lamp, 0)
    except ValueError as e:
        print(f"OrderLine quantity=0 -> ValueError: {e}")


# ---------------------------------------------------------------------
# Section 5.2: loading products from a file
# ---------------------------------------------------------------------
def predict_load_products(supplier: Supplier) -> None:
    heading("SECTION 5.2: load_products() WITH products.csv")
    # >>> PREDICT FIRST (Section 5.2): how many load, which messages, what order?
    inventory = Inventory()
    load_products(PRODUCTS_FILE, inventory, supplier)
    inventory.display_all()

    heading("SECTION 5.2: load_products() WITH A FILE THAT DOES NOT EXIST")
    # >>> PREDICT FIRST (Section 5.2): which of except, else and finally run?
    load_products("products_renamed.csv", Inventory(), supplier)


# ---------------------------------------------------------------------
# Section 5.1: user input
# ---------------------------------------------------------------------
def predict_user_input() -> None:
    heading("SECTION 5.1: get_positive_float()")
    # >>> PREDICT FIRST (Section 5.1): what prints after each entry?
    print("Type abc, then -5, then 12.50")
    value = get_positive_float("Price: ")
    print("Returned:", repr(value))


# ---------------------------------------------------------------------
# Section 3.2: unknown product type, with nothing catching the exception
# ---------------------------------------------------------------------
def predict_unknown_type(supplier: Supplier) -> None:
    heading("SECTION 3.2: ProductFactory.create(\"service\", ...) NOT CAUGHT")
    # >>> PREDICT FIRST (Section 3.2): which line raises, and what happens next?
    ProductFactory.create("service", "S001", "Installation", 30.00, 5, supplier)
    print("This line never runs.")


if __name__ == "__main__":
    acme = Supplier("S001", "Acme Supplies", "sales@acme.com")
    predict_strategy(acme)
    predict_relationship(acme)
    predict_validation(acme)
    predict_load_products(acme)
    predict_user_input()
    predict_unknown_type(acme)   # crashes on purpose: keep this last
