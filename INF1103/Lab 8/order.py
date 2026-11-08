"""
order.py
--------
Order class.
Responsibility (SRP): hold the order lines of one order and total them.

Relationship: COMPOSITION with OrderLine. The Order CREATES and manages its
own OrderLine objects: callers pass a Product and a quantity, never an
OrderLine. When the Order goes away, so do its lines.
"""

from order_line import OrderLine
from product import Product


class Order:
    def __init__(self, order_id: str):
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    # ---------------- Getters ----------------
    def get_order_id(self) -> str:
        return self.__order_id

    def get_order_lines(self) -> list[OrderLine]:
        """Returns a copy of the list (protects the private list)."""
        return list(self.__order_lines)

    # ---------------- Behaviour ----------------
    def add_order_line(self, product: Product, quantity: int) -> None:
        """The Order creates the OrderLine itself (this is what makes it composition)."""
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        """Removes the line for that product from THIS order.
        Returns False if the order has no such line."""
        for order_line in self.__order_lines:
            if order_line.get_product().get_product_id() == product_id:
                self.__order_lines.remove(order_line)
                return True
        return False

    def calculate_total(self) -> float:
        """Asks each OrderLine for its subtotal and adds them up."""
        total: float = 0.0
        for order_line in self.__order_lines:
            total += order_line.calculate_subtotal()
        return total

    def display_information(self) -> None:
        print(f"Order {self.__order_id}")
        for order_line in self.__order_lines:
            order_line.display_information()
        print(f"  Total: ${self.calculate_total():.2f}")