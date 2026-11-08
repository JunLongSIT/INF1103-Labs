"""
inventory.py
------------
Inventory class.
Responsibility (SRP): manage a COLLECTION of Product objects.
It does not ask for user input or read/write files.

Relationship: AGGREGATION with Product. The Inventory holds references to
Products but does not create them or control their lifecycle. A Product can
exist before it is added, and can be removed or moved to another Inventory
without being destroyed.

LSP: the collection is typed with the base class Product, so the Inventory
never needs to know whether an item is a PhysicalProduct or a DigitalProduct.
"""

from product import Product


class Inventory:
    def __init__(self):
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        """Adds an existing Product. Returns False if the ID already exists."""
        if self.find_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> bool:
        """Removes the matching Product REFERENCE from this inventory.
        The Product object itself is not destroyed.
        Returns False if no product has that ID."""
        product = self.find_product(product_id)
        if product is None:
            return False
        self.__products.remove(product)
        return True

    def find_product(self, product_id: str) -> Product | None:
        """Returns the matching Product, or None if not found."""
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def update_stock(self, product_id: str, quantity: int) -> bool:
        """Returns True if the product exists and the update was accepted."""
        product = self.find_product(product_id)
        if product is None:
            return False
        return product.update_stock(quantity)

    def display_all(self) -> None:
        """Prints every product in the inventory."""
        print("\nCurrent Inventory")
        print("-" * 50)
        if not self.__products:
            print("No products in inventory.")
        for product in self.__products:
            product.display_information()
        print("-" * 50 + "\n")

    def get_all_products(self) -> list[Product]:
        """Returns a copy of the product list (protects the private list)."""
        return list(self.__products)