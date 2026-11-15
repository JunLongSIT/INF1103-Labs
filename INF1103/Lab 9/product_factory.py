"""
ProductFactory class (Factory pattern).
Responsibility (SRP): decide WHICH Product subclass to create.

The rest of the program asks the factory for a product and only works with
the base type Product. This is the one place that knows about every concrete
product class, so a new product type means one change here instead of a
change in every place that creates products.

Relationship: DEPENDENCY on Product. The factory creates products and hands
them back; it does not store them.
"""

from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


class ProductFactory:
    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock: int, supplier: Supplier, size: float = 0.0) -> Product:
        """Creates the Product subclass that matches product_type.

        size is the one value that differs between the types:
          - "physical": the weight in kilograms
          - "digital":  the download size in megabytes

        Raises ValueError if product_type is not a known type."""
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock, supplier, size)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock, supplier, size)
        else:
            raise ValueError(f"Unknown product type: {product_type}")
