import asyncio
import logging
from logging.config import dictConfig
import os
import sys
import threading
import time
import websockets
import json


class FyersSocket:
    """
    A class for sending and receiving data via WebSocket for orders, trades, and positions.

    """

    def __init__(self, access_token,run_background, log_path=None): 
        self.access_token = access_token
        self.log_path = log_path
        self.run_background = run_background
        self.logger_setup()
        self.websocket_task = None
        self.logger.info("Initiate socket object")
        self.logger.debug('access_token ' + self.access_token)

        self.socket_type = {
               "orderUpdate" : "trades,positions,orders",
               "OnOrders":"orders",
               "OnTrades":"trades",
               "OnPositions":"positions",
               "OnPriceAlert":"pricealerts",
               "OnEdis":"edis"}


    def parse_position_data(self, msg):
        try:
            position_data_keys = ["buy_avg", "buy_qty", "buy_val", "cf_buy_qty", "cf_sell_qty", "day_buy_qty", "day_sell_qty", "fy_token", "id", "net_avg",
                                   "net_qty", "pl_realized", "product_type", "segment", "sell_avg", "sell_qty", "sell_val", "symbol", "tran_side"]
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
        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logging.error("payload_creation :: ERR : -> Line:{} Exception:{}".format(exc_tb.tb_lineno, str(e)))

    def parse_trade_data(self, msg):
        try:
            trade_data_keys = ["id_fill", "id", "qty_traded", "price_traded", "traded_val", "product_type", "client_id", "id_exchange", "ord_type",
                                "tran_side", "symbol", "time_epoch", "fy_token"]
            trade_data = dict((key, msg['trades'][key]) for key in trade_data_keys)
            trade_data['tradeNumber'] = msg['trades']['id']

            return {
                "ws_type": 1,
                "s": msg["s"],
                "d": trade_data,
            }
        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logging.error("payload_creation :: ERR : -> Line:{} Exception:{}".format(exc_tb.tb_lineno, str(e)))
    
    def parse_orderUpdate_data(self, msg):
        try:
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
        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logging.error("payload_creation :: ERR : -> Line:{} Exception:{}".format(exc_tb.tb_lineno, str(e)))

    async def ScoketConnect(self,data_type):
        self.data_type = [self.socket_type[(type)] for type in data_type.split(",")]
        async with websockets.connect(
                "wss://socket.fyers.in/trade/v3",
                extra_headers={"authorization": self.access_token}
        ) as websocket:
            message = json.dumps({"T": "SUB_ORD", "SLIST": self.data_type, "SUB_T": 1})
            await websocket.send(message)
            while True:
                msgRcv = await websocket.recv()
                response = json.loads(msgRcv)
                if "orders" in response:
                    response = self.parse_orderUpdate_data(response)
                elif "positions" in response:
                    response = self.parse_position_data(response)
                elif "trades" in response:
                    response = self.parse_trade_data(response)
                else:
                    pass
                
                if self.run_background:
                    self.logger.debug(f"Response:{response}")
                else:
                    print(f"Received response: {response}")
                    self.logger.debug(f"Response:{response}")
    
    # async def close(self):
    #     if self.websocket_task and not self.websocket_task.closed:
    #         await self.websocket_task.close()
    async def close(self):
        if not self.websocket_task.done():
            websocket = self.websocket_task.result()
            if not websocket.closed:
                await websocket.close()

    async def subscribe(self,data_type):
        self.data_type = [self.socket_type[(type)] for type in data_type.split(",")]
        loop = asyncio.get_event_loop()
        self.websocket_task = loop.create_task(self.ScoketConnect())
        websocket_task= self.websocket_task
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


    def logger_setup(self):
        if self.log_path is None:
            self.log_path = os.getcwd()
        try:
            os.chmod(self.log_path, 0o750)
        except:
            self.log_path = os.getcwd()
            os.chmod(self.log_path, 0o750)
        LOGGING = {
			'version': 1,
			'disable_existing_loggers': False,
			'formatters': {
				'verbose': {
					'format': '%(asctime)s - %(name)s - %(levelname)s - %(pathname)s - %(lineno)d - %(message)s'
				}
			},
			'handlers': {
				'console': {
					'class': 'logging.StreamHandler',
					'level': 'DEBUG',
					'formatter': 'verbose',
				},
				'file': {
					'class': 'logging.FileHandler',
					'level': 'DEBUG',
					'formatter': 'verbose',
					'filename': os.path.join(self.log_path, 'fyers_socket.log')
				}
			},
			'loggers': {
				'fyers_socket': {
					'handlers': ['file'],
					'level': 'DEBUG',
					'propagate': False,
				}
			},
		}
        dictConfig(LOGGING)
        self.logger = logging.getLogger('fyers_socket')

async def main():
    client_id = "XC4EOD67IM-100"
    access_token=  "XC4EOD67IM-100:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2ODU1MDYzMTIsImV4cCI6MTY4NTU3OTQ1MiwibmJmIjoxNjg1NTA2MzEyLCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCa2Rza0lkcmpGWldPVHBkLUxseTU2dUd2N2NNd3MxY0ZtOWcwMi1wNUgtYmZhbUV6NmQzWWhxZlYzdlhLWUhCVUdTYUtlRlAzcHVJckFDQ3FJLXpjWUVhRDdVQ2ZQZnNQVjdZb0duY0Z3amg4blhhWT0iLCJkaXNwbGF5X25hbWUiOiJWSU5BWSBLVU1BUiBNQVVSWUEiLCJvbXMiOiJLMSIsImZ5X2lkIjoiWFYyMDk4NiIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.0er3yuQaHJk79nYOUHL1i-Ms8FHva8mBKF3lBQYuoBo"

    fyers= FyersSocket(access_token,False , None)
    connect_task = asyncio.create_task(fyers.ScoketConnect("OnOrders,OnTrades,OnPositions"))
    await asyncio.sleep(10)
    # await fyers.close()

    await connect_task

loop = asyncio.get_event_loop()
loop.run_until_complete(main())