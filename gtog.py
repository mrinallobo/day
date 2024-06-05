import neo_api_client
import time
from neo_api_client import NeoAPI

client = NeoAPI(consumer_key="dTkSDTUbbKjSfegaWwfM4C0wuLka", consumer_secret="KZszrVNqpDECpepvblVJZSTMqwoa", 
                environment='prod')

client.login(mobilenumber="+917600527005", password="Op7VPpd8")
client.session_2fa(OTP="100394")

def on_message(message):
    print(message)
    

def on_error(error_message):
    print(error_message)

def on_close(message):
    print("WebSocket closed:", message)
    # client.hsWebsocket.close()
    # client.NeoWebSocket.hsWebsocket.close()

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
    if week_number == 4:
        return nearest_wednesday_date.strftime("%y%b").upper()
    else:
        month = nearest_wednesday_date.strftime("%m").lstrip("0")
        return nearest_wednesday_date.strftime("%y{0}%d").format(month) + nearest_wednesday_date.strftime("%y%m%d")[6:]

# Fetch LTP of call and put options
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

# print(call_ltp, "Call LTP")
# print(put_ltp, "Put LTP")

# Close the WebSocket connection after getting the LTP values
# client.__on_close()

print("WebSocket connection closed after fetching LTP values.")
a =3
if a >2 :
    print("we go about our business")

client.subscribe_to_orderfeed()
client.logout()