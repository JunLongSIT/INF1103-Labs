"""
inventory.py
------------
Inventory class.
Responsibility (SRP): manage a COLLECTION of Product objects.
It does not ask for user input or read/write files.
"""


class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        """Adds a Product. Returns False if the ID already exists."""
        if self.search_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id):
        """Returns the matching Product, or None if not found."""
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def update_stock(self, product_id, quantity):
        """Returns True if the product exists and the update was accepted."""
        product = self.search_product(product_id)
        if product is None:
            return False
        return product.update_stock(quantity)

    def display_all(self):
        """Prints every product in the inventory."""
        print("\nCurrent Inventory")
        print("-" * 50)
        if not self.__products:
            print("No products in inventory.")
        for product in self.__products:
            product.display_information()
        print("-" * 50 + "\n")

    def get_all_products(self):
        """Returns a copy of the product list (protects the private list)."""
        return list(self.__products)