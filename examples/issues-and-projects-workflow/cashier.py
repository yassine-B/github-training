"""Cashier calculation module (Unfixed / Problem State)."""

def calculate_order_total(price, quantity):
    # Problem: Direct multiplication without validating types or zero boundaries
    return price * quantity