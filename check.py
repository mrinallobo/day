from ib_insync import *

# Connect to Interactive Brokers TWS/Gateway
ib = IB()
ib.connect('localhost', 7497, clientId=1)

# Place an order and get the order ID
contract = Stock('AAPL', 'SMART', 'USD')
order = MarketOrder('BUY', 100)
trade = ib.placeOrder(contract, order)
order_id = trade.order.orderId

# Check if the order is open
open_orders = ib.openOrders()
is_order_open = any(order.orderId == order_id for order in open_orders)

if is_order_open:
    print(f"Order with ID {order_id} is open.")
else:
    print(f"Order with ID {order_id} is not open.")

# Disconnect from Interactive Brokers
ib.disconnect()

from ib_insync import *

# Connect to Interactive Brokers TWS/Gateway
ib = IB()
ib.connect('localhost', 7497, clientId=1)

# Create a contract
contract = Stock('AAPL', 'SMART', 'USD')

# Create an order
order = MarketOrder('BUY', 100)

# Place the order
trade = ib.placeOrder(contract, order)

# Fetch the order ID
order_id = trade.order.orderId

print(f"Order placed with ID: {order_id}")

# Disconnect from Interactive Brokers
ib.disconnect()
