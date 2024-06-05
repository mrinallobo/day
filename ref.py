import datetime
import pandas as pd
import asyncio
async def cancel_orders(client):
    orders = client.order_report()
    for ord in orders['data']:
        oid = ord['nOrdNo']
        client.cancel_order(oid)
    print("Orders cancelled successfully")


async def close_positions(client):
    await cancel_orders(client)
    response_dict = client.positions()
    if 'data' not in response_dict:
        print("No data found in the response")
        return
    
    data = response_dict['data']
    
    for item in data:
        segment = item.get('exSeg', '')
        prdct = item.get('prod', '')
        prc = "0"
        o_type = 'MKT'
        qty = int(item.get('cfBuyQty', 0)) + int(item.get('flBuyQty', 0))
        val = "DAY"
        trad_sym = item.get('trdSym', '')

        try:
            client.place_order(exchange_segment=segment, product=prdct, price=prc, order_type=o_type, quantity=qty, validity=val, trading_symbol=trad_sym,
                            transaction_type="S", amo="NO", disclosed_quantity="0", market_protection="0", pf="N",
                            trigger_price="0", tag=None)
        except Exception as e:
            print("Exception when calling OrderApi->place_order:", e)
    
    print("Positions squared off")

    
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


async def get_strike(client,direction):
    onst_tokens = [{"instrument_token": "26009", "exchange_segment": "nse_cm"}]
    b = client.quotes(instrument_tokens = onst_tokens, quote_type="ltp", isIndex=False, session_token="", sid="",server_id="")
    message_list = b['message']

    # Access the dictionary within the list (assuming it's the first item in the list)
    first_item = message_list[0]

    # Access the value associated with the 'ltp' key
    ltp_value = int(round(float(first_item['ltp']) / 100) * 100)
    if direction == 1:
        stk = ltp_value + 500
        return str(stk)
    elif direction == -1:
        stk = ltp_value - 500
        return str(stk)
    

async def place_order(client,seg,prdct,prc,o_type,quantity,val,symb,tt):
    try:
    # Place a Order
        client.place_order(exchange_segment=seg, product=prdct, price=prc, order_type=o_type, quantity=quantity, validity=val, trading_symbol=symb,
                        transaction_type=tt, amo="NO", disclosed_quantity="0", market_protection="0", pf="N",
                        trigger_price="0", tag=None)
    except Exception as e:
        print("Exception when calling OrderApi->place_order: %s\n" % e)
async def fire(client,direction):
    await close_positions(client)
    epx =  get_exp()
    stk = await get_strike(client,direction)
    seg = 'nse_fo'
    prdct = 'NRML'
    prc = '0'
    o_type = 'MKT'
    quantity = '15'
    val = 'DAY'
    symb = f"BANKNIFTY{epx}{stk}CE" if direction == 1 else f"BANKNIFTY{epx}{stk}PE"
    tt= 'B'
    await place_order(client,seg,prdct,prc,o_type,quantity,val,symb,tt)


# print(get_strike(client,1))  
