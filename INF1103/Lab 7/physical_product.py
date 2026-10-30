"""
physical_product.py
-------------------
PhysicalProduct: a Product that has a weight and can be shipped.
  - is-a Product            (inheritance)
  - CanBeShipped            (interface realisation)
"""

from product import Product
from can_be_shipped import CanBeShipped


class ç(Product, CanBeShipped):
    # Simple shipping rule: flat base fee + a rate per kilogram
    BASE_SHIPPING_FEE = 5.00
    RATE_PER_KG = 2.00

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight  # kilograms

    def get_weight(self):
        return self.__weight

    # ---- Overrides ----
    def display_information(self):
        super().display_information()  # parent prints the common info
        print(f"    Weight: {self.__weight} kg")

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data

    # ---- Implements abstract method from Product ----
    def get_fulfilment_info(self):
        return "Physical product: requires packing and physical shipping."

    # ---- Implements abstract method from CanBeShipped ----
    def calculate_shipping_cost(self):
        return self.BASE_SHIPPING_FEE + self.RATE_PER_KG * self.__weight