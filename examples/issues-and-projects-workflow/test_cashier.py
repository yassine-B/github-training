"""Integration tests for checkout and order total calculations."""
import unittest
from cashier import calculate_order_total

class TestCashierCheckout(unittest.TestCase):
    def test_valid_calculation(self):
        self.assertEqual(calculate_order_total(10.50, 2), 21.00)

    def test_zero_quantity_raises_error(self):
        with self.assertRaises(ValueError):
            calculate_order_total(15.00, 0)

if __name__ == '__main__':
    unittest.main()