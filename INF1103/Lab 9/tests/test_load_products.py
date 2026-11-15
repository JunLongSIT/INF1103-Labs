"""
Section 5.2: loading products from a CSV file.
tmp_path is a temporary folder pytest creates for each test, so the tests
never touch the real products.csv.
"""

from inventory import Inventory
from inventory_manager import load_products

LAB_CSV = """product_type,product_id,name,price,stock_quantity
physical,P001,Desk Lamp,25.00,10
digital,D001,Photo Editor,49.90,100
service,S001,Installation,30.00,5
physical,P002,Office Chair,abc,3
physical,P003,Monitor Stand,39.50,7
"""


def write_csv(tmp_path, text: str) -> str:
    path = tmp_path / "products.csv"
    path.write_text(text)
    return str(path)


def test_valid_rows_load_and_bad_rows_are_skipped(tmp_path, supplier):
    inventory = Inventory()
    load_products(write_csv(tmp_path, LAB_CSV), inventory, supplier)

    loaded_ids = [p.get_product_id() for p in inventory.get_all_products()]
    assert loaded_ids == ["P001", "D001", "P003"]


def test_messages_print_in_order(tmp_path, supplier, capsys):
    load_products(write_csv(tmp_path, LAB_CSV), Inventory(), supplier)

    printed = capsys.readouterr().out.splitlines()
    assert len(printed) == 4
    assert printed[0].startswith("Skipped line 4")
    assert "Unknown product type: service" in printed[0]
    assert printed[1].startswith("Skipped line 5")
    assert "abc" in printed[1]
    assert printed[2] == "3 products loaded."
    assert printed[3] == "Load attempt finished."


def test_loaded_products_use_the_given_supplier(tmp_path, supplier):
    inventory = Inventory()
    load_products(write_csv(tmp_path, LAB_CSV), inventory, supplier)

    for product in inventory.get_all_products():
        assert product.get_supplier() is supplier


def test_missing_file_is_handled_gracefully(tmp_path, supplier, capsys):
    inventory = Inventory()
    missing = str(tmp_path / "no_such_file.csv")

    load_products(missing, inventory, supplier)  # must not raise

    printed = capsys.readouterr().out.splitlines()
    assert printed == [f"Products file not found: {missing}",
                       "Load attempt finished."]
    assert inventory.get_all_products() == []


def test_row_that_fails_validation_is_skipped(tmp_path, supplier, capsys):
    text = ("product_type,product_id,name,price,stock_quantity\n"
            "physical,P001,Desk Lamp,-25.00,10\n"
            "physical,P002,Office Chair,89.00,-3\n"
            "physical,P003,Monitor Stand,39.50,7\n")
    inventory = Inventory()
    load_products(write_csv(tmp_path, text), inventory, supplier)

    assert [p.get_product_id() for p in inventory.get_all_products()] == ["P003"]
    assert "1 products loaded." in capsys.readouterr().out


def test_duplicate_product_id_is_skipped(tmp_path, supplier, capsys):
    text = ("product_type,product_id,name,price,stock_quantity\n"
            "physical,P001,Desk Lamp,25.00,10\n"
            "physical,P001,Desk Lamp Copy,25.00,10\n")
    inventory = Inventory()
    load_products(write_csv(tmp_path, text), inventory, supplier)

    assert len(inventory.get_all_products()) == 1
    assert "already exists" in capsys.readouterr().out
