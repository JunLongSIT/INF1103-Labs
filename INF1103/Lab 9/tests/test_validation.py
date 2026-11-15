"""
Section 4: each class rejects data that breaks its own rules.
"""

import pytest

from digital_product import DigitalProduct
from order import Order
from order_line import OrderLine
from physical_product import PhysicalProduct


@pytest.mark.parametrize("price", [0, -0.01, -25.00])
def test_price_must_be_greater_than_zero(supplier, price):
    with pytest.raises(ValueError, match="Price must be greater than zero"):
        PhysicalProduct("P001", "Desk Lamp", price, 10, supplier, 1.2)


def test_stock_cannot_be_negative(supplier):
    with pytest.raises(ValueError, match="Stock quantity cannot be negative"):
        PhysicalProduct("P001", "Desk Lamp", 25.00, -1, supplier, 1.2)


def test_stock_of_zero_is_allowed(supplier):
    product = PhysicalProduct("P001", "Desk Lamp", 25.00, 0, supplier, 1.2)
    assert product.get_stock() == 0


def test_digital_product_follows_the_same_rules(supplier):
    """LSP: a subclass cannot skip the rules of Product."""
    with pytest.raises(ValueError):
        DigitalProduct("D001", "Photo Editor", 0, 100, supplier, 350.0)
    with pytest.raises(ValueError):
        DigitalProduct("D001", "Photo Editor", 49.90, -5, supplier, 350.0)


def test_update_stock_still_rejects_negative_quantity(chair):
    assert chair.update_stock(-1) is False
    assert chair.get_stock() == 10


@pytest.mark.parametrize("quantity", [0, -1])
def test_order_line_quantity_must_be_greater_than_zero(chair, quantity):
    with pytest.raises(ValueError, match="Quantity must be greater than zero"):
        OrderLine(chair, quantity)


def test_order_does_not_keep_an_invalid_line(chair):
    order = Order("O001")
    with pytest.raises(ValueError):
        order.add_order_line(chair, 0)
    assert order.get_order_lines() == []
