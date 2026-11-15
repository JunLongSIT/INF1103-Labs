"""
discount_strategy.py
--------------------
Discount strategies (Strategy pattern).
Responsibility (SRP): each class knows ONE way of discounting an order total.

Every strategy provides the same apply() method, so the Order can use any
of them without knowing how the discount is worked out. A new discount is
a new class in this file; the Order class does not change (OCP).
"""

from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        """Takes an order total and returns the discounted total.
        Every strategy MUST implement this."""
        pass


class NoDiscount(DiscountStrategy):
    """Leaves the total unchanged."""

    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    """Takes a percentage off the total.
    PercentageDiscount(10) takes 10% off."""

    def __init__(self, percentage: float):
        self.__percentage: float = percentage

    def get_percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)


class BulkDiscount(DiscountStrategy):
    """Takes a fixed amount off once the total reaches a threshold.
    BulkDiscount(200, 20) takes 20 off any total of 200 or more."""

    def __init__(self, threshold: float, amount: float):
        self.__threshold: float = threshold
        self.__amount: float = amount

    def get_threshold(self) -> float:
        return self.__threshold

    def get_amount(self) -> float:
        return self.__amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return total - self.__amount
        return total


class StudentDiscount(DiscountStrategy):
    """Takes a fixed 5% off for students.
    Added in Section 2.4 WITHOUT changing the Order class."""

    STUDENT_RATE: float = 0.05

    def apply(self, total: float) -> float:
        return total * (1 - self.STUDENT_RATE)
