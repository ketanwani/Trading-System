import unittest
from collections import deque
from sortedcontainers import SortedDict
from order import Order
from order_book import OrderBook


class MockOrder:
    def __init__(self, order_id, order_type, price, quantity):
        self.order_id = order_id
        self.order_type = order_type
        self.price = price
        self.quantity = quantity

class TestOrderBook(unittest.TestCase):
    
    def setUp(self):
        # Initialize a new OrderBook for each test
        self.order_book = OrderBook('AAPL')

    def test_add_buy_order(self):
        # Add a buy order and check the buy_book
        buy_order = Order(1, 'BUY', 'AAPL', 100, 10)
        trades = self.order_book.add_order(buy_order)
        
        self.assertEqual(len(trades), 0)  # No trades since no matching sell orders
        self.assertIn(10, self.order_book.buy_book)
        self.assertEqual(self.order_book.buy_book[10].total_volume, 100)

    def test_add_sell_order(self):
        # Add a sell order and check the sell_book
        sell_order = Order(2, 'SELL', 'AAPL', 105, 5)
        trades = self.order_book.add_order(sell_order)
        
        self.assertEqual(len(trades), 0)  # No trades since no matching buy orders
        self.assertIn(5, self.order_book.sell_book)
        self.assertEqual(self.order_book.sell_book[5].total_volume, 105)

    def test_match_buy_and_sell_orders(self):
        # Add a buy order and a matching sell order
        buy_order = Order(1, 'BUY', 'AAPL', 10, 100)
        self.order_book.add_order(buy_order)

        sell_order = Order(2, 'SELL', 'AAPL', 5, 100)
        trades = self.order_book.add_order(sell_order)

        # Check that trade is generated
        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0].quantity, 5)
        self.assertEqual(trades[0].price, 100)

        # Check the remaining buy quantity
        self.assertEqual(self.order_book.buy_book[100].total_volume, 5)

    def test_cancel_order(self):
        # Add and cancel a buy order
        buy_order = Order(1, 'BUY', 'AAPL', 10, 5)
        self.order_book.add_order(buy_order)

        # Cancel the order
        cancel_result = self.order_book.cancel_order(buy_order.order_id)
        self.assertTrue(cancel_result)

        # Ensure the order is removed
        self.assertNotIn(100, self.order_book.buy_book)

    def test_cancel_nonexistent_order(self):
        # Expecting an exception when canceling a non-existent order
        with self.assertRaises(Exception) as context:
            self.order_book.cancel_order(1)  # Use a non-existent order ID

        self.assertEqual(str(context.exception), "Order ID 1 not found")  

    

if __name__ == '__main__':
    unittest.main()
