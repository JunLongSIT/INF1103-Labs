"""
physical_product.py
-------------------
PhysicalProduct class.
A PhysicalProduct IS-A Product, and it CanBeShipped.
"""

from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    # Simple shipping rule: flat base fee + a rate per kilogram
    BASE_SHIPPING_FEE = 5.00
    RATE_PER_KG = 2.00

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight  # in kilograms

    def get_weight(self):
        return self.__weight

    # ---- Overrides ----
    def display_information(self):
        super().display_information()
        print(f"    Weight: {self.__weight} kg")

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data

    # ---- Abstract method from Product ----
    def get_fulfilment_info(self):
        return "Physical product: requires physical shipping."

    # ---- Abstract method from CanBeShipped ----
    def calculate_shipping_cost(self):
        return self.BASE_SHIPPING_FEE + self.RATE_PER_KG * self.__weight