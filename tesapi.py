# import asyncio
from fyerstest.fyersApi import SessionModel, FyersModelv3
import time
from fyerstest import ws
import webbrowser
import sys
sys.path.insert(0, "/home/piyush/Documents/fyers_v2/Python_SDK/fyers-api-py/")
# import asyncio


def api_call(token, client_id):
    # access_token = "your_access_token_from_generate_access_token_function" ## access_token from the rgenerate_access_token function
    # If you want to make asynchronous API calls then assign the below variable as True and then pass it in the functions, by default its value is False
    # is_async = True
    access_token = token
    # appId = client_id.split(":")[0]
    # import ipdb;ipdb.set_trace()
    fyers = FyersModelv3(token=access_token, is_async=False, client_id=client_id)

    # fyers = fyersModel.FyersModel(token=access_token,is_async=True,client_id=client_id)
    fyers.token = access_token
    #
    # print(fyers.get_profile())
    data = {"symbol":"NSE:HCLTECH-EQ","resolution":"D","date_format":"0","range_from":"1679961600","range_to":"1680652800","cont_flag":"1"}
    # print(fyers.history(data))
    start_time = time.time()
    # print(fyers.quotes({"symbols":"NSE:ONGC-EQ,NSE:SBIN-EQ"}))
	# end_time = time.time()print(f"end_time:{end_time-start_time}")
    # print(fyers.depth({"symbol":"NSE:SBIN-EQ","ohlcv_flag":"1"}))
    # print(fyers.ws.({"data_type":"symbolUpdate","symbol":"MCX:SILVERMIC21JUNFUT"}))
    # print(fyers.tradebook())
    # print(fyers.tradebook_with_filter({"orderNumber":"808078094451"}))  #tradebook_with_filter
    # print(fyers.positions())
    # print(fyers.holdings())
    # print(fyers.holdings_with_filter({"symbol":"NSE:JPASSOCIAT-"}))
    # print(fyers.convert_position({"symbol":"MCX:SILVERMIC20AUGFUT","positionSide":"1","convertQty":"1","convertFrom":"MARGIN","convertTo":"INTRADAY"}))
    # print(fyers.funds())
    # print(fyers.funds_with_filter({'id':"1"}))
    # print(fyers.orderbook())
    # print(fyers.orderbook({'id':'23050200000003'}))

    # print(fyers.orderBook_with_filter({'id':'23050200000003'}))
    # print(fyers.cancel_order({'id':'23052300000006'}))
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(asyncio.gather(fyers.place_order({"productType":"INTRADAY","side":1,"symbol":"NSE:IRFC-EQ","qty":1,"disclosedQty":0,"type":2,"validity":"DAY","filledQty":0,"limitPrice":0,"stopPrice":0,"offlineOrder":True})))
    data = {
            "symbol":"NSE:IDEA-EQ",
            "qty":1,
            "type":1,
            "side":1,
            "productType":"INTRADAY",
            "limitPrice":6.5,
            "stopPrice":0,
            "disclosedQty":0,
            "validity":"DAY",
            "offlineOrder":False,
            "stopLoss":0,
            "takeProfit":0
            }
    # print(fyers.place_order(data))
    # print(fyers.orderbook())
    gttData = {
        "side": 1,
        "symbol": "NSE:IDEA-EQ",
        "orderInfo": {
            "leg1": {
                "price": 6.95,
                "triggerPrice": 6.30,
                "qty": 1
            },
            "leg2": {
                "price": 7,
                "triggerPrice": 6.80,
                "qty": 2
            }
        }
    }
    # print(fyers.place_gttorder(gttData))

    modifyGttData = {
    "id": "22110900000001",
    "orderInfo": {
        "leg1": {
            "price": 83,
            "triggerPrice": 85.7,
            "qty": 10
        },
        "leg2": {
            "price": 86,
            "triggerPrice": 85.7,
            "qty": 3
        }
    }
    }
    # print(fyers.modify_gttorder(modifyGttData))

    # print(fyers.get_gttorders())
    # print(fyers.modify_order({"id":"23052300000006", "qty":2,"type":1,"limitPrice":6.5,"stopPrice":0})) #modify instead of update
    # # print(fyers.minquantity())
    # print(fyers.orderStatus_with_filter({'id':'808078094451'}))
    # # print(fyers.market_status())
    # print(fyers.exit_positions({"id":"MCX:SILVERMIC20AUGFUT-MARGIN"}))
    # # print(fyers.generate_data_token({"vendorApp":"0KMS0EZVXI"}))
    # # print(fyers.multiple_orders())
    # print(fyers.multiple_cancel_orders([{"id":"120080780536"},{"id":"120080777069"}]))
    # print(fyers.multiple_place_orders([{"symbol":"NSE:SBIN-EQ","qty":"1","type":"1","side":"1","productType":"INTRADAY","limitPrice":"191","stopPrice":"0","disclosedQty":"0","validity":"DAY","offlineOrder":"False","stopLoss":"0","takeProfit":"0"},{"symbol":"NSE:SBIN-EQ","qty":"1","type":"1","side":"1","productType":"INTRADAY","limitPrice":"191","stopPrice":"0","disclosedQty":"0","validity":"DAY","offlineOrder":"False","stopLoss":"0","takeProfit":"0"}]))
    #
    # print(fyers.multiple_modify_orders([{"id":"120080780536", "type":1, "limitPrice": 190, "stopPrice":0},{"id":"120080777069", "type":1, "limitPrice": 190}]))

    # p = threading.Thread(target=fyersSocket.subscribe)
    # p.start()
    # data = {"symbol":"NSE:SBIN-EQ","resolution":"D","date_format":"0","range_from":"1622097600","range_to":"1622097685","cont_flag":"1"}
    # fyers.history(data)
    # print(response)
    # for i in range(0,100):
    # 	print(fyers.get_profile())
    # 	print(fyers.tradebook())
    # 	print(fyers.positions())
    # access_token = "L9NY34Z6BW-100:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2MzM2Njc5MjksImV4cCI6MTYzMzczOTQ0OSwibmJmIjoxNjMzNjY3OTI5LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCaFg4dFotcFZpOGdvYmMtMlRfNmNmYlowQlVFbVJFel9XSjJCRmJTRURWUm1GbDRzdW5tQ3FmQWN6bDVESkZsMEJLeEw3N3E5RUttMWRYNzcta05VaXhiNE4xY3ZoVGU0RGx4YUFBTERuekhqeU4xQT0iLCJkaXNwbGF5X25hbWUiOiJQSVlVU0ggUkFKRU5EUkEgS0FQU0UiLCJmeV9pZCI6IkRQMDA0MDQiLCJhcHBUeXBlIjoxMDAsInBvYV9mbGFnIjoiTiJ9.SqubA2d3axSDQW3xah8d_ZI_xFQSkDeSExv4EvotuGs"
    # # # loop = asyncio.new_event_loop()
    # data_type = "symbolData"
    # # data_type = "orderUpdate"
    # # symbol =  ["MCX:SILVERMIC21NOVFUT","MCX:NATURALGAS21SEPFUT"]
    # symbol = ["NSE:NIFTY50-INDEX", "NSE:NIFTYBANK-INDEX",
    #           "NSE:NIFTYAUTO-INDEX", "NSE:NIFTYALPHA50-INDEX", "BSE:150MIDCAP-INDEX"]
    # symbol =["NSE:NIFTY50-INDEX"]
    # symbol=["NSE:NIFTY2190917350CE","NSE:NIFTY2190917350PE"]
    # symbol = ["NSE:SBIN-EQ","NSE:ONGC-EQ"]
    # 	# fs = ws.FyersSocket(access_token=access_token, data_type=data_type,run_background=True)
    fs = ws.FyersSocket(access_token=access_token,run_background=False,log_path="/home/piyush/Downloads/")
    # fs.websocket_data = custom_message
    # fs.on_open = onopen
    # fs.on_error = onerror
    # fs.init_connection()
    # time.sleep(5)
    # import ipdb;ipdb.set_trace()
    # fs.subscribe(symbol=symbol)
    # def op_open(fs,fetch_symbol):
    # 	on_open(fetch_data_symbolhigh low)
    # def on_close(fs,time):
    # 	on_close(3:15)
    # def custom_message(message):
    # 	print(message)
    # fs.on_open()
    # fs.on_close()
    # fs.on_message()
    # fs.on_error()
    # fs.init_connection()
    # import ipdb;ipdb.set_trace()
    # fs.subscribe(symbol=symbol,data_type=data_type)
    # # time.sleep(5)
    # # fs.subscribe(symbol=["MCX:SILVER21SEPFUT"])
    # print(fyers.get_profile())
    # print(fyers.tradebook())
    # print(fyers.positions())
    # # print("unsubscribed symbol")
    # # symbol = ["NSE:ONGC-EQ"]
    # # fs.unsubscribe(symbol=symbol)
    # fs.keep_running()
    # fs.subscribe(run_background=False)
    # with ThreadPoolExecutor(3) as executor:
    # 	task = executor.submit(fs.subscribe())


