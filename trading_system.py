from collections import defaultdict
import threading
from uuid import uuid4
from user import User
from order import Order
from order_book import OrderBook


class TradingSystem:
    def __init__(self):
        self.users = {}
        self.order_books = {}        
        self.trades = []        

    def register_user(self, name, phone, email):
        user_id = str(uuid4())
        user = User(user_id, name, phone, email)
        self.users[user_id] = user
        return user_id

    def place_order(self, user_id, order_type, symbol, quantity, price):
        if user_id not in self.users:
            raise Exception(f"Invalid user ID: {user_id}")
        order = Order(user_id, order_type, symbol, quantity, price)        
        if symbol not in self.order_books:
            self.order_books[symbol] = OrderBook(symbol)
        trades = self.order_books[symbol].add_order(order)
        self.trades.extend(trades)
        return order.order_id

    def cancel_order(self, symbol, order_id):        
        self.order_books[symbol].cancel_order(order_id)

    def modify_order(self, symbol, order_id, order_type, price, quantity):
        self.order_books[symbol].modify_order(order_id, order_type, price, quantity)

    def get_total_trades(self):
        return len(self.trades)
    
    def get_total_trade_quantity(self):
        quantity = 0
        for trade in self.trades:
            quantity += trade.quantity
        return quantity

    def get_order_status(self, order_id, symbol):
        return self.order_books[symbol].get_order_status(order_id);                        
    
    def print_order_book(self, symbol):
        if symbol in self.order_books:
            order_book = self.order_books[symbol]
            order_book.print()
