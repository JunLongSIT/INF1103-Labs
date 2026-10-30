"""
can_be_shipped.py
-----------------
CanBeShipped interface (interface-style abstract base class).
It is a contract only: any class that can be shipped must be able to
calculate its shipping cost. No attributes, no shipping logic here.
"""

from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        """Returns the shipping cost for this item."""
        pass