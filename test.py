import neo_api_client
from neo_api_client import NeoAPI
def on_message(message):
    print(message)
    
def on_error(error_message):
    print(error_message)

client = NeoAPI(consumer_key="dTkSDTUbbKjSfegaWwfM4C0wuLka", consumer_secret="KZszrVNqpDECpepvblVJZSTMqwoa", 
                environment='prod')


client.login(mobilenumber="+917600527005", password="Op7VPpd8")
client.session_2fa(OTP="100394")




import datetime
import time

# Kotak Neo API credentials
username = "your_username"
password = "your_password"
api_key = "your_api_key"
api_secret = "your_api_secret"

# Initialize API connection
from kotakdesktopapi.api import Api
api = Api(username, password, api_key, api_secret)
api.login()

# Function to place order
def place_order(instrument, quantity, price, order_type, product_type):
    order = {
        "instrument": instrument,
        "quantity": quantity,
        "price": price,
        "ordertype": order_type,
        "producttype": product_type
    }
    api.place_order(order)

# Function to cancel order
def cancel_order(order_id):
    api.cancel_order(order_id)

# Function to get LTP of an instrument
def get_ltp(instrument):
    quote = api.get_quote(instrument)
    ltp = quote["last_price"]
    return ltp

# Get user inputs
strike_put = int(input("Enter strike price for put: "))
strike_call = int(input("Enter strike price for call: "))
lots = int(input("Enter number of lots: "))

# Wait until 9:31
while datetime.datetime.now().time() < datetime.time(9, 31):
    time.sleep(1)

# Get LTP of both call and put
ltp_put = get_ltp("NFO:OPTIDX:" + str(strike_put) + "PE")
ltp_call = get_ltp("NFO:OPTIDX:" + str(strike_call) + "CE")

# Place stoploss limit orders
stoploss_put = ltp_put * 1.2
stoploss_call = ltp_call * 1.2

order_put = place_order("NFO:OPTIDX:" + str(strike_put) + "PE", lots, stoploss_put, "SL-LMT", "NRML")
order_call = place_order("NFO:OPTIDX:" + str(strike_call) + "CE", lots, stoploss_call, "SL-LMT", "NRML")

# Initialize order status
order_put_filled = False
order_call_filled = False

while True:
    # Check if orders are filled
    order_put_status = api.get_order_status(order_put["orderid"])
    order_call_status = api.get_order_status(order_call["orderid"])

    if order_put_status["status"] == "filled":
        order_put_filled = True
    if order_call_status["status"] == "filled":
        order_call_filled = True

    # Case 1: One order gets filled
    if order_put_filled and not order_call_filled:
        stoploss_put = ltp_put * 0.7
        place_order("NFO:OPTIDX:" + str(strike_put) + "PE", lots, stoploss_put, "SL-LMT", "NRML")
        if order_call_status["status"] == "filled":
            cancel_order(order_call["orderid"])
            break
    elif order_call_filled and not order_put_filled:
        stoploss_call = ltp_call * 0.7
        place_order("NFO:OPTIDX:" + str(strike_call) + "CE", lots, stoploss_call, "SL-LMT", "NRML")
        if order_put_status["status"] == "filled":
            cancel_order(order_put["orderid"])
            break

    # Case 2: Both orders get filled
    elif order_put_filled and order_call_filled:
        stoploss_put = ltp_put * 0.7
        stoploss_call = ltp_call * 0.7
        place_order("NFO:OPTIDX:" + str(strike_put) + "PE", lots, stoploss_put, "SL-LMT", "NRML")
        place_order("NFO:OPTIDX:" + str(strike_call) + "CE", lots, stoploss_call, "SL-LMT", "NRML")

        # Trail stoploss
        while True:
            ltp_put = get_ltp("NFO:OPTIDX:" + str(strike_put) + "PE")
            ltp_call = get_ltp("NFO:OPTIDX:" + str(strike_call) + "CE")

            if order_put_status["status"] == "filled" and order_call_status["status"] == "triggered":
                trail_price = max(ltp_put, ltp_call) - 5
                place_order("NFO:OPTIDX:" + str(strike_put) + "PE", lots, trail_price, "SL-LMT", "NRML")
            elif order_call_status["status"] == "filled" and order_put_status["status"] == "triggered":
                trail_price = max(ltp_put, ltp_call) - 5
                place_order("NFO:OPTIDX:" + str(strike_call) + "CE", lots, trail_price, "SL-LMT", "NRML")

            # Check if trail stoploss is hit
            if order_put_status["status"] == "triggered" and order_call_status["status"] == "triggered":
                break

            time.sleep(1)

    time.sleep(1)

api.logout()



#ok can you build me a script for maybe kotak neo api using this strategy.
# 1. We ask user inputs for strike for put and call and number of lots at 9:29
# 2. We will start the bot at 9:31 and fetch the LTP of both call and put
# 3. We will place stoploss limit order with trigger at ltp*1.2 
# 4. Then we keep monitoring if the orders get filled 
# Case 1: One order gets filled , we will immediately place the SL at ltp*0.7. Now if this hits SL and the other order is still open, we will cancel open orders and exit the program. 
# Case 2: Both orders get filled, now we will keep SL as ltp*0.7 on both of them, suppose one hits then we have to go to our range of 40-65 points, if it is within this range we trail the other remaining position to cost first/if it is lesser than 40 then we will trail it to below cost, assume its 35, suppose entry of the option was 220 , we will trail it to 220-5 = 215. Now if its greater than the 65 point limit then say for example we bought at 220, but the other leg SL hit for 85 points, then we to first trail to cost, then if option price goes ltp+the sl hit points +20, we trail it to that level, and then keep trailing every 5 points until we exit. We will only trail and keep target if atleast one SL is hit. Say our stoploss hit is between 40-65 then first we trail to the cost, then if the price goes above the cost+ 20+ The SL hit points , we will trail to that price and then will trail every 5 point increment till we are out. Give me code for this please
