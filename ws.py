import asyncio
import websockets
import json
import urllib.parse
import requests
import asyncio
import websockets
from fyersModel1 import SessionModel , FyersModelv3


import asyncio
import websockets
import json

class websocket:

    def parse_position_data( self , msg ):
        message = msg['positions']
        positionData = {}
        positionData["buy_avg"] = message['buy_avg']
        positionData["buy_qty"]= message['buy_qty']
        positionData["buy_val"]= message['buy_val']
        positionData["cf_buy_qty"]= message['cf_buy_qty']
        positionData["cf_sell_qty"]= message['cf_sell_qty']
        positionData["day_buy_qty"]= message['day_buy_qty']
        positionData["day_sell_qty"]= message['day_sell_qty']
        positionData["fy_token"]= message['fy_token']
        positionData["id"]= message['id']
        positionData["net_avg"]= message['net_avg']
        positionData["net_qty"]= message['net_qty']
        positionData["pl_realized"]= message['pl_realized']
        positionData["product_type"]= message['product_type']
        positionData["qty_multi"]= message['qty_multiplier']
        positionData["rbi_ref_rate"]= message['rbirefrate']
        positionData["segment"]= message['segment']
        positionData["sell_avg"]= message['sell_avg']
        positionData["sell_qty"]= message['sell_qty']
        positionData["sell_val"]= message['sell_val']
        positionData["sym_desc"]= message['symbol_desc']
        positionData["symbol"]= message['symbol']
        positionData["tran_side"]= message['tran_side']
        return positionData

    def parse_trade_data( self, msg ):
        message = msg['trades']
        tradeData = {}
        tradeData['id_fill'] = message['id_fill']
        tradeData['id'] = message['id']
        tradeData['qty_traded'] = message['qty_traded']
        tradeData['price_traded'] = message['price_traded']
        tradeData['traded_val'] = message['traded_val']
        tradeData['product_type'] = message['product_type']
        tradeData['client_id'] = message['client_id']
        tradeData['id_exchange'] = message['id_exchange']
        tradeData['ord_type'] = message['ord_type']
        tradeData['tran_side'] = message['tran_side']
        tradeData['symbol'] = message['symbol']
        tradeData['time_epoch'] = message['time_epoch']
        tradeData['time_oms'] = message['time_oms']
        tradeData['fy_token'] = message['fy_token']
        tradeData['tradeNumber'] = message['id']
        return tradeData


    def parse_orderUpdate_data(self, msg):

        response = {}
        message = msg


        if  "code" in message:
            return msg
        elif "orders" in message:
            order = message["orders"]
            orderData = {}
            orderData["orderDateTime"] = order["update_time_epoch_oms"]
            orderData["id"] = order["id"]
            orderData["exchOrdId"] = order["id"]
            orderData["side"] = order["tran_side"]
            orderData["instrument"] = order["instrument"]
            orderData["productType"] = order["product_type"]
            orderData["status"] = order["ord_status"]
            orderData["qty"] = order["qty"]
            orderData["filledQty"] = order["qty_filled"] if "qty_filled" in order else  0
            orderData["remainingQuantity"] = order["qty_remaining"] if "qty_remaining" in order else  0
            orderData["type"] = order["ord_type"]
            orderData["orderValidity"] = order["validity"]
            orderData["offlineOrder"] = order["offline_flag"]
            orderData["message"] = order["status_msg"]
            orderData["orderNumStatus"] = order["id"] + ":" + str(order["org_ord_status"])
            orderData["fyToken"] = order["fy_token"]
            orderData["symbol"] = order["symbol"]
            orderData["segment"] = order["segment"]
            orderData["slNo"] = 0
            orderData["dqQtyRem"] = order["dqQtyRem"] if "dqQtyRem" in order else  0
            orderData["limitPrice"] = order["price_limit"] if "price_limit" in order else  0
            orderData["stopPrice"] = order["price_stop"] if "price_stop" in order else  0
            orderData["discloseQty"] = order["qty_disc"] if "qty_disc" in order else  0
            orderData["tradedPrice"] = order["price_traded"] if "price_traded" in order else  0
            response["ws_type"] = 1
            response["s"] = message["s"]
            response["d"] = orderData
            return response
        





# {'s': 'ok', 'code': 1101, 'message': 'Order Submitted Successfully. Your Order Ref. No. 23042500360760', 'id': '23042500360760'}
# {'code': 1101, 'message': 'Order placement request submitted successfully', 's': 'ok', 'id_fyers': '0fc566ea-6193-4664-a9d4-d8a0516ac4fd'}
    def __init__(self, access_token):
        self.access_token = access_token
        self.orderResponse = {
            "s":"",
            "code": 0,
            "message":"",
            "id":""
        }
    async def connectWS(self):
        async with websockets.connect(
            "wss://socket.fyers.in/trade/v3",
            extra_headers={"authorization": self.access_token}
        ) as websocket:
            message = json.dumps({"T": "SUB_ORD", "SLIST": ["orders"], "SUB_T": 1})
            await websocket.send(message)
            print(f"Sent message: {message}")
            while True:
                response = await websocket.recv()
                # print(f"Received response: {response}")
                response = json.loads(response)
                if "orders" in response:
                    print(self.parse_orderUpdate_data(response))
                elif "positions" in response:
                    print(self.parse_position_data(response))
                elif "trades" in response:
                    print(self.parse_trade_data(response))
                else:
                    print(response)
            print("Connection Closed")


    async def main(self):
        try:
            await self.connectWS()
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection closed with error: {e.code} - {e.reason}")
        except Exception as e:
            print(f"Error: {e}")

client_id = "XC4EOD67IM-100"
access_token=  "XC4EOD67IM-100:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2ODMwMDE4OTgsImV4cCI6MTY4MzA3MzgzOCwibmJmIjoxNjgzMDAxODk4LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCa1VKSXFKLTNQMl9BSXFWWFNWUlg5UXlIVW5QWlpGRnFnNG5xRkNWRzYwQU5qX0F6T2hVWmxPZmtCNUV4ak03MXBMWVlqSEpjWXBsaVpVNWpFREQ1R3JFVkt4Rmx0SzR4RDh2SERVdkZndWgwUEVGRT0iLCJkaXNwbGF5X25hbWUiOiJWSU5BWSBLVU1BUiBNQVVSWUEiLCJvbXMiOiJLMSIsImZ5X2lkIjoiWFYyMDk4NiIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.MghUuBXEV3INDwH-buwTUvJDvBQ0HS37d69nwRCE7nE"

# access_token=  "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2ODIzOTg0NTYsImV4cCI6MTY4MjQ2OTAxNiwibmJmIjoxNjgyMzk4NDU2LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCa1IxejROQ29wSHEtcEhQbm00cFFaeUhVMy1SU3dpLXJEODdjbTAwZmZEdjZVZGp4TDBwclVqNGhSVG5TQ1JKMmlnX1Z0WjR1bXNjX09xWGNGNXlmdEFDelJLdm9XMUpoMHZ3OGdVVG82a2hIdG5SUT0iLCJkaXNwbGF5X25hbWUiOiJWSU5BWSBLVU1BUiBNQVVSWUEiLCJvbXMiOiJLMSIsImZ5X2lkIjoiWFYyMDk4NiIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.8fnXs8Dgl-lDCtqsE5NtpdH3fvtSrXzDcHnQT0la-48"

# fyers = FyersModelv3(client_id = client_id,token=access_token,is_async=False)
# data = {
#     "disclosedQty": 0,
#     "limitPrice": 0,
#     "offlineOrder": False,
#     "productType": "CNC",
#     "qty": 1,
#     "side": 1,
#     "stopPrice": 0,
#     "symbol": "NSE:IRFC-EQ",
#     "type": 2,
#     "validity": "DAY"
# }


# id = fyers.place_orders(data)
# print(id)
fyers= websocket(access_token)
asyncio.run(fyers.connectWS())

