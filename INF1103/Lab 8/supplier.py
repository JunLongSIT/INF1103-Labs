"""
supplier.py
-----------
Supplier class.
Responsibility (SRP): hold and display the details of a supplier.

Relationship: ASSOCIATION with Product. A Supplier is created on its own
and is then handed to each Product it supplies. A Supplier does not store
its Products (loose coupling) and a Product is not a part of a Supplier.
"""


class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self.__supplier_id: str = supplier_id
        self.__name: str = name
        self.__contact_email: str = contact_email

    # ---------------- Getters ----------------
    def get_supplier_id(self) -> str:
        return self.__supplier_id

    def get_name(self) -> str:
        return self.__name

    def get_contact_email(self) -> str:
        return self.__contact_email

    # ---------------- Behaviour ----------------
    def display_information(self) -> None:
        """Prints the supplier details on one line."""
        print(f"Supplier ID: {self.__supplier_id} | Name: {self.__name} | "
              f"Email: {self.__contact_email}")