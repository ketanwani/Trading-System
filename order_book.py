from collections import deque
import threading
from sortedcontainers import SortedDict, SortedSet

from trade import Trade

"""
OrderBook Structure:
+--------------------------+
| OrderBook               |
|--------------------------|
| symbol: "AAPL"          |
|                          |
| buy_book:               |                sell_book:
| +--------------------+  |   +--------------------+
| | SortedDict         |  |   | SortedDict         |
| |                    |  |   |                    |
| |  Price Level 150  |  |   |  Price Level 100   | 
| |  total_volume: 20  |  |   |  total_volume: 30  |
| |  orders:           |  |   |  orders:           |
| |  deque([           |  |   |  deque([           |
| |      Order ID 1   |  |   |      Order ID 5   |  
| |      quantity: 10  |  |   |      quantity: 15  |  
| |      Order ID 2   |  |   |      Order ID 6   |  
| |      quantity: 10  |  |   |      quantity: 10  |  
| |  ])                |  |   |  ])                |  
| +--------------------+  |   +--------------------+  
|                          |   |                    |
|                          |   |  Price Level 110   | 
|                          |   |  total_volume: 25   |
|                          |   |  orders:           |
|                          |   |  deque([           |
|                          |   |      Order ID 8   |  
|                          |   |      quantity: 25  |  
|                          |   |  ])                |  
+--------------------------+   +--------------------+
"""

class PriceLevel:
    def __init__(self, limit_price):
        self.limit_price = limit_price
        self.total_volume = 0
        self.orders = deque()

    def append(self, order):        
        self.total_volume += order.quantity
        self.orders.append(order)
    
    def remove(self, deleting_order):                
        for i, order in enumerate(self.orders):
            if order.order_id == deleting_order.order_id:
                self.total_volume -= order.quantity
                del self.orders[i]
                break



class OrderBook:
    def __init__(self, symbol):
        self.buy_book = SortedDict(lambda x: -x) 
        self.sell_book = SortedDict() 
        self.lock = threading.Lock()
        self.symbol = symbol
        self.orders = {}

    def add_order(self, order):
        trades = []        
        with self.lock:
            if order.order_id in self.orders:
                raise Exception(f"Order ID {order.order_id} already exists in the system")
            if order.order_type == "BUY":
                trades = self._match_buy_order(order)
            elif order.order_type == "SELL":
                trades = self._match_sell_order(order)
            self.orders[order.order_id] = order
            return trades

    def _match_buy_order(self, new_order):        
        trades = []
        while self.sell_book and new_order.quantity > 0:
            #Fetch the lowest selling price of the stock
            lowest_selling_price, level = self.sell_book.peekitem(0)
            if lowest_selling_price <= new_order.price:
                sell_queue = level.orders
                sell_order = sell_queue[0]
                if sell_order.is_expired():
                    sell_queue.popleft()
                    continue
                trade_quantity = min(sell_order.quantity, new_order.quantity)
                sell_order.quantity -= trade_quantity
                new_order.quantity -= trade_quantity
                self.sell_book[lowest_selling_price].total_volume -= trade_quantity
                new_trade = Trade(new_order, sell_order, trade_quantity, lowest_selling_price)
                trades.append(new_trade)
                if sell_order.quantity == 0:
                    sell_queue.popleft()
                
                if len(sell_queue) == 0:
                    del self.sell_book[lowest_selling_price]  # Delete the price level in case if there are no more orders
            else:
                break

        if new_order.quantity > 0 and new_order.order_id not in self.orders:
            self._add_to_book(new_order)
        elif new_order.quantity == 0 and new_order.order_id in self.orders:
            self._remove_from_book(new_order)
        return trades
    
    def _match_sell_order(self, new_order):        
        trades = []
        while len(self.buy_book) > 0 and new_order.quantity > 0:
            highest_buying_price, level = self.buy_book.peekitem(0)
            if highest_buying_price >= new_order.price:
                buy_queue = level.orders
                buy_order = buy_queue[0]
                if buy_order.is_expired():
                    buy_queue.popleft()
                    continue
                trade_quantity = min(buy_order.quantity, new_order.quantity)
                trade = Trade(buy_order, new_order, trade_quantity, highest_buying_price)
                trades.append(trade)

                # Adjust the order quantities after they are converted to trades
                new_order.quantity -= trade_quantity
                buy_order.quantity -= trade_quantity
                self.buy_book[highest_buying_price].total_volume -= trade_quantity

                if buy_order.quantity == 0:
                    buy_queue.popleft()   # Remove the buy order from queue if its quantity is 0
                if len(buy_queue) == 0:
                    del self.buy_book[highest_buying_price]  # Remove the price level if there  are no more orders in that level

            else:
                break
        
        # Append the order to the book in case if its not fully executed
        if new_order.quantity > 0 and new_order.order_id not in self.orders:
            self._add_to_book(new_order)
        if new_order.quantity == 0 and new_order.order_id in self.orders:
            new_order.quantity = trade_quantity
            self._remove_from_book(new_order)
        return trades
    
    def cancel_order(self, order_id):
        with self.lock:
            if order_id not in self.orders:
                raise Exception(f"Order ID {order_id} not found")
            order = self.orders[order_id]
            if order.status == "CANCELLED":
                return True
                        
            self._remove_from_book(self.orders[order_id])
            return True
                

    def _add_to_book(self, order):
        if order.order_type == "BUY":
            book = self.buy_book
        else:
            book = self.sell_book
        if order.price not in book:
            book[order.price] = PriceLevel(order.price)
        book[order.price].append(order)

    def _remove_from_book(self, order):
        if order.order_type == "BUY":
            book = self.buy_book
        else:
            book = self.sell_book
        if order.price not in book:
            raise Exception(f"Order id {order.order_id} not found for price level {order.price}")
        book[order.price].remove(order)
        if book[order.price].total_volume == 0:
            del book[order.price]
        

    def modify_order(self, order_id, order_type, price, quantity):
        if order_id not in self.orders:
            raise Exception(f"Order id {order_id} not found")
        with self.lock:
            order = self.orders[order_id]
            order.quantity = quantity
            if order.order_type != order_type or order.price != price:
                self._remove_from_book(order)
                order.order_type = order_type
                order.price = price
                self._add_to_book(order)     
            if order_type == "BUY":
                self._match_buy_order(order)
            else:
                self._match_sell_order(order)
                
                       


    def get_order_status(self, order_id):
        if order_id in self.orders:
            return self.orders[order_id].status
        raise Exception(f"Order id {order_id} not found")
    
    def print(self):
        print("--------------------------")
        print(f"Buy orderbook for {self.symbol}:")
        for price in self.buy_book:
            print(f"Price: {price}, Total Volume:{self.buy_book[price].total_volume}")

        print("")
        print(f"Sell orderbook for {self.symbol}:")
        for price in self.sell_book:
            print(f"Price: {price}, Total Volume:{self.sell_book[price].total_volume}")
        print("--------------------------")