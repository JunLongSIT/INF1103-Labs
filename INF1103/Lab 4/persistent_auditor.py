"""
Smart Inventory Auditor (persostent_auditor Version)
------------------------------------------
Processes daily stock deliveries. Validates each entry against business
rules without crashing. Now split into functions so new features (tax,
discounts, etc.) can be added without touching the main loop.
"""

import ast
import os

TAX_RATE = 0.10
OVERSTOCK_LIMIT = 500
INVENTORY_FILE = "inventory.txt"


def load_inventory():
    """
    Reads the previously saved inventory total and order history from
    inventory.txt. Returns (0, []) if the file doesn't exist or can't be
    parsed, so the program can always start cleanly.
    """
    if not os.path.exists(INVENTORY_FILE):
        return 0, []

    total_inventory = 0
    transaction_history = []

    try:
        with open(INVENTORY_FILE, "r") as f:
            for line in f:
                if line.startswith("Total:"):
                    total_inventory = int(line.split(":", 1)[1].strip())
                elif line.startswith("History:"):
                    transaction_history = ast.literal_eval(line.split(":", 1)[1].strip())
    except (IOError, ValueError, SyntaxError):
        return 0, []

    return total_inventory, transaction_history


def save_inventory(total_inventory, transaction_history):
    """Writes the final total and transaction history to inventory.txt."""
    try:
        with open(INVENTORY_FILE, "w") as f:
            f.write(f"Total: {total_inventory}\n")
            f.write(f"History: {transaction_history}\n")
        print("Order successfully saved to inventory.txt")
    except IOError as e:
        print(f"  ⚠️  Warning: could not save inventory ({e})")


def display_orders(transaction_history):
    """Prints the current list of orders, if any."""
    if not transaction_history:
        return
    print("Current Orders:\n")
    for order_id, product_name, quantity in transaction_history:
        print(f"{order_id}, {product_name}, {quantity}")
    print()


def get_valid_input():
    """
    Prompts the user for a stock quantity.
    Returns:
        - an int if the entry is a valid, non-negative whole number
        - the string "quit" if the user wants to stop
        - None if the entry was invalid (caller should count it as failed)
    """
    user_input = input("Enter stock quantity: ")

    if user_input.lower() == "quit":
        return "quit"

    if not user_input.isdigit():
        print(f"  ❌ Invalid entry: '{user_input}' is not a valid whole number.\n")
        return None

    quantity = int(user_input)

    if quantity < 0:
        print(f"  ❌ Invalid entry: {quantity} is negative. Stock cannot be negative.\n")
        return None

    return quantity


def process_delivery(current_total, new_value):
    """Adds a new delivery to the running total and returns the new total."""
    return current_total + new_value


def calculate_tax(amount):
    """Returns the tax owed on a single delivery amount (10% of that delivery)."""
    return amount * TAX_RATE


def generate_report(total_units, failed_attempts, deliveries_processed, total_tax, transaction_history):
    """Prints the final end-of-session summary."""
    print("\n=== End of Session Report ===")
    print(f"Total Deliveries Processed: {deliveries_processed}")
    print(f"Total Units Processed: {total_units}")
    print(f"Total Tax Collected: {total_tax:.2f}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")
    print(f"Transaction History: {transaction_history}")


def main():
    total_inventory, transaction_history = load_inventory()
    failed_entries = 0
    deliveries_processed = 0
    total_tax_collected = 0.0
    next_order_id = max((order[0] for order in transaction_history), default=1000) + 1

    print("=== Smart Inventory Auditor (Modular) ===")
    print("Enter stock quantities one at a time. Type 'quit' to finish.\n")
    if total_inventory > 0:
        print(f"📦 Loaded existing inventory: {total_inventory} units\n")

    display_orders(transaction_history)

    while True:
        result = get_valid_input()

        if result == "quit":
            save_inventory(total_inventory, transaction_history)
            break

        if result is None:
            failed_entries += 1
            continue

        quantity = result

        product_name = input("Enter Product Name: ")

        total_inventory = process_delivery(total_inventory, quantity)
        deliveries_processed += 1

        order_id = next_order_id
        next_order_id += 1
        transaction_history.append((order_id, product_name, quantity))

        delivery_tax = calculate_tax(quantity)
        total_tax_collected += delivery_tax

        print(f"\nNew Order Added:\n{order_id},{product_name},{quantity}")
        print(f"  ✅ Accepted. Delivery tax: {delivery_tax:.2f} | Running total: {total_inventory}\n")

        if total_inventory > OVERSTOCK_LIMIT:
            print(f"  🚨 OVERSTOCK ALERT: Inventory ({total_inventory}) exceeds limit of {OVERSTOCK_LIMIT}!")
            print("  Rejecting further entries.\n")
            break
        elif total_inventory == OVERSTOCK_LIMIT:
            print("  ⚠️  Inventory is exactly at capacity. Next entry will trigger an alert.\n")

    generate_report(total_inventory, failed_entries, deliveries_processed, total_tax_collected, transaction_history)


if __name__ == "__main__":
    main()