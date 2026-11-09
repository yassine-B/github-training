"""Order workflow (Unfixed / Problem State)."""

class Order:
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.status = "active"

    # Problem: Lacks state checking or cancellation protection methods