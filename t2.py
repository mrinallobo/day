import neo_api_client
import time
from neo_api_client import NeoAPI


client = NeoAPI(consumer_key="dTkSDTUbbKjSfegaWwfM4C0wuLka", consumer_secret="KZszrVNqpDECpepvblVJZSTMqwoa", 
                environment='prod')


client.login(mobilenumber="+917600527005", password="Op7VPpd8")
client.session_2fa(OTP="100394")


def on_message(message):
    print(message)
    on_close(message)
    # instrument_tokens = "35582"
    # client.un_subscribe(instrument_tokens=instrument_tokens, isIndex=False, isDepth=False)
    # instrument_tokens = "35567"
    # client.un_subscribe(instrument_tokens=instrument_tokens, isIndex=False, isDepth=False)
def on_error(error_message):
    print(error_message)

def on_close(message):
    print(message)
    
def on_open(message):
    print(message)

client.on_message = on_message  # called when message is received from websocket
client.on_error = on_error  # called when any error or exception occurs in code or websocket
client.on_close = on_close  # called when websocket connection is closed
client.on_open = on_open


def get_exp():
    from datetime import datetime, timedelta
    current_date = datetime.now()

    day_of_week = current_date.weekday()


    days_until_nearest_wednesday = (2 - day_of_week + 7) % 7
    nearest_wednesday_date = current_date + timedelta(days=days_until_nearest_wednesday)
    week_number = (nearest_wednesday_date.day - 1) // 7 + 1
    print(week_number)
    if week_number == 4:
        return nearest_wednesday_date.strftime("%y%b").upper()
    else:
        month = nearest_wednesday_date.strftime("%m").lstrip("0")
        return nearest_wednesday_date.strftime("%y{0}%d").format(month) + nearest_wednesday_date.strftime("%y%m%d")[6:]   



# User inputs
# put_strike = int(input("Enter the strike price for put option: "))
# call_strike = int(input("Enter the strike price for call option: "))
# num_lots = int(input("Enter the number of lots: "))

# # Wait until 9:31
# while True:
#     current_time = time.localtime()
#     if current_time.tm_hour == 9 and current_time.tm_min == 31:
#         break
#     time.sleep(1)

# Fetch LTP of call and put options
exp ='06JUN2024'
ce_scrip = client.search_scrip(exchange_segment='nse_fo',expiry=exp,option_type='CE',strike_price='47000')
pe_scrip = client.search_scrip(exchange_segment='nse_fo',expiry=exp,option_type='PE',strike_price='47000')


# try:
#     # get scrip search details for particular exchange segment
#     print(client.search_scrip(exchange_segment = "nse_cm", symbol = "YESBANK",  expiry = "", option_type = "", strike_price = ""))
# except Exception as e:
#     print("Exception when calling scrip search api->scrip_search: %s\n" % e)
call_symbol = ce_scrip[0]['pSymbol']
put_symbol = pe_scrip[0]['pSymbol']

print(call_symbol, "Call sym")
print(put_symbol, "put sym")

# Create the list of dictionaries for call and put symbols
call_instrument_tokens = [{"instrument_token": call_symbol, "exchange_segment": "nse_fo"}]
put_instrument_tokens = [{"instrument_token": put_symbol, "exchange_segment": "nse_fo"}]

# Now you can pass these lists to the client.quotes method
call_ltp = client.quotes(instrument_tokens=call_instrument_tokens, quote_type="ltp", isIndex=False,session_token="", sid="",server_id="")
put_ltp = client.quotes(instrument_tokens=put_instrument_tokens, quote_type="ltp", isIndex=False,session_token="", sid="",server_id="")

print(call_ltp, "Call LTP")
print(put_ltp, "Put LTP")

client.NeoWebSocket.on_close

# call_ltp = client.quotes(instrument_tokens = call_symbol, quote_type="ltp", isIndex=False, session_token="", sid="",server_id="")
# put_ltp = client.quotes(instrument_tokens = put_symbol, quote_type="ltp", isIndex=False, session_token="", sid="",server_id="")

# print(put_ltp)
# call_ltp = kite.ltp(f"NFO:BANKNIFTY{call_strike}CE")["last_price"]
# put_ltp = kite.ltp(f"NFO:BANKNIFTY{put_strike}PE")["last_price"]

