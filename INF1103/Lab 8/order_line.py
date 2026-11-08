"""
order_line.py
-------------
OrderLine class.
One product and the quantity of it requested in ONE order.

Relationship: ASSOCIATION with Product (it refers to a Product but does not
own it) and the PART in a COMPOSITION with Order. An OrderLine is created by
its Order (see Order.add_order_line) and is never moved to another Order.
"""

from product import Product


class OrderLine:
    def __init__(self, product: Product, quantity: int):
        self.__product: Product = product
        self.__quantity: int = quantity

    # ---------------- Getters ----------------
    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    # ---------------- Behaviour ----------------
    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def display_information(self) -> None:
        print(f"    {self.__product.get_name()} | Qty: {self.__quantity} | "
              f"Unit: ${self.__product.get_price():.2f} | "
              f"Subtotal: ${self.calculate_subtotal():.2f}")