def getauthToken(client_id, redirect_uri, response_type, scope, state, nonce):
    appSession = SessionModel(client_id=client_id, redirect_uri=redirect_uri,
                              response_type=response_type, scope=scope, state=state, nonce=nonce)
    generateTokenUrl = appSession.generate_authcode()
    print((generateTokenUrl))
    webbrowser.open(generateTokenUrl, new=1)


def generate_access_token(auth_code, client_id, redirect_uri, secret_key, grant_type):
    appSession = SessionModel(client_id=client_id, redirect_uri=redirect_uri,
                              secret_key=secret_key, grant_type=grant_type)
    appSession.set_token(auth_code)
    access_token = appSession.generate_token()
    return access_token



def main():

    redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
    client_id = "XC4EOD67IM-100"
    secret_key = "5O0CK73DM8"
    grant_type = "authorization_code"
    response_type = "code"
    state = "sample_state"
    nonce = "baka"
    scope = "openid"
    # getauthToken(client_id, redirect_uri,response_type,scope,state,nonce)

    auth_code = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkubG9naW4uZnllcnMuaW4iLCJpYXQiOjE2ODQ3MzgzMDgsImV4cCI6MTY4NDc2ODMwOCwibmJmIjoxNjg0NzM3NzA4LCJhdWQiOiJbXCJ4OjBcIiwgXCJ4OjFcIiwgXCJ4OjJcIiwgXCJkOjFcIiwgXCJkOjJcIiwgXCJ4OjFcIiwgXCJ4OjBcIl0iLCJzdWIiOiJhdXRoX2NvZGUiLCJkaXNwbGF5X25hbWUiOiJYVjIwOTg2Iiwib21zIjoiSzEiLCJub25jZSI6ImJha2EiLCJhcHBfaWQiOiJYQzRFT0Q2N0lNIiwidXVpZCI6IjI3MjM0MWQzN2NmMzQxMTQ5ZmU0NzIwZTllYTQ0YTZiIiwiaXBBZGRyIjoiMC4wLjAuMCIsInNjb3BlIjoib3BlbmlkIn0.z7lrSZ2K1HiqDPNfdduqBwnDqazPDrgmFSh0wzqCR0A"

    # print(generate_access_token(auth_code, client_id, redirect_uri,secret_key,grant_type))

    # access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2ODMwMDE4OTgsImV4cCI6MTY4MzA3MzgzOCwibmJmIjoxNjgzMDAxODk4LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCa1VKSXFKLTNQMl9BSXFWWFNWUlg5UXlIVW5QWlpGRnFnNG5xRkNWRzYwQU5qX0F6T2hVWmxPZmtCNUV4ak03MXBMWVlqSEpjWXBsaVpVNWpFREQ1R3JFVkt4Rmx0SzR4RDh2SERVdkZndWgwUEVGRT0iLCJkaXNwbGF5X25hbWUiOiJWSU5BWSBLVU1BUiBNQVVSWUEiLCJvbXMiOiJLMSIsImZ5X2lkIjoiWFYyMDk4NiIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.MghUuBXEV3INDwH-buwTUvJDvBQ0HS37d69nwRCE7nE"
    access_token ="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2ODQ4MTM5NTgsImV4cCI6MTY4NDg4ODIzOCwibmJmIjoxNjg0ODEzOTU4LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCa2JEaUd1Q1BGek1uUFlXTVFxRjNvUGt0T3lsRDhpNzMyOTJfS0VVZUl6RU1oc2lKMTNLV2dfc2ZWU1BBWTFNdmxGblQtQzh0dG1VX1hqM1NYSklLLTNkaVFHMTZJVE5kTDlvVTJKSmxVbjBwNlI1UT0iLCJkaXNwbGF5X25hbWUiOiJWSU5BWSBLVU1BUiBNQVVSWUEiLCJvbXMiOiJLMSIsImZ5X2lkIjoiWFYyMDk4NiIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.s4CJCOZCnUohVaMttSwA_Iz0p9t-HHSHNwqED5NemhQ"
    api_call(access_token, client_id)


if __name__ == '__main__':
    main()
