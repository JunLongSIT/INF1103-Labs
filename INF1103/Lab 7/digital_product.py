"""
digital_product.py
------------------
DigitalProduct: a Product that has a download size.
It is NOT shippable, so it does not implement CanBeShipped.
"""

from product import Product


class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.__download_size = download_size  # megabytes

    def get_download_size(self):
        return self.__download_size

    # ---- Overrides ----
    def display_information(self):
        super().display_information()  # parent prints the common info
        print(f"    Download size: {self.__download_size} MB")

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data

    # ---- Implements abstract method from Product ----
    def get_fulfilment_info(self):
        return "Digital product: delivered via download. No shipping required."