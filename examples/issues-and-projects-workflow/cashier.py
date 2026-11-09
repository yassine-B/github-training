"""Cashier calculation module with quantity validation fix."""

def calculate_order_total(price: float, quantity: int) -> float:
    """Calculates order total with validation to prevent invalid numbers."""
    try:
        parsed_price = float(price)
    except (TypeError, ValueError):
        parsed_price = 0.0

    try:
        parsed_quantity = int(quantity)
    except (TypeError, ValueError):
        parsed_quantity = 0

    if parsed_quantity < 1:
        raise ValueError("Quantity must be at least 1")

    return parsed_price * parsed_quantity