import random
import sys
import threading
import time
import tracemalloc
from trading_system import TradingSystem

# Function to simulate placing multiple orders
def place_orders(trading_system, user_id, order_type, symbol, num_orders):
    for i in range(num_orders):
        price = 100 + i  # Increment price for variety
        quantity = 10 + i  # Increment quantity for variety
        order_id = trading_system.place_order(user_id, order_type, symbol, quantity, price)
        print(f"User {user_id}: Placed {order_type} order for {quantity} shares at {price}.")

start_time = time.time()
tracemalloc.start()
# Initialize the trading system
tr = TradingSystem()

# Create 100 users and store their user IDs
num_users = 100
users = []
for i in range(num_users):
    user_name = f"User_{i+1}"
    phone = f"900000000{i%10}"  # Generate a mock phone number
    email = f"user_{i+1}@example.com"
    user_id = tr.register_user(user_name, phone, email)
    users.append(user_id)

# Number of orders per user
num_orders_per_user = 100
symbol = "AAPL"

# Create and start threads for each user to place orders
threads = []
for user_id in users:
    order_type = random.choice(["BUY", "SELL"])   # Alternate between buy and sell orders
    thread = threading.Thread(target=place_orders, args=(tr, user_id, order_type, symbol, num_orders_per_user))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

# Print the final order book
tr.print_order_book(symbol)

end_time = time.time()
print(f"Total trades executed: {tr.get_total_trades()}")
print(f"Total traded quantity: {tr.get_total_trade_quantity()}")
print(f"Execution time: {end_time - start_time} seconds")
current, peak = tracemalloc.get_traced_memory()

print(f"Current memory usage: {current / 1024 / 1024:.2f} MB")
print(f"Peak memory usage: {peak / 1024 / 1024:.2f} MB")

# Stop tracing memory
tracemalloc.stop()