# # Place stoploss limit orders
# call_trigger_price = call_ltp * 1.2
# call_limit_price = call_trigger_price
# put_trigger_price = put_ltp * 1.2
# put_limit_price = put_trigger_price

# call_order_id = kite.place_order(
#     variety=kite.VARIETY_REGULAR,
#     exchange=kite.EXCHANGE_NFO,
#     tradingsymbol=f"BANKNIFTY{call_strike}CE",
#     transaction_type=kite.TRANSACTION_TYPE_BUY,
#     quantity=num_lots * 25,
#     product=kite.PRODUCT_MIS,
#     order_type=kite.ORDER_TYPE_SL,
#     price=call_limit_price,
#     trigger_price=call_trigger_price,
# )

# put_order_id = kite.place_order(
#     variety=kite.VARIETY_REGULAR,
#     exchange=kite.EXCHANGE_NFO,
#     tradingsymbol=f"BANKNIFTY{put_strike}PE",
#     transaction_type=kite.TRANSACTION_TYPE_BUY,
#     quantity=num_lots * 25,
#     product=kite.PRODUCT_MIS,
#     order_type=kite.ORDER_TYPE_SL,
#     price=put_limit_price,
#     trigger_price=put_trigger_price,
# )

# # Monitor orders
# call_filled = False
# put_filled = False

# while True:
#     call_order = kite.order_history(call_order_id)
#     put_order = kite.order_history(put_order_id)

#     if call_order["status"] == "COMPLETE":
#         call_filled = True
#         call_entry_price = call_order["average_price"]
#         call_sl_price = call_trigger_price * 0.7
#         kite.place_order(
#             variety=kite.VARIETY_REGULAR,
#             exchange=kite.EXCHANGE_NFO,
#             tradingsymbol=f"BANKNIFTY{call_strike}CE",
#             transaction_type=kite.TRANSACTION_TYPE_SELL,
#             quantity=num_lots * 25,
#             product=kite.PRODUCT_MIS,
#             order_type=kite.ORDER_TYPE_SL,
#             price=call_sl_price,
#             trigger_price=call_sl_price,
#         )

#     if put_order["status"] == "COMPLETE":
#         put_filled = True
#         put_entry_price = put_order["average_price"]
#         put_sl_price = put_trigger_price * 0.7
#         kite.place_order(
#             variety=kite.VARIETY_REGULAR,
#             exchange=kite.EXCHANGE_NFO,
#             tradingsymbol=f"BANKNIFTY{put_strike}PE",
#             transaction_type=kite.TRANSACTION_TYPE_SELL,
#             quantity=num_lots * 25,
#             product=kite.PRODUCT_MIS,
#             order_type=kite.ORDER_TYPE_SL,
#             price=put_sl_price,
#             trigger_price=put_sl_price,
#         )

#     if call_filled and put_filled:
#         while True:
#             call_ltp = kite.ltp(f"NFO:BANKNIFTY{call_strike}CE")["last_price"]
#             put_ltp = kite.ltp(f"NFO:BANKNIFTY{put_strike}PE")["last_price"]

#             if call_ltp >= call_sl_price:
#                 damage = call_sl_price - call_entry_price
#                 if damage < 40:
#                     new_put_sl_price = put_entry_price + (40 - damage)
#                     kite.modify_order(
#                         variety=kite.VARIETY_REGULAR,
#                         order_id=put_order_id,
#                         order_type=kite.ORDER_TYPE_SL,
#                         trigger_price=new_put_sl_price,
#                     )
#                     if put_ltp <= put_entry_price - damage - 20:
#                         new_put_sl_price = put_entry_price - damage - 20
#                         kite.modify_order(
#                             variety=kite.VARIETY_REGULAR,
#                             order_id=put_order_id,
#                             order_type=kite.ORDER_TYPE_SL,
#                             trigger_price=new_put_sl_price,
#                         )
#                 elif damage >= 40 and damage <= 65:
#                     new_put_sl_price = put_entry_price
#                     kite.modify_order(
#                         variety=kite.VARIETY_REGULAR,
#                         order_id=put_order_id,
#                         order_type=kite.ORDER_TYPE_SL,
#                         trigger_price=new_put_sl_price,
#                     )
#                     if put_ltp <= put_entry_price - damage - 20:
#                         new_put_sl_price = put_entry_price - damage - 20 
#                         kite.modify_order(
#                             variety=kite.VARIETY_REGULAR,
#                             order_id=put_order_id,
#                             order_type=kite.ORDER_TYPE_SL,
#                             trigger_price=new_put_sl_price,
#                         )
#                 else:
#                     new_put_sl_price = put_entry_price - 20
#                     kite.modify_order(
#                         variety=kite.VARIETY_REGULAR,
#                         order_id=put_order_id,
#                         order_type=kite.ORDER_TYPE_SL,
#                         trigger_price=new_put_sl_price,
#                     )
#                     if put_ltp <= put_entry_price - damage - 20:
#                         new_put_sl_price = put_entry_price - damage - 20
#                         kite.modify_order(
#                             variety=kite.VARIETY_REGULAR,
#                             order_id=put_order_id,
#                             order_type=kite.ORDER_TYPE_SL,
#                             trigger_price=new_put_sl_price,
#                         )

