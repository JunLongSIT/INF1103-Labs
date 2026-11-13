"""
discount_strategy.py
--------------------
Discount strategies (Strategy pattern).

Problem solved: one task (discounting an order total) can be done in several
different ways. Instead of an if/elif block inside Order, each way of
discounting lives in its own class. Every strategy provides the same apply()
method, so Order can use any of them without knowing how they work.

OCP: a new discount means a new class here. Order does not change.
"""

from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        """Takes an order total and returns the discounted total."""
        pass


class NoDiscount(DiscountStrategy):
    """Default strategy: the total is unchanged."""

    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    """Takes a percentage off, e.g. PercentageDiscount(10) takes 10% off."""

    def __init__(self, percentage: float):
        if percentage < 0 or percentage > 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.__percentage: float = percentage

    def get_percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)


class BulkDiscount(DiscountStrategy):
    """Takes a fixed amount off any total at or above a threshold,
    e.g. BulkDiscount(200, 20) takes 20 off any total of 200 or more."""

    def __init__(self, threshold: float, amount: float):
        if threshold < 0 or amount < 0:
            raise ValueError("Threshold and amount cannot be negative.")
        self.__threshold: float = threshold
        self.__amount: float = amount

    def get_threshold(self) -> float:
        return self.__threshold

    def get_amount(self) -> float:
        return self.__amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return max(total - self.__amount, 0.0)  # never below zero
        return total


class StudentDiscount(DiscountStrategy):
    """Section 2.4: a 5% student discount.
    Added as a NEW class only - Order did not need to change (OCP)."""

    RATE: float = 0.05

    def apply(self, total: float) -> float:
        return total * (1 - self.RATE)
