import threading
from trading_system import TradingSystem


tr = TradingSystem()
user1_id = tr.register_user("Ketan Wani", "9764050900", "ketan.wa@gmail.com")
user2_id = tr.register_user("Shivaay Wani", "9890444505", "shivaay.wani@gmail.com")


order1 = tr.place_order(user1_id, "BUY", "AMZN", 10, 100)
order2 = tr.place_order(user2_id, "SELL", "AMZN", 11, 99)
tr.print_order_book("AMZN")
order3 = tr.place_order(user1_id, "BUY", "AMZN", 10, 98)
order4 = tr.place_order(user2_id, "SELL", "AMZN", 10, 100)
tr.print_order_book("AMZN")
tr.modify_order("AMZN", order4, "SELL", 98, 10)
tr.print_order_book("AMZN")
tr.modify_order("AMZN", order2, "BUY", 98, 1)
tr.print_order_book("AMZN")
