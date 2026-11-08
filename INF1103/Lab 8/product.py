"""
product.py
----------
Product class (abstract).
Responsibility (SRP): hold the details COMMON to every product.
It cannot be instantiated directly: every product must be a
PhysicalProduct or a DigitalProduct.

Relationship: ASSOCIATION with Supplier. The Supplier object is created
independently and passed in; the Product only keeps a reference to it.
"""

from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier):
        # Private by convention (name mangling): outside code should use methods
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.__supplier: Supplier = supplier

    # ---------------- Getters ----------------
    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    # ---------------- Behaviour ----------------
    def update_stock(self, quantity: int) -> bool:
        """Sets the stock. Returns False (no change) if quantity is negative."""
        if quantity < 0:
            return False
        self.__stock = quantity
        return True

    def display_information(self) -> None:
        """Prints the common product information on one line."""
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    def to_dict(self) -> dict:
        """Returns the common product data as a dictionary.
        Subclasses extend this with their own type and attributes."""
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": {
                "id": self.__supplier.get_supplier_id(),
                "name": self.__supplier.get_name(),
                "contact_email": self.__supplier.get_contact_email(),
            },
        }

    # ---------------- Abstract method ----------------
    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Returns a message describing how this product is fulfilled.
        Every subclass MUST implement this."""
        pass