from datetime import datetime, timedelta
from uuid import uuid4


class Order:
    def __init__(self, user_id, order_type, symbol, quantity, price):
        self.order_id = str(uuid4())
        self.user_id = user_id
        self.order_type = order_type
        self.symbol = symbol
        self.quantity = quantity
        self.price = price
        self.timestamp = datetime.now()
        self.status = "ACCEPTED"

    def is_expired(self):
        expiration_time = self.timestamp + timedelta(minutes=30)  # Set expiration time to 30 minutes
        return datetime.now() > expiration_time 