#             if put_ltp >= put_sl_price:
#                 damage = put_sl_price - put_entry_price
#                 if damage < 40:
#                     new_call_sl_price = call_entry_price + (40 - damage)
#                     kite.modify_order(
#                         variety=kite.VARIETY_REGULAR,
#                         order_id=call_order_id,
#                         order_type=kite.ORDER_TYPE_SL,
#                         trigger_price=new_call_sl_price,
#                     )
#                     if call_ltp <= call_entry_price - damage - 20:
#                         new_call_sl_price = call_entry_price - damage - 20
#                         kite.modify_order(
#                             variety=kite.VARIETY_REGULAR,
#                             order_id=call_order_id,
#                             order_type=kite.ORDER_TYPE_SL,
#                             trigger_price=new_call_sl_price,
#                         )
#                 elif damage >= 40 and damage <= 65:
#                     new_call_sl_price = call_entry_price
#                     kite.modify_order(
#                         variety=kite.VARIETY_REGULAR,
#                         order_id=call_order_id,
#                         order_type=kite.ORDER_TYPE_SL,
#                         trigger_price=new_call_sl_price,
#                     )
#                     if call_ltp <= call_entry_price - damage - 20:
#                         new_call_sl_price = call_entry_price - damage - 20
#                         kite.modify_order(
#                             variety=kite.VARIETY_REGULAR,
#                             order_id=call_order_id,
#                             order_type=kite.ORDER_TYPE_SL,
#                             trigger_price=new_call_sl_price,
#                         )
#                 else:
#                     new_call_sl_price = call_entry_price - 20
#                     kite.modify_order(
#                         variety=kite.VARIETY_REGULAR,
#                         order_id=call_order_id,
#                         order_type=kite.ORDER_TYPE_SL,
#                         trigger_price=new_call_sl_price,
#                     )
#                     if call_ltp <= call_entry_price - damage - 20:
#                         new_call_sl_price = call_entry_price - damage - 20
#                         kite.modify_order(
#                             variety=kite.VARIETY_REGULAR,
#                             order_id=call_order_id,
#                             order_type=kite.ORDER_TYPE_SL,
#                             trigger_price=new_call_sl_price,
#                         )

#             # Trailing stoploss for every 5 points increase
#             if call_ltp <= call_sl_price - 5:
#                 new_call_sl_price = call_sl_price - 5
#                 kite.modify_order(
#                     variety=kite.VARIETY_REGULAR,
#                     order_id=call_order_id,
#                     order_type=kite.ORDER_TYPE_SL,
#                     trigger_price=new_call_sl_price,
#                 )
#                 call_sl_price = new_call_sl_price

#             if put_ltp <= put_sl_price - 5:
#                 new_put_sl_price = put_sl_price - 5
#                 kite.modify_order(
#                     variety=kite.VARIETY_REGULAR,
#                     order_id=put_order_id,
#                     order_type=kite.ORDER_TYPE_SL,
#                     trigger_price=new_put_sl_price,
#                 )
#                 put_sl_price = new_put_sl_price

#             # Exit if both orders are completed
#             if call_order["status"] == "COMPLETE" and put_order["status"] == "COMPLETE":
#                 break

#             time.sleep(1)

#     elif call_filled or put_filled:
#         if call_filled:
#             if call_ltp >= call_sl_price:
#                 kite.cancel_order(variety=kite.VARIETY_REGULAR, order_id=put_order_id)
#                 break
#         else:
#             if put_ltp >= put_sl_price:
#                 kite.cancel_order(variety=kite.VARIETY_REGULAR, order_id=call_order_id)
#                 break

#     time.sleep(1)