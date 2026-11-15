"""
Section 2.3 / 2.4: the Order calculates its total through a DiscountStrategy.
"""

import pytest

from discount_strategy import (BulkDiscount, DiscountStrategy, NoDiscount,
                               PercentageDiscount, StudentDiscount)
from order import Order


def make_order_of_250(chair, discount=None) -> Order:
    order = Order("O001", discount)
    order.add_order_line(chair, 2)  # 2 x 125.00 = 250.00
    return order


def test_order_uses_no_discount_by_default(chair):
    order = make_order_of_250(chair)
    assert isinstance(order.get_discount(), NoDiscount)
    assert order.calculate_total() == pytest.approx(250.0)


def test_order_total_with_bulk_discount(chair):
    order = make_order_of_250(chair, BulkDiscount(200, 20))
    assert order.calculate_total() == pytest.approx(230.0)


def test_set_discount_changes_strategy_on_existing_order(chair):
    order = make_order_of_250(chair, BulkDiscount(200, 20))
    order.set_discount(PercentageDiscount(10))
    # The new strategy REPLACES the old one: 10% off 250, not off 230
    assert order.calculate_total() == pytest.approx(225.0)


def test_order_total_with_student_discount(chair):
    order = make_order_of_250(chair, StudentDiscount())
    assert order.calculate_total() == pytest.approx(237.5)


def test_new_strategy_works_without_changing_order(chair):
    """A strategy the Order has never heard of still works (OCP)."""

    class HalfPriceDiscount(DiscountStrategy):
        def apply(self, total: float) -> float:
            return total / 2

    order = make_order_of_250(chair, HalfPriceDiscount())
    assert order.calculate_total() == pytest.approx(125.0)


def test_two_orders_can_share_one_strategy(chair):
    """Association: the strategy is used by the orders, not owned by one."""
    shared = PercentageDiscount(10)
    order_1 = make_order_of_250(chair, shared)
    order_2 = Order("O002", shared)
    order_2.add_order_line(chair, 1)

    assert order_1.get_discount() is order_2.get_discount()
    assert order_1.calculate_total() == pytest.approx(225.0)
    assert order_2.calculate_total() == pytest.approx(112.5)


def test_empty_order_total_is_zero():
    assert Order("O003").calculate_total() == 0.0
