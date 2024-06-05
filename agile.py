import configparser
import pyotp
from jugaad_trader import Zerodha
from datetime import datetime, timedelta
import pytz
import pandas as pd
import neo_api_client
import time
from neo_api_client import NeoAPI

client = NeoAPI(consumer_key="dTkSDTUbbKjSfegaWwfM4C0wuLka", consumer_secret="KZszrVNqpDECpepvblVJZSTMqwoa", 
                environment='prod')

client.login(mobilenumber="+917600527005", password="Op7VPpd8")
client.session_2fa(OTP="100394")

def on_message(message):
    for item in message['data']:
        trading_symbol = item['trading_symbol']
        ltp = item['ltp']
        print(f"Trading Symbol: {trading_symbol}, LTP: {ltp}")
    neo_api_client.HSIWebSocket.close(neo_api_client)

def on_error(error_message):
    print(error_message)

def on_close(message):
    print("WebSocket closed:", message)

def on_open(message):
    print(message)

client.on_message = on_message  # called when message is received from websocket
client.on_error = on_error  # called when any error or exception occurs in code or websocket
client.on_close = on_close  # called when websocket connection is closed
client.on_open = on_open

exp = '06JUN2024'
ce_scrip = client.search_scrip(exchange_segment='nse_fo', expiry=exp, option_type='CE', strike_price='47000')
pe_scrip = client.search_scrip(exchange_segment='nse_fo', expiry=exp, option_type='PE', strike_price='47000')

call_symbol = ce_scrip[0]['pSymbol']
put_symbol = pe_scrip[0]['pSymbol']

print(call_symbol, "Call sym")
print(put_symbol, "put sym")

# Create the list of dictionaries for call and put symbols
call_instrument_tokens = [{"instrument_token": call_symbol, "exchange_segment": "nse_fo"}]
put_instrument_tokens = [{"instrument_token": put_symbol, "exchange_segment": "nse_fo"}]

# Fetch LTP for call and put symbols
call_ltp = client.quotes(instrument_tokens=call_instrument_tokens, quote_type="ltp", isIndex=False, session_token="", sid="", server_id="")
put_ltp = client.quotes(instrument_tokens=put_instrument_tokens, quote_type="ltp", isIndex=False, session_token="", sid="", server_id="")

def place_order(seg, prdct, prc, o_type, quantity, val, symb, tt):
    try:
        client.place_order(exchange_segment=seg, product=prdct, price=prc, order_type=o_type, quantity=quantity, validity=val, trading_symbol=symb,
                           transaction_type=tt, amo="NO", disclosed_quantity="0", market_protection="0", pf="N",
                           trigger_price="0", tag=None)
        print("Order placed")
    except Exception as e:
        print("Exception when calling OrderApi->place_order: %s\n" % e)

print("reached here")
order = place_order('nse_fo','NRML','0','MKT','15','DAY',call_symbol,'B')
print(order)
