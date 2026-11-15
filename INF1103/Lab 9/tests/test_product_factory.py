"""
Section 3: products are created through the ProductFactory.
"""

import pytest

from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from product_factory import ProductFactory


def test_factory_creates_physical_product(supplier):
    product = ProductFactory.create("physical", "P001", "Desk Lamp",
                                    25.00, 10, supplier, 1.2)
    assert isinstance(product, PhysicalProduct)
    assert product.get_weight() == 1.2


def test_factory_creates_digital_product(supplier):
    product = ProductFactory.create("digital", "D001", "Photo Editor",
                                    49.90, 100, supplier, 350.0)
    assert isinstance(product, DigitalProduct)
    assert product.get_download_size() == 350.0


def test_factory_passes_common_values_to_product(supplier):
    product = ProductFactory.create("physical", "P001", "Desk Lamp",
                                    25.00, 10, supplier)
    assert product.get_product_id() == "P001"
    assert product.get_name() == "Desk Lamp"
    assert product.get_price() == 25.00
    assert product.get_stock() == 10
    assert product.get_supplier() is supplier


def test_factory_products_can_be_used_as_product(supplier):
    """Polymorphism: callers only need the base type Product."""
    products = [
        ProductFactory.create("physical", "P001", "Desk Lamp", 25.00, 10, supplier),
        ProductFactory.create("digital", "D001", "Photo Editor", 49.90, 100, supplier),
    ]
    for product in products:
        assert isinstance(product, Product)
        assert isinstance(product.get_fulfilment_info(), str)


def test_unknown_product_type_raises_value_error(supplier):
    with pytest.raises(ValueError, match="Unknown product type: service"):
        ProductFactory.create("service", "S001", "Installation", 30.00, 5, supplier)
