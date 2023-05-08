import asyncio
import threading
import time
import websockets
import json
import asyncio



class websocket:
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

    def parse_position_data(self, msg):
        position_data_keys = ["buy_avg", "buy_qty", "buy_val", "cf_buy_qty", "cf_sell_qty", "day_buy_qty", "day_sell_qty", "fy_token", "id", "net_avg", "net_qty", "pl_realized", "product_type", "segment", "sell_avg", "sell_qty", "sell_val", "symbol", "tran_side"]
        position_data = {key: msg['positions'][key] for key in position_data_keys}
        position_data.update({
            "qty_multi": msg['positions']['qty_multiplier'],
            "rbi_ref_rate": msg['positions']['rbirefrate'],
            "sym_desc": msg['positions']['symbol_desc']
        })

        return {
            "ws_type": 1,
            "s": msg["s"],
            "d": position_data,
        }

    def parse_trade_data(self, msg):
        trade_data_keys = ["id_fill", "id", "qty_traded", "price_traded", "traded_val", "product_type", "client_id", "id_exchange", "ord_type", "tran_side", "symbol", "time_epoch", "fy_token"]
        trade_data = dict((key, msg['trades'][key]) for key in trade_data_keys)
        trade_data['tradeNumber'] = msg['trades']['id']

        return {
            "ws_type": 1,
            "s": msg["s"],
            "d": trade_data,
        }
    
    def parse_orderUpdate_data(self, msg):
        keyMap = {
            "update_time_epoch_oms": "orderDateTime",
            "id": "exchOrdId",
            "product_type": "productType",
            "instrument": "instrument",
            "side": "side",
            "ord_status": "status",
            "qty": "qty",
            "qty_filled": "filledQty",
            "qty_remaining": "remainingQuantity",
            "ord_type": "type",
            "validity": "orderValidity",
            "offline_flag": "offlineOrder",
            "status_msg": "message",
            "symbol": "symbol",
            "fy_token": "fyToken",
            "segment": "segment",
            "dqQtyRem": "dqQtyRem",
            "price_limit": "limitPrice",
            "price_stop": "stopPrice",
            "qty_disc": "discloseQty",
            "price_traded": "tradedPrice",
        }

        order = msg["orders"]
        order_data = {keyMap[key]: order.get(key, 0) for key in keyMap}

        order_data["orderNumStatus"] = order["id"] + ":" + str(order["org_ord_status"])
        order_data["id"] = order["id"]
        order_data["slNo"] = int(time.time())

        return {
            "ws_type": 1,
            "s": msg["s"],
            "d": order_data,
        }


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

