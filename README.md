Here’s a helpful summary and README guide you can use for your GitHub project:

---

# Trading System Prototype

This is a simple prototype of a **trading system** that maintains buy and sell orders in an **order book**. The system supports multiple users, allows placing, modifying, and canceling orders, and automatically matches buy and sell orders based on price levels. The trades are recorded in the system for tracking.

## Key Features

- **Order Matching Engine**: Matches buy and sell orders based on price and quantity.
- **Order Book**: Manages orders in separate buy and sell books, with price levels sorted accordingly.
- **Multi-threading Support**: Ensures safe concurrent access with locks.
- **Trade Execution**: Automatically executes trades when orders are matched.
- **User Management**: Registers and tracks users by unique IDs.
- **Order Modification and Cancellation**: Supports modifying existing orders or canceling them before execution.

## Project Structure

- **TradingSystem**: The main class managing users, order books, and trades.
- **OrderBook**: Manages buy and sell orders for a specific symbol. Orders are sorted by price.
- **Order**: Represents an individual order placed by a user.
- **PriceLevel**: Represents a level in the order book with a specific price and the queued orders.
- **User**: Tracks user details such as name, phone, and email.
- **Trade**: Represents a matched buy-sell transaction between two orders.

---

## Installation

To run this project, ensure you have Python installed.

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/trading-system-prototype.git
   cd trading-system-prototype
   ```


## Usage

### 1. Registering a User

```python
from trading_system import TradingSystem

system = TradingSystem()
user_id = system.register_user(name="John Doe", phone="123456789", email="john@example.com")
```

### 2. Placing an Order

```python
order_id = system.place_order(user_id, order_type="BUY", symbol="AAPL", quantity=10, price=150)
```

### 3. Modifying an Order

```python
system.modify_order(symbol="AAPL", order_id=order_id, order_type="BUY", price=155, quantity=5)
```

### 4. Canceling an Order

```python
system.cancel_order(symbol="AAPL", order_id=order_id)
```

### 5. Viewing Order Book

```python
system.print_order_book(symbol="AAPL")
```

### 6. Retrieving Total Trades and Quantity

```python
total_trades = system.get_total_trades()
total_quantity = system.get_total_trade_quantity()
```

---

## Contributing

Feel free to fork this repository, submit pull requests, or report issues.

---

This guide provides a brief overview of how to get started with the **Trading System Prototype**. For more details, refer to the individual class documentation and code comments.

---

Let me know if you need further changes to this!
