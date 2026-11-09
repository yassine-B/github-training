"""Order state management workflow including cancellation."""

class Order:
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.status = "active"

    def cancel_order(self) -> bool:
        """Cancels an active order before it reaches the kitchen."""
        if self.status != "active":
            raise ValueError(f"Cannot cancel order in status: {self.status}")
        self.status = "cancelled"
        return True