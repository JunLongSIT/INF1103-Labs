"""
Section 2.2 / 2.4: each discount strategy on its own.
"""

import pytest

from discount_strategy import (BulkDiscount, DiscountStrategy, NoDiscount,
                               PercentageDiscount, StudentDiscount)


def test_discount_strategy_is_abstract():
    with pytest.raises(TypeError):
        DiscountStrategy()


def test_no_discount_returns_total_unchanged():
    assert NoDiscount().apply(250.0) == 250.0


def test_percentage_discount_takes_percentage_off():
    assert PercentageDiscount(10).apply(250.0) == pytest.approx(225.0)


def test_bulk_discount_applies_at_threshold():
    assert BulkDiscount(200, 20).apply(200.0) == pytest.approx(180.0)


def test_bulk_discount_applies_above_threshold():
    assert BulkDiscount(200, 20).apply(250.0) == pytest.approx(230.0)


def test_bulk_discount_not_applied_below_threshold():
    assert BulkDiscount(200, 20).apply(199.99) == pytest.approx(199.99)


def test_student_discount_takes_five_percent_off():
    assert StudentDiscount().apply(200.0) == pytest.approx(190.0)


def test_every_strategy_is_a_discount_strategy():
    strategies = [NoDiscount(), PercentageDiscount(10),
                  BulkDiscount(200, 20), StudentDiscount()]
    for strategy in strategies:
        assert isinstance(strategy, DiscountStrategy)
