"""
digital_product.py
------------------
DigitalProduct class.
A DigitalProduct IS-A Product. It is NOT shipped, so it does not
implement CanBeShipped.
"""

from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, download_size: float):
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size: float = download_size  # in megabytes

    def get_download_size(self) -> float:
        return self.__download_size

    # ---- Overrides ----
    def display_information(self) -> None:
        super().display_information()
        print(f"    Download Size: {self.__download_size} MB")

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data

    # ---- Abstract method from Product ----
    def get_fulfilment_info(self) -> str:
        return "Digital product: delivered digitally via download."