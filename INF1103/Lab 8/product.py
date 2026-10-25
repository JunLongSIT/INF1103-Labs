"""
product.py
----------
Product class.
Responsibility (SRP): represent and manage ONE product.
It does not load/save files, show menus or ask the user for input.
"""


class Product:
    def __init__(self, product_id, name, price, stock):
        # Private by convention (name mangling): outside code should use methods
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    # ---------------- Getters ----------------
    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    # ---------------- Behaviour ----------------
    def update_stock(self, quantity):
        """Sets the stock. Returns False (no change) if quantity is negative."""
        if quantity < 0:
            return False
        self.__stock = quantity
        return True

    def display_information(self):
        """Prints this product on one line."""
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    def to_dict(self):
        """Returns the product as a dictionary (same keys as Week 5 JSON)."""
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }