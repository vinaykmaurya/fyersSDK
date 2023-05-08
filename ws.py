import asyncio
import threading
import time
import websockets
import json
import asyncio



class websocket:

    def parse_position_data( self , msg ):
        print("Position-----------------")

        response = {}
        message = msg['positions']
        positionData = {}
        keyList = ["buy_avg","buy_qty","buy_val","cf_buy_qty","cf_sell_qty","day_buy_qty","day_sell_qty","fy_token","id","net_avg","net_qty","pl_realized","product_type",
                   "segment","sell_avg","sell_qty","sell_val","symbol","tran_side"]
        positionData = {key: message[key] for key in keyList}

        # positionData["buy_avg"] = message['buy_avg']
        # positionData["buy_qty"]= message['buy_qty']
        # positionData["buy_val"]= message['buy_val']
        # positionData["cf_buy_qty"]= message['cf_buy_qty']
        # positionData["cf_sell_qty"]= message['cf_sell_qty']
        # positionData["day_buy_qty"]= message['day_buy_qty']
        # positionData["day_sell_qty"]= message['day_sell_qty']
        # positionData["fy_token"]= message['fy_token']
        # positionData["id"]= message['id']
        # positionData["net_avg"]= message['net_avg']
        # positionData["net_qty"]= message['net_qty']
        # positionData["pl_realized"]= message['pl_realized']
        # positionData["product_type"]= message['product_type']

        # positionData["segment"]= message['segment']
        # positionData["sell_avg"]= message['sell_avg']
        # positionData["sell_qty"]= message['sell_qty']
        # positionData["sell_val"]= message['sell_val']

        # positionData["symbol"]= message['symbol']
        # positionData["tran_side"]= message['tran_side']
        positionData["qty_multi"]= message['qty_multiplier']
        positionData["rbi_ref_rate"]= message['rbirefrate']
        positionData["sym_desc"]= message['symbol_desc']
        response["ws_type"] = 1
        response["s"] = msg["s"]
        response["d"] = positionData
        return response

    def parse_trade_data( self, msg ):
        print("Trades-----------------")
        message = msg['trades']
        response = {}
        keyList = ["id_fill","id","qty_traded","price_traded","traded_val","product_type","client_id","id_exchange","ord_type","tran_side","symbol","time_epoch","fy_token"]
        tradeData = {key: message[key] for key in keyList}
        # tradeData['id_fill'] = message['id_fill']
        # tradeData['id'] = message['id']
        # tradeData['qty_traded'] = message['qty_traded']
        # tradeData['price_traded'] = message['price_traded']
        # tradeData['traded_val'] = message['traded_val']
        # tradeData['product_type'] = message['product_type']
        # tradeData['client_id'] = message['client_id']
        # tradeData['id_exchange'] = message['id_exchange']
        # tradeData['ord_type'] = message['ord_type']
        # tradeData['tran_side'] = message['tran_side']
        # tradeData['symbol'] = message['symbol']
        # tradeData['time_epoch'] = message['time_epoch']
        # tradeData['time_oms'] = message['time_oms']
        # tradeData['fy_token'] = message['fy_token']
        tradeData['tradeNumber'] = message['id']
        response["ws_type"] = 1
        response["s"] = msg["s"]
        response["d"] = tradeData
        return response


    def parse_orderUpdate_data(self, msg):
        response = {}   
        order = msg["orders"]
        orderData = {}
        keyMap = {
            "update_time_epoch_oms":"orderDateTime",
            # "id":"id",
            "id":"exchOrdId",
            "product_type":"productType",
            "instrument":"instrument",
            "side":"side",
            "ord_status":"status",
            "qty":"qty",
            "qty_filled":"filledQty",
            "qty_remaining":"remainingQuantity",
            "ord_type":"type",
            "validity":"orderValidity",
            "offline_flag":"offlineOrder",
            "status_msg":"message",
            "symbol":"symbol",
            "fy_token":"fyToken",
            "segment":"segment",
            "dqQtyRem":"dqQtyRem",
            "price_limit":"limitPrice",
            "price_stop":"stopPrice",
            "qty_disc":"discloseQty",
            "price_traded":"tradedPrice",

        }

        orderData = {keyMap[key]: order.get(key, 0) for key in keyMap.keys()}
        print("orderData---")
        # orderData["orderDateTime"] = order["update_time_epoch_oms"]
        # orderData["exchOrdId"] = order["id"]
        # orderData["side"] = order["tran_side"]
        # orderData["instrument"] = order["instrument"]
        # orderData["productType"] = order["product_type"]
        # orderData["status"] = order["ord_status"]
        # orderData["qty"] = order["qty"]
        # orderData["filledQty"] = order["qty_filled"] if "qty_filled" in order else  0
        # orderData["remainingQuantity"] = order["qty_remaining"] if "qty_remaining" in order else  0
        # orderData["type"] = order["ord_type"]
        # orderData["orderValidity"] = order["validity"]
        # orderData["offlineOrder"] = order["offline_flag"]
        # orderData["message"] = order["status_msg"]
        # orderData["fyToken"] = order["fy_token"]
        # orderData["symbol"] = order["symbol"]
        # orderData["segment"] = order["segment"]
        # orderData["dqQtyRem"] = order["dqQtyRem"] if "dqQtyRem" in order else  0
        # orderData["limitPrice"] = order["price_limit"] if "price_limit" in order else  0
        # orderData["stopPrice"] = order["price_stop"] if "price_stop" in order else  0
        # orderData["discloseQty"] = order["qty_disc"] if "qty_disc" in order else  0
        # orderData["tradedPrice"] = order["price_traded"] if "price_traded" in order else  0
        orderData["orderNumStatus"] = order["id"] + ":" + str(order["org_ord_status"])
        orderData["id"] = order["id"]
        orderData["slNo"] =int(time.time())

        response["ws_type"] = 1
        response["s"] = msg["s"]
        response["d"] = orderData
        return response


    def __init__(self, access_token,data_type): 
        self.access_token = access_token

        self.socket_type = {
               "orderUpdate" : "trades,positions,orders",
               "OnOrders":"orders",
               "OnTrades":"trades",
               "OnPositions":"positions",
               "OnPriceAlert":"pricealerts",
               "OnEdis":"edis"}
        self.data_type = [self.socket_type[(type)] for type in data_type.split(",")]




    async def subscribe(self):
        async with websockets.connect(
                "wss://socket.fyers.in/trade/v3",
                extra_headers={"authorization": self.access_token}
        ) as websocket:
            message = json.dumps({"T": "SUB_ORD", "SLIST": self.data_type, "SUB_T": 1})
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

    async def close(self, websocket_task):
        if not websocket_task.done():
            websocket = websocket_task.result()
            if not websocket.closed:
                await websocket.close()

    def main(self):
        loop = asyncio.get_event_loop()
        websocket_task = loop.create_task(self.subscribe())
        try:
            loop.run_until_complete(websocket_task)
        except KeyboardInterrupt:
            websocket_task.cancel()
            try:
                loop.run_until_complete(websocket_task)
            except asyncio.CancelledError:
                pass
            finally:
                loop.run_until_complete(self.close(websocket_task))
        finally:
            loop.close()


client_id = "XC4EOD67IM-100"
access_token=  "XC4EOD67IM-100:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2ODM1MTg1NDksImV4cCI6MTY4MzU5MjIyOSwibmJmIjoxNjgzNTE4NTQ5LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCa1dIUlZQalBZYnpWODFfM1BJMHNXN1g1TXhDU0R3VjRsb29WZFhudUNGUHlqY2VwdDZwYkdDeFBRN0JYY2ZDdVpOT0xMSGRjN2R3emdFa0JJSXc1QjdHMFNIUWZjbFF4Y2J3OXJjc2ZhQm9PbTVzWT0iLCJkaXNwbGF5X25hbWUiOiJWSU5BWSBLVU1BUiBNQVVSWUEiLCJvbXMiOiJLMSIsImZ5X2lkIjoiWFYyMDk4NiIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.7r_NPh7GdNt7iudLwISMQAEhHksowkxuEHlG8-76mzo"

fyers= websocket(access_token,"OnOrders,OnTrades,OnPositions")
fyers.main()

