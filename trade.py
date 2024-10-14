from datetime import datetime
from uuid import uuid4


class Trade:
    def __init__(self, buyer_order, seller_order, quantity, price):
        self.trade_id = str(uuid4())
        self.buyer_order_id = buyer_order.order_id
        self.seller_order_id = seller_order.order_id
        self.symbol = buyer_order.symbol
        self.quantity = quantity
        self.price = price
        self.timestamp = datetime